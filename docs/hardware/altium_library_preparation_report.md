> **Current update, 2026-11-07:** electrical closure added9 symbols/8 footprints;

<!-- AUTONOMOUS_CLOSURE_20261108_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- AUTONOMOUS_CLOSURE_20261108_END -->

> source libraries and generated IntLib now contain46 symbols/23 footprints.
> Native compilation completed with6 `Missing Component Models` warnings and
> no errors returned. BSP numbered mapping remains blocked. Current electrical,
> BOM and CAD limits are in [schematic_readiness_gate.md](schematic_readiness_gate.md).
> The report below preserves the original November6 preparation result.

# Gateway Academic - native library preparation

Date: 2026-11-06. **Final schematic readiness: Conditional.**

Editable, nonempty libraries are saved and independently readable. Electrical
selections remain provisional. Full CAD qualification is unfinished: native
reopen/placement and IntLib compilation remain pending. The user asked to leave
problem components unfinished and then requested the computer back for studying;
no further desktop control or Altium operations were performed after that request.

## Delivered files

| File | Saved content |
|---|---|
| `hardware/academic_rev1/libraries/Gateway_Academic.SchLib` | 37 symbols: 8 active specifications, 22 passive specification variants, 7 auxiliary variants |
| `hardware/academic_rev1/libraries/Gateway_Academic.PcbLib` | 15 footprints: 7 authored package variants and 8 relevant professor candidates; required embedded models retained |
| `hardware/academic_rev1/libraries/Gateway_Academic.LibPkg` | Two relative members: `Gateway_Academic.SchLib`, `Gateway_Academic.PcbLib` |
| `hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb` | Created natively; relative references to the two academic libraries, no circuit sheets or PCB geometry |
| `docs/hardware/passive_bom.csv` | All 111 original rows, IDs, quantities, MPNs and electrical selections preserved; independent readiness fields added/normalized |
| `docs/hardware/cad_library_mapping.csv` | 111 original mappings plus 8 stable `ACTIVE_<MPN>` specification IDs; active quantities are blank |

`Gateway_Academic.IntLib` **was not generated**. No compilation success is claimed.
All dependencies are project-local. No global library registration, download,
installation, security/configuration change, commit or push was performed.

## Protection and provenance

The original professor IntLib and all six existing editable source libraries were
hashed before work. All seven hashes match after work. The original IntLib remains
`91594ede8aadf6449fff5b44b7443deafeb73cfaf0bc1eb1ff434d8ac1fb6159`.
The original source manifest is unchanged. Requirements also retain their recorded
hash. Rev. A and firmware were not edited by this work.

- Initial destination backup: `hardware/academic_rev1/libraries/backups/20261106T121033/`.
  These are the newly created blank destinations before population, including the
  LibPkg. No previous Gateway_Academic destination existed at initial inspection.
- Every subsequent library mutation also retained the backend's timestamped
  `Gateway_Academic.*.YYYYMMDD_HHMMSS_*.bak` beside the destination. Exact backup
  paths appear in the operation-result JSON files. They remain available.
- Initial Git state and source hashes: `evidence/library_preparation/git_status_before.txt`
  and `source_hashes_before.json`.
- Original BOM/mapping snapshots: `passive_bom_before.csv`, `cad_mapping_before.csv`
  in the same evidence directory.
- Manufacturer inputs were existing files in
  `C:/dev/7mo/design/Datasheets_industrial_gateway/` and the academic library
  `sources/` directory. No source was fetched from the network.
- Professor glyphs and geometry were inspected using the official file-library
  reader, retained in `source_models_readback.json`. Only relevant assets were used.

## Coverage and counting

These counts distinguish readable candidate resources from fully qualified models.
**CAD_VERIFIED assets: 0. ELECTRICAL_VERIFIED selections: 0.** Source/disk comparisons
passed, but native placement and remaining manufacturer/assembly checks have not
closed. Compilation alone would not close those checks either.

| Scope | Coverage |
|---|---|
| Active specifications | **7/8 candidate symbol/footprint pairs**; BSP75NTA has an unfinished role-labelled symbol and no footprint |
| Existing 26 mandatory specifications | **19/26 symbol candidates**, **15/26 candidate symbol/footprint pairs**; 11 specifications still lack footprints |
| Defined deduplicated package requirements, mandatory plus active | **9/14 have candidate footprints**, **0/14 fully verified** |
| Unresolved mandatory package/selection groups | **7**, counted separately from the 14 defined package requirements |
| Conditional passive specifications | **11**, separately retained; 2 have candidate pairs (20 pF CFF and pulse resistor) |
| DNP ferrite | One separate candidate asset; no placement quantity added |
| Auxiliary BOM rows | 16 original rows; 7 distinct symbol variants prepared, including an unfinished reset switch |

The 14 defined package requirements are LQFP100, RHB32, RNX12, shared SOIC8,
DBQ16, DCT8, BSP75N Type DN, capacitor 0603, resistor 0603, capacitor 0805,
XAL4030, XAL4040, capacitor 2220 and capacitor 1210. SOIC8 is shared only because
the TI and Microchip cited land examples agree in pitch, span and pad dimensions.
RNX revisions A/B are two saved variants of one package requirement. Candidate
0603 reuse does not establish manufacturer land-pattern compatibility.

The seven unresolved mandatory groups are the PHY clock, clock load capacitors,
magnetics, center-tap network, Bob Smith resistors, Bob Smith capacitor and DI MELF
threshold resistor. They are not counted as selected physical packages. The legacy
26-specification denominator includes clock/magnetics requirements; those remain
blocked rather than being filled with generic two-terminal assets.

Known required passive quantity remains **71**, with **4 required rows of unknown
quantity**. Conditional known quantity remains **14**. No active mapping row
contributes a passive placement quantity.

## Active model evidence, in requested priority order

All datasheet page references below refer to the existing local PDFs. Where the
printed page differs from its PDF index, the PDF page is explicitly identified.
`model_inputs.json` records every intended pin and pad. Saved official-reader
snapshots retain the actual destination objects.

| Specification | Source and prepared model | Remaining qualification |
|---|---|---|
| STM32H723VET6 | DS13313 Rev5 fig5/table7, pp57-71; LQFP100 fig65 printed p218 / PDF p219. 100 numbered pins; NRST is bidirectional per table7. `GW_LQFP100_ST_1L`: 0.5mm pitch, 0.3x1.2mm pads, 16.7mm outside span | Explicit +0.05mm mask and 1:1 paste are engineering choices; fabrication/assembly and native placement pending |
| DP83826IRHBR | SNLS647I table5-1 pp5-6, ground/EP requirement p7; RHB0032M 4223725/A PDF pp111-113. 33 pins including GND EP33. `GW_RHB0032M_TI`: 0.5mm pitch, 0.6x0.25mm lands, 2.1mm square EP | Four 0.94mm square paste windows at +/-0.57mm retained; EP full paste suppressed. Thermal vias remain a board decision. Mode/straps/clock unresolved |
| LMR36015FBRNXR candidate | SNVSB49D p4; RNX0012A 4222858/A PDF pp44-46 and RNX0012B 4223969/C pp47-49. 12 numbered pins; pin12=SW, not GND | Confirm delivered RNX revision. Both mask variants retained; A's SMD copper extends 0.05mm beyond dimensioned openings. Two 0.25x0.812mm paste windows on SW12; full-pad paste suppressed. Window corners are rectangular approximations of the rounded stencil example, so stencil qualification remains open |
| THVD1420DR | SLLSF78B table4-1 p3; D0008A 4214825/C PDF pp30-32. Eight numbered pins. Shared `GW_SOIC8_1P27_5P4`, 1.27mm pitch, 1.55x0.6mm lands, 5.4mm row span | Exact circuit protection, native placement and assembly review pending |
| ATA6561-GAQW | DS20005991B pin table p3; SOIC C04-2057-OA RevE p19. Eight numbered pins, including VIO5. Same sourced SOIC8 geometry | No VDFN substitution. Native placement and assembly review pending |
| ISO1212DBQR | SLLSEY7G table4-2 p4; DBQ0016A 4214846/A PDF pp44-46. 16 numbered pins. `GW_DBQ0016A_TI`, 0.635mm pitch, 1.6002x0.4064mm lands | SUB12 and SUB13 stay distinct passive substrate pins, never power/ground aliases. Separate floating 2x2mm copper islands are a board-layout requirement, not fabricated into this footprint. Isolation/layout review pending |
| SN74LVC2T45DCTR candidate | SCES516N table4-1 p2; DCT0008A 4220784/D PDF pp28-30. Eight numbered pins, no OE. `GW_DCT0008A_TI`, 0.65mm pitch, 1.1x0.4mm lands, 3.8mm span | Electrical VOH/load/startup review and native placement pending |
| BSP75NTA | Diodes DS33016 Rev7-2 pp1,8 confirms IN/D/S positions and Source tab | Manufacturer terminal numbers absent. Symbol pins deliberately use `IN`, `D`, `S`, `S_TAB` role identifiers. No numbered pin map or footprint invented. CAD_BLOCKED; unfinished, excluded from placement |

Strap/multiplexed PHY pins use conservative bidirectional ERC types; these do not
approve a mode. MCU GPIOs are bidirectional and VCAP pins remain explicit power
pins with the LDO-output limitation. ISO1212 NC6/7 remain separate passive NC pins.
All active electrical statuses remain PROVISIONAL.

## Passive and auxiliary preparation

The capacitor, resistor, inductor, ferrite, header, connector and switch source
glyphs were inspected once and reused. Every distinct electrical specification
gets its own named symbol, with a stable specification-key hash. New parameters
replace inherited MPN, manufacturer, Value, Comment, tolerance, rating and power;
supplier numbers and old product links were removed. The professor's Walsin Y5V
identity is not used as the identity of any KEMET X7R/C0G candidate.

The three mandatory reusable professor geometries remain CAD_CANDIDATE:
0603 capacitor/resistor lands are 0.9398x1.016mm at +/-0.8001mm; 0805 capacitor
lands are 1.3x1.5mm at +/-1.1mm. Their exact-MPN manufacturer land-pattern,
mask/paste and assembly qualification is open. Body size alone was not treated
as a qualified land pattern. Electrical Ceff, ESR and thermal limits remain open.

XAL4030-682MEC, XAL4040-103MEC, C5750X7R2A475K230KA and C3225X7R1C156M250AB
have independent symbol candidates but no substitute footprints. The already
unselected clocks, RJ45, magnetics and input protection were not completed by
choosing replacements. Existing SS3P6L and CL10B103 sources remain untouched and
were not silently selected into the academic BOM.

The 2-way professor terminal footprint has unequal pad Y coordinates (0.254 and
0.127mm). Its geometry is retained and explicitly unqualified. Headers and
3-way terminals are candidates pending exact drawings. The four-pad reset-switch
source intentionally repeats contact numbers 1/1 and 2/2; the official writer
rejected those duplicates. Its destination symbol therefore has no footprint
link. No terminal renumbering or guessed pairing was introduced.

## Native failure, file validation and compiler result

The existing access-test report was used; its connectivity smoke test was not
repeated. Native project and blank-library creation succeeded. Native symbol
creation succeeded, but `eda__lib_add_pins` stopped in the debugger at
`Component.CurrentPartID`, with **Undeclared identifier: CurrentPartID**. No pins
from that failed batch were assumed saved, and no batch was replayed blindly.
Disk inspection still showed the blank default symbol.

The user dismissed the error. Computer Use then selected the observed Run > Stop
command and closed the incomplete academic SchLib. No plugin script or security
setting was edited. The bridge continued to report **An EDA handler is still
running**, so native authoring was replaced by the official file-library writer.
Final file-based models were written only after the stale academic documents
were closed. No desktop action followed the user's request to resume studying.

Five initially dangling embedded-model references were repaired through official
cross-library copy, which transferred the referenced models. Temporary duplicate
footprints used for that transfer were removed; the 15 intended footprints and
their referenced model payloads remain. A full-source export attempt did not
return and was abandoned; it was not used as proof of model transfer.

| Check | Actual result |
|---|---|
| Official saved SchLib read/validation | 37 components, 0 errors, 0 warnings |
| Official saved PcbLib read/validation | 15 components, 0 errors, 0 warnings |
| Pin names/types/numbers and footprint links versus source-derived inputs | PASS for all saved objects; BSP role-only exception explicitly blocked |
| Pad numbering, coordinates, dimensions, drills, layers, mask/paste and window readback | PASS versus recorded authored/source inputs, within 0.00002mm comparison tolerance; manufacturer qualification limits above remain |
| Missing footprint links / missing embedded models | No dangling links or missing referenced embedded models in final libraries |
| BOM conservation, quantity accounting, active mapping rows | PASS |
| Original sources/requirements hashes | PASS, unchanged |
| Generator regeneration stability | Checked by regeneration and hash comparison; cannot restore obsolete professor bindings/statuses |
| Native close/reopen of final libraries | PENDING |
| Isolated passive/MCU/EP/BSP placement and native readback | NOT RUN; BSP is unavailable, other cases pending |
| LibPkg compilation | **NOT RUN** after the native handler failure and user computer handback |
| Actual Altium compiler messages | **None collected; no compiler invocation completed** |
| Generated IntLib existence/inventory | **Absent; not verified** |
| ERC/DRC, electrical simulation, hardware test | Not performed in this library-preparation task |

Validation scope: escalated artifact/package validation. Commands run from the
repository root with the existing interpreter `C:/dev/tools/python/python.exe`:

```text
docs/hardware/evidence/library_preparation/prepare_models.py
docs/hardware/evidence/library_preparation/build_library_payloads.py
docs/hardware/evidence/build_passive_deliverables.py
docs/hardware/evidence/validate_passive_deliverables.py
docs/hardware/evidence/library_preparation/validate_prepared_libraries.py
git diff --check
git status --short
```

The first two scripts emit API input/evidence JSON; they do not synthesize binary
CAD files. Binary library operations used Electronics AI's official `libraries__`
backend. Detailed validation, final file hashes and package inventory are in
`evidence/library_preparation/validation.json`. `destination_*_final.json` are the
independent saved-file readbacks. All CAD/electrical states remain separate in the
BOM and mapping, and the passive generator reads `cad_assets.json` for bindings.

## Unfinished components and exact remaining inputs

As requested, these components remain unfinished; no further file request needs
to interrupt the user's study time.

| Component/problem | Exact file or decision needed later |
|---|---|
| **BSP75NTA** | Manufacturer-numbered SOT223 **Type DN** pin/pad drawing or exact editable Altium symbol/footprint proving terminal numbers and Source-tab mapping. Local DS33016 pp1,8 supplies roles/dimensions but no terminal numbers |
| **LMR36015FBRNXR** | Delivered RNX0012A/B package confirmation and approved stencil drawing; review rounded paste-window corners and mask details. Both candidates remain available |
| **Reset switch MCU_SRESET** | Exact selected MPN datasheet showing terminal pairs and land pattern, plus native copy/placement check permitting repeated electrical pad numbers |
| **XAL4030-682MEC / XAL4040-103MEC** | Local Coilcraft XAL4030/XAL4040 manufacturer land-pattern drawing with terminal dimensions/orientation; no 5.8mm or 7.2mm professor-inductor substitution |
| **C5750X7R2A475K230KA / C3225X7R1C156M250AB** | Exact TDK recommended land-pattern/termination drawings for 2220 and 1210, plus Ceff/ESR/derating evidence for the existing provisional selections |
| **All reused 0603/0805 KEMET/Samsung/Yageo/FOJAN/Vishay candidates** | Manufacturer recommended mounting-pad and mask/paste drawings, including actual FOJAN FRC0603J103TS and pulse-rated CRCW0603010RJNEAHP documents. Exact-value sheets/body dimensions alone do not qualify the shared lands |
| **JL126-50002G01, MX126-5.0-03P-GN01-Cu-S-A and SWD/BOOT headers** | Exact manufacturer mating/top-view numbered drawings, pitch/drill tolerances and ratings; resolve the 2-way terminal Y offset before approving geometry |
| **PHY/MCU clocks and load networks** | Selected clock/crystal MPN, frequency/topology, CL/ESR/drive/startup evidence, then the exact numbered package/land-pattern drawing |
| **HX1188FNLT and SS-7188S-A-NF** | Selection approval and exact Pulse/magnetics and RJ45 numbered schematics/land-pattern/mating drawings, shield/HPOT information. EVM references remain unselected |
| **DI_RTHR1/2** | Selected 1kOhm, >=0.25W pulse-rated MELF MPN with manufacturer surge data and land-pattern drawing; no generic 0603 replacement |
| **ETH center-tap/Bob Smith/chassis network** | Adopted magnetics topology, PE/isolation policy, exact HV capacitor/resistor MPNs and drawings; 1812GC472KAT1A remains an EVM candidate |
| **TPD4E05U06DQAR / CDSOT23-SM712 and CAN/DO/input protection** | Exact manufacturer pin/land-pattern evidence for proposed protections plus approved clamp/load/transient/EMC requirements. No replacements selected |
| **All final native qualification** | Reopen the saved libraries, perform isolated representative placements/readbacks, and compile the LibPkg in a later Altium session; retain actual compiler messages and verify generated IntLib inventory |

Electrical blockers also remain: buck capacitance/stability/thermal review,
STM32 VCAP/analog/startup details, PHY straps/clock/MDI network, bus termination and
protection, translator VOH and BSP75N startup/load behavior, DI Type 3 adoption and
isolation layout, and the input-front-end specification. None is approved by
having a readable CAD model.

## 2026-11-07 TPS26620 and symbol-convention update

Current saved inventory:64 symbols /35 footprints. TPS26620DRCR plus four exact
Yageo resistors and KEMET10nF added;13 existing discrete symbols redrawn; NIS3071
preserved with superseded metadata. No existing footprint changed in this stage.
Both libraries pass the file backend's structural validation with0errors/0warnings.
Readback and component-level comparisons are saved under `evidence/tps26620/`.

TPS thermal-pad copper geometry is saved as CAD_CANDIDATE, not fully released:
the backend rejected repeated pad11 for the copper tongues. Native custom-pad
conversion/net inheritance and rounded-region corner review remain unfinished.
See [current connection plan](input_protection_reference.md#10-academic-revision--approved-schematic-connection-plan)
and [graphics/pin-map verification](symbol_library_verification.md).

Backup before this stage: `hardware/academic_rev1/libraries/backups/tps26620_20261107T172600Z/`.
The preceding academic-freeze backup is `backups/academic_freeze_20261107T170417Z/`.
Professor libraries, schematic/PCB/project documents and LibPkg remain hash-identical.
Native compile, close/reopen, representative placement and schematic ERC were not run:
no new Altium automation session was opened. Existing IntLib remains stale; use the
project-local source libraries for manual capture and compile later in Altium.

## Ethernet75Ω closure — 2026-11-07

Current inventory65symbols/36footprints. Added only CRCW080575R0FKEA and GW_CRCW0805_VISHAY_20035_REFLOW. All prior64symbols/35footprints unchanged by backend diff. C844859 exact identity verified by public catalog; C1511836 is the distinct C-suffix commodity version and was not substituted. Four ETH_RBOB instances retain their approved topology. File validation0errors/0warnings; native compilation not performed and IntLib stale. See [closure report](ethernet_75ohm_library_closure.md), source links, backup and readback under `evidence/ethernet_75ohm/`. No resistor CAD blocker remains; HV capacitors/chassis and TPS custom-pad issues remain separate.

## Ethernet1nF CAD closure — 2026-11-07

ETH_CBOB quantity2 now has saved C1206C102KGRACAUTO / GW_C1206_KEMET_C1076_DENSITY_B, verified C600002 identity and KEMET densityB reflow geometry. One capacitor per nodeA/B to CHASSIS; no topology change. CAD_VERIFIED is separate from provisional application/safety class. Current66symbols/37footprints validate with0errors/0warnings; prior65/36 objects unchanged. Native compilation not run, IntLib stale. [Details and local datasheet](ethernet_1nf_library_closure.md).


## BSP75NTA correction ? current physical closure (7 November 2026)

The earlier request for a manufacturer-numbered Type DN drawing is withdrawn. Diodes DS33016 pp1,8 identify physical functions and lands sufficiently. `BSP75NTA` now links to verified `GW_BSP75N_SOT223_DN_DIODES`: tab-up top view, lower IN/D/S, upper S_TAB=Source. Functional Altium pin/pad IDs are intentional; no generic numeric mapping is substituted. Physical CAD is **CAD_VERIFIED**; drive electrical approval remains pending separately. Current source libraries:66 symbols/38 footprints; structural validation0 errors/0 warnings,65 unrelated symbols and37 old footprints unchanged. Native compilation/ERC not run.

Use the [current physical closure and evidence](bsp75n_physical_closure.md) and [construction guide ?10](schematic_construction_guide.md#10-sn74lvc2t45-and-two-bsp75n-digital-outputs). Earlier blocked-numbering statements below/above are historical, superseded by this correction. Retain BSP as a functional smart-switch block, not a bare MOSFET.
