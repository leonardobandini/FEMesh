# Corresponding source for FEMesh {VERSION}

This binary package is distributed under the terms in `LICENSE` (GPLv2),
`GPL-3.0.txt`, `LICENSE-APPLICATION.md` and `THIRD_PARTY_NOTICES.md`. The
original program code is GPL-2.0-or-later. For the combined binary with
OpenSSL 3 (Apache-2.0), this release elects the GPLv3 option available for
our code and Gmsh. Gmsh retains its own, narrower exception. The SAP2000 API
is **not** distributed here.

Version v{VERSION} is a user release, following **v1.0.79,
the first downloadable user version**. Builds before v1.0.79 were development
or test builds. Equivalent public access to this release's source is provided
beside its binary ZIP on the release page:

https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/tag/v{VERSION}

Download both `Sap2000QuadMesher-{VERSION}-source.zip` (plugin, installer,
Python backend, exact Gmsh Python binding, build scripts and instructions)
and `gmsh-4.15.2-source.tgz` (unmodified upstream Gmsh source). Each has an
accompanying `.sha256` checksum file. The SHA-256 values of the original
Windows Gmsh wheel and the exact DLL bundled here are recorded in
`THIRD_PARTY_NOTICES.md` and the source archive's build instructions.

The same sources are also kept at stable public addresses if a newer version
later replaces this release page:

- Plugin/backend source: https://raw.githubusercontent.com/leonardobandini/sap2000-quad-mesher-updates/source-archive/v{VERSION}/Sap2000QuadMesher-{VERSION}-source.zip
- Original Gmsh 4.15.2 source: https://raw.githubusercontent.com/leonardobandini/sap2000-quad-mesher-updates/source-archive/gmsh-4.15.2-source.tgz

Development and test builds before v1.0.79 were not offered as official versions
for users; if someone obtained one, its existing rights remain in force. If you
redistribute this binary package, you must comply with the GPL's corresponding-
source requirements yourself.
