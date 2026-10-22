# Local-only backup numbering and update URL migration checks.
param([Parameter(Mandatory=$true)][string]$Plugin,
      [Parameter(Mandatory=$true)][string]$ResultsRoot,
      [string]$NextVersion='2.0.59', [switch]$ExpectLegacyOnly)
$ErrorActionPreference='Stop'
$parent=Join-Path $env:TEMP 'opencode'
if(-not(Test-Path -LiteralPath $parent -PathType Container) -or
   -not $ResultsRoot.StartsWith(($parent.TrimEnd('\')+'\'),[StringComparison]::OrdinalIgnoreCase) -or
   (Test-Path -LiteralPath $ResultsRoot) -or
   -not(Test-Path -LiteralPath $Plugin -PathType Leaf)){throw 'Unsafe branding test inputs.'}
New-Item -ItemType Directory -Path $ResultsRoot|Out-Null
Add-Type -Path 'C:\Program Files\Computers and Structures\SAP2000 27\CSiAPIv1.dll'
$assembly=[Reflection.Assembly]::LoadFrom($Plugin)
$pluginType=$assembly.GetType('SapQuadTransitionPlugin.cPlugin',$true)
$method=$pluginType.GetMethod('CreateNumberedBackup',[Reflection.BindingFlags]'Static,NonPublic')
$source=Join-Path $ResultsRoot 'example.sdb'
[IO.File]::WriteAllBytes($source,[byte[]]@(1,2,3,4,5))
[IO.File]::WriteAllBytes((Join-Path $ResultsRoot 'example.quadmesher-backup-0001.sdb'),[byte[]]@(1))
[IO.File]::WriteAllBytes((Join-Path $ResultsRoot 'example.FEMesher-backup-0002.sdb'),[byte[]]@(2))
$backupArguments=[object[]]::new(1)
$backupArguments[0]=[string]$source
$created=[string]$method.Invoke($null,$backupArguments)
if(-not $ExpectLegacyOnly -and ($created -ne (Join-Path $ResultsRoot 'example.FEMesher-backup-0003.sdb') -or
   (Get-FileHash -LiteralPath $created -Algorithm SHA256).Hash -ne
       (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash)){
    throw 'FEMesher backup did not continue the old/new sequence exactly.'
}
if(-not $ExpectLegacyOnly){'FEMESHER_BACKUP_NAME=PASS LEGACY_0001 BRANDED_0002 NEW_0003'}
$dialog=$assembly.GetType('SapQuadTransitionPlugin.cPlugin+MeshOptionsDialog',$true)
$parser=$dialog.GetMethod('TryGetNewRelease',[Reflection.BindingFlags]'Static,NonPublic')
foreach($filename in @("Sap2000QuadMesher-$NextVersion.zip","FEMesher-$NextVersion.zip",
    "other-$NextVersion.zip")){
    $json=@{schemaVersion=1;version=$NextVersion;
        releaseUrl="https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/tag/v$NextVersion";
        downloadUrl="https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/download/v$NextVersion/$filename"} | ConvertTo-Json -Compress
    $args=[object[]]::new(4)
    $args[0]=[string]$json
    $accepted=[bool]$parser.Invoke($null,$args)
    $expected=if($ExpectLegacyOnly){$filename -like 'Sap2000QuadMesher-*'}else{$filename -notlike 'other-*'}
    if($accepted -ne $expected -or
       ($accepted -and ($args[1] -ne $NextVersion -or $args[3] -notlike "*/$filename"))){
        throw "Update URL validation mismatch: $filename accepted=$accepted"
    }
    "UPDATE_URL=$filename ACCEPTED=$accepted"
}
