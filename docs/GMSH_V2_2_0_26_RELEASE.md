# Gmsh V2 2.0.26 — New UI, bilingual guide and upgrade for V1 users

## Scope

The installable Windows x64/.NET Framework 4.8 package replaces the V1 COM plugin through the existing SAP2000 **Tools > SAP2000 Quad Mesher** entry. It includes Python/Gmsh 4.15.2 as a frozen runtime; end users do not install Python or Gmsh separately. The V2 beta supports SAP2000 27.1 and the tested SAP2000 27.2 beta, with the limitations below.

The default window has **Gmsh | Additional Options | Gmsh JSON | Transfer Options** / **Gmsh | Opzioni aggiuntive | JSON Gmsh | Opzioni di trasferimento**. Symmetry now lives with the grouped holes and openings in Additional Options. Transfer Options contains FAST and numbered model backup. The exact option definitions, conditional enablement, defaults and JSON mapping are in [English](help-gmsh-v2/index-en.html) and [Italian](help-gmsh-v2/index-it.html) offline help. All 23 new-interface examples include the configuration screenshot, original/result SAP-generated SVGs, settings JSON and measured quality. The previous 24 Classic cases are retained only under the labelled historical guides.

The numerical meshing paths are shared by the former and current interfaces. Gmsh algorithm **9 (Packing of Parallelograms)** is not selectable or accepted by the backend: it caused two native worker crashes even with recombination/optimization disabled on the one-shell reference fixture. The historical 40-case local catalog `artifacts/gmsh-ui-preview-catalog-2026-10-09` preserves both failures and their exact inputs; it is separate from the installable package. The shipped offline help includes fresh source/result diagrams and screenshots of the actual 2.0.26 New UI.

## Test evidence and limits

- V2 Python backend tests and both language/layout tests: run from the built candidate, including the backend rejection of algorithm 9.
- 36 isolated SAP2000 atomic cases exercised in three parallel groups on the 27.2 beta; each run logged the actual Gmsh JSON. Unit normalization of the verification harness resolved false failures on selected edges, seams and holes; nTEST006, nTEST027–nTEST036 (except nTEST026) passed again with SAP database length units.
- **Known unresolved case:** nTEST026, three intersecting shells, 12 small circular holes, 50 mm nominal size and 20 mm diameter. Gmsh produced a JSON and mesh, but SAP2000 27.2's object-API `AddByPoint` reported success for a generated child that was not subsequently addressable (`GetPoints` returned code 1); modifier assignment returned code 1. The plugin rolled back the attempted mesh. This is not a successful SAP regression and should be inspected on this geometry; the source model is not overwritten by the test. The failure trace is preserved under `%TEMP%\opencode\sqm-v226-modifier-diagnostic-run\nTEST026\failure.txt`.
- Some completed meshes have quality warnings. Completion does not imply that size/shape checks passed; each regenerated help example states its actual `qualityPassed` and surface-weighted summary.

## Distribution and V1 migration

The V2 ZIP, its corresponding source ZIP, the pinned Gmsh source tarball and SHA-256 checksums are attached to the GitHub release. The `source-archive` branch permanently preserves corresponding source archives. The public `manifest-v2.json` advertises the new release to V2 users; the separately updated public `manifest.json` offers the same V2 ZIP to existing V1 users, whose updater accepts a higher version and uses the same installer/Tools registration. The installer replaces the per-user plugin only after SAP2000 is closed and verified backups/Undo remain the responsibility of the model workflow. Historical V1 source packages and releases remain available.
