param(
    [string]$Plugin = 'packaging\build\plugin\net48\SapQuadTransitionPlugin.dll',
    [ValidateSet('Current', 'Future')][string]$Scenario = 'Current',
    [int]$DisplaySeconds = 0
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -Path 'C:\Program Files\Computers and Structures\SAP2000 27\SAP2000v1.dll'
Add-Type -Path 'C:\Program Files\Computers and Structures\SAP2000 27\CSiAPIv1.dll'
$assembly = [Reflection.Assembly]::LoadFrom((Resolve-Path -LiteralPath $Plugin).Path)
$type = $assembly.GetType('SapQuadTransitionPlugin.cPlugin+MeshOptionsDialog', $true)
$axis = $assembly.GetType('SapQuadTransitionPlugin.cPlugin+SymmetryAxis', $true)
$axes = [Array]::CreateInstance($axis, 0)
$constructor = @($type.GetConstructors([Reflection.BindingFlags]'Instance,Public,NonPublic') |
    Where-Object { $_.GetParameters().Count -eq 6 })[0]
if ($null -eq $constructor) { throw 'Mesh options constructor missing.' }
$pluginType = $assembly.GetType('SapQuadTransitionPlugin.cPlugin')
$currentVersion = [version]$pluginType.GetField('PluginVersion',
    [Reflection.BindingFlags]'Static,NonPublic').GetRawConstantValue()
$current = "$($currentVersion.Major).$($currentVersion.Minor).$($currentVersion.Build)"
$future = "$($currentVersion.Major).$($currentVersion.Minor).$($currentVersion.Build + 1)"
$channel = if ($currentVersion.Major -eq 2) { 'manifest-v2.json' } else { 'manifest.json' }
$feed = [string]$pluginType.GetField('UpdateManifestUrl',
    [Reflection.BindingFlags]'Static,NonPublic').GetRawConstantValue()
if ($feed -ne "https://raw.githubusercontent.com/leonardobandini/sap2000-quad-mesher-updates/main/$channel") {
    throw "Plugin is reading the wrong update channel: $feed"
}
$version = if ($Scenario -eq 'Future') { $future } else { $current }
$release = "https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/tag/v$version"
$download = "https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/download/v$version/Sap2000QuadMesher-$version.zip"
$env:SAP_QUAD_TEST_UPDATE_MANIFEST_JSON = (@{
    schemaVersion = 1; version = $version; releaseUrl = $release; downloadUrl = $download
} | ConvertTo-Json -Compress)
$dialog = $constructor.Invoke([object[]]@('mm', $false, [string[]]@(), [string[]]@(), $axes, $true))
try {
    $dialog.Show()
    $flags = [Reflection.BindingFlags]'Instance,NonPublic'
    $notice = $type.GetField('updateNotice', $flags).GetValue($dialog)
    $timer = $type.GetField('updateBlinkTimer', $flags).GetValue($dialog)
    if ($currentVersion.Major -eq 2 -and -not $notice.Visible) { throw 'V2 update notice is hidden.' }
    $deadline = (Get-Date).AddSeconds(12)
    while ((Get-Date) -lt $deadline) {
        [System.Windows.Forms.Application]::DoEvents()
        if ($Scenario -eq 'Future' -and $timer.Enabled -or
            $Scenario -eq 'Current' -and $notice.Text -match '(up to date|aggiornata)') { break }
        Start-Sleep -Milliseconds 100
    }
    if ($Scenario -eq 'Future') {
        if (-not $timer.Enabled -or $notice.Text -notmatch '(Update available|Aggiornamento disponibile)' -or
            $notice.Text -notmatch '(Download|Scarica)') { throw "Blinking update notice missing: $($notice.Text)" }
        $actual = [string]$type.GetField('availableDownloadUrl', $flags).GetValue($dialog)
        if ($actual -ne $download) { throw "The V2 download does not target its verified ZIP: $actual" }
        $first = $notice.BackColor.ToArgb()
        $deadline = (Get-Date).AddSeconds(3)
        $changed = $false
        while ((Get-Date) -lt $deadline) {
            [System.Windows.Forms.Application]::DoEvents()
            if ($notice.BackColor.ToArgb() -ne $first) { $changed = $true; break }
            Start-Sleep -Milliseconds 100
        }
        if (-not $changed) { throw 'Available-update notice did not blink.' }
    } else {
        if ($timer.Enabled -or $notice.Text -notmatch '(up to date|aggiornata)') {
            throw "Up-to-date state missing: $($notice.Text)"
        }
    }
    "UPDATE_NOTICE_$($Scenario.ToUpperInvariant())=PASS TEXT=$($notice.Text) BLINK=$($timer.Enabled)"
    $deadline = (Get-Date).AddSeconds($DisplaySeconds)
    while ((Get-Date) -lt $deadline) { [System.Windows.Forms.Application]::DoEvents(); Start-Sleep -Milliseconds 100 }
} finally {
    $dialog.Close(); $dialog.Dispose()
    $env:SAP_QUAD_TEST_UPDATE_MANIFEST_JSON = $null
}
