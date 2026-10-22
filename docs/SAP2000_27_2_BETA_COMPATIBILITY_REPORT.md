# SAP2000 27.2.0 Beta Compatibility Report

## Scope

This report records observed API differences between SAP2000 27.1.0 and SAP2000 27.2.0 build 3919 beta. The tested compatibility changes were first validated in local candidate 2.0.19 and are included in release 2.0.21. This remains a compatibility report, not a certification of SAP2000 27.2.0.

The verified 27.1.0 baseline remains the complete 36-model matrix in `GMSH_V2_TRANSFER_MATRIX_2_0_18.md`. The 27.2.0 results below cover the open `Circular_Floor.sdb` model and focused atomic transfer fixtures.

## Executive Summary

SAP2000 27.2.0 changes several editable-table schemas and some import semantics. The meshing algorithm and Gmsh backend were not the cause of the initial failures. The failures occurred in SAP2000 snapshot, import, and restoration paths before or after Gmsh execution.

After the compatibility changes described below:

- Standard object insertion generates and undoes the selected eight-area `Circular_Floor` mesh successfully.
- FAST table insertion generates and undoes the same `Circular_Floor` selection successfully.
- Parent-to-child property transfer passes in both FAST and Standard focused fixtures.
- FAST full-quad Apply-to-Undo passes with tabular restoration.
- Standard mixed quad/triangle Apply-to-Undo passes with object restoration.
- FAST mixed quad/triangle insertion is not yet certified on 27.2.0.

## Observed Changes From 27.1.0

### Blank editable-array field keys

`GetTableForEditingArray` returns valid row values but blank field-key arrays for at least:

- `Joint Coordinates`
- `Connectivity - Area`
- `Area Section Assignments`

The 27.2 compatibility path reconstructs field keys from `GetTableForEditingCSVString`, validates them against `GetAllFieldsInTable`, and compares every CSV value with the editing-array value before accepting the recovered schema. Hard-coded column positions are not used.

### Metadata and editable-schema width differences

The following global or definition tables expose metadata/CSV shapes that differ from their editable-array shapes:

- `Database Format Types`
- `Program Control`
- `Frame Section Properties 01 - General` and the `Frame Section Properties*` family

These tables are not modified by shell meshing. They are omitted from the mesh rollback snapshot on 27.2. Geometry, shell sections, loads, springs, groups, and object-bound assignments remain mandatory.

### Area design procedure schema

`Area Design Procedures` no longer exposes the expected `Area` field through the tested editable-array path. The plugin records this as an unpreserved design assignment and continues with the existing manual-review warning. It does not claim that a non-default procedure was transferred.

### Material-temperature import units

Replaying `Area Material Temperatures` through the 27.2 editable-table importer changed `26.5` to `-3.0555555555555554`, which is the Fahrenheit-to-Celsius interpretation of 26.5. The compatibility candidate therefore restores this assignment with `AreaObj.SetMatTemp` in current model units instead of replaying that table. Focused Standard and FAST Apply-to-Undo tests pass after this change.

### FAST triangle connectivity

The 27.1 FAST path represented a generated triangle by repeating `Joint3` in `Joint4`, avoiding the blank-trailing-joint diagnostic produced by 27.1. SAP2000 27.2 rejects some such rows and can consequently reject dependent section rows. A candidate using blank `Joint4` and explicit post-import connectivity verification was prepared, but the mixed FAST regression did not complete within the test timeout. FAST mixed quad/triangle import remains open and must not be reported as verified.

## Compatibility Changes

The local candidate contains these narrowly scoped changes:

1. Recover blank editable-table field keys from validated CSV headers and metadata.
2. Omit only proven global/definition tables that shell meshing does not modify.
3. Treat unreadable `Area Design Procedures` as an explicit preservation warning.
4. Delay the `insertionStarted` flag until FAST snapshot capture succeeds, preventing unnecessary rollback after a read-only preflight failure.
5. Restore area material temperature through the object API to preserve current-unit semantics.
6. Keep full inventory, connectivity, GUID, property, and assignment verification after Undo.

## Test Results

| Test | Mode | SAP2000 27.2.0 result | Evidence |
| --- | --- | --- | --- |
| `Circular_Floor`, 8 areas + 281 joints + 176 frames | Standard | PASS | Preview generated; Undo completed; 8 areas and 281 joints restored with the original names. |
| `Circular_Floor`, same selection | FAST | PASS | Preview generated; Undo completed; 8 areas and 281 joints restored with the original names. |
| `nTEST001`, explicit parent/edge fixture, 50 quads | FAST | PASS | Parent-to-child section, axes, mass, edge constraint, modifiers, material, temperature, group, load, pressure, surface/edge spring verified. |
| `nTEST001`, Apply then Undo | FAST | PASS | `csv-undo-method=tabular verified=true`; original edge fixture restored. |
| `nTEST003`, explicit parent/edge fixture, 49 quads + 12 triangles | Standard | PASS | Parent-to-child fixture verified on all 61 children. |
| `nTEST003`, Apply then Undo | Standard | PASS | `csv-undo-method=legacy-object verified=true`; original edge fixture restored. |
| `nTEST002`, mixed mesh | FAST | OPEN | Original 27.1 triangle padding is rejected by 27.2; the revised trial did not complete within 30 minutes. |
| Non-default area design procedure | FAST and Standard | NOT VERIFIED | 27.2 schema does not expose the expected object identity field. |
| EC2 shell design overwrite | FAST and Standard | NOT VERIFIED | Existing xAPI getter/setter limitation remains. |

## Safety Checks

- The original `Circular_Floor.sdb` SHA-256 remained `CA15037D18AC9351DCCBFF17F9DE507A1A45E1EC80EABCB1F605442AB83FA3BD` after the tests.
- Attached tests used Generate followed by Undo and did not save the open model.
- Property fixtures ran in separate SAP2000 processes on disposable atomic model copies.
- Failed isolated trials were closed without saving.
- The open model inventory remained 8 areas, 281 joints, and 176 frames after the attached tests.

## Current Support Statement

The local candidate demonstrates useful 27.2.0 beta compatibility, but it is not a complete certification. Standard transfer is the safer general path. FAST is verified for the tested `Circular_Floor` selection and a full-quad property fixture, but FAST mixed quad/triangle import and non-default design assignments require further work.

The 27.1.0 release matrix must remain the compatibility baseline until the complete 36-model suite passes on 27.2.0 in both modes.
