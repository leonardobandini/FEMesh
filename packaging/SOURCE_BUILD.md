# Build FEMesh from corresponding source

This archive contains the preferred form of the project's GPL-2.0-or-later
original source code, build/installation scripts, the exact Gmsh Python
binding and both GPLv2/GPLv3 license texts. The binary combination elects
GPLv3 as explained in `LICENSE-APPLICATION.md`. Download
`gmsh-4.15.2-source.tgz` from the **same public release**
for the unmodified upstream C/C++ Gmsh source, including its bundled
third-party components and build configuration. Source availability for the
included Python, OpenSSL and libffi components is governed by their own
licenses; their applicable notices are provided with the binary distribution.

The bundled `gmsh-4.15.dll` is unmodified and matches the official PyPI wheel
`gmsh-4.15.2-py2.py3-none-win_amd64.whl` (SHA-256
`7b36083bb410fa27c5d0e052929d1a9844a5b09169d66017b72b41aabd49d711`)
byte for byte (DLL SHA-256
`6cac3eefb477265d9fa60bbd869dbbbf7c7ca4cb308c0f8f2b43e91d43de3c1c`).
The wheel's `gmsh.py` binding also matches `third_party/gmsh.py` in this source
archive (SHA-256
`a56ebe69dc57a3ea15eee191cae4f1881b06784174b2d9df306a98bdd8b06606`).
The original Gmsh source archive SHA-256 is
`be3f66f225d27ba9fa014f07e83169285da8a051b0e8ab7103d88066b39bdd3e`.
The source archive's generated API file `api/gmsh.py` is not byte-identical to
the packaged wheel's `gmsh.py`, so the exact binding is separately included.

To build on Windows x64, install SAP2000 27 and .NET Framework 4.8 plus the
.NET SDK, Python 3.12 and dependencies from `packaging/requirements-build.txt`.
The proprietary `SAP2000v1.dll` is supplied by the separately licensed SAP2000
installation, not by this archive. From the top directory of this archive:

```cmd
python -m pip install -r packaging\requirements-build.txt
dotnet build SapQuadTransitionPlugin\SapQuadTransitionPlugin.csproj -c Release -p:Sap2000ApiPath="C:\Program Files\Computers and Structures\SAP2000 27\SAP2000v1.dll" -o packaging\build\plugin\net48
dotnet build packaging\SQMPluginInstaller.csproj -c Release -o packaging\build\installer\net48
python -m PyInstaller --noconfirm --clean --distpath packaging\dist --workpath packaging\build packaging\SapQuadMesherBackend.spec
powershell -NoProfile -File packaging\build-release.ps1 -SkipBuild
```

The release script verifies the three mesh scripts, checks Gmsh source and
binding hashes, assembles the archive and refuses to package `SAP2000v1.dll`
or SAP2000 models. The report documents and small test CSV fixtures used by
the release script are included here. Other model datasets in the original
project are not needed to modify or build the executable. The compilation
uses the official wheel and source archive rather than requiring a rebuild
of Gmsh itself.

The original C# component has a limited SAP2000 API additional permission in
`SAP2000-LINKING-EXCEPTION.md`; this does not apply to Gmsh.
