# SPDX-License-Identifier: GPL-2.0-or-later
"""Dedicated frozen backend for the SAP2000 Gmsh v2 installation."""
import sys

from mesher_backend import ALLOWED_SCRIPTS, main, self_test


FEMESH_VERSION = "2.0.68"

ALLOWED_SCRIPTS.add("sap_gmsh_mesher.py")

if __name__ == "__main__":
    if sys.argv[1:] == ["--version"]:
        print("FEMesh backend " + FEMESH_VERSION)
    elif sys.argv[1:] == ["--self-test"]:
        self_test()
        print("FEMesh backend " + FEMESH_VERSION)
    else:
        main()
