# Corresponding source for FEMesh {VERSION}

The original FEMesh code is GPL-2.0-or-later and Gmsh 4.15.2 is GPL-2.0-or-later
under its own copyright holders. For the combined binary containing OpenSSL 3
(Apache-2.0), this distribution elects **GPLv3**, not GPLv2-only. Gmsh keeps
its original license and narrowly scoped exception. `LICENSE`, `GPL-3.0.txt`,
`LICENSE-APPLICATION.md` and `THIRD_PARTY_NOTICES.md` contain the applicable
terms. No CSI API binary is included; CSI is licensed separately.

Version v{VERSION} is a user release, following **v1.0.79,
the first downloadable user version**. Builds before v1.0.79 were development
or test builds. Equivalent public access to this release's source is provided
beside its binary ZIP on the release page:

https://github.com/leonardobandini/FEMesh/releases/tag/v{VERSION}

Download both `Sap2000QuadMesher-{VERSION}-source.zip` (plugin, installer,
Python backend, exact Gmsh Python binding, build scripts and instructions)
and `gmsh-4.15.2-source.tgz` (unmodified upstream Gmsh source). Each has an
accompanying `.sha256` checksum file. The SHA-256 values of the original
Windows Gmsh wheel and the exact DLL bundled here are recorded in
`THIRD_PARTY_NOTICES.md` and the source archive's build instructions.

The independently maintained CPython 3.12.7 runtime, OpenSSL 3.0.15,
libffi, PyInstaller bootloader and Microsoft redistributable components retain
their own terms; see `THIRD_PARTY_NOTICES.md` and `licenses/PYTHON-LICENSE.txt`.
The matching CPython sources are available from
https://www.python.org/downloads/release/python-3127/ ; OpenSSL 3.0.15 sources
from https://github.com/openssl/openssl/releases/tag/openssl-3.0.15 .

The same sources are also kept at stable public addresses if a newer version
later replaces this release page:

- Plugin/backend source: https://raw.githubusercontent.com/leonardobandini/sap2000-quad-mesher-updates/source-archive/v{VERSION}/Sap2000QuadMesher-{VERSION}-source.zip
- Original Gmsh 4.15.2 source: https://raw.githubusercontent.com/leonardobandini/sap2000-quad-mesher-updates/source-archive/gmsh-4.15.2-source.tgz

Development and test builds before v1.0.79 were not offered as official versions
for users; if someone obtained one, its existing rights remain in force. If you
redistribute this binary package, you must comply with the GPL's corresponding-
source requirements yourself.
