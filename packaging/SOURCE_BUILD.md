# Build FEMesh from the corresponding source

This archive contains the preferred source for the FEMesh plugin, installer,
Python backend and packaging scripts. The independently maintained upstream
Gmsh source is the `gmsh-4.15.2-source.tgz` asset on the **same release**.
The project's original code and Gmsh are GPL-2.0-or-later. Because the bundled
CPython runtime contains OpenSSL 3 (Apache-2.0), the combined binary elects
GPLv3. The complete license texts, notices and third-party terms are in
`LICENSE`, `GPL-3.0.txt`, `LICENSE-APPLICATION.md`,
`THIRD_PARTY_NOTICES.md` and `licenses/`.

The distributed `gmsh-4.15.dll` comes from the unmodified official Gmsh
4.15.2 Windows wheel (wheel SHA-256
`7b36083bb410fa27c5d0e052929d1a9844a5b09169d66017b72b41aabd49d711`,
DLL SHA-256 `6cac3eefb477265d9fa60bbd869dbbbf7c7ca4cb308c0f8f2b43e91d43de3c1c`).
The exact Python binding is included as `third_party/gmsh.py` (SHA-256
`a56ebe69dc57a3ea15eee191cae4f1881b06784174b2d9df306a98bdd8b06606`).
The upstream source tarball SHA-256 is
`be3f66f225d27ba9fa014f07e83169285da8a051b0e8ab7103d88066b39bdd3e`.

To build from the extracted archive on Windows x64, install .NET SDK and .NET
Framework 4.8, Python **3.12.7**, and either SAP2000 or CSiBridge 27+ with
`CSiAPIv1.dll`. The API DLL is supplied by the independently licensed host;
**it is not distributed with FEMesh**. Install the
[official Microsoft Visual C++ Redistributable x64](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist),
version **14.42.34226.3 or later compatible**, separately before running the
backend or installer: Visual C++ runtime DLLs are not included in FEMesh. From
the top directory of this source archive, in PowerShell:

```powershell
python -m pip install -r packaging\requirements-build.txt
New-Item -ItemType Directory -Path artifacts, packaging\cache -Force | Out-Null
Copy-Item -LiteralPath "<downloaded release>\gmsh-4.15.2-source.tgz" -Destination packaging\cache\gmsh-4.15.2-source.tgz
powershell -NoProfile -ExecutionPolicy Bypass -File packaging\build-release-v2.ps1
```

The release script compiles `SapQuadTransitionPlugin/SapGmshReplacement.csproj`
against the locally installed CSiAPI, compiles `packaging/SQMV2Installer.csproj`,
builds `packaging/SapGmshBackend.spec` with PyInstaller, verifies the pinned
Gmsh library and sources, validates the help, and creates matching binary and
corresponding-source ZIPs under `artifacts/`. An older V1/V2 installable in that
directory enables additional upgrade tests; it is not required to build the
current package. `-SkipBackendBuild` reuses a previously built frozen backend.

The source build uses the pinned official Python 3.12.7 runtime. Its separate
source is available at https://www.python.org/downloads/release/python-3127/ ;
OpenSSL 3.0.15 sources at
https://github.com/openssl/openssl/releases/tag/openssl-3.0.15 . See
`THIRD_PARTY_NOTICES.md` for libffi, Microsoft and PyInstaller terms.
