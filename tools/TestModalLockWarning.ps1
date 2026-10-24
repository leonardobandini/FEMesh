# SPDX-License-Identifier: GPL-2.0-or-later
# Verify the lock warning blocks SAP's window and an already open SAP dialog.
param([Parameter(Mandatory=$true)][string]$Plugin,
      [string]$ApiPath = 'C:\Program Files\Computers and Structures\SAP2000 27\CSiAPIv1.dll')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -Path $ApiPath
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Threading;
public static class FEMeshWarningWindows {
    public static IntPtr HostWindow, ConfirmationWindow;
    public static volatile bool Seen, Observed, Dismissed;
    [DllImport("user32.dll")]
    public static extern bool IsWindowEnabled(IntPtr window);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)]
    public static extern IntPtr FindWindow(string className, string caption);
    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr window, uint message, IntPtr wParam, IntPtr lParam);
    public static void Watch(string caption) {
        ThreadPool.QueueUserWorkItem(_ => {
            for (int attempt = 0; attempt < 120; attempt++) {
                IntPtr box = FindWindow("#32770", caption);
                if (box != IntPtr.Zero) {
                    Seen = true;
                    Observed = !IsWindowEnabled(HostWindow) && !IsWindowEnabled(ConfirmationWindow);
                    Dismissed = PostMessage(box, 0x0111, (IntPtr)1, IntPtr.Zero);
                    Thread.Sleep(400);
                    if (FindWindow("#32770", caption) == box)
                        PostMessage(box, 0x0010, IntPtr.Zero, IntPtr.Zero);
                    return;
                }
                Thread.Sleep(100);
            }
        });
    }
}
'@
$assembly = [Reflection.Assembly]::LoadFrom((Resolve-Path -LiteralPath $Plugin).Path)
$pluginType = $assembly.GetType('SapQuadTransitionPlugin.cPlugin', $true)
$type = $assembly.GetType('SapQuadTransitionPlugin.cPlugin+MeshOptionsDialog', $true)
$axis = $assembly.GetType('SapQuadTransitionPlugin.cPlugin+SymmetryAxis', $true)
$axes = [Array]::CreateInstance($axis, 0)
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$version = $pluginType.GetField('PluginVersion', $flags).GetRawConstantValue()
$constructor = @($type.GetConstructors([Reflection.BindingFlags]'Instance,Public,NonPublic') |
    Where-Object { $_.GetParameters().Count -eq 6 })[0]
if (-not $constructor) { throw 'Mesh options constructor missing.' }
$oldManifest = $env:SAP_QUAD_TEST_UPDATE_MANIFEST_JSON
$env:SAP_QUAD_TEST_UPDATE_MANIFEST_JSON = '{}'
$hostWindow = New-Object Windows.Forms.Form
$hostWindow.Text = 'SAP2000 test host'
$confirmation = New-Object Windows.Forms.Form
$confirmation.Text = 'SAP2000 test unlock confirmation'
$dialog = $null
try {
    $hostWindow.Show()
    $confirmation.Show()
    $dialog = $constructor.Invoke([object[]]@('m', $false, [string[]]@(), [string[]]@(), $axes, $true))
    $dialog.Show()
    $dialog.AllowViewportInteraction($hostWindow.Handle)
    [FEMeshWarningWindows]::HostWindow = $hostWindow.Handle
    [FEMeshWarningWindows]::ConfirmationWindow = $confirmation.Handle
    [FEMeshWarningWindows]::Watch('FEMesh ' + $version)
    $dialog.ReportModelLockViolation('Simulated unlock during FEMesh.')
    if (-not [FEMeshWarningWindows]::Seen -or -not [FEMeshWarningWindows]::Observed -or
        -not [FEMeshWarningWindows]::Dismissed) {
        throw 'The warning did not block the SAP windows or could not be dismissed.'
    }
    if (-not [FEMeshWarningWindows]::IsWindowEnabled($hostWindow.Handle) -or
        -not [FEMeshWarningWindows]::IsWindowEnabled($confirmation.Handle)) {
        throw 'SAP windows remained disabled after the warning was dismissed.'
    }
    'MODAL_LOCK_WARNING=PASS HOST_AND_CONFIRMATION_BLOCKED=YES RESTORED=YES'
} finally {
    if ($dialog) { $dialog.Close(); $dialog.Dispose() }
    $confirmation.Close(); $confirmation.Dispose()
    $hostWindow.Close(); $hostWindow.Dispose()
    $env:SAP_QUAD_TEST_UPDATE_MANIFEST_JSON = $oldManifest
}
