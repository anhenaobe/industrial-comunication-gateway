# Gateway Academic symbol and TPS26620 library verification

<!-- AUTONOMOUS_CLOSURE_20261108_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- AUTONOMOUS_CLOSURE_20261108_END -->

> Historical TPS/symbol-style stage snapshot below. Current source inventory is66symbols/38footprints after the [Ethernet75Ω addition](ethernet_75ohm_library_closure.md) and [1nF capacitor addition](ethernet_1nf_library_closure.md); BSP75NTA metadata/link are subsequently updated as documented in the current closure below.


Updated2026-11-07. **SS3P6L graphics complete; TPS symbol complete; TPS footprint
native custom-pad verification unfinished.** All operations targeted the two
project-local source libraries. No schematic, PCB or placed component was updated.

## Graphical changes

`SS3P6L-M3_86A` now uses a conventional Schottky diode graphic with cathode hooks,
anode side on the left and cathode on the right. Both physical anodes are shown
as separate visible/connectable pins, joined graphically on the internal side.
Pin1=ANODE1, pin2=ANODE2, pinK=CATHODE; all retain passive electrical type.
Exact MPN parameter remains `SS3P6L-M3/86A` and the current model remains
`GW_SS3P6L_VISHAY_88987`. The footprint copper was not changed.
The [Vishay source](../../hardware/academic_rev1/libraries/sources/SS3P6L_88987.pdf)
pp1/4 supports that numbering and the saved land pattern.

| Other existing symbol modified | Graphic |
|---|---|
|RC0603FR-0762KL; RC0603FR-0715KL; RC0603FR-0710KL; MM204F1K00TKRTR3K0|IEC resistor, no IC body|
|C5750X7R2A475K230KA; C0805C224K1RACTU; C0805C225K5RACTU; C0603C680J5GACTU; C3225X7R1C156M250AB|Parallel capacitor plates|
|XAL4030-682MEC; XAL4040-103MEC|Conventional coil winding|
|0451002.MRL|IEC fuse rectangle with through conductor|

Total:13 existing symbols changed graphically including SS3P6L. Four new Yageo
resistor symbols and the new exact KEMET10nF symbol follow the same convention.
Physical pin names/numbers/types, MPN parameters, footprint associations and other
component parameters are preserved for every graphics-only change. Pin placement,
length, reference position and passive label visibility are presentation changes;
the electrical terminals remain present. Existing readable professor-derived
passive glyphs were left unchanged. No plain NMOS/PMOS or BJT block was found in
the academic library requiring conversion.

Intentionally retained as functional blocks: TDS3011P.C and TDS3311P.C
(triggered shunt-FET suppressors, not ordinary avalanche diodes), BSP75NTA
(protected smart switch, not a bare NMOS), CDSOT23-SM712 (asymmetric multi-terminal
protection network), TPD4E05U06DQAR (ESD array), NIS3071MT4TWG and TPS26620DRCR
(eFuses), and the other active ICs/oscillator. HX1188FNL retains its existing
multiwinding magnetics block; it was not reduced to a simple inductor.
These graphical choices do not waive their previously recorded CAD/electrical limitations.

The concise future standard is [SYMBOL_CONVENTIONS.md](../../hardware/academic_rev1/libraries/SYMBOL_CONVENTIONS.md).
Both new authoring inputs and the earlier freeze authoring helper use
[symbol_style.py](evidence/symbol_style.py), so regeneration does not restore block
graphics for the affected new passives. The [offline preview](evidence/tps26620/symbol_preview.svg)
is drawn from saved file readback; it is not a native Altium screenshot.

## TPS26620 resource and limitation

Saved symbol `TPS26620DRCR`; associated candidate `GW_DRC0010J_TI_TPS2662`.
Pin1IN,2UVLO,3OVP,4SHDN_N,5RTN,6GND,7ILIM,8dVdT,9FLT_N,10OUT,11RTN_EP.
The exposed pad is **RTN, not system GND**. TI's pin table and DRC0010J package
examples are saved [locally](../../hardware/academic_rev1/libraries/sources/tps26620/tps2662.pdf).
Package/pad positions and numbering were read back and checked numerically.
Current/UV/OV/startup calculations and the manual pin checklist are in
[input_protection_reference.md section10](input_protection_reference.md).

The file backend rejected four repeated-designator11 pads used to form the thermal
copper tongues; the failed attempt left PcbLib hash unchanged. A single pad11 plus
four source-dimensioned copper regions was saved as a **candidate**, with explicit
mask and windowed paste. Native conversion to a true custom pad11 or verified
net assignment/inheritance, and final0.05mm region/stencil corner review, remain
required before PCB use. A structurally valid file does not prove those regions
inherit EF_RTN. No made-up electrical terminals or generic default land pattern
were substituted. Optional thermal vias and3D/courtyard qualification are not claimed.

NIS3071 was retained with `SUPERSEDED_BY_TPS26620DRCR` metadata, unchanged pins
and footprint links. Its BOM quantity is0/DNP, with stable historical specification
ID. TPS approved-component status is separate from CAD_CANDIDATE and proposed
application values; it is not described as electrically tested.

## Saved-state checks

Before editing, backed up SchLib/PcbLib/LibPkg to
`hardware/academic_rev1/libraries/backups/tps26620_20261107T172600Z/` and recorded
SHA256 in [backup.json](evidence/tps26620/backup.json). The preceding freeze stage
has its own timestamped backup and evidence. Professor source libraries remain unchanged.

| Check | Result |
|---|---|
|Fresh backend SchLib read|64 symbols; six new,14 modified including NIS status,44 unchanged|
|Fresh backend PcbLib comparison|35 footprints; one new candidate,34 unchanged,none removed|
|All58 pre-existing symbol pin identities/types/hidden state and footprint links|Preserved|
|Graphics-only symbol MPNs and parameter values|Preserved|
|SS3P6L1/2/K and visible independent anodes|Verified in saved readback|
|Structural validation|SchLib and PcbLib:0errors,0warnings|
|Original professor/library/project/schematic/PCB source hashes|Preserved; only intended Gateway SchLib/PcbLib hashes changed in this stage|
|BOM preservation|Every original requirement ID retained; only intended ILIM/dVdT/FLT quantities or MPN bindings changed; three UV/OV rows added|
|Local reference links|Existence checked; no invented missing Semtech local path|
|LibPkg and existing IntLib|Unchanged; IntLib stale and must not be used as current inventory|
|Native compile/reopen/isolated placement/ERC|**NOT RUN**; no new Altium automation session launched under the existing constraint|
|TPS custom-pad/net inheritance and final assembly outputs|**UNVERIFIED**, candidate not PCB-release ready|

Machine evidence: [verification.json](evidence/tps26620/verification.json),
[symbol readback](evidence/tps26620/symbols_after.json),
[footprint readback](evidence/tps26620/footprint_after.json),
[symbol diff](evidence/tps26620/diff_0.json), [footprint diff](evidence/tps26620/diff_1.json),
[SchLib validation](evidence/tps26620/validate_schlib.json),
[PcbLib validation](evidence/tps26620/validate_pcblib.json).
File checks and drafting preview do not claim native compiler or electrical test results.

Next native task: finish only the TPS thermal custom pad, verify that it inherits
EF_RTN on isolated placement, inspect the updated discrete graphics in Altium and
compile Gateway_Academic.LibPkg. Do not automatically update placed gateway objects.


## BSP75NTA correction ? current physical closure (7 November 2026)

The earlier request for a manufacturer-numbered Type DN drawing is withdrawn. Diodes DS33016 pp1,8 identify physical functions and lands sufficiently. `BSP75NTA` now links to verified `GW_BSP75N_SOT223_DN_DIODES`: tab-up top view, lower IN/D/S, upper S_TAB=Source. Functional Altium pin/pad IDs are intentional; no generic numeric mapping is substituted. Physical CAD is **CAD_VERIFIED**; drive electrical approval remains pending separately. Current source libraries:66 symbols/38 footprints; structural validation0 errors/0 warnings,65 unrelated symbols and37 old footprints unchanged. Native compilation/ERC not run.

Use the [current physical closure and evidence](bsp75n_physical_closure.md) and [construction guide ?10](schematic_construction_guide.md#10-sn74lvc2t45-and-two-bsp75n-digital-outputs). Earlier blocked-numbering statements below/above are historical, superseded by this correction. Retain BSP as a functional smart-switch block, not a bare MOSFET.
