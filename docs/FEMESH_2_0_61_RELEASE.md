# FEMesh 2.0.61 — SAP2000/CSiBridge

Before Generate checks options or creates a backup, FEMesh compares the editable `Connectivity - Area` and `Joint Coordinates` tables with the live object names. Only if the editing getter omits objects while the display getter contains all of them does the plugin show a bilingual, host-specific warning. It directs the user to `Display->Show Tables` and the `Selection Only` checkbox in the upper-right corner. The dialog stays ready to retry; a complete model produces no warning. FEMesh does not open SAP's table dialogs automatically.

The local candidate also retains verified numeric labels after Apply, the preview/Undo transaction and the menu registration for installed SAP2000/CSiBridge 27-or-later profiles. Six screenshots of the 2.0.61 window were freshly captured in Italian and English. The Classic archive is marked as historical and the current help has no other host references.

The binary ZIP is offered under both `Sap2000QuadMesher-2.0.61.zip` and `FEMesher-2.0.61.zip`, with identical SHA-256 checksums for compatibility with already installed update clients. Corresponding plugin source and upstream Gmsh source accompany the installer.

Host matrix results will be recorded after running the SAP2000 and CSiBridge suites on disposable copies.
