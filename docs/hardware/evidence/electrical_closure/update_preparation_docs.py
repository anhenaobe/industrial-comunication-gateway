"""Refresh the current decision front matter; preserve historical baseline copies."""
from pathlib import Path
DOC=Path('docs/hardware')
header='''# Passive and auxiliary component selection - capture revision

Date: November 7, 2026. **CONDITIONAL GO for independent schematic sheets.**
The authoritative current decisions and limits are in
[schematic_readiness_gate.md](schematic_readiness_gate.md). This selection is not
a purchase or manufacturing release. Rev. A is unchanged.

The selected architecture is STM32H723VET6 / DP83826I / HX1188FNL /
SS-7188S-A-NF, one THVD1420, one ATA6561, one ISO1212 for two Type3 inputs,
two BSP75N, one logic-translator candidate and two LMR36015FBRNXR converters,
with one18-30V input. Two independent25MHz active oscillators are selected for
capture; crystal-load networks are DNP. UART default115200baud and CAN nominal1M /
data2M are engineering capture defaults, subject to field-system confirmation.

All111 original requirement IDs remain. Three new rows cover oscillator bypasses
and the conventional CAN end-termination option. [passive_bom.csv](passive_bom.csv)
contains114 passive/auxiliary requirement rows. [final_bom.csv](final_bom.csv)
adds eight active specifications with actual quantities. CAD active-specification
rows retain blank quantities to avoid counting them as passive placements.

Clocks, magnetics and connectors are accounted separately from ordinary passive
placements. The regenerated [counts](evidence/passive_selection_counts.json)
give78 known mandatory passive placements, three unresolved quantity groups
(both buck CIN banks and input bulk),24 distinct mandatory passive specifications,
and8 conditional passive placements. The previous26-specification denominator
included unresolved clock/magnetics requirements and remains historical evidence;
it is not silently treated as today's ordinary-passive count. No final purchasing
total is claimed while those quantity groups and conditional/DNP options remain.

The BOM explicitly changes the MPN/quantity/assembly fields supported by this
closure: confirmed magnetics/jack; complete EVM Ethernet termination variant;
MM2041k threshold resistors; Yageo10k replacing the unqualified FOJAN identity;
two oscillator bypasses; and unselected crystal/filter/split-termination networks
marked DNP. Every accepted change is in
[bom_decisions.json](evidence/electrical_closure/bom_decisions.json). Regeneration
consumes that overlay and the saved CAD additions, so it cannot restore old
unselected magnetics, crystal loads or FOJAN identities. Original files are
preserved in `evidence/electrical_closure/baseline/`.

Library resources now have46 symbols and23 footprints, with a regenerated
Altium IntLib. Six actual compiler warnings remain for missing component models.
CAD_CANDIDATE is independent of ELECTRICAL_VERIFIED; no mask/stencil, surge,
thermal or stability approval follows from a saved symbol or compilation.
The BSP75N numbered map remains blocked. New9 symbols/8 footprints and compiled
source readback are documented in the readiness gate.

Availability: no unobserved part is labelled JLC Basic/Preferred. C233005/MM204
has public Extended classification and incomplete out-of-stock evidence; exact
assembly quantity is unknown. Other stock is unknown. Confirmed RJ45 selection
is retained independently from sourcing risk. No P0 design was changed to save
a small passive cost.

## Source identifiers used in the CSV

| ID | Manufacturer source and decisive locator |
|---|---|
| S1 | ST DS13313 Rev5, existing `DS_stm32h723zg.pdf`: LQFP100 fig5/table7; VCAP table14; HSE table31; IO table51; current table20 |
| S2 | [ST AN5419 Rev3](https://www.st.com/resource/en/application_note/an5419-getting-started-with-stm32h723733-stm32h725735-and-stm32h730-mcu-hardware-development-stmicroelectronics.pdf): table2, figures3/15/19, sections3/6 |
| S3 | TI SNLS647I `dp83826i.pdf`: pin table5-1, section7.6 clocks/reset, section8.3.10, straps tables8-6..8-10, section9 |
| S4 | Existing DP83826EVM SNLU262A: fig6-2/native sheet3, table7-1. Current CEXT requirement overrides its older C57 value |
| S5 | TI SNVSB49D `lmr36015.pdf`: exact FB variant; section10.1, table10-1 explicitly RATED COUT columns; equations3-11; sections11-12 |
| S6 | TI SLLSF78B `thvd1400.pdf`: shared1400/1420 bus ratings, figure8-5/table8-1, section9/10.1. Example uses1400/5V and two10ohm resistors |
| S7 | Existing Microchip ATA656x EVKit DS50002649A: sections3.3-3.8, appendixA/tableB-2 |
| S8 | Microchip DS20005991B `20005991B.pdf`: ATA6561 pin table, modes, figure1-6 and table2.0 |
| S9 | TI SCES516N `sn74lvc2t45.pdf`: table5.5 loaded VOH, supply sequencing and DIR; no OE |
| S10 | Diodes DS33016 Rev7-2 `BSP75N.pdf`: Source-tab note, VIN>=4.5V protection, input current, thermal/current tables and single-pulse conditions |
| S11 | TI SLLSEY7G `iso1212.pdf`: table4-2 SUB ownership, DC table5.9, equations1-4, figure8-2/table8-1, section8.4 |
| FCLK | Local Kyocera TNY1T-H1-DEX01-11: pp3-4,6 pinout, standby, CMOS limits, load,10nF bypass and lands |
| FETH | Local Pulse HX1188FNL revB sheets2-3; Cinch CT710001 B0 component-side numbered/hole drawing |
| FESD / FSM | Local TI SLVSBO7O table4-2 and DQA0010A; Bourns CDSOT23-SM712 pp1-3 |
| FDI | Manufacturer-authored Firstohm MM Rev08-March-2023 pp75-78, acquired from Alfatec; MM204 normal curve and reflow lands, not MM204P |
| FL | Local Coilcraft document806 Rev02/25/26 pp1,4 exact XAL4030/XAL4040 data/lands |
| FIN | TDK-Lambda external DC-DC components figure5; Vishay88987; Littelfuse SMBJ electrical table. Prototype front-end remains unqualified |
| P1-P5/P10 | Existing exact KEMET/Yageo nominal-value sheets in `hardware/academic_rev1/libraries/sources/passives/` and DI source PDFs |
| P6-P9 | Coilcraft/TDK/Samsung exact-part data from earlier work; TDK DC-bias/ESR qualification remains open, not filled with nominal capacitance |

Supporting calculations, manufacturer acquisition URLs/hashes, compiler messages,
native-file preservation checks and change records are under
`evidence/electrical_closure/`. The generated tables below are the current CSV
view, including explicit unresolved and DNP requirements.

'''
p=DOC/'passive_component_selection.md'
marker='<!-- GENERATED_BOM_TABLES -->'
tail=p.read_text(encoding='utf-8').split(marker,1)[1]
p.write_text(header+marker+tail,encoding='utf-8')

p=DOC/'altium_library_preparation_report.md'
text=p.read_text(encoding='utf-8')
banner='''> **Current update, 2026-11-07:** electrical closure added9 symbols/8 footprints;
> source libraries and generated IntLib now contain46 symbols/23 footprints.
> Native compilation completed with6 `Missing Component Models` warnings and
> no errors returned. BSP numbered mapping remains blocked. Current electrical,
> BOM and CAD limits are in [schematic_readiness_gate.md](schematic_readiness_gate.md).
> The report below preserves the original November6 preparation result.

'''
if not text.startswith('> **Current update, 2026-11-07:**'):
    p.write_text(banner+text,encoding='utf-8')
print('Updated current selection front matter and historical library-report pointer')
