# SPDX-License-Identifier: GPL-2.0-or-later
# Build a standalone Gmsh V2 ZIP which upgrades the existing V1 COM registration.
param([switch]$SkipBackendBuild, [switch]$RebuildExisting)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$artifacts = Join-Path $root 'artifacts'
if (-not (Test-Path -LiteralPath $artifacts -PathType Container)) { throw "Artifact directory missing: $artifacts" }
[xml]$project = Get-Content (Join-Path $root 'SapQuadTransitionPlugin\SapGmshReplacement.csproj')
$version = $project.Project.PropertyGroup.Version
$stage = Join-Path $artifacts "Sap2000QuadMesher-$version"
$zipPath = "$stage.zip"
$brandedZip = Join-Path $artifacts "FEMesher-$version.zip"
$sourceZip = Join-Path $artifacts "Sap2000QuadMesher-$version-source.zip"
if ($RebuildExisting) {
    if (-not (Test-Path -LiteralPath (Join-Path $stage 'sap_gmsh_mesher.py') -PathType Leaf) -or
        -not (Test-Path -LiteralPath (Join-Path $stage 'SQMPluginInstaller.exe') -PathType Leaf)) {
        throw 'Refusing to replace a directory not recognized as a generated V2 package.'
    }
    Remove-Item -LiteralPath $stage -Recurse -Force
    $publicZip = Join-Path $artifacts "FEMesh-$version.zip"
    foreach ($file in @($zipPath, "$zipPath.sha256", $brandedZip, "$brandedZip.sha256",
            $publicZip, "$publicZip.sha256", $sourceZip, "$sourceZip.sha256")) {
        if (Test-Path -LiteralPath $file) { Remove-Item -LiteralPath $file -Force }
    }
}
$build = Join-Path $env:TEMP ('opencode\sqm-v2-release-build-' + [guid]::NewGuid().ToString('N'))
if (-not (Test-Path -LiteralPath (Split-Path -Parent $build) -PathType Container)) { throw 'Missing temporary build parent.' }
New-Item -ItemType Directory -Path $build | Out-Null
try {
    $pluginBuild = Join-Path $build 'plugin'
    $installerBuild = Join-Path $build 'installer'
    & dotnet build (Join-Path $root 'SapQuadTransitionPlugin\SapGmshReplacement.csproj') -c Release -o $pluginBuild
    if ($LASTEXITCODE -ne 0) { throw 'V2 replacement plugin build failed.' }
    & dotnet build (Join-Path $root 'packaging\SQMV2Installer.csproj') -c Release -o $installerBuild
    if ($LASTEXITCODE -ne 0) { throw 'V2 installer build failed.' }
    if (-not $SkipBackendBuild) {
        & python -m PyInstaller --noconfirm --clean --distpath (Join-Path $PSScriptRoot 'dist-v2') --workpath (Join-Path $PSScriptRoot 'build-v2') (Join-Path $PSScriptRoot 'SapGmshBackend.spec')
        if ($LASTEXITCODE -ne 0) { throw 'Frozen Gmsh V2 backend build failed.' }
    }
    $backend = Join-Path $PSScriptRoot 'dist-v2\SapQuadMesherBackend'
    if (-not (Test-Path -LiteralPath (Join-Path $backend 'SapQuadMesherBackend.exe'))) { throw 'V2 backend is missing.' }
    $source = Join-Path $PSScriptRoot 'cache\gmsh-4.15.2-source.tgz'
    if (-not (Test-Path -LiteralPath $source)) { throw 'Corresponding Gmsh sources missing.' }
    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sourceHash -ne 'be3f66f225d27ba9fa014f07e83169285da8a051b0e8ab7103d88066b39bdd3e') { throw 'Gmsh source hash mismatch.' }
    if (Test-Path -LiteralPath $stage) { throw "Release destination already exists: $stage" }
    New-Item -ItemType Directory -Path $stage | Out-Null
    foreach ($name in @('SapQuadTransitionPlugin.dll','sap_gmsh_mesher.py')) {
        Copy-Item -LiteralPath (Join-Path $pluginBuild $name) -Destination $stage
    }
    Copy-Item -LiteralPath (Join-Path $installerBuild 'SQMPluginInstaller.exe') -Destination $stage
    foreach ($name in @('install_plugin.cmd','uninstall_plugin.cmd','README-GMSH-V2.md')) {
        Copy-Item -LiteralPath (Join-Path $root "SapQuadTransitionPlugin\$name") -Destination $stage
    }
    Copy-Item -LiteralPath (Join-Path $root 'SapQuadTransitionPlugin\README-GMSH-V2.md') -Destination (Join-Path $stage 'README.md')
    foreach ($name in @('LICENSE','GPL-3.0.txt','LICENSE-APPLICATION.md','SAP2000-LINKING-EXCEPTION.md','THIRD_PARTY_NOTICES.md')) {
        Copy-Item -LiteralPath (Join-Path $root $name) -Destination $stage
    }
    $sourceGuide = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'SOURCE.template.md')).Replace('{VERSION}', [string]$version)
    [IO.File]::WriteAllText((Join-Path $stage 'SOURCE.md'), $sourceGuide, [Text.Encoding]::UTF8)
    if ($sourceGuide -notmatch [regex]::Escape("https://github.com/leonardobandini/FEMesh/releases/tag/v$version")) {
        throw 'The packaged corresponding-source address does not match this release.'
    }
    Copy-Item -LiteralPath (Join-Path $pluginBuild 'docs') -Destination $stage -Recurse
    Copy-Item -LiteralPath (Join-Path $pluginBuild 'img') -Destination $stage -Recurse
    Copy-Item -LiteralPath $backend -Destination (Join-Path $stage 'mesher') -Recurse
    $licenses = Join-Path $stage 'licenses'
    New-Item -ItemType Directory -Path $licenses | Out-Null
    $gmshLicense = Join-Path $PSScriptRoot 'cache\gmsh-4.15.2-source\LICENSE.txt'
    if (-not (Test-Path -LiteralPath $gmshLicense)) { & tar -xzf $source -C (Join-Path $PSScriptRoot 'cache') 'gmsh-4.15.2-source/LICENSE.txt' }
    Copy-Item -LiteralPath $gmshLicense -Destination (Join-Path $licenses 'GMSH-LICENSE.txt')
    $pythonRoot = & python -c 'import sys; print(sys.base_prefix)'
    Copy-Item -LiteralPath (Join-Path $pythonRoot 'LICENSE.txt') -Destination (Join-Path $licenses 'PYTHON-LICENSE.txt')
    $fileVersion = (Get-Item (Join-Path $stage 'SapQuadTransitionPlugin.dll')).VersionInfo.FileVersion
    if ($fileVersion -ne "$version.0") { throw "Wrong V2 DLL version: $fileVersion" }
    & (Join-Path $stage 'SQMPluginInstaller.exe') verify $stage
    if ($LASTEXITCODE -ne 0) { throw 'Standalone installer verification failed.' }
    & python (Join-Path $root 'tools\VerifyGmshV2Help.py')
    if ($LASTEXITCODE -ne 0) { throw 'Bilingual help validation failed.' }
    $trial = Join-Path $build 'upgrade-trial'
    $old = Join-Path $artifacts 'Sap2000QuadMesher-1.0.120'
    if (Test-Path -LiteralPath (Join-Path $old 'SQMPluginInstaller.exe') -PathType Leaf) {
        & (Join-Path $old 'SQMPluginInstaller.exe') test-install $trial
        if ($LASTEXITCODE -ne 0) { throw 'V1 fixture installation failed.' }
        & (Join-Path $stage 'SQMPluginInstaller.exe') test-install $trial
        if ($LASTEXITCODE -ne 0) { throw 'V1 to V2 replacement failed.' }
        if ((Get-Item (Join-Path $trial 'SapQuadTransitionPlugin.dll')).VersionInfo.FileVersion -ne "$version.0" -or
            -not (Test-Path -LiteralPath (Join-Path $trial 'docs\help-gmsh-v2\index-it.html')) -or
            (Test-Path -LiteralPath (Join-Path $trial 'docs\help\index-it.html'))) { throw 'V1 files survived replacement or V2 files are missing.' }
    }
    $previous = if ($version -eq '2.0.12') { '2.0.11' } elseif ($version -eq '2.0.13') { '2.0.12' }
        elseif ($version -eq '2.0.23') { '2.0.22' } elseif ($version -eq '2.0.24') { '2.0.23' }
        elseif ($version -eq '2.0.26') { '2.0.24' }
        elseif ($version -eq '2.0.28') { '2.0.26' }
        elseif ($version -eq '2.0.29') { '2.0.28' }
        elseif ($version -eq '2.0.30') { '2.0.29' }
        elseif ($version -eq '2.0.32') { '2.0.30' }
        elseif ($version -eq '2.0.36') { '2.0.32' }
        elseif ($version -eq '2.0.37') { '2.0.36' }
        elseif ($version -eq '2.0.38') { '2.0.37' }
        elseif ($version -eq '2.0.39') { '2.0.38' }
        elseif ($version -eq '2.0.40') { '2.0.39' }
        elseif ($version -eq '2.0.41') { '2.0.40' }
        elseif ($version -eq '2.0.42') { '2.0.41' }
        elseif ($version -eq '2.0.43') { '2.0.42' }
        elseif ($version -eq '2.0.44') { '2.0.43' }
        elseif ($version -eq '2.0.45') { '2.0.44' }
        elseif ($version -eq '2.0.46') { '2.0.45' }
        elseif ($version -eq '2.0.50') { '2.0.46' }
        elseif ($version -eq '2.0.52') { '2.0.50' }
        elseif ($version -eq '2.0.53') { '2.0.52' }
        elseif ($version -eq '2.0.54') { '2.0.53' }
        elseif ($version -eq '2.0.57') { '2.0.54' }
        elseif ($version -eq '2.0.58') { '2.0.57' }
        elseif ($version -eq '2.0.59') { '2.0.58' }
        elseif ($version -eq '2.0.60') { '2.0.59' }
        elseif ($version -eq '2.0.61') { '2.0.59' }
        elseif ($version -eq '2.0.62') { '2.0.61' }
        elseif ($version -eq '2.0.63') { '2.0.62' } else { '2.0.13' }
    $oldV2 = Join-Path $artifacts "Sap2000QuadMesher-$previous"
    if (Test-Path -LiteralPath (Join-Path $oldV2 'SQMPluginInstaller.exe') -PathType Leaf) {
        $trialV2 = Join-Path $build 'v2-upgrade-trial'
        & (Join-Path $oldV2 'SQMPluginInstaller.exe') test-install $trialV2
        if ($LASTEXITCODE -ne 0) { throw "V2 $previous fixture installation failed." }
        & (Join-Path $stage 'SQMPluginInstaller.exe') test-install $trialV2
        if ($LASTEXITCODE -ne 0 -or
            (Get-Item (Join-Path $trialV2 'SapQuadTransitionPlugin.dll')).VersionInfo.FileVersion -ne "$version.0") {
            throw "V2 $previous to $version replacement failed."
        }
    }
    $forbidden = @(Get-ChildItem -LiteralPath $stage -Recurse -File | Where-Object { $_.Name -in @('SAP2000v1.dll','CSiAPIv1.dll') -or $_.Extension -in @('.sdb','.bdb','.sbk') })
    if ($forbidden.Count) { throw 'The V2 package contains SAP2000 proprietary/test model files.' }
    $zip = "$stage.zip"
    if (Test-Path -LiteralPath $zip) { throw "ZIP already exists: $zip" }
    Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal
    $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
    [IO.File]::WriteAllText("$zip.sha256", "$hash  $(Split-Path -Leaf $zip)`n", [Text.Encoding]::ASCII)
    if (Test-Path -LiteralPath $brandedZip) { throw "Branded ZIP already exists: $brandedZip" }
    Copy-Item -LiteralPath $zip -Destination $brandedZip
    if ((Get-FileHash -LiteralPath $brandedZip -Algorithm SHA256).Hash.ToLowerInvariant() -ne $hash) {
        throw 'Branded ZIP differs from the legacy-compatible ZIP.'
    }
    [IO.File]::WriteAllText("$brandedZip.sha256", "$hash  $(Split-Path -Leaf $brandedZip)`n", [Text.Encoding]::ASCII)
    $publicZip = Join-Path $artifacts "FEMesh-$version.zip"
    if (Test-Path -LiteralPath $publicZip) { throw "FEMesh ZIP already exists: $publicZip" }
    Copy-Item -LiteralPath $zip -Destination $publicZip
    if ((Get-FileHash -LiteralPath $publicZip -Algorithm SHA256).Hash.ToLowerInvariant() -ne $hash) {
        throw 'Public FEMesh ZIP differs from the legacy-compatible ZIP.'
    }
    [IO.File]::WriteAllText("$publicZip.sha256", "$hash  $(Split-Path -Leaf $publicZip)`n", [Text.Encoding]::ASCII)
    & python (Join-Path $PSScriptRoot 'build-source-v2.py') $version
    if ($LASTEXITCODE -ne 0) { throw 'V2 corresponding source archive failed.' }
    Copy-Item -LiteralPath $source -Destination (Join-Path $artifacts 'gmsh-4.15.2-source.tgz') -Force
    [IO.File]::WriteAllText((Join-Path $artifacts 'gmsh-4.15.2-source.tgz.sha256'),
        "$sourceHash  gmsh-4.15.2-source.tgz`n", [Text.Encoding]::ASCII)
    "V2_PACKAGE=$zip"; "V2_SHA256=$hash"
} finally {
    if (Test-Path -LiteralPath $build) { Remove-Item -LiteralPath $build -Recurse -Force }
}
