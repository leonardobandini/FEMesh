# SPDX-License-Identifier: GPL-2.0-or-later
"""Dedicated frozen backend for the SAP2000 Gmsh v2 installation."""
from mesher_backend import ALLOWED_SCRIPTS, main

ALLOWED_SCRIPTS.add("sap_gmsh_mesher.py")

if __name__ == "__main__":
    main()
