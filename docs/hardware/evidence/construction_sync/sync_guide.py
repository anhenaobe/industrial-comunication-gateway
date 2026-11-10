"""Documentation-only synchronization; native CAD/BOM inputs are read-only.
Retain original pin tables and sources; refresh construction choices from current CSVs.
"""
import csv,json,re
from pathlib import Path
O=Path(__file__).parent;D=O.parent.parent
old=(O/'before_schematic_construction_guide.md').read_text(encoding='utf-8')
bom={r['component_id']:r for r in csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig'))}
mapping={r['component_id']:r for r in csv.DictReader((D/'cad_library_mapping.csv').open(encoding='utf-8-sig'))}
intro='''# Academic Gateway Rev. 1 — manual schematic construction guide

Current baseline: **2026-11-07**. This is the primary construction reference for
manual drawing in Altium. Use the exact connections below and current
[BOM](final_bom.csv), [passive BOM](passive_bom.csv) and [CAD mapping](cad_library_mapping.csv).
Earlier recovery/qualification analysis is retained in [input_protection_reference.md](input_protection_reference.md)
sections1–9 and [the earlier readiness gate](schematic_readiness_gate.md); it does not
restore superseded selections. Source decisions and calculations are in input-reference
section10, [TPS verification](evidence/tps26620/calculations.json) and
[academic freeze decisions](evidence/input_protection_freeze/bom_decisions.json).

Scope: supervised academic prototype; regulated, current-limited laboratory supply,
nominal24V,18–30V operating objective. No industrial certification gate is imposed.
Datasheet ratings, complete power connections and correct physical mapping still apply.
The user draws, places and routes; this document update changes no native CAD.

**Design selected** means a chosen architecture/MPN. **Schematic ready** means the
connections/passives are established (proposed TPS settings are identified explicitly).
**PCB ready** additionally requires verified lands, mapping and assembly implementation.
A saved candidate footprint is not PCB ready; no routed-board readiness is claimed.

| Subsystem | Selected component / design | Schematic readiness | CAD / PCB readiness | Actual dependency |
|---|---|---|---|---|
| Input | F1 + SS3P6L + TDS3311P + TPS26620 | Conditional ready; calculated settings proposed | Symbols saved; TPS footprint candidate | TPS EP custom-pad/net check; input connector polarity drawing |
|3.3V buck|LMR36015FBRNXR,6.8µH|Ready under prototype capacitor assumptions|Linked models; RNX candidate|Delivered RNX variant/stencil; startup/ripple test later |
|5V buck|LMR36015FBRNXR,10µH|Ready under same assumptions|Linked models; RNX candidate|Same package and functional checks |
|MCU minimum|STM32H723VET6/internal LDO|Ready for core power/boot/reset/SWD|MCU model saved; accessories incomplete|VCAP application check; exact reset/header mechanics |
|Clocks|Two KC2016Z25.0000C15XXK|Connections ready; separate25MHz references|Saved candidate model|Load budget and PHY clock performance confirmation |
|Ethernet PHY|DP83826IRHBR/RMII Leader|Conditional ready|Saved candidate RHB model|Reset/clock timing and EP/stencil review |
|Magnetics/RJ45|HX1188FNL + SS-7188S-A-NF|Signal map ready; chassis policy open|Models saved, some passive models missing|Four75Ω and two HV-capacitor models; chassis treatment |
|RS-485|THVD1420DR,115200baud|Basic circuit ready|Saved model; connector candidate|Exact connector; end termination only if required |
|CAN-FD|ATA6561-GAQW,1/2Mbit/s|Basic node ready|Saved model; connector candidate|Exact connector; optional end termination |
|Two DI|ISO1212DBQR,Type3|Normal18–30V sensing ready|Saved candidate models|Connector; preserve substrate/isolation domains |
|Two DO|BSP75NTA + translator candidate|Role diagram only; numbered circuit held|BSP footprint missing|Diodes terminal numbering and guaranteed loaded drive≥4.5V |

Use project-local `hardware/academic_rev1/libraries/Gateway_Academic.SchLib` and
`.PcbLib` (saved readback: **64 symbols /35 footprints**). LibPkg references these
sources. The historical46/23 IntLib is **stale**: do not use it as current inventory.
File structural validation passed with0errors/0warnings; no new native compilation,
ERC, DRC, placement or electrical test is claimed. See [symbol verification](symbol_library_verification.md).

SS3P6L symbol `SS3P6L-M3_86A` is now a conventional Schottky: visible anodes1/2,
cathodeK; exact MPN and `GW_SS3P6L_VISHAY_88987` association unchanged. Resistor,
capacitor, inductor and fuse graphics were improved. TDS active suppressors,
eFuses/protection arrays and BSP smart switches remain functional blocks.
Follow [SYMBOL_CONVENTIONS.md](../../hardware/academic_rev1/libraries/SYMBOL_CONVENTIONS.md).
NIS3071 remains in the library for history only, quantity0/DNP in the current BOM.

Local source aliases in preserved manufacturer references:
**DS**=`C:/dev/7mo/design/Datasheets_industrial_gateway/`;
**SRC**=`hardware/academic_rev1/libraries/sources/` relative to repository root;
**EC**=`SRC/electrical_closure/`. PDF pages are one-based file pages unless stated.
Package-specific pin tables below are retained; do not substitute another package.

Ground/net policy: `GND_PWR` is source/electronics power return. Existing logic
`GND` is the **same non-isolated electrical return**, with separate quiet routing
intent. In manual capture use one canonical net name or an explicit documented
same-net connection; do not leave two disconnected grounds or place an unapproved
impedance/net-tie between them. `EF_RTN` is a **different** TPS reference and must
not be shorted to either. `FIELD_COM` stays on the isolated DI side. `CHASSIS`
serves RJ45 shield/cable AC returns; no automatic DC logic-ground bond is selected.
External DO load supply is not `24V_ELEC`,3V3 or5V; see section10.

'''
input_section='''## 1. Single-input protection — current construction plan

### A. Selected configuration

`J_IN+ → F1 → SS3P6L → VIN_CLAMP → TPS26620DRCR → 24V_ELEC → both bucks`

TDS3311P.C is **shunt**, VIN_CLAMP to GND_PWR. J_IN− returns to GND_PWR.
Retain SS3P6L: TPS integrated reverse protection does not protect the upstream
TDS branch from reverse forward-conduction. Removal requires a separate revision.
NIS3071MT4TWG, TDS3011P.C and SMBJ33A are superseded. LTC4414/DMP6023LSS
redundant ORing is excluded. External DO drain/load current bypasses this chain.

### B. Manufacturer evidence

[Exact TI datasheet](../../hardware/academic_rev1/libraries/sources/tps26620/tps2662.pdf),
SLVSDT4F Dec2021, byte-identical to `C:/Users/justa/Downloads/tps2662.pdf`:
Table5/Table6-1 p4 (variant/pins),Table7.5 pp6–7,Eq2 p18,Eq5–7 p26,
Fig10-1 p25,§§9.3.8–9.4.1 pp23–24,§10.4 p32,DRC0010J pp43–45.
Diode: [Vishay88987](../../hardware/academic_rev1/libraries/sources/SS3P6L_88987.pdf),pp1/4.
Fuse: [Littelfuse land drawing](../../hardware/academic_rev1/libraries/sources/academic_freeze/fuse_manufacturer_drawing.pdf),printedp371.
TDS: [Semtech Rev2.4](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf),pp2,7–9;
local TDS3311 PDF is not claimed. Exact resistor/capacitor local links are in
[input reference section10.5](input_protection_reference.md#105-sources-cad-readiness-and-actual-unfinished-work).

### C. Components to place

__INPUT_TABLE__

Quantities are populated positions, not passive-specification counts. FLT pull-up
and optional output clamp are DNP. No LC filter or additional24V output bulk is selected.

### D. Pin-by-pin wiring and net labels

| Device / physical terminal | Required connection |
|---|---|
| J_IN functional + / − | + to F1,− to GND_PWR; exact numbered connector polarity still pending |
| F1 terminals1/2 | Series in positive lead; nonpolar; output net VIN_FUSED |
| SS3P6L1 and2 | Both anodes to VIN_FUSED; both visible/connectable |
| SS3P6LK | Cathode to VIN_CLAMP; never drop a physical anode |
| TDS3311P4/5/6 | All IN terminals to VIN_CLAMP |
| TDS3311P1/2/3 | All GND terminals to GND_PWR |
| TPS1 IN | VIN_CLAMP;4.7µF100V +220nF100V input bypass to GND_PWR/pin6 |
| TPS2 UVLO | Junction of768kΩ from pin1 and33.2kΩ to pin3 |
| TPS3 OVP | Junction of33.2kΩ from pin2 and30.1kΩ to EF_RTN |
| TPS4 SHDN_N | Open using internal weak pull-up/default enable; intentional NC. No24V tie |
| TPS5 RTN | EF_RTN; support-component returns; independently connected, not through EP only |
| TPS6 GND | GND_PWR, source/electronics return |
| TPS7 ILIM |13.3kΩ to EF_RTN |
| TPS8 dVdT |10nF to EF_RTN; populated, not the old NIS68pF option |
| TPS9 FLT_N | Unused/open with NC; no selected buck-EN/MCU fault connection |
| TPS10 OUT |24V_ELEC, both buck input banks |
| TPS11 RTN_EP | Solder EP to EF_RTN copper, not system ground |

Ladder order is exactly **IN—768k—UVLO—33.2k—OVP—30.1k—RTN**.
Never connect RTN/support components to GND_PWR. Never connect VCAP/3V3/5V to RTN.
TPS26620 has **adjustable OV cutoff and overload/thermal latch-off**, not auto-retry
or the fixed-clamp behaviour of other variants. After removing a fault, reset by
cycling SHDN, UVLO or input power. Unused SHDN stays open; supervised input cycling
is the selected reset method. Buck EN pins remain tied to24V_ELEC, not FLT.

### E. Values, acceptance and remaining practical work

`I_LIMIT=6.636/13.3=0.49895A`; TI Table7.5 gives0.47/0.50/0.52A at13.3kΩ
under its stated conditions, before resistor tolerance. The approximately0.217A
electronics budget (about0.218A with TPS screening losses) excludes external DO loads.
62kΩ is not reused: it would give only about0.107A by this equation.

| Threshold at IN relative RTN | Typical calculated value |
|---|---:|
| UVLO rising / enable |15.759V|
| UVLO falling / disable |14.446V|
| OVP rising / cutoff |33.142V|
| OVP falling / recovery |30.932V|

Total ladder831.3kΩ. Equations6/7 use Table7.5's1.20V rising typical rather than
the application prose's1.19V. Rising tolerance estimates: UV15.21–16.45V and
OV31.97–34.63V before leakage. Thresholds are local after SS3P6L, not exact source
18/30V cutoffs; source values additionally include diode drop. The enabled window
permits the18–30V operating objective; it does not impose a narrower nominal range.
Current-limited laboratory use remains the assumption, not arbitrary source faults.

Two buck input networks total19.68µF nominal /21.648µF at+10%.10nF gives
`t_ramp=20.5e3×VIN×C`:3.69/4.92/6.15ms at18/24/30V. Estimated charging current
is0.105A typical,0.141A at the screened fast corner; adding0.218A gives0.359A,
below an approximately0.465A lower screening limit. Default open-dVdT charging
would approach0.787A at24V, so **populate10nF**. Startup assumes no full constant-power
load during the low-voltage ramp; verify with MCU reset held initially, then release.
Do not claim the calculation proves all buck startup states or loop stability.

**CAD unfinished:** candidate `GW_DRC0010J_TI_TPS2662` has0.5mm lead pitch,
0.60×0.24mm lead lands, central1.65×2.40mm EP and four0.25×0.50mm extensions.
The extensions remain separate unassigned copper regions; library pads normally
have no net, but these regions do not yet have proven pad11 net inheritance.
Finish native custom-pad11 conversion or verified EF_RTN assignment, R0.05 corners
and mask/paste review before PCB use. EP is never GND_PWR. Use windowed paste;
TI's stencil example is approximately80% coverage at0.125mm thickness. Optional
thermal vias need assembler treatment, not automatic insertion. This does not block
source-backed symbol connections. Input terminal exact numbered polarity is also pending.

### F. Construction verification

- [ ] F1 series, D_REV both anodes present, TDS shunt after diode.
- [ ] TPS pin5 and EP11 on EF_RTN; pin6 on GND_PWR; no external short between them.
- [ ]13.3kΩ pin7-to-RTN;10nF pin8-to-RTN; three-resistor ladder order correct.
- [ ] Local input bypass returns to GND_PWR; both buck input banks retained.
- [ ] FLT and SHDN intentionally open; latch-off/manual-reset behaviour recorded.
- [ ] Protected24V_ELEC feeds electronics only; DO supply and FIELD_COM stay separate.
- [ ] TPS footprint candidate and connector numbering remain visible practical tasks.

'''
parts=re.split(r'(?=^## \d+\.)',old,flags=re.M)[1:]
sections={int(re.match(r'## (\d+)',s)[1]):s for s in parts}
sections[1]=input_section
def replace_sub(s,letter,body):
 return re.sub(r'^### '+letter+r'\..*?(?=^### [A-Z]\.|\Z)',body.rstrip()+'\n\n',s,flags=re.M|re.S)
for n in [2,3]:
 s=sections[n];pfx='B3' if n==2 else 'B5';v='3.3V' if n==2 else '5V';ind='6.8µH XAL4030-682MEC' if n==2 else '10µH XAL4040-103MEC';lower='43.2kΩ' if n==2 else '24.9kΩ'
 s=replace_sub(s,'A',f'''### A. Selected configuration

Selected LMR36015FBRNXR,1MHz FPWM,{ind},100kΩ/{lower} feedback;
{v} allocation{'0.7A' if n==2 else '0.1A'}. Input and EN use **24V_ELEC** from TPS.
PG unused; no FLT-driven enable. Prototype capacitor network is now selected:
2×4.7µF100V CIN,2×220nF100V HF,1×2.2µF50V CVCC,1×100nF CBOOT,
3×15µF16V COUT. CFF20pF is conditional/DNP; no added damping bulk selected.
Capture can proceed; physical RNX/stencil and functional bring-up checks remain.
''')
 s=re.sub(r'^- Exact TDK CIN/COUT.*?(?=^### C\.)','''- Later source closure: [TDK exact input sheet](../../hardware/academic_rev1/libraries/sources/academic_freeze/TDK_exact.pdf),p1lands/p2bias, and [academic capacitor decisions](evidence/input_protection_freeze/bom_decisions.json) supersede the earlier403/missing-land statements. Output lands and exact saved model bindings are in the current mapping.

''',s,flags=re.M|re.S)
 s=s.replace('VIN_PROT','24V_ELEC').replace('three provisional 15-uF','three selected 15-uF')
 # Replace stale explanatory text between component table and connection subsection.
 a=s.index('\n\nUse ',s.index('### C.'));b=s.index('### D.',a)
 s=s[:a]+'''

Use the exact linked inductor and new exact-MPN capacitor symbols in the table.
Each CIN4.7µF part has about3.6µF on the saved30V bias curve; two give about6.48µF
after a10% allowance, supporting the4.7µF effective prototype target. CVCC is now
KEMET2.2µF50V X7R, not the former Samsung1µF part with0.656µF at5V. The selected
prototype assumption of60% retention and−10% tolerance gives1.188µF; confirm VCC
startup/ripple during bring-up. COUT45µF is **rated**, not effective capacitance
or a guarantee of stability. Keep CFF DNP unless application review selects it.

'''+s[b:]
 s=replace_sub(s,'E','''### E. Remaining practical work

- Capture values/quantities are selected; no missing CIN count or CVCC replacement gate remains.
- Confirm delivered RNX0012A/B package and stencil before PCB use; neither SW12 nor NC3 is ground.
- At bring-up verify eFuse/buck startup, VCC, rail ripple/load steps and temperature under the stated allocations. This is functional confirmation, not industrial qualification.
''')
 s=s.replace('CIN count and COUT nominal/effective wording remain correct; CVCC failure is not hidden by its 50-V rating.','CIN has two4.7µF parts; COUT is three15µF rated parts; CVCC is selected2.2µF50V.')
 s=s.replace('CVCC is still flagged blocked until effective-capacitance/internal-LDO compatibility is proven.','CVCC is2.2µF50V X7R; confirm the stated prototype retention assumption at bring-up.')
 sections[n]=s
# Drop obsolete industrial gates from E only; preserve exact pin/source tables.
practical={5:'Clock receiver/route load≤15pF; PHY clock performance and reset/supply timing require prototype confirmation. Preserve all straps and RMII pin reservations.',
6:'Create exact four75Ω CRCW080575R0FKEA models and two C1206C102KGRACAUTO HV capacitor models. Resolve chassis/shield treatment and capacitor application rating; no arbitrary GND bond. Signal map can be drawn meanwhile.',
7:'Finish connector physical numbering. If used at a cable end, select the120Ω termination MPN/jumper. Optional SM712/two10Ω network stays unpopulated and is not needed to draw the selected basic circuit.',
8:'Finish connector physical numbering and optional bus-end120Ω termination/jumper. No additional TVS/filter or mandatory47µF bulk is selected. Confirm intended cable operation during functional tests.',
9:'Finish connector physical numbering; keep SUB1/SUB2 floating separately and FIELD_COM isolated. Normal Type3 sensing is ready. No surge withstand is claimed or required by this academic task.',
10:'Hold numbered BSP capture until exact Diodes terminal numbering/Source-tab map and a required footprint exist. Loaded translator drive≥4.5V remains unproven. Define actual external load/return terminals; verify reset-OFF and intended thermal/inductive operation before energizing those loads.'}
for n,b in practical.items():sections[n]=replace_sub(sections[n],'E','### E. Remaining practical work\n\n'+b)
sections[10]=sections[10].replace('load positive -> selected field-supply distribution','load positive -> external DO supply positive (DO_EXT+)').replace('intended common field/input return compatible with nonisolated logic control','DO_EXT_RETURN connected to BSP source/logic GND_PWR return for the nonisolated control stage')
sections[10]=sections[10].replace('Input TVS candidate clamp does not ensure the BSP 36-V protection condition.','The electronics TDS/eFuse is not in the external DO load path.')
# Refresh every BOM-backed placement row; preserve non-BOM pin tables verbatim.
seen=[]
def row_for(id,description=None):
 r=bom[id];m=mapping.get(id,r);seen.append(id)
 desc=description or r['function'];q=r['quantity'] or 'TBD'
 rating='; '.join(x for x in [r['rated_voltage_or_current'],r['tolerance'],r['power_rating'],r['package']] if x and x!='N/A')
 value=r['recommended_mpn']+('; '+r['nominal_value'] if r['nominal_value'] else '')
 if id=='ACTIVE_TPS26620DRCR':rating='4.5–60V; adjustable OV cutoff; latch-off; DRC10 + RTN EP'
 return '| '+id+' / '+q+' / '+desc+' | '+value+' | '+rating+' | `'+m['symbol']+'` / `'+m['footprint']+'` | '+r['electrical_status']+'; '+m['cad_status']+'; '+r['assembly']+' |'
def refresh(line):
 if not line.startswith('| '):return line
 cells=line.split('|');first=cells[1].strip();id=first.split(' / ')[0]
 if id not in bom and id.startswith('ACTIVE_'):
  mpn=cells[2].strip().split(';')[0].strip()
  id=next((k for k,r in bom.items() if r['item_kind']=='ACTIVE' and r['recommended_mpn']==mpn),id)
 if id not in bom:return line
 desc=first.split(' / ',2)[2] if ' / ' in first else None
 rendered=row_for(id,desc)
 if id.startswith('ACTIVE_'):
  cols=rendered.split('|');cols[3]=cells[3];rendered='|'.join(cols)
 # LMR global quantity is2, one instance per each buck section.
 if id=='ACTIVE_LMR36015FBRNXR':rendered=rendered.replace(id+' / 2 / ',id+' / 1 / ',1)
 return rendered
ids=['IN_FUSE','IN_REVERSE','IN_TVS','ACTIVE_TPS26620DRCR','IN_RLIM','IN_CDVDT','IN_UV_TOP','IN_UV_MID','IN_UV_BOTTOM','IN_BULK','IN_HF','IN_J','IN_RFAULT','IN_SOUT']
table='| BOM ID / quantity / function | MPN / value | Ratings / package | Symbol / footprint | Recorded electrical / CAD / population |\n|---|---|---|---|---|\n'+'\n'.join(row_for(k) for k in ids)
sections[1]=sections[1].replace('__INPUT_TABLE__',table)
nets={1:'VIN_FUSED,VIN_CLAMP,24V_ELEC,EF_RTN,GND_PWR; no VIN_PROT alias.',2:'24V_ELEC,3V3,B3_SW (pins3/12/BOOT return),B3_VCC_INTERNAL, B3_FB (pin7),GND_PWR/GND.',3:'24V_ELEC,5V,B5_SW,B5_VCC_INTERNAL,B5_FB,GND_PWR/GND; never join B3/B5 internal nets.',4:'3V3,GND,VCORE_CAP,NRST,BOOT0,SWDIO,SWCLK,MCU_HSE25 plus the peripheral reservation labels in the table.',5:'3V3,GND,PHY_XI25,PHY_nRESET,ETH_RMII_REF_CLK,ETH_MDIO,ETH_MDC and RMII data/control labels from section4; PHY_XI25 is not MCU_HSE25.',6:'MDI_TXP,MDI_TXN,MDI_RXP,MDI_RXN, cable CT nodeA, unused-pair nodeB,CHASSIS. NodesA/B remain distinct.',7:'RS485_TX (PD8),RS485_RX (PD9),RS485_DE (PD10),RS485_nRE (PD11),RS485_A,RS485_B,GND,3V3.',8:'FDCAN1_TX (PD1),FDCAN1_RX (PD0),CAN_STBY (PE7),CANH,CANL,3V3,5V,GND.',9:'DI1,DI2,FIELD_COM,DI1_SENSE,DI1_IN,DI2_SENSE,DI2_IN,3V3,GND; do not share field/control returns.',10:'DO1 (PE2),DO2 (PE3),DO1_DRIVE,DO2_DRIVE,DO_EXT+,DO_EXT_RETURN,3V3,5V,GND_PWR. External DO return is not FIELD_COM/CHASSIS/EF_RTN.'}
for n,s in sections.items():
 if n!=1:s='\n'.join(refresh(l) for l in s.splitlines())+'\n'
 s+='\n### G. Required net labels\n\n'+nets[n]+'\n\n'
 sections[n]=s
out=intro+''.join(sections[n] for n in sorted(sections))
do_section=D/'evidence/bsp75n_closure/construction_section.md'
if do_section.exists():
 current=sections[10].split('### C. Components to place')[1].split('### D.')[0]
 table='\n'.join(l for l in current.splitlines() if l.startswith('|'))
 table=table.replace('intended 0.5 A/channel; IN>=4.5 V for protected operation; Source tab; numbered map blocked',
  '60V VDS;0.5A/channel prototype target;VPROT≥4.5V;IN/D/S/S_TAB physical mapping verified')
 replacement=do_section.read_text(encoding='utf-8').replace('__DO_COMPONENTS__',table).replace('DO1_LOAD−','DO1_DRAIN').replace('DO2_LOAD−','DO2_DRAIN')
 out=re.sub(r'^## 10\..*?(?=^## \d+\.|\Z)',lambda m:replacement,out,flags=re.M|re.S)
 out=out.replace('Role diagram only; numbered circuit held','Physical wiring ready; drive acceptance pending')
 out=out.replace('BSP footprint missing','BSP footprint verified; driver candidate')
 out=out.replace('Diodes terminal numbering and guaranteed loaded drive≥4.5V','Loaded drive≥4.5V and reset-OFF acceptance')
 out=out.replace('GPIO; **BLOCKED DO implementation**','GPIO; **DO drive acceptance pending**')
out=out.replace('Both have missing CAD models, separate from the six retained-library warnings.','Both have missing CAD models; the historical compiler warnings are not current validation.')
out=out.replace('Some passive rows still mention DCUR; the actual prepared/active candidate is **DCTR/DCT8**, not a silently interchangeable DCU8 package. This is a recorded inconsistency to resolve before physical placement, not authorization to change packages.',
 'The prepared/active candidate is **DCTR/DCT8**. The two bypass parent labels were corrected from historical DCUR text; no package substitution or drive approval occurred.')
out=out.replace('translator DCTR/DCUR row inconsistency; ','')
out=out.replace('Translator identity/package matches DCTR/DCT; DCUR row inconsistency is resolved before placement.','Translator identity/package matches the current DCTR/DCT BOM and mapping; no DCU substitute.')
out+='''## 11. Construction closure and correction record

The old guide's SMBJ33A/VIN_PROT circuit, unselected fuse/bulk and missing
2220/1210 land statements are replaced by the selected TDS3311/TPS chain and
current exact-MPN capacitor models. NIS62kΩ/68pF settings are historical, not TPS
connections. TPS pin assignments/ladder were checked against Table6-1/Eq5–7;
no pin reversal was found in the latest TPS proposal. The1.19V application-prose
versus1.20V electrical-table discrepancy is explicitly resolved in section1.

MCU power/VCAP/debug/boot/oscillator and peripheral pin tables were preserved;
there is no reassignment or added VDDLDO pin. Old compilation messages remain
historical evidence, not validation of current64/35 sources. No new ERC/DRC is claimed.

Remaining work that affects full component construction: exact connector/header/
button mechanics and numbered assignments; four75Ω and two HV Ethernet capacitor
models; optional bus-end resistor/jumper selections only where termination is used;
BSP numbering/footprint and guaranteed driver voltage. TPS custom thermal pad and
RNX/other candidate assembly checks affect PCB completion, not the established
symbol wiring. Normal laboratory startup/ripple/temperature checks are bring-up
tasks; absent industrial certification is not a blocker.

Current source-record discrepancy: conditional CFF rows carry quantity1 as reserved
positions, while selected capture leaves them DNP pending application review.
Likewise optional RS surge, CAN bulk and DI-PE candidate rows are not mandatory
population. No BOM selection/quantity was silently changed in this documentation task.
Current75Ω CAD status is MISSING; do not substitute a generic resistor with an
unverified0805 footprint just to hide this pending task.

Metadata corrections only: IN_BULK/IN_HF descriptions now name TPS26620 instead
of NIS; DO supply bypass parent references now name the selected DCTR rather
than the obsolete DCUR text. MPNs, values, quantities and drive approval did not change.

Before marking a manually drawn sheet complete, check every power/ground/NC,
symbol-to-pad mapping, passive quantity and cross-sheet label against its section.
Run native ERC and compile libraries when actually performed; save actual results.
Do not propagate library edits to schematic/PCB automatically.
'''
out=re.sub(r'\b(pin|pad|Table|Figure|section|Eq)(?=\d)',r'\1 ',out)
eth_closed=(D/'evidence/ethernet_75ohm/cad_assets.json').exists()
if eth_closed:
 out=out.replace('64 symbols /35 footprints','65 symbols /36 footprints')
 out=out.replace('Four75Ω and two HV-capacitor models; chassis treatment','Two HV-capacitor models; chassis treatment')
 out=out.replace('Create exact four75Ω CRCW080575R0FKEA models and two C1206C102KGRACAUTO HV capacitor models.',
  'The four75Ω positions now use saved CRCW080575R0FKEA / GW_CRCW0805_VISHAY_20035_REFLOW, C844859. Create the two C1206C102KGRACAUTO HV capacitor models.')
 out=out.replace('Both have missing CAD models; the historical compiler warnings are not current validation.',
  'The75Ω model is now verified; only the HV capacitor model remains missing. Historical compiler warnings are not current validation.')
 out=out.replace('four75Ω and two HV Ethernet capacitor\nmodels','two HV Ethernet capacitor\nmodels')
 out=out.replace('Current75Ω CAD status is MISSING; do not substitute a generic resistor with an\nunverified0805 footprint just to hide this pending task.',
  'Current75Ω CAD status is VERIFIED: retain CRCW080575R0FKEA, C844859, four instances. See [resistor closure](ethernet_75ohm_library_closure.md) for exact reflow geometry, sources and supplier-suffix distinction.')
 out+='\n## 12. Ethernet75Ω library closure\n\nFour ETH_RBOB instances use `CRCW080575R0FKEA` / `GW_CRCW0805_VISHAY_20035_REFLOW`, verified catalog code C844859. C1511836 is the different commodity C-suffix part and is not adopted. Conventional resistor pins1/2 map to pads1/2 (nonpolar). Copper lands0.95×1.45mm, inner gap1.00mm, centers1.95mm per Vishay20035p9 REFLOW. Mask+.05mm and1:1paste are explicit prototype process choices. Topology and all MCU/interface pins remain unchanged. [Local datasheet](../../hardware/academic_rev1/libraries/sources/ethernet_75ohm/C844859.pdf). Native compilation has not been performed for the65/36 sources.\n'
cap_closed=(D/'evidence/ethernet_1nf/cad_assets.json').exists()
if cap_closed:
 out=out.replace('65 symbols /36 footprints','66 symbols /37 footprints')
 out=out.replace('Two HV-capacitor models; chassis treatment','Chassis treatment; physical layout')
 out=out.replace('Models saved, some passive models missing','Resistor/capacitor models saved')
 out=out.replace('Create the two C1206C102KGRACAUTO HV capacitor models.',
  'The two C1206C102KGRACAUTO models are now saved: GW_C1206_KEMET_C1076_DENSITY_B, C600002. No remaining CAD model blocker for the termination resistors/capacitors.')
 out=out.replace('The75Ω model is now verified; only the HV capacitor model remains missing.',
  'Both75Ω and1nF2kVDC models are now verified; the application does not acquire safety-Y certification from a voltage rating.')
 out=out.replace('two HV Ethernet capacitor\nmodels; optional bus-end','optional bus-end')
 out=out.replace('Native compilation has not been performed for the65/36 sources.','Native compilation has not been performed for the current66/37 sources.')
 out+='\n## 13. Ethernet1nF capacitor library closure\n\nBoth ETH_CBOB instances use `C1206C102KGRACAUTO` / `GW_C1206_KEMET_C1076_DENSITY_B`, C600002:1nF,10%,2000VDC,X7R,1206. KEMET C1076p10 Table3 densityB reflow pads1.15×1.80mm atx±1.50mm; body3.20×1.60mm. Pin1-to-pad1 and pin2-to-pad2 are nonpolar project conventions. Mask+.05mm and1:1paste are explicit process choices. Connect one instance nodeA-to-CHASSIS and the other nodeB-to-CHASSIS; do not join nodesA/B or logic GND. [Capacitor evidence](ethernet_1nf_library_closure.md). No safety-Y or industrial pulse/insulation certification is claimed.\n'
if do_section.exists():
 out=out.replace('66 symbols /37 footprints','66 symbols /38 footprints')
 out=out.replace('BSP numbering/footprint and guaranteed driver voltage.','BSP loaded driver voltage/reset-OFF acceptance. Physical BSP mapping and lands are closed using Diodes function-identified positions.')
 out=out.replace('Native compilation has not been performed for the current66/37 sources.','Native compilation has not been performed for the current66/38 sources.')
 out+='\n## 14. BSP75N physical closure\n\nThe prior numbering/land-pattern blocker is superseded by verified Diodes top-view positions and suggested lands. Alphabetic pin/pad IDs IN,D,S,S_TAB are retained deliberately; no equivalent-vendor numbering was borrowed. [Actionable DO construction is section10](#10-sn74lvc2t45-and-two-bsp75n-digital-outputs). [Saved model verification](bsp75n_physical_closure.md). Drive electrical approval remains pending independently.\n'
mission_overlay=D/'evidence/autonomous_closure/guide_overlay.py'
if mission_overlay.exists():
 import runpy
 out=runpy.run_path(str(mission_overlay))['apply'](out,D)
(D/'schematic_construction_guide.md').write_text(out,encoding='utf-8')
# Keep older evidence readable but make construction authority unambiguous.
p=D/'schematic_readiness_gate.md';t=p.read_text(encoding='utf-8')
notice='''> Current manual-construction authority: [schematic_construction_guide.md](schematic_construction_guide.md).
> The original gate below is a historical closure snapshot, followed by the later TPS amendment.
> Its old SMBJ33A/fuse/bulk/CVCC holds and46/23 compiled-library claims are superseded
> by the guide and input-reference section10. The current source libraries have64/35;
> their integrated library has not been recompiled. Other unresolved device issues
> remain visible in the current guide; historical qualification lists are not new requirements.

'''
if '> Current manual-construction authority:' not in t:
 a=t.index('\n')+1;t=t[:a]+'\n'+notice+t[a:]
if eth_closed:t=t.replace('current source libraries have64/35','current source libraries have65/36')
if cap_closed:t=t.replace('current source libraries have65/36','current source libraries have66/37')
if do_section.exists():t=t.replace('current source libraries have66/37','current source libraries have66/38')
p.write_text(t,encoding='utf-8')
p=D/'passive_component_selection.md';t=p.read_text(encoding='utf-8')
t=t.replace('The authoritative current decisions and limits are in\n[schematic_readiness_gate.md](schematic_readiness_gate.md).',
 'Use [schematic_construction_guide.md](schematic_construction_guide.md) for current manual\nconstruction and [schematic_readiness_gate.md](schematic_readiness_gate.md) for historical closure evidence.')
if eth_closed:
 t=t.replace('Library resources now have64 symbols and35 footprints','Library resources now have65 symbols and36 footprints')
 if 'ETH_RBOB CAD closure:' not in t:t+='\nETH_RBOB CAD closure: four CRCW080575R0FKEA/C844859, symbol and manufacturer reflow footprint verified. [Closure evidence](ethernet_75ohm_library_closure.md). FKEAC/C1511836 is not substituted.\n'
if cap_closed:
 t=t.replace('Library resources now have65 symbols and36 footprints','Library resources now have66 symbols and37 footprints')
 if 'ETH_CBOB CAD closure:' not in t:t+='\nETH_CBOB CAD closure: two C1206C102KGRACAUTO/C600002 capacitors, source-backed symbol/footprint saved. [Evidence](ethernet_1nf_library_closure.md).2kVDC is not safety-Y certification; application status remains provisional.\n'
if do_section.exists():
 t=t.replace('Library resources now have66 symbols and37 footprints','Library resources now have66 symbols and38 footprints')
 t=t.replace('The BSP75N numbered\nmap remains unfinished; no schematic or PCB was modified.',
  'BSP75N physical mapping/lands are now verified using functional pin IDs; loaded drive remains pending. No schematic or PCB was modified.')
p.write_text(t,encoding='utf-8')
(O/'table_bindings.json').write_text(json.dumps(sorted(set(seen)),indent=2)+'\n')
print('Updated guide; BOM-linked component rows:',len(seen))
