# SAP2000 API unit-context policy

## Problem

SAP2000 27.2.0 beta can return or consume geometric values according to API context rather than only the unit shown in the user interface. A model may, for example, show `m` while its database geometry is expressed in `mm`. Mixing a mesh size converted to present units with coordinates returned in database units can change the effective size by a factor of 1,000.

## Plugin contract

- SAP2000 versions before 27.2 retain the historical present-unit behavior.
- On SAP2000 27.2.0 and later, the plugin records the original present units before reading geometry.
- If present and database units differ, the plugin sets present units to database units before every mesh-related API operation begins.
- Geometry, user length inputs, Gmsh files, generated coordinates, quality metrics, FAST tables and object-API insertion consequently share one unit system.
- The original present units are restored in a `finally` block after success, cancellation or failure.
- Explicit input suffixes (`m`, `cm`, `mm`, `ft`, `in`) remain supported. Bare values use the effective unit displayed by the plugin while its deterministic scope is active.

The SAP version string is compared structurally (`27.2.0`, `27.10.0`, `28.0.0`) rather than as a decimal number. The numeric API version is used only as a fallback when the string cannot be parsed.

## Verification

`tools/TestSapUnitContext.ps1` checks the version policy without opening a model. The MODO integration case exercises a model whose original present units are `kip_in_F` and database units are `kN_mm_C`: `40mm` mesh size and `30mm` BOLT holes are serialized as `40` and `30`, then the original units are restored. An intentional invalid-hole run verifies the same restoration path after an exception.
