# Changelog

Le modifiche rilevanti saranno documentate in questo file seguendo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Storia di sviluppo:** tutte le versioni fino alla 1.0.78 inclusa erano build di sviluppo o di prova. Le precedenti pagine di download temporanee non costituivano una distribuzione agli utenti. La **1.0.79 e la prima beta destinata agli utenti**; le voci precedenti restano come storico tecnico.

## [Unreleased]

- Ongoing development notes remain in the local reports.

## [2.0.62] - 2026-10-22

- Check live area/joint tables before Generate and provide a host-specific warning if the editing tables omit objects hidden by Selection Only; preserve applied numeric labels and existing preview/Undo behavior.
- Keep all stations on circular O-grid hole boundaries at the specified diameter using true Gmsh arcs instead of chords. SAP2000 and CSiBridge atomic matrices: 36/36 PASS each on disposable model copies; eight 20 mm holes measured in an applied SAP2000 model at 10 mm radius with negligible numerical error.
- Publish the same verified package and corresponding sources in the FEMesh public release repository while keeping the legacy update feed for installed clients.

## [2.0.59] - 2026-10-21

- Recapture the current FEMesh window in Italian and English for all three help tabs; replace outdated interface screenshots and refer to both SAP2000/CSiBridge throughout the current bilingual guide. Keep historic SDB results separate from the current controls. Preserve the language selector in the header.
- Register Tools > FEMesh in initialized SAP2000/CSiBridge versions 27 and newer with `CSiAPIv1.dll`; verify future-profile menu migration on isolated 28/29/31 fixtures. Distribute the same verified installer under legacy `Sap2000QuadMesher-2.0.59.zip` and new `FEMesher-2.0.59.zip` names for existing update clients.
- Verify SAP2000 27.1 **36/36 PASS** using two persistent workers (18 cases each), and CSiBridge 27.1 **36/36 PASS** with saved/reopened BDB outputs. The nTEST029 input already contains 258 temporary-style names; the current mesh adds none.

## [2.0.54] - 2026-10-21

- Rebrand the installed UI and SAP2000/CSiBridge Tools entries as FEMesh without changing the existing COM identity or GitHub repository path. Restore FAST and backup checkbox availability after a late area selection while retaining their checked values. Select `CSiAPIv1.dll` from CSiBridge when SAP2000 is absent; install the Tools entry in both supported hosts.
- SAP2000 27.1: 36/36 atomic cases PASS across two persistent workers; Standard/FAST Preview Undo PASS. CSiBridge 27.1: 36/36 corresponding disposable SDB-to-BDB meshing trials PASS, with saved BDB results reopened; targeted FAST Apply/Undo 2/2 each PASS.

## [2.0.53] - 2026-10-20

- Align the backup checkbox and its multiline description in Transfer options. Keep the checkbox focusable and make its separate text label clickable; no meshing or SAP data-transfer change compared with 2.0.52. SAP2000 27.1 atomic catalog: 36/36 PASS on two persistent, parallel sessions (24 and 12 models opened sequentially per worker; licensing prevented a third simultaneous session).

## [2.0.52] - 2026-10-19

- When SAP2000's editing getter reports zero area design procedures after Show Tables although the display getter still has the original rows, capture the complete displayed procedures for the mesh and CSV Undo snapshot instead of treating them as missing. Check the complete transfer against live areas and area section assignments. If the children really remain at No Design, require explicit, non-suppressible consent before Apply and restore original design procedures via the snapshot on Undo.
- Validate 36/36 atomic SAP cases with four initial parallel SAP sessions (a SAP file-open timeout in group 1 required a new isolated session for its 9/9 retry), Standard/FAST preview Undo, the standalone installer, bilingual help and the user-reproduced Concrete_Barrier GUI sequence.

## [2.0.50] - 2026-10-16

- Include the local 2.0.47–2.0.49 FAST, joint identity, assignment-transfer, preview and backup-confirmation improvements. Center the non-dismissible Apply/Undo/view wait windows on SAP2000; show them before SAP view-menu actions and explain that the host may appear frozen until completion. SAP2000 27.1 atomic catalog: 36/36 PASS in four isolated sessions.

## [2.0.46] - 2026-10-15

- Investigate the `17_bug` circular and multiple-silo models on isolated SAP2000 copies; document 19 numbered combinations, three-worker results, error screenshots and the release blockers in `reports/BUG17_2026-10-14.md`.
- Require zero errors/warnings on V2 FAST insert/restore, pad SAP triangle connectivity without changing its three-joint count, and validate every backend triangle before attempting SAP insertion; verify object-API shell identities and filter orphan design-procedure rows while preserving live assignments. Retest the complete 36-case SAP catalog and the Python backend.
- Make the Gmsh 1D area-mesh guide intervals even before integrated Full-Quad methods 2/3 halve them. The original circular and multi-silo Full-Quad selections now generate all-quad meshes with zero SAP import errors and unchanged SAP frame inventories; selected immutable boundary edges and manual odd transfinite divisions are rejected instead of silently altered. The reported BAMG 7 configuration remains unresolved.
- Report nearly collinear BAMG failures in the selected UI language with a practical alternative (Gmsh algorithm 8), before SAP import and without a Python traceback or an undisclosed algorithm switch. Quality warnings remain visible but do not prevent generation. See `docs/GMSH_V2_2_0_46_RELEASE.md`.

## [2.0.32] - 2026-10-11

- Remove leftover V1 controls from the shipped V2 form (including the partially covered Tolerance control), and ignore formerly saved hidden V1 profile/strict-size/worker choices. Visible V2 options such as Gmsh sizes, hole settings, FAST and backup continue to restore normally.
- Align the quality report headline with its own graded metrics: when the aggregate acceptance checks pass and every displayed metric is EXCELLENT, display EXCELLENT QUALITY; otherwise retain ACCEPTABLE QUALITY or the failure headline as appropriate. The sizing thresholds, shape score, mesh generation and disclosed exceptions are unchanged.
- Wrap the full shell summary at the top of the quality dialog (including invalid elements), and give the two-row selection/result summary in the main plugin window enough vertical room. Verify English and Italian labels, the three headline outcomes and the real `Circular_Floor` default example without saving its source SDB.

## [2.0.30] - 2026-10-10

- Separate the supported V2 plugin into `PluginV2.cs` and retain the still-buildable V1 in `Plugin.cs`. Remove the dormant Classic Gmsh and old V1 options-tab construction from the V2 assembly, along with the unused Classic option catalog, developer-only plugin project and obsolete UI tests/generators. Preserve the historical Classic guide as an archive, not an available interface.
- Verify the complete V2 atomic catalog on three isolated persistent SAP2000 27.2 instances in parallel: **36/36 PASS** (12 per worker), with preserved original models, backend JSON and per-case import/conformity checks. The size-quality policy and Gmsh backend remain unchanged from 2.0.29.

## [2.0.29] - 2026-10-10

- Keep the actual longest free shell edge and size exceptions visible, but judge minor localized excess with the surface-weighted mean excess above the existing 20% size target. Fail when oversized shells cover more than 10% of surface, weighted excess exceeds 2%, or any free edge exceeds 1.5 times nominal size; original protected edges remain separate. V1 meshing and SAP2000 auto-merge tolerance are unchanged.
- On an isolated SAP2000 27.2 beta copy of `nTEST026`, the installed 2.0.29 reports `quality_passed=true` for the unchanged 1,096-shell mesh: shape score 0.793/1, size excess 0.064% by area, two disclosed size exceptions (1.854% of area) and maximum free edge 0.062 m versus 0.05 m nominal. This is a change to the quality policy, not a new geometry fix.

## [2.0.28] - 2026-10-10

- Align Generate/Apply, Mesh quality, Undo mesh and Reset defaults in one bottom row of four equal-width buttons. Reset restores all plugin defaults but preserves both typed shell sizes, including explicit units; disable it during generation. Update bilingual help and UI checks.
- Grade the free mesh outward from circular O-grid seams, safely flip eligible pairs of sliver triangles without moving joints or frame edges, and reject any remaining near-collinear transitions before SAP2000 import.
- `nTEST026` now imports on SAP2000 27.2 beta with all twelve 20 mm holes intact (1,096 shells; zero invalid elements). Quality is **not approved**: two size exceptions cover 1.854% of the area, with a maximum edge of 0.062 m against the nominal 0.05 m. Isolated O-grid and shared-seam checks also pass for `nTEST005` and `nTEST027`.

## [2.0.26] - 2026-10-09

- Rename the four default Gmsh tabs to **Gmsh | Additional Options | Gmsh JSON | Transfer Options** (Italian: **Gmsh | Opzioni aggiuntive | JSON Gmsh | Opzioni di trasferimento**) and move exact symmetry beside circular holes and frame openings, without changing its SAP/Gmsh behavior.
- Document every exposed New-interface control, numeric limit, internal fixed option and SAP transfer setting in bilingual offline help. Include 23 fresh SAP-verified New UI examples with option screenshots, original/result SVGs, backend JSON and honest quality status; retain the earlier 24 Classic examples separately as a historical archive.
- Keep Classic developer-only, remove unstable Gmsh algorithm 9 and preserve the V1/V2 installation identity. Regression of 36 SAP atomic examples recorded one real SAP 27.2 beta failure on `nTEST026` at its coarse-hole setting; all other cases pass after test-harness unit normalization. The failure is documented rather than counted as a pass.

## [2.0.24] - 2026-10-09

- Classify circular O-grid sectors only against coplanar SAP2000 areas, preventing perpendicular or inclined shells that overlap only in projection from being mistaken for competing sector owners.
- Add a non-coplanar multi-area O-grid regression and make batch boundary tracing available for diagnosing multi-shell generation failures.

## [2.0.23] - 2026-10-08

- Recover SAP2000 27.2 beta editing-table schemas when CSV values contain unquoted commas, without omitting affected material tables or weakening snapshot verification.
- Route FAST insertion through the object API when SAP exposes incomplete field keys or the generated mesh contains triangles, while retaining snapshot capture, assignment transfer and verified Undo.
- Restore area connectivity, section and design procedure atomically so newly reconstructed shells retain `Concrete Shell Design`; verify all assignments after Undo and accept SAP-generated GUIDs only where the original GUID was unspecified.
- Validate the final DLL with 36 FAST and 36 Standard Apply-to-Undo cases, plus four-node and eight-node pattern, thickness and joint-offset fixtures.

## [2.0.22] - 2026-10-08

- Transfer both documented SAP2000 area joint-offset modes to generated child areas: preserve joint pattern and scale for type 1, and geometrically interpolate explicit source-vertex values for type 2. Support triangles, quadrilaterals and general polygons in the assignment path shared by Standard and FAST, then read every assignment back through the SAP2000 API before completing the mesh.
- Treat return code 1 from `GetPatternValue` as the effective zero value when a defined pattern has no explicit point-assignment row. Keep other nonzero API codes as errors and cover both explicit and implicit pattern values in four-node and eight-node SAP fixtures.
- Record recoverable generation failures in `plugin-errors.log` before rollback and localization, without logging user-requested cancellation as a fault.
- Document the offset transfer rules, validation limits and remaining manual design-overwrite review in the bilingual offline help and engineering log.

## [2.0.21] - 2026-10-08

- Improve interior joint-pattern transfer for parent polygons with more than four joints by using an affine-preserving thin-plate interpolant, while retaining exact linear boundary values, bilinear quadrilateral values and mean-value thickness interpolation. Clamp joint-pattern results to the source range, as observed in SAP's nonnegative native basis weights.
- Validate interpolation with symmetric-difference volume instead of signed volume alone. On the irregular eight-joint fixture the local boolean-volume difference against SAP falls from 18.25% to 15.33%; across eight independent native SAP basis patterns, weight RMS falls from 0.06708 to 0.05727. The other two atomic fields remain unchanged.
- Propagate every readable nonzero joint pattern to generated joints and preserve pattern-driven area assignments. Use exact edge interpolation, inverse bilinear natural coordinates for four-node parents and mean-value coordinates in the parent plane for polygonal parents.
- Transfer nodal area thickness overrides to every child with the same geometric weights, including padded SAP triangle arrays, and verify joint-pattern and thickness values through the object API before completing the mesh. Add real four-node and eight-node SAP fixtures and an in-memory regression trial.
- FAST uses full-model SAP2000 tables for mesh insertion and Undo; because SAP2000 27.1 cannot import polygon continuation rows at zero errors, Undo has a narrow object-API exception for missing original areas with more than four joints and their missing prerequisite joints. Standard keeps the per-object insertion and recovery path. Validate complete area/joint inventories before tabular Undo and verify geometry, GUIDs, coordinates, sections and object assignments afterward.
- Keep unsupported parent-to-child design settings visible in the status tooltip and diagnostic trace without interrupting generation with the initial modal warning.

## [1.0.120] - 2026-10-05

- Correzione del crash SAP2000 durante l'interazione con la finestra del plugin. Due dump WER del processo SAP2000 mostrano la stessa `System.NullReferenceException` nel reverse P/Invoke del callback `SetWinEventHook` sul thread ausiliario del plugin durante `Application.DoEvents()`. Eliminare hook e message loop nativo dal watcher: il solo avviso esatto `Plugin completed successfully.` viene ora riconosciuto mediante polling Win32 protetto; nessun altro avviso SAP2000 viene nascosto. Gestire inoltre le eccezioni nei thread della finestra e dell'annullamento con diagnostica locale `plugin-errors.log`, evitando che un errore UI non gestito termini SAP2000. Eliminare anche la corsa fra rilascio del callback e smaltimento del segnale usato per avviare il thread della finestra. Su copia isolata con un nodo non salvato, 160 click sulla simmetria disabilitata non hanno terminato SAP2000 né rimosso il nodo.

## [1.0.119] - 2026-10-04 (build locale di prova)

- Intercetta l'avviso nativo SAP2000 di completamento tramite l'evento di comparsa della finestra, nascondendo e chiudendo solo il messaggio esatto senza toccare gli errori. Centra la finestra indipendente di annullamento su quella del plugin. Il valore iniziale della tolleranza diventa 20%, mantenendo le preferenze salvate e ripristinando il valore precedente quando si disattiva l'inserimento di nodi sui bordi selezionati.
- Nel percorso simmetrico con frame e bordi vincolati, prepara una mesh meno fitta prima della suddivisione finale e privilegia, fra i candidati con dimensione e forma ammissibili, quello con meno quadrilateri. Prova SAP2000 su copia isolata di `mod1.sdb` a 1 m e 20%: 2.914 → 548 quadrilateri, spigolo mediano lontano dai frame 0,25 → 0,705 m, percentile 90 pari a 0,857 m, massimo 1,084 m, zero triangoli, simmetria esatta; Annulla ripristina area, 14 selezionati e file originali. Rimangono segnalati alcuni angoli fuori riferimento (distorsione massima 48,626°). Tutte le 36 regressioni SAP2000 sono PASS sulla versione finale.

## [1.0.118] - 2026-10-04

- Adopt the author's revisions to the Italian help and align the English help: a direct mesh-generation heading, concise introduction and practical 20% tolerance guidance. Vertically center the GPL, update-status and version labels in the dialog footer; show only the version number in the interface and guide. Include the verified bilingual offline help, annotated SVG examples, screenshots, taskbar icon and responsive cancellation from the local 1.0.116–1.0.117 builds.

## [1.0.117] - 2026-10-04 (build locale di prova)

- Add offline, language-matched Italian/English HTML help opened by F1 or the title-bar ? button. Explain the workflow and each tab with real UI screenshots; include five verified atomic examples as localized before/after SVGs annotated with selected joints, frame boundaries and hole centers. Add an original multiresolution Quad Mesher icon to the options and quality windows and the Windows taskbar. Package and validate all help, screenshot and vector assets together with their reproducible build scripts.

## [1.0.116] - 2026-10-04 (build locale di prova)

- On a 302-area/355-node selection of TEST03, generation could block before the Undo button was enabled. Offer an independent responsive cancellation window even while preparing the initial selection, enter the cancellable work state before capturing the model snapshot, add periodic cancellation checkpoints to table capture and multi-area boundary/constraint preparation, and eliminate quadratic CSV-row slicing during snapshot writing. Keep rollback and original selection restoration in the existing cancellation path. On an isolated TEST03 copy, cancellation at 1, 4 and 9 seconds restored all 302 areas and 657 selected objects; all 36 atomic regressions passed before the final startup-cancellation extension.

## [1.0.115] - 2026-10-04

- Remove the external CUBIT and COMSOL hyperlinks from the mesh-quality dialog, retaining its numerical metrics, reference ranges, quality checks and Close action. Publish the locally verified interface, preview/navigation, Apply/Undo and meshing improvements from 1.0.102–1.0.114 as the next beta update.

## [1.0.114] - 2026-10-04 (build locale di prova)

- Auto-dismiss only SAP2000's native `Plugin completed successfully.` dialog (window class `#32770`, SAP2000 caption and owner, exact static text and OK button), immediately after the early plugin callback. Keep other SAP2000 warnings untouched. Confirm the exact native dialog closes and restores the SAP2000 main window without closing the Quad Mesher preview.

## [1.0.113] - 2026-10-04 (build locale di prova)

- After the user confirmed SAP2000 zoom works with the 1.0.112 callback change, keep the options window always on top during the unapplied preview, including after Apply and Undo. The SAP2000 viewport remains interactive in the visible, uncovered area. Verify the topmost dialog and enabled viewport together in the native-window UI test.

## [1.0.112] - 2026-10-04 (build locale di prova)

- Release the SAP2000 plugin callback before running the interactive options window on an STA thread. SAP2000's host command loop stayed blocked despite the modeless dialog and Win32 window being enabled; returning from Main permits native viewport input in the still-unapplied preview. Keep scripted/atomic runs synchronous and reject a second simultaneous interactive dialog.

## [1.0.111] - 2026-10-04 (build locale di prova)

- During the generated-mesh preview, release the SAP2000 main window if the plugin host disabled it and remove the dialog's always-on-top setting; the dialog stays accessible from the taskbar. Temporarily pause viewport interaction during generation, Apply and Undo, then restore the host window's previous state on close. Exercise the native enabled/disabled-window transitions in the three-action UI test. This window-level change alone did not unblock native SAP2000 navigation; see 1.0.112.
- Gather regression, development and bug-reproduction `.sdb` models in a local Desktop collection with original paths and SHA-256 checksums; keep source files and numbered backups untouched.

## [1.0.110] - 2026-10-04 (build locale, pronta per verifica)

- Il report degli oggetti generati sostituisce i conteggi della selezione nello stesso riquadro e senza spostare le schede; Annulla, cancellazione ed errore ripristinano la selezione iniziale.
- Se la mesh richiesta non riesce, il recupero prova prima ad aggiungere nodi sugli spigoli con nodi selezionati, mantenendo inizialmente la simmetria; il controllo nella finestra riflette l'opzione effettivamente usata. I messaggi di errore del generatore non mostrano traceback misti italiano/inglese; i dettagli originali rimangono nel registro diagnostico.

## [1.0.109] - 2026-10-04 (build locale di prova)

- Expand the upper selection panel after mesh generation with a second, bilingual inventory of all effective model objects: total shell areas broken down into quads, triangles and polygons, frames, links and joints. Exclude original areas temporarily retained for Undo from the preview count; refresh the inventory after Apply. Undo, cancellation and failure return the panel and selection to their original state. Keep the bottom status, element count, progress and three actions in place. Verify the post-mesh and restored counts on isolated `Multiple_Silo_Slab` (2,284 quads, 75 frames, 0 links, 2,409 joints in preview; original six areas and 179 selected objects after FAST Apply/Undo), plus modern/legacy and language-specific UI regressions.

## [1.0.108] - 2026-10-04 (build locale di prova)

- Apply the author's Italian wording edits in `docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md` to the actual options dialog, supply corresponding English labels and tooltips for Standard, Regular/Aligned, Refinement, symmetry, strict-size subdivisions and radial bands, and use "Frame" consistently in Italian UI text. Keep the material presets and meshing behavior unchanged. Verify both languages and the modern/legacy layouts, including label bounds and runtime tooltip text.

## [1.0.107] - 2026-10-04 (build locale di prova)

- Extend exact symmetry to non-regular, multi-area meshes: reflect generated elements and protected boundaries into matching source areas, use the existing half-domain mesher for areas invariant under reflection, preserve target-specific SAP2000 assignments, and verify topology across the full selection. Keep symmetric strategies ahead of nonsymmetric recovery alternatives; validate reflected selected joints, frames, boundaries and circular-hole pairs. On an isolated six-area `Multiple_Silo_Slab` with 98 joints and 75 frames selected, strict 0.5 m Standard with exact symmetry generates 2,284 quads and zero triangles; Regular automatically chooses that symmetric Standard solution, and FAST Apply/Undo restores the original assignment tables.
- For multi-area selections, calculate per-element shape quality and aggregate by shell surface area instead of listing the worst value of each original area. Display the area-weighted overall score, average element metrics, low-quality element count and affected area share; keep maximum size, inversion and degeneracy as hard checks. A synthetic 1,000-element regression confirms that one small outlier does not dominate the mean, while a single over-limit or inverted element fails. References and the plugin's score formula are in `docs/QUALITA_MESH_AGGREGATA.md`.
- Rename the options tabs to **Opzioni della mesh | Fori e Aperture | Opzioni Avanzate**, with English equivalents **Mesh Options | Holes and Openings | Advanced Options**. Record every current Italian option label and tooltip for editorial review in `docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md`. Material-profile behavior is unchanged pending the planned true default-option presets.

## [1.0.106] - 2026-10-04 (build locale di prova)

- Recover automatically when the requested meshing strategy fails: prepare alternative Standard, Refinement and Regular meshes without changing the SAP model, reject broken shared edges and strict-size/orientation violations, and select a viable candidate by quality acceptance, number of elements, triangles and area-weighted quality score. Preserve all selected joints, frames, openings and the requested maximum size. Only the chosen candidate enters the existing FAST/COM preview, Apply and Undo flow.
- After automatic recovery, report the effective strategy, size, retained constraints, symmetry, element/triangle counts and quality warnings; remember the effective settings for the next interactive run. On an isolated copy of the current Multiple_Silo_Slab selection (6 areas, 98 joints, 75 frames, 0.5 m strict), Regular fails on area 8; Standard generates 2,316 quads and no triangles, with no invalid elements or edges above 0.5 m. Some quadrilateral angles/Jacobians remain outside the acceptable-quality thresholds and are explicitly reported.

## [1.0.105] - 2026-10-02 (build locale di prova)

- Present selection-at-opening counts for original triangular, quadrilateral and polygonal areas, frames, links and joints below the existing blue header. Reorganize the same meshing controls into three task-based tabs (Mesh, Holes, Advanced), with a compact material preset and mutually exclusive Standard/Regular/Refinement radio choices. Keep generation status, created-element count, progress and the three original actions visible below the tabs. Preserve the former layout behind `SAP_QUAD_OPTIONS_LAYOUT=legacy` for immediate visual rollback. The aggregate quality-report proposal is documented but not implemented.
- Validate all 36 isolated SAP2000 atomic examples. On Multiple_Silo_Slab, the modern and legacy layouts produce byte-identical backend meshes on all six source areas and preserve seven shared seams; FAST/COM Apply-to-Undo, frame openings, circular holes and both languages pass focused regressions.

## [1.0.104] - 2026-10-02 (build locale di prova)

- Prevent specialized rectangular transitions from dropping prescribed stations on a third side of a shared shell. In frame-constrained meshing, distinguish a first area's deliberate full-quad boundary refinement from a later area's already-generated seam: preserve the latter instead of subdividing it again. Align selection-wide Cartesian guides before meshing regular shells with selected interior points; reject grid cells distorted by very close fixed joints or oblique frames with actionable alternatives. Reproduce the 0.5 m Multiple_Silo_Slab mismatch between areas 8 and 9 on an isolated copy, then verify all seven original shared seams in standard, regular and stress-refined FAST/COM configurations. The proposed task-based options layout and area-weighted quality report are documented only, not implemented.

## [1.0.103] - 2026-10-02 (build locale di prova)

- Apply now commits the generated mesh immediately, removing the original areas while keeping the three-button modeless dialog and Undo available. Capture all nonempty editable SAP2000 model tables and original global joint positions in an integrity-checked local CSV snapshot before generation; Undo removes only the generated mesh and restores source geometry, GUIDs, area/joint assignments, loads, restraints, patterns, groups, local axes, masses, modifiers and edge constraints. Keep the snapshot after Apply for recovery; cancel an unapplied preview without changing the original model. Verify exact assignment-table round trips on annotated Nodo_2 copies in FAST and COM, a partial selection with untouched neighboring areas, and pre-existing polygons/triangles.
- Re-run all 36 SAP2000 atomic examples to PASS on the local 1.0.103 implementation, including FAST and COM multi-area insertion, symmetry and framed openings.

## [1.0.102] - 2026-10-02 (build locale di prova)

- Replace the four bottom buttons with three ordered actions: Generate (then Apply), Mesh quality, and Undo mesh at the right. Apply keeps the modeless topmost dialog open and preserves its Undo until the window closes; closing after Apply finalizes the mesh, while closing an unapplied preview restores the original selection and geometry. During generation the right-hand Undo button safely cancels the current attempt. Verify Apply then Undo on real FAST and standard COM meshes, and leave the SAP viewport usable for zoom.

## [1.0.101] - 2026-10-02

- Release the verified 0.6–0.7 m conforming annular-sector improvements and Cartesian steel-shell meshing from local trials 1.0.98–1.0.100. On Nodo_2, strict 30 mm regular meshing produces 1,653 quadrilaterals with no hanging intersection nodes; strict 100 mm produces 128 Cartesian squares. Keep automated regressions independent of persisted interactive options. Preserve the source models and validate FAST Undo, all 30 original joints, and the full SAP2000 atomic regression catalog.

## [1.0.100] - 2026-10-02 (build locale di prova)

- Prevent a synthetic regular-mesh midpoint from splitting an unprescribed boundary on only one of two intersecting orthogonal shells. On an isolated Nodo_2 copy with all 14 areas and 30 joints selected, Steel profile, regular meshing and strict 30 mm maximum, verify 1,653 axis-aligned quads, all original joints connected, no edge over 30 mm, and FAST Undo. The 100 mm grid and regular/symmetric atomic cases remain valid.

## [1.0.99] - 2026-10-02 (build locale di prova)

- Offer regular aligned meshing in the Steel Structures profile with a direct switch from the default stress refinement. Allow a rectangular Cartesian grid across preselected boundary joints when its exact stations preserve locked edges, including strict-size subdivision; explain when an immutable edge instead prevents the grid. On isolated Nodo_2 copies at 0.1 m, verify 128 all-quad square elements with the 30 source joints connected, conforming multi-plane intersections, and FAST Undo restoring original areas, joints and selection.

## [1.0.98] - 2026-10-02 (build locale di prova)

- Keep selection-wide annular bands conforming when 0.6–0.7 m sizing introduces missing guide stations or extra selected-edge stations. Insert shared guide nodes consistently, allocate enough radial transition rows, and use a local opening collar only for long immutable intervals. Fall back to the frame-constrained mesher when the complete selection cannot support a sound band; extend its strict-size search before reporting failure. On isolated copies of Circular_Floor, verify 0.5, 0.6 and 0.7 m with and without strict sizing, matching original circle joints, maximum strict edge size, and FAST Undo.

## [1.0.97] - 2026-10-02

- Show the available-update link as two centered lines inside the footer space, keeping the Italian announcement and the download/version line fully visible. Verify Italian and English layout and text bounds at runtime.

## [1.0.96] - 2026-10-02

- Re-enable the strict maximum mesh-size checkbox after Undo mesh, allowing the next generation to enforce the limit between selected nodes. Verify two consecutive Generate/Undo dialog cycles and FAST Undo on an isolated SAP2000 model.

## [1.0.95] - 2026-10-02

- Keep the modeless plugin dialog in front of SAP2000, including after the immediate Generate refresh, while SAP2000 remains enabled for inspecting the preview mesh.
- Pass all 36 isolated SAP2000 atomic regressions on the 1.0.95 package, including FAST and standard insertion, multi-area seams, symmetry, framed openings, circular holes and immutable selected nodes. Verify the circular-floor dense-band mesh preview (1,956 shell elements) and FAST Undo against the unmodified source model.

## [1.0.94] - 2026-10-01 (build locale di prova)

- Refresh the SAP2000 viewport immediately after Generate so the preview mesh is visible before Apply. Keep the SAP2000 window enabled and open the plugin as an independent modeless taskbar window, allowing the user to switch between mesh inspection and Apply/Undo.

## [1.0.93] - 2026-10-01 (build locale di prova)

- Integrate the geometry-fitted dense global band for compatible multi-sector radial slabs, preserving original frames, exterior joints and conforming seams; fall back to the previous structured mesher when the guide fit fails. The original circular-floor SAP trial at 0.5 m and 25% tolerance imports 1,848 quads and 108 triangles (1,956 shells); FAST Undo restores the source model.
- Remember validated generation settings per user across plugin launches (including explicit lengths converted across model units); keep automated regression settings separate.
- Defer the SAP2000 view refresh until the dialog closes, and localize additional model, mesh and FAST error messages.
- Allow local installer replacement when an existing installation directory cannot be renamed because an unchanged PDF is open; preserve rollback and skip only byte-identical locked files. Include the new dense-band module in the corresponding-source archive.

## [1.0.92] - 2026-09-30

- Expose the automatically geometry-selected radial quad bands as a default-on dialog option, "Prefer structured quad bands in framed radial slabs" / "Preferisci fasce quad ordinate nelle solette radiali con telai". Unchecking it retains the prior mesher. The option is routed to the backend for every generation, without model-name or test-ID exceptions.
- Preserve the separate v1.0.91 comparison report outside the installable and source archives. All 36 atomic SAP2000 regressions pass with the option checked by default, with identical saved meshes and diagrams to v1.0.91. On the original circular slab, checking the option generates 1,823 shells (138 triangles), versus 2,439 shells (364 triangles) when unchecked; FAST Undo restores all original objects. Verify the same outputs using the installed build.

## [1.0.91] - 2026-09-30 (build comparativa locale, non pubblicata)

- Automatically select the structured radial-sector route by geometry: a horizontal annular sector, a selected outer chord, compatible radial sides and guide chains. Other framed polygons keep the existing Gmsh path. `SAP_QUAD_SECTOR_BLOCKS=0` disables the route for controlled comparisons without any file or test ID branches.
- Compare the existing 36-example SAP regression baseline with a separate run and store the graphical comparison outside the distributable archive; do not modify the public update manifest or installed v1.0.90 during the experiment.

## [1.0.90] - 2026-09-30 (build locale, non pubblicata)

- Add an explicit, default-zero maximum-edge tolerance percentage (0–50%) in the mesh dialog. It keeps the nominal mesh spacing unchanged while permitting the stated excess on newly generated edges; strict meshing between selected nodes disables the tolerance.
- Build topologically graded quadrilateral bands across compatible radial sectors and complete selected guide chains, with a local first collar where immutable opening edges exceed two nominal steps. Preserve frame coverage, fixed boundary stations, conformity and FAST Undo; the sector-block route was initially opt-in pending wider validation.
- On the isolated `Circular_Floor` selection at 500 mm with 25% tolerance, generate 1,685 quadrilaterals and 138 triangles (1,823 total); measure a maximum free edge of 615.6 mm below the explicit 625 mm limit, without local edge-splitting repairs. Retain the 120 original outer-circle stations and every selected hole station.

## [1.0.89] - 2026-09-29

- Restore polygon GUIDs correctly after FAST Undo: SAP2000 continuation rows must not replace the area's primary connectivity row during verification. Exercise the actual Undo action on `tt.sdb` (two triangles, a quadrilateral and a seven-sided polygon), on the triangle and polygon individually, and in standard COM mode; compare original area and joint identities after the rollback.
- Before each interactive mesh, offer an enabled-by-default numbered copy of the last saved `.sdb` in the same directory; preserve previous backups, fail before changing the model if the copy fails, and explain that unsaved changes must first be saved in SAP2000. Test two successive numbered copies on an isolated test model.
- Favor size-compliant, less over-refined Gmsh candidates when reducing a few remaining triangles would otherwise multiply shell count. On `tt` at a strict 1000 mm edge limit, reduce 1017 elements to 563 (17 triangles in both cases); the SAP2000 reference has 303 all-quadrilateral shells but a measured maximum edge of approximately 1184 mm.
- Indicate when the installed version is up to date and highlight an available update with a blinking, prominent download link. Network failures still leave a manual retry link.

## [1.0.88] - 2026-09-29

- Do not treat the coarse edges of an unselected coplanar shell fully contained in a selected null-property area as immutable shared seams. Such overlapping shells must remain untouched, while the selected null area can respect the requested mesh size in both directions. Actual neighboring seams remain constrained.
- Reproduced the defect on the pre-fix package: area 294 alone at 500 mm generated eight elongated quads with 2340 mm edges. The final v1.0.88 package generated 36 quads with maximum edge 455 mm and maximum aspect ratio 1.72; the structural shells 86 and 87 retained their original vertices and section `N.ParetiSp40`. The original SAP2000 model was not saved. All 36 atomic SAP2000 regressions passed with three parallel persistent instances after the fix; the rebuilt installable package passed its backend and installer checks and the specific 294 test.

## [1.0.87] - 2026-09-29

- Preserve actual joint segments from unselected neighboring triangles, quadrilaterals and polygons when meshing an area; on TEST02b, area 2 at 600 mm reuses all 16 SAP joints and shared-edge segments of its already meshed triangular neighbor.
- Import generated triangles through FAST without exhausting SAP2000's 20-error limit by repeating Joint3 in the Joint4 table field, which SAP2000 reads back as a three-node area. Keep exact diagnostic checks for pre-existing triangles and polygon continuation records.
- Add bounded parallel Gmsh candidate processes for constrained general polygons, with cancellation of the whole process tree, per-candidate and total time limits, boundary and quality checks. Default to the maximum available workers; allow 1 through the machine's logical CPU count, capped at runtime by the nine independent candidates and available memory. Gmsh remains CPU-based.
- Generate conforming 400 mm meshes of TEST02 areas 1 and 2 in FAST with regular, refined and no optional mode, preserving their shared edge. Confirm on reopened copies of TEST03 that areas 1 and 3 at 500 mm preserve the 300 unselected areas. All 36 atomic regressions passed sequentially in one monitored persistent SAP2000 instance; the new v1.0.87 report documents their times and an identical-geometry, one-worker versus maximum-worker backend comparison.

## [1.0.85] - 2026-09-28

- Accept only the expected SAP2000 blank-joint import diagnostics for pre-existing triangular areas and continuation rows of polygons in FAST table imports and restores. Match the original record and joint field exactly; errors in generated connectivity remain fatal. Include the relevant detailed log in unexpected FAST import failures.
- Reproduce the error on area 294 of a mixed-shell model at 600 mm, then verify general, regular and refined FAST meshes and preservation of its three triangles; verify a five-node polygon retained while another area is meshed. Mesh areas 294, 296, 298 and 74 successively on reopened copies without changing prior areas, with all new edges below 600 mm. All 36 atomic regressions passed using three persistent monitored SAP2000 instances.

## [1.0.84] - 2026-09-28

- Add `SapQuadTransitionPlugin` to the current user's SAP2000 27 Tools menu automatically after installation, retaining other plugin names and their order. Unhide an existing menu record instead of duplicating it; repeat installation remains idempotent.
- Update both SAP2000 plugin preference files using staged replacements with rollback on error. If preferences have not yet been initialized, explain how to add the menu entry manually after starting SAP2000.
- Confirm the menu appears in SAP2000 with a local v1.0.83 installer trial; verify normal, repeated, hidden and locked-preference scenarios on separate test profiles.

## [1.0.83] - 2026-09-28

- Preselect the existing FAST bulk-import option when the plugin dialog opens. Users can still turn FAST off to use the standard COM path.

## [1.0.82] - 2026-09-28

- Enable **Cancel generation / Annulla generazione** while meshing. Stop the owned Python/Gmsh backend promptly, or wait for the current indivisible SAP2000 API call to return, then undo imported COM/FAST objects and restore the original selection before allowing another attempt. Keep UI pumping limited to the existing backend wait and infrequent, time-gated checks when assembling large tables.
- Accept explicit `m`, `cm`, `mm`, `ft` and `in` in maximum-mesh-size and circular-hole-diameter inputs; bare values still use the current SAP2000 length unit. Show both options in bilingual tooltips and display the converted value before meshing.
- Verify cancellation during the backend, single-area FAST, multi-area FAST after import and standard COM insertion on separate SAP2000 copies. Check the five length units, implicit units and invalid values, and compare explicit-unit meshes to the same numeric settings.
- Run all 36 atomic integrations to PASS with three controlled persistent SAP2000 workers on the corrected code, without changing the historical development PDF.

## [1.0.81] - 2026-09-27

- Keep automatically refined seams conforming when **Prefer regular meshes** falls back to the general mesher for inclined surfaces or skew frames. Revalidate the selected-area shared edges before any FAST import.
- Allow a small corner-centered circular hole to preserve all prescribed boundary nodes: adapt the quarter O-grid radial layers when the hole diameter is much smaller than the requested maximum size. Verify the 0.03 m hole on four selected nTEST006 areas, 0.10 m maximum size and FAST.
- Verify nTEST026 with three intersecting areas, regular preference, 0.05 m maximum size and twelve holes of diameter 0.02 m. All 36 examples passed in a full regression with three controlled persistent SAP2000 instances; the independent small-hole nTEST006 check confirmed an empty 0.03 m opening and both reflection axes.

## [1.0.80] - 2026-09-27

- Generate all selected-area meshes in sequence while propagating shared-edge constraints, then use one FAST table import for their points, quadrilaterals and sections; preserve per-area loads, the full-selection preview and undo.
- Prevent Gmsh's global refinement from subdividing already-refined shared edges a second time. Verify coincident segments before importing: fixes non-conforming MODO plate/wall intersections in refined mode and the shared seams of four-area framed openings, including nTEST028 and nTEST036.
- Recheck regular MODO geometry and properties against v1.0.79, refined MODO, 3D perforated intersections, symmetric multi-area holes and FAST multi-area undo. The recorded timings are single development comparisons with another SAP2000 instance open, not performance guarantees.

## [1.0.79] - 2026-09-26

- First downloadable educational beta intended for users: demonstrate C# and Python/Gmsh integration with SAP2000 through a working quadrilateral mesher.
- Clarify development-only history and report provenance; simplify authorship/licensing explanations without attributing any rights in third-party software to the author.
- Preserve source archives at stable public URLs while retaining only the newest binary release.

## [1.0.78] - 2026-09-26

- License the original code under GPL-2.0-or-later, with a narrowly scoped additional permission for the separately installed SAP2000 API; preserve separate third-party licenses and elect the GPLv3 option for the combined binary backend.
- Publish matching source archives for the C# plugin, installer, Python backend and Gmsh 4.15.2 alongside the binary release.
- Validate that the bundled Gmsh DLL and Python binding match the official Windows wheel before packaging.

## [1.0.77] - 2026-09-26

- Fix the CMD installer launcher: derive the package directory from the executable instead of passing a quoted path ending in `\`, which .NET interprets as an invalid path.

## [1.0.76] - 2026-09-26

- Restore the single per-user installation directory name `SAP2000QuadMesher` and retain staged replacement/rollback.
- Center the update link in the footer and add a bilingual "Verified examples" link above the language selector to the bundled atomic-report PDF.
- Label the historical PDF with the tested plugin version (0.0.57) and clarify that its durations cover complete SAP2000 regressions, not current mesh-generation speed.

## [1.0.75] - 2026-09-26

- Install from the extracted release into `%LOCALAPPDATA%\Programs\SQM_Plugin`, replacing the previous installation only after validating the new package; downloaded files are not the runtime location.
- Bundle a native .NET installer invoked by `install_plugin.cmd` without PowerShell execution-policy bypass; preserve per-user COM registration and migrate the former installation directory after success.

## [1.0.74] - 2026-09-26

- Development build introducing the `MAJOR.MINOR.BUILD` scheme; carries forward the tested regular-mesh and TLS update fixes from 0.5.11.
- Future internal builds increment the third component; important features increment the second, radical changes the first.

## [0.5.11] - 2026-09-26

- Move the update link into the right-hand footer beside the plugin version.
- Negotiate TLS 1.2 explicitly for update checks when hosted inside SAP2000.

## [0.5.10] - 2026-09-26

- Propagate generated plate intersection edges to subsequent selected areas so the regular FAST mesh of MODO with a 30 mm maximum size and 30 mm holes shares nodes and edges with adjacent vertical shells.
- Link available updates directly to the public release ZIP, with instructions to extract it and run the bundled installer after closing SAP2000; validate the versioned download URL from the manifest.

## [0.5.9] - 2026-09-25

- Open the options dialog without selected areas, with generation and dependent options disabled until an area is selected and the dialog reopened.
- Replace the CSi Italia footer text with the bundled logo, retaining the website link.
- Check a GitHub-hosted version manifest asynchronously and offer a release link when a newer version is available.
- Preserve the user's SAP2000 plugin menu during parallel showcase runs.

## [0.0.59] - 2026-09-25

- Generate O-grid candidates before expensive clipped-hole fallbacks; run the fallback only if no O-grid candidate passes existing quality checks.
- On MODO with ten holes and three frame constraints, the backend fell from 250.3 s to 15.1 s (94% faster), while all 7,312 quads, section assignments, and pixels of the rendered mesh remained identical.
- Added optional per-process backend timing and an automated three-instance MODO showcase with before/after SVGs and a dedicated DOCX/PDF report.

## [0.0.58] - 2026-09-25

- Convert the default maximum mesh size (0.1 m) and O-grid hole diameter (0.05 m) to the active SAP2000 length unit when opening the dialog.
- Display elapsed generation time alongside the number of completed area elements.

## [0.0.57] - 2026-09-25

- Added a refined all-quad circular-hole fallback when a structured O-grid cannot fit between frame or incident-shell constraints.
- Preserved exact circular-boundary nodes and required every frame/incident constraint segment to coincide with shell edges in the fallback mesh.
- Clipped selected frames to the union of selected areas, allowing constraints to extend beyond the remeshed region.
- Fixed frame coverage across shared area boundaries by partitioning each constraint against the complete selected-area union.
- Added focused verification for a 0.20 m circular hole at a four-area intersection with four skew frame constraints.

## [0.0.56] - 2026-09-25

- Reworked regular unequal-edge transitions to create a large Cartesian region aligned with the rectangular area edges.
- Confined unavoidable topology changes to the smallest transition band that satisfies edge-length, aspect, skew, and Jacobian limits.
- Strengthened nTEST034 to require at least 80 percent of internal edges to align with the two principal area axes.

## [0.0.55] - 2026-09-25

- Added runtime English/Italian localization for the complete plugin interface, including progress, validation, and quality reporting.
- Renamed the post-generation close action to Apply/Applica to clarify when the generated mesh is committed.
- Added regular horizontal-chain alignment to exact-symmetry transitions with unequal immutable opposite-edge discretizations.
- Extended nTEST034 to combine regular alignment, exact symmetry, and preservation of all 46 selected edge nodes.

## [0.0.54] - 2026-09-25

### Added

- `nTEST034` verifies that exact symmetry preserves the immutable 11-node and 35-node opposite-edge discretizations.
- Symmetric transition meshes are geometrically revalidated before insertion into SAP2000.

### Fixed

- Exact-symmetry generation for rectangular opposite-edge transitions no longer inserts midpoint nodes between explicitly selected boundary nodes.

## [0.0.53] - 2026-09-25

### Added

- The options and mesh-quality dialogs now use the report visual language, with a white canvas, Segoe UI typography, navy headers, blue actions, and light borders.
- Both dialogs include a footer link to CSi Italia and the current plugin version.
- Atomic regressions now compare actual SAP point names and segment sets across the shared edges of four-area meshes in general, stress-refined FAST, and standard COM modes.

### Fixed

- Frame-constrained macro areas no longer apply geometry-dependent extra global refinement that could create hanging nodes on only one side of a shared edge.
- Standard COM insertion now explicitly reuses the common coordinate index, matching FAST insertion and preventing coincident duplicate joints.

## [0.0.52] - 2026-09-25

### Fixed

- Multi-area exact-symmetry O-grids are no longer rejected by the regular-mesh guard.

## [0.0.51] - 2026-09-25

### Fixed

- Atomic regression startup now attaches by SAP2000 process and rejects launcher instances without a valid model.
- Atomic batches can skip report regeneration while the Word report is open.

## [0.0.50] - 2026-09-25

### Fixed

- Restored full-solution compilation by declaring the WinForms and drawing references in the duplicate FAST test project.

## [0.0.49] - 2026-09-25

### Changed

- Final validation build for the combined TEST10 and TEST11 symmetry, refinement, frame-opening, and circular O-grid workflows.

## [0.0.48] - 2026-09-25

### Added

- Circular O-grid holes can coexist with selected frame and shell-edge mesh constraints.
- Double-symmetric quarter-domain O-grid generation mirrors holes, frame constraints, and protected opening edges.
- The framed region can independently remain meshed or be removed through the selected opening group.

## [0.0.47] - 2026-09-25

### Changed

- Selecting regular meshing disables stress refinement, and selecting stress refinement disables regular meshing.

## [0.0.46] - 2026-09-25

### Fixed

- Persisted the mandatory combined-axis selection whenever two principal symmetry axes are available.

## [0.0.45] - 2026-09-25

### Changed

- Enabling symmetry on geometry with two valid principal axes now always enforces the combined double-axis mode.

## [0.0.44] - 2026-09-25

### Fixed

- The options dialog now keeps a dedicated reference to the double-axis selection instead of relying on ComboBox item casting.

## [0.0.43] - 2026-09-25

### Fixed

- Preserved the explicit double-symmetry selection mapping in the compiled plugin source.

## [0.0.42] - 2026-09-25

### Fixed

- The selected double-symmetry UI entry now always serializes both principal axes to the mesher input.

## [0.0.41] - 2026-09-25

### Fixed

- Double-axis symmetry with stress refinement for the `TEST10` framed opening.
- Exact-symmetry requests no longer fall back silently to a non-symmetric mesh.

## [0.0.40] - 2026-09-25

### Added

- Exact symmetry for geometries with symmetric frame constraints.
- Deterministic regular rectangular meshes invariant between single-area and 2x2 source subdivisions.
- Double symmetry about both principal axes when both axes are detected.

### Changed

- Regular-mesh preference and local refinement are mutually exclusive.

## [0.0.39] - 2026-09-24

### Added

- Exact-symmetric circular O-grids for holes centered on the reflection axis.
- Automated SAP2000 coverage for `TEST06`, including constrained-edge preservation and circular-boundary checks.

### Fixed

- Full-quad generation for small axis-centered holes using the default `0.05` diameter.

## [0.0.38] - 2026-09-24

### Added

- Many-to-many conforming constraints for complete and partial shell edges crossing one or more selected areas.
- Graded local refinement around automatic shell-edge constraints using Gmsh distance and threshold fields.
- Hole generation for closed regions bounded by selected frames, incident shell edges or both.
- Automated SAP2000 coverage for the multi-area `TEST02` and `TEST03` models.

### Changed

- Constraint curves are clipped in each host plane, split at crossings and propagated back to every source edge.
- FAST uses short alphanumeric temporary labels, scale-aware point reuse and targeted object rollback.
- Known SAP2000 continuation-row diagnostics for polygonal areas are validated without hiding unrelated import errors.
- Test automation always closes SAP2000 after success, failure or timeout.

## [0.0.37] - 2026-09-23

### Added

- Maximum-size label using only the SAP2000 length unit active when the plugin opens.
- Final area-element count in the main plugin window.

### Changed

- Entire plugin UI, progress text, quality report and error messages translated to English.
- Undo restores the original object selection and returns the dialog to a reusable ready state.
- Geometry contexts are rebuilt for every retry so changed options are applied from a clean state.

## [0.0.36] - 2026-09-23

### Added

- Runtime autonomo Python 3.12 e Gmsh 4.15.2 prodotto con PyInstaller.
- Installer e disinstaller COM per-utente senza privilegi amministrativi.
- Smoke test automatici dei tre backend durante il packaging.
- Licenze Python/Gmsh e sorgente Gmsh pubblicati con la release.

### Changed

- Il plugin usa esclusivamente il backend incluso e non dipende piu dal `PATH`.
- `AssemblyVersion` COM stabilizzata a `1.0.0.0` per evitare registrazioni storiche concorrenti.

### Repository

- Documentazione dello stato tecnico, dello sviluppo e del processo di rilascio.
- Configurazione portabile del percorso dell'API SAP2000.
- Dichiarazione riproducibile della dipendenza Python/Gmsh.
- Regole Git LFS per le fixture SAP2000.
- Script iniziale per creare pacchetti di release controllati.
- Licenza open source MIT.

## [0.0.35] - 2026-09-23

### Added

- Mesh quad-dominant generale per poligoni piani.
- Transizioni rettangolari automatiche e simmetriche.
- Vincoli per point object e frame interni, inclusa generazione di aperture.
- Elaborazione multi-area con congruenza di bordi e intersezioni.
- Inserimento standard COM e FAST tramite tabelle SAP2000.
- Anteprima e rollback transazionale.
- Trasferimento delle principali proprieta e dei carichi area.
- Report interattivo della qualita geometrica.
