param([string]$Version = '2.0.26')
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dll = Join-Path $root 'artifacts\Sap2000QuadMesher-1.0.120\SapQuadTransitionPlugin.dll'
$api = 'C:\Program Files\Computers and Structures\SAP2000 27\SAP2000v1.dll'
if (-not (Test-Path -LiteralPath $dll -PathType Leaf) -or -not (Test-Path -LiteralPath $api -PathType Leaf)) {
    throw 'Released V1 plugin/API fixture missing.'
}
Add-Type -Path $api
$type = [Reflection.Assembly]::LoadFrom($dll).GetType('SapQuadTransitionPlugin.cPlugin+MeshOptionsDialog', $true)
$method = $type.GetMethod('TryGetNewRelease', [Reflection.BindingFlags]'Static,NonPublic')
if (-not $method) { throw 'V1 updater parser missing.' }
$manifest = [IO.File]::ReadAllText((Join-Path $root 'updates\manifest.json'))
[object[]]$parameters = @($manifest, '', '', '')
if (-not [bool]$method.Invoke($null, $parameters) -or
    $parameters[1] -ne $Version -or
    $parameters[2] -ne "https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/tag/v$Version" -or
    $parameters[3] -ne "https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/download/v$Version/Sap2000QuadMesher-$Version.zip") {
    throw "V1 1.0.120 does not recognize the V2 upgrade feed: $($parameters -join '|')"
}
"V1_TO_V2_UPGRADE_FEED=PASS VERSION=$Version"
