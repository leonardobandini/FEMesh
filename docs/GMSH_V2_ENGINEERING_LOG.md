# Gmsh V2 engineering log

This log records runtime problems, root causes, corrections, their intended scope, residual limits and verification.
Corrections must target the SAP2000 assignment model rather than one fixture or one customer model.

## 2026-10-08 - Variable area joint offsets blocked meshing

### Symptom

Meshing the selected eight polygonal areas in `Circular_Floor` stopped after Gmsh completed. The Italian UI only reported that a valid mesh could not be generated.

### Root cause

Area `2` had a nonzero SAP2000 joint-offset assignment. `CaptureAreaLoads` explicitly rejected every nonzero offset type before child elements were created. This was unrelated to mesh geometry or Gmsh.

SAP2000 defines two distinct nonzero modes:

- type `1`: offsets calculated from a joint pattern and scale factor;
- type `2`: explicit offset values at the source area vertices.

### General correction

`AreaValueTransfer` now handles the complete documented SAP2000 offset model:

- type `1` preserves the pattern name and scale factor and relies on the already-generalized joint-pattern transfer to populate generated joints;
- type `2` interpolates source vertex values with the same geometric coordinates used for thickness overrides;
- exact source vertices and source edges remain exact/linear;
- quadrilateral interiors use inverse bilinear natural coordinates;
- polygon interiors use mean-value coordinates;
- triangular child arrays are padded to four entries as required by SAP2000;
- every child assignment is read back through `GetOffsets`; a mismatch aborts and enters the existing rollback path;
- unsupported future offset types fail explicitly instead of being guessed.

The implementation is in the assignment-transfer path shared by Standard and FAST insertion. It is not conditional on area names, the circular-floor geometry, or a fixed source vertex count.

### Verification

- Build: zero warnings, zero errors.
- Four-node source fixture: explicit type `2` offsets, thickness overrides and joint patterns passed.
- Eight-node source fixture: pattern-based type `1` offsets, thickness overrides and joint patterns passed.
- Tests modify fixtures only in memory and close SAP2000 without saving.
- Full `Circular_Floor` Standard-mode application passed: 8 source areas became 1747 child areas while all 176 frames remained.
- Exactly 241 child areas were read back with offset type `1`, pattern `Default` and scale `0.5`.
- Every resulting area retained section property `slab`.
- The live mesh was not saved. The saved eight-area model and numbered backup `0003` had the same SHA-256 hash.

### Residual limits

- The interpolation is the plugin's documented geometric interpolation, not an undocumented SAP2000 internal interpolation.
- A future SAP2000 offset type outside `0..2` is rejected until its semantics are documented and tested.

## 2026-10-08 - Defined joint pattern without explicit point rows

### Symptom

After offset transfer was enabled, area `2` still stopped during capture: `GetPatternValue` returned code `1` for pattern `Default` at joint `4145`.

### Root cause

SAP2000 permits a defined joint pattern to have no explicit assignment row at a point. The effective value is zero, but `GetPatternValue` reports code `1` rather than returning an explicit zero. The previous capture logic treated every nonzero code as an API failure when the pattern was required by an area assignment.

### General correction

For point names read from valid area connectivity and pattern names read from `PatternDef.GetNameList`, return code `1` is represented as the effective value zero. Other nonzero API codes still fail explicitly. This applies to every defined joint pattern, not only the built-in name `Default`, and preserves mixed patterns containing both explicit values and implicit zeros.

### Verification

- The type `1` offset fixture now uses a newly defined pattern with no source point rows.
- The transfer creates zero pattern values on generated joints, preserves pattern name and scale on child areas, and verifies both through SAP2000.
- Existing nonzero pattern interpolation remains covered by both the four-node and eight-node fixtures.

## 2026-10-08 - Recoverable failures lost their technical diagnostic

### Symptom

The Italian dialog instructed the user to consult the log, but `plugin-errors.log` contained no entry for failures handled inside the generate/retry loop.

### Root cause

The outer plugin exception handler logged failures, while the inner recoverable-generation handler rolled back and called `dialog.Fail` without logging the original exception. Italian localization then replaced many English messages with a generic warning.

### General correction

The inner handler now calls `LogPluginException(exception)` before rollback and localization. This covers Gmsh, SAP API, assignment-transfer, verification and rollback-triggering failures handled by the same loop. User-requested `OperationCanceledException` remains a normal control path and is not logged as a fault.

### Verification

- Build: zero warnings, zero errors.
- The correction is at the common recoverable-failure boundary and does not depend on a specific exception text or language.

## 2026-10-08 - Gmsh algorithm choice on constrained circular selection

### Observation

Algorithm `8 - Frontal-Delaunay for quads` did not produce a valid candidate for the current eight-area, 176-frame, 281-joint selection. Algorithm `6 - Frontal-Delaunay` generated all eight backend mesh files successfully with the otherwise equivalent settings.

### Decision

Do not add a silent algorithm fallback. Gmsh V2 intentionally preserves the selected algorithm. Use algorithm `6` for this run and report it explicitly. A future automatic fallback, if introduced, must be opt-in, visible in the result, and regression-tested across all supported algorithms.

## 2026-10-08 - Test DLL staged without its private runtime

### Symptom

An isolated corrected DLL passed assignment tests but failed an end-to-end run because `mesher/SapQuadMesherBackend.exe` was not adjacent to it.

### Root cause

The test staged one assembly rather than the deployable plugin directory. Runtime discovery is intentionally relative to the loaded assembly so the plugin does not depend on a machine-wide Python/Gmsh installation.

### General correction

End-to-end plugin trials now stage a complete private package from a verified installation and replace only the tested DLL. The staging check requires the plugin assembly, meshing script and private backend, then verifies the staged DLL hash.

### Scope

This changes the test/deployment procedure, not runtime discovery. Falling back to an arbitrary machine-wide runtime would make results non-reproducible and was rejected.

## 2026-10-08 - SAP selection changed between UI invocations

### Symptom

After reopening the model and invoking the SAP plugin menu, one of eight areas was no longer selected while all joints and frames remained selected.

### General correction

Automated live-model runs no longer assume that a saved model or a previous UI action preserves selection. Immediately before meshing they rebuild the intended selection and verify object-type counts against the current model inventory. The plugin still captures and restores the exact selection supplied at its own entry point.

### Scope

This is a general precondition check for automation. It does not change interactive user selections or silently add objects in production plugin code.

## 2026-10-08 - Concrete shell design overwrites remain manual

The live model contains records in `Overwrites - Concrete Design - Italian NTC 2008`. SAP2000 does not expose a reliable object-level transfer for this table through the current implementation. Generation therefore completes with a visible warning and a numbered backup, but these design overwrites must be reviewed and replicated manually on child areas. This limitation was not bypassed to make the specific model pass.

## 2026-10-08 - SAP2000 27.2 beta CSV fields containing commas

### Symptom

The full snapshot preflight for `Multiple_Silo_Slab.sdb` stopped on material tables whose material name was `Calcestruzzo, Gettato in opera, Grigio`. The beta CSV export emitted those commas without quoting, so the CSV row appeared two columns wider than the editing array.

### General correction

Snapshot schema recovery now aligns each CSV row uniquely with the authoritative editing-array values, joining adjacent CSV cells with commas where required. Ambiguous, missing or extra alignments still abort capture; no table is skipped.

### Verification

The full Silos snapshot preflight completed with `FULL_SNAPSHOT_PREFLIGHT=PASS MODEL_NOT_SAVED=PASS` while preserving every table.

## 2026-10-08 - Incomplete FAST editing schema in SAP2000 27.2 beta

### Symptom

FAST table insertion failed on mixed triangle/quad meshes and on models with dependent joint and area records. SAP2000 reported blank field keys or accumulated invalid joint references even though the same geometry was valid through the object API.

### General correction

FAST now checks the `Joint Coordinates` field keys before insertion. An incomplete schema, or any generated triangle, selects the existing object-API insertion path before model mutation. Assignment transfer, snapshot capture, rollback and verified Undo remain mandatory; the recorded Undo method reflects the path actually used.

## 2026-10-08 - Area design procedure lost after object reconstruction

### Symptom

Undo recreated the geometry of `nTEST025`, but area `2` changed from `Concrete Shell Design` to `No Design`. SAP2000 27.2 reported a successful later import of `Area Design Procedures` while silently retaining `No Design` on an area created by `AreaObj.AddByPoint`.

### General correction

Object-path Undo now stages joint coordinates, area connectivity, area sections and area design procedures in one SAP editing transaction. This lets SAP create each area with its design procedure rather than trying to alter it afterward. Original nonempty GUIDs remain exact; a generated GUID is accepted only where the source table explicitly left the GUID blank.

### Verification

- FAST Apply-to-Undo: 36 of 36 cases passed.
- Standard Apply-to-Undo: 36 of 36 cases passed.
- `nTEST002`, `nTEST015`, `nTEST025` and `nTEST029` passed their isolated reproducers.
- Four-node and eight-node pattern, thickness and joint-offset fixtures passed without saving their models.

## Generalization checklist

Every future correction must answer and record:

1. Is the cause in geometry, SAP API semantics, assignment transfer, UI state, persistence, or packaging?
2. Does the correction cover every documented SAP mode for the affected property?
3. Is the correction shared by Standard and FAST paths where applicable?
4. Does it support triangles, quadrilaterals and general polygons where applicable?
5. Is the result read back or otherwise verified before commit?
6. Does failure preserve rollback and the original model?
7. Are both the original reproducer and a structurally different fixture tested?
8. Are unsupported cases explicit rather than silently approximated?
9. Is the user-visible diagnostic actionable and retained in the log?
10. Are remaining limitations documented in the help and release notes before publication?
