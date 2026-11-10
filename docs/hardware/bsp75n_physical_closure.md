# BSP75NTA ? physical CAD closure, 7 November 2026

<!-- AUTONOMOUS_CLOSURE_20261108_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- AUTONOMOUS_CLOSURE_20261108_END -->

The earlier demand for manufacturer **numeric** terminal identifiers was unnecessary. Diodes identifies the physical terminals by function. Its own top-view pinout and suggested land pattern close the physical mapping; no equivalent manufacturer's part is used.

## Manufacturer evidence and saved model

[Local Diodes DS33016 Rev7-2, January 2024](../../hardware/academic_rev1/libraries/sources/bsp75n_closure/BSP75N.pdf): p1 Top View Pin Out and Source-tab note; p8 Suggested Pad Layout; pp3?4 ratings. [Official PDF](https://www.diodes.com/assets/Datasheets/BSP75N.pdf).

Symbol `BSP75NTA` is linked to `GW_BSP75N_SOT223_DN_DIODES`. Altium supports the retained functional pin/pad identifiers; numeric assignments are not invented. Rotate the manufacturer's p1 top view 90 degrees clockwise: tab above, small leads below. Never mirror this view.

| Symbol pin = footprint pad | Physical position | Center x,y (mm) | Copper width ? height (mm) |
|---|---|---|---|
| IN | Lower left | ?2.30,?3.20 | 1.20 ? 1.60 |
| D | Lower center | 0,?3.20 | 1.20 ? 1.60 |
| S | Lower right | +2.30,?3.20 | 1.20 ? 1.60 |
| S_TAB | Upper large tab, Source | 0,+3.20 | 3.30 ? 1.60 |

These reproduce p8 C=2.30, C1=6.40, X=1.20, X1=3.30, Y=1.60, Y1=1.60, Y2=8.00 mm. Manual mask expansion +0.05 mm and 1:1 paste are explicit prototype process choices, not dimensions claimed from Diodes. Nominal body outline 6.50 ? 3.50 mm is on Mechanical1. No 3D/courtyard or assembly-process approval is claimed. Drain copper and Source tab must remain isolated; the p1 thermal recommendation calls for significant **drain copper**, not a presumed drain-connected tab.

## Manual capture

The complete component list, translator pins, eight BSP terminal connections, return paths and acceptance procedure are in [construction guide ?10](schematic_construction_guide.md#10-sn74lvc2t45-and-two-bsp75n-digital-outputs).

- First BSP IN ? translator pin7/B1; second IN ? pin6/B2. Each has its existing 10 k? pull-down to Source/common return.
- Each D ? its own load negative (`DO1_DRAIN` or `DO2_DRAIN`). Each external load positive ? external `DO_EXT+`.
- Each S **and** S_TAB ? `DO_EXT_RETURN`, referenced to logic GND_PWR for the established nonisolated drive. Do not join isolated FIELD_COM, chassis or EF_RTN.
- Retain DIR=3V3, MCU PE2/PE3, two A-side 10 k? pull-downs and two local 100 nF translator supply bypasses. External DO load current bypasses the electronics eFuse.

## Separate electrical status

**CAD_VERIFIED; physical wiring ready. Drive electrical approval remains pending.** Diodes p4 VPROT=4.5 V minimum concerns overtemperature protection, not ordinary turn-on. Its maximum 1.2 mA input current is specified at VIN=5 V. Including the 10 k? pull-down gives approximately 1.723 mA screening load; this is not an all-voltage worst-case bound.

TI SN74LVC2T45 SCES516N Table5.5 does not explicitly guarantee ?4.5 V at the selected asymmetric 3.3/5 V rails and this load. The 3.8 V guaranteed row at 4.5 V supplies/?32 mA and the near-rail row at ?100 ?A cannot establish that guarantee. See [calculations and limitations](evidence/bsp75n_closure/calculations.json).

Recommended academic resolution: retain the candidate for capture, then verify loaded IN-to-local-S ?4.5 V including ripple at the actual low 5 V rail, with both channels HIGH and real inputs/pull-downs fitted. Verify reset/HiZ/partial-rail default-OFF before energizing external loads. A pass approves only recorded prototype conditions. Failure requires a separate drive revision; a guaranteed alternative must explicitly cover ?4.5 V at ?1.8 mA over the rail range and safe startup. No alternate component or automatic electrical approval is introduced.

## Verification performed

- Timestamped backups: `hardware/academic_rev1/libraries/backups/bsp75n_20261107T231133Z/`; [hash manifest](evidence/bsp75n_closure/backup.json).
- Saved symbol and footprint read back through the Electronics AI file-library backend. Original four complete pin records, electrical types and connection coordinates preserved. Footprint association and status/provenance metadata updated; symbol graphics unchanged.
- Library diff: BSP symbol only modified, other65 symbols unchanged; one new footprint, all37 existing footprints unchanged.
- Structural validation:66 symbols /38 footprints, zero errors and zero warnings. [SchLib result](evidence/bsp75n_closure/validate_sch.json), [PcbLib result](evidence/bsp75n_closure/validate_pcb.json), [symbol diff](evidence/bsp75n_closure/diff_0.json), [footprint diff](evidence/bsp75n_closure/diff_1.json).
- Native compilation, ERC, placement and electrical testing **not performed**. Existing IntLib is not refreshed by this task. Use saved source libraries; structural success does not establish drive or thermal performance.

Remaining practical dependencies: loaded-drive/reset-OFF acceptance; exact external connector numbering; intended load thermal/inductive envelope. No missing numbered drawing or missing BSP footprint remains a blocker.

Hash comparison found `Ethernet.SchDoc` changed concurrently; no operation in this task wrote it, and it was left untouched. All other original native schematic/PCB/project and professor-library hashes remain unchanged; only the intended academic SchLib/PcbLib were edited by this task. `git diff --check` passed (only existing CRLF conversion notices).
