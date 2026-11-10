# Academic Gateway Rev.1 — initial native schematic audit

> Actualización nativa 2026-11-10: ver [cierre y evidencia actual](closure_verification_rev1.md) y [BOM real por designador](assembly_bom_rev1.csv). Los pendientes de captura/modelos descritos debajo son históricos y quedan sustituidos por ese cierre; la validación del diálogo ECO sigue pendiente.


<!-- AUTONOMOUS_CLOSURE_20261108_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- AUTONOMOUS_CLOSURE_20261108_END -->

**Phase1 baseline recorded before any schematic/project correction.** Academic laboratory prototype; no certification requirement is introduced. This report is an initial, immutable findings baseline; subsequent changes are recorded separately in schematic_correction_log_rev1.md.

## Actual project and evidence

Project: `hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb`. Native Electronics AI context was TopLevel.SchDoc in this project. Five schematic members are loaded: Power,MCU,Ethernet,Field_IO,TopLevel. PCB1.PcbDoc exists but was neither audited nor modified. SchLib/PcbLib are project members; additional open LibPkg validation documents are not gateway schematic sheets. Hierarchy mode is **Flat**; local port names do not become net names (`AllowPortNetNames=0`). Compiled port connectivity, rather than matching visible strings alone, is the evidence.

Read native BOM and **all437 pin/net assignments for106 components**; component/model/parameter records were independently read from saved SchDocs without reconstructing connectivity geometrically. Native library readback:66 symbols/38 footprints. No unsaved schematic flag was reported; modified-flag detection is not globally complete. Baseline hashes are preserved. The initial combined snapshot's components/nets sections failed because they demanded a loaded PCB; explicit project-scoped `proj_get_nets` and native `proj_get_bom` succeeded. This limitation was not worked around by loading/modifying a PCB.

| Sheet | Components |
|---|---|
| Power.SchDoc | 40 |
| MCU.SchDoc | 18 |
| Ethernet.SchDoc | 33 |
| Field_IO.SchDoc | 15 |
| TopLevel.SchDoc | 0 |

## Scope and practical limits

Every placed component and pin assignment is recorded, including intentional unused MCU GPIOs; unused pins are not automatically defects. Full rendered wire readability/physical component placement and every off-grid primitive were not visually audited. Native wire X1/Y1 reads were unsupported, so no geometric inference substitutes for compiled connectivity. A complete per-part electrical qualification and every manufacturer mechanical drawing have not been revalidated in this task; unresolved package/manufacturer evidence is explicit in the inventory. PCB readiness is NO.

## Baseline findings and exact change plan

| ID | Severity | Sheet / pins | Actual | Expected / correction | Evidence |
|---|---|---|---|---|---|
| A01 | CRITICAL | Power / U2.12,U3.12,L1.1,L2.1,C10.1,C19.1 | All on SW | Independent B3_SW and B5_SW; Rename the two SW power ports in each converter; no shared switch node | Native437-pin table; guide2/3; TI SNVSB49D p4/Fig10-1 |
| A02 | CRITICAL | Power / C7,C16 | C0805C475K4RACTU,16V on 24V | C5750X7R2A475K230KA,100V; Replace these with selected100V parts; add one extra4.7uF per buck per selected bank | Placed MPN/rating; guide2/3 exact capacitor selection |
| A03 | MAJOR | Power / U2.9/10,U3.9/10 | Vin only connected to both regulators/PG pullups; distinct from24V | Both VIN pins and EN to TPS OUT/24V; Rename Vin power ports to24V; retain existing protected rail alias | Native pins; TI SNVSB49D p4 pins2/10/9 |
| A04 | MAJOR | Power / R5,R7,R6 | R5=43.2k upper;R7=43.2k lower;R6=100k on PG | Upper100k/lower43.2k; PG open; R5 exact100k; remove/DNP PG pullupR6 separately; result currently nominal2V | TI SNVSB49D Table10-1/1V VFB; guide2 |
| A05 | MAJOR | Power / R8,R10,R9 | R8=43.2k upper;R10=24.9k lower;R9=100k on PG | Upper100k/lower24.9k;PG open; R8 exact100k; remove/DNP PG pullupR9 separately; result currently nominal2.735V | TI SNVSB49D Table10-1; guide3 |
| A06 | MAJOR | Power / U2.3,U3.3 | Individually single-pin nets | Each to its own SW12; Connect U2.3 to B3_SW and U3.3 to B5_SW; never join switch nodes | TI SNVSB49D p4 Pin Functions |
| A07 | MAJOR | Power / C12,C21 | CL10A105KB8NNNC1uF | Selected C0805C225K5RACTU2.2uF50V; Replace exact selected CVCC parts; source1uF alone is not intrinsically wrong but superseded application selection | Guide2/3 current capacitor closure; TI p4 requires quality1uF |
| A08 | MAJOR | Power / D2.1–6 | TDS3011P.C | TDS3311P.C same functional6-pin shunt; Replace exact approved source model preserving1/2/3GND,4/5/6VIN_CLAMP; do not merely rename comment | Approved freeze; guide1 |
| A09 | MAJOR | Ethernet / J2.2,T1.14 | J2.1/2 bothTX+;T1.14TX- single-pin | J2.2 to T1.14TX-; Change only TX+ label at9600,5000 toTX- | Native nets; Pulse HX1188FNL sheet2/StewartCT710001;guide6 |
| A10 | MAJOR | Ethernet / C46.1,C52.1 | Both on logicGND | Both on CHASSIS; independent A/B capacitor branches; Reassign both capacitor returns to defined CHASSIS after chassis policy confirmed; ground-boundary edits require separate approval | Guide6 accepted topology; native nets |
| A11 | MAJOR | Ethernet / J2.S1/S2 | Separate single-pin floating nets | Defined CHASSIS shield return; Finish shield/chassis implementation; do not bond logicGND automatically | Guide6; CT710001 shell drawing |
| A12 | MAJOR | MCU / U4.71/76 | SWCLK onPA12/71;PA14/76 single-pin | SWCLK onPA14/76; Move SWCLK label to actual PA14 connection6400,4000; no peripheral reassignment | ST DS13313 LQFP100/Table7/8;guide4 |
| A13 | MAJOR | MCU / Debug/reset access | No SWD header,NRST14 only capacitorC28;SW1 is BOOT recovery | Six-pin SWD/header + reset access perguide4; Add selected header/reset contacts after exact MPN/contact drawing closure; do not mistake SW1 for reset | Actual106-component inventory; guide4 |
| A14 | MAJOR | Ethernet / PHY-side ESD | No TPD4E05U06DQAR placed | Selected PHY-side ESD array and explicit pass-through connections; Place selected model and four signal paths; avoid mass reroute | Guide6 accepted circuit |
| A15 | MAJOR | Ethernet / U6.6/7 and U7.6/7 | Single-pin bus nets; no RS485/CAN connector/termination jumper | A/B and CANH/L to approved external connectors; optional termination; Complete external interfaces after connector pin drawings; no extra bias/TVS selection | Native nets/inventory; guide7/8 |
| A16 | CRITICAL | Field_IO / R21.2/U8.4/U4.3 and R22.2/U8.5/U4.4 | 1k field threshold resistor tied to logic OUT/MCU net | 1k high side to external field input; low side to SENSE; never OUT; Remove RTHR free ends from OUT1/OUT2 and terminate on separate fieldDI terminals; ground/isolation-boundary correction requires separate approval | TI ISO1212 SLLSEY7G p4 Pin Functions/Fig8-2;guide9 |
| A17 | MAJOR | Field_IO / U10/U11.IN/D/S/S_TAB | All eight terminals individual single-pin nets; U9B1/B2 separate | IN←B1/B2; D→separate load negatives;S+tab→DO_EXT_RETURN; Complete local BSP wiring and external terminals; no invented numeric pads | Diodes DS33016 pp1,8;guide10 |
| A18 | MAJOR | Field_IO / U9B1/B2 | No B-side10k pull-downs | One10k from each DO_DRIVE to established source return; Add two selected10k parts; preserve architecture and confirm defaultOFF before loads | Guide10; native inventory R24/25 only A-side |
| A19 | MAJOR | Field_IO / U9→BSP drive | Physical wiring absent and loadedVOH not guaranteed | ≥4.5V IN-to-localS for overtemperature protection; Retain separate loaded-drive/resetOFF acceptance; no driver architecture substitution | Diodesp4/TI SCES516N Table5.5;guide10 |
| A20 | MAJOR | TopLevel / Four sheet symbols | FileName=File Name;Designator=Designator | Actual four sheet filenames and meaningful unique sheet IDs; Map each intended block explicitly; labels/positions alone do not prove which child was intended | Native eSheetSymbol/ERC detail; project Flat |
| A21 | CAD PENDING | All / R12,R14,C46,R19,R17,C52,U10,U11,R22,R21,SW1,L1,C6,C4,C5,L2,C15,C13,C14,F1,D1,U1,C2,C1,R1,R3,R4,R2 | 28 placed components have no footprint model | Exact compatible model required for PCB; Bind verified models locally; do not global-update or infer missing links from library presence | Native BOM independently matched saved records |
| A22 | CAD PENDING | Power/Ethernet/Field_IO / TPS,RNX,RHB,DBQ,DCT,genericR/C | Existing source CAD_CANDIDATE or absent instance models | Verified exact land/mask/paste/pin-pad map before PCB; Next footprint task; no fabrication readiness claim | Current CAD mapping; TPS custom EP unresolved |
| A23 | MINOR | Power / C11,C20,R6,R9 | No project variants; conditionalCFF and PG resistors physically present withoutDNP | CFF DNP unless approved;PG unused; Record DNP explicitly or remove only intended option; no bulk variant changes | Guide2/3;project variant_count0 |
| A24 | INFORMATIONAL | Power / U1.4/U1.9 | Open; ERC reports SHDN floating | Intentional internal enable; FLT unused; Do not wire SHDN to24V or groundRTN to silenceERC; targeted NC markers only | TI SLVSDT4F p4/9.3;guide1 |
| A25 | INFORMATIONAL | Ethernet / U5.1/.26/.27 | Open; ERC calls floating | Enhanced ModeSelect open;unusedRMII TXD2/3 perguide; No false repair based onERC alone; mark intentional NC where appropriate | TI SNLS647I pp5–7;guide5 |
| A26 | INFORMATIONAL | Power / J1 | TB002-500-02BE;BOM JL126-50002G01 | Actual selected/accepted connector identity needs reconciliation; Do not substitute valid connector automatically; retain actual identity in inventory | Placed metadata vs currentBOM |
| A27 | INFORMATIONAL | MCU/other / 10k pull-down parts | Several FOJAN5%FRC0603J103TS instead of selectedYageo1% | Selected exactMPN consistency; Record mismatch; not an automatic electrical failure or mandatory equivalent replacement | Placed metadata/currentBOM |

## Subsystem coverage

| Subsystem | Native result |
|---|---|
| Input | F1→D1 both anodes→clamped input→U1OUT24V is present;D2 wrongMPN. U1 pins5/11=EF_RTN distinct from6=GND. LadderR1=768k,R3=33.2k,R4=30.1k in correct order;R2=13.3k7→RTN,C3=10nF8→RTN. 6.636/13.3=0.49895A;1.2×831.3/63.3=15.759V UV;1.2×831.3/30.1=33.142V OV;TI Table7.5/Eq2/5–7 and Table5 latch-off confirmed. No NIS placed. |
| Bucks | Both input/HF networks and feedback/switch nodes audited; critical sharedSW and16V capacitors;two missing mainCIN parts;wrong divider uppers/PG pullups;CVCC stale. BOOT capacitors span BOOT/SW;VCC rails separate;grounds common as intended. |
| MCU | FiveVDD11/27/50/75/100=3.3V,fiveVSS10/26/49/74/99=GND;VDDA21,VREF20,VBAT6 supplied;VSSA19GND;VCAP48/73 joined only toC33/C34,not3V3. Five100nF VDD,bypass/bulk and independentY1 present;PH012 driven/PH113 unused. NRST14 hasC28;BOOT94R11down+SW1to3.3V. DebugSWCLK wrong;header/reset access absent. Peripheral port pin links checked against guide;no reassignments made. |
| Ethernet | All9RMII/MDIO/MDC nets match selectedMCU pins;PHYreset32→PE6/5;25MHzY2→XI9;RBIAS6.49k,CEXT2nF,RMIIstrap14pullup2.49k;other defaultstraps unloaded perguide. CT2/7 each2×100nFtoGND. Four selected75Ω present with correct two branch nodes;A/B remain separate but wronglogicGND capacitor returns;TXpolaritylabel fault;shieldfloating;ESDabsent. |
| RS485 | U6R1→PD9/56,D4←PD8/55,DE3←PD10/57 withR18down,nRE2←PD11/58 withR16up,VCC3.3V+C51. A/Bsinglepins;externalconnector/terminationoptions absent. No extra bias/protection introduced. |
| CAN | U7TXD1←PD1/82,RXD4→PD0/81,STBY8←PE7/37,VCC5V+C53,VIO3.3V+C54,GNDpresent. No STBY pull resistor selected byguide; firmware startup remains application condition. CANH/Lsinglepins;connector/endtermination absent. |
| DI | U8VCC2/EN3=3.3V,GND1/8logicGND,FGND9/14FIELD_COM distinct,SUB12/13 andNC6/7 separate. R20/R23=562Ω IN↔SENSE,C55/C57=10nF SENSE→FIELD_COM. R21/R22=1k misplaced to logicOUTnets;externalfieldconnectorabsent. |
| DO | U9VCCA3.3V/VCCB5V/DIR3.3V/GND andC58/C59 present;A1/2←PE2/PE3,R24/R25down. B1/2 unconnected to BSP;Bpulldownsabsent;allBSPterminals unwired;noexternalconnectors. Physical mapping is already verified in source,not blocked by lack of numeric identifiers. Loadeddrive remains separate. |
| Cross-sheet | Port-basedRMII/UART/CAN/DI/DO links checked fromcompiled memberships. Fourdummychildfilenames breakTopLevelreferences;flatconnectivity still links existingports. NoobservedFIELD_COM-toGNDnetmerge;DIresistorlink nevertheless crosses domains incorrectly. |

## Component/BOM/model comparison

| Designator | Sheet | Exact placed MPN | Value / tolerance / rating | Model |
|---|---|---|---|---|
| U5 | Ethernet.SchDoc | DP83826IRHBR | DP83826IRHBR; NOT_RECORDED; NOT_RECORDED | GW_RHB0032M_TI |
| R13 | Ethernet.SchDoc | RC0603FR-076K49L | 6.49 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| Y2 | Ethernet.SchDoc | KC2016Z25.0000C15XXK | KC2016Z25.0000C15XXK; NOT_RECORDED; NOT_RECORDED | GW_KC2016Z_KYOCERA |
| C37 | Ethernet.SchDoc | C0603C202J5GACTU | 2 nF; 5% seleccion; 50 V; C0G | GW_CAND_0603_cap |
| C38 | Ethernet.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C39 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C40 | Ethernet.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| C41 | Ethernet.SchDoc | CL21A106KAYNNNE | 10 uF; 10%; 25 V; X5R; -55..85 C | GW_CAND_0805_cap |
| R15 | Ethernet.SchDoc | RC0603FR-072K49L | 2.49 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| C36 | Ethernet.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C47 | Ethernet.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C48 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C49 | Ethernet.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| C50 | Ethernet.SchDoc | CL21A106KAYNNNE | 10 uF; 10%; 25 V; X5R; -55..85 C | GW_CAND_0805_cap |
| T1 | Ethernet.SchDoc | HX1188FNL | HX1188FNL; NOT_RECORDED; NOT_RECORDED | GW_HX1188FNL_PULSE |
| C43 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C42 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C45 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C44 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| U6 | Ethernet.SchDoc | THVD1420DR | THVD1420DR; NOT_RECORDED; NOT_RECORDED | GW_SOIC8_1P27_5P4 |
| J2 | Ethernet.SchDoc | SS-7188S-A-NF | SS-7188S-A-NF; NOT_RECORDED; NOT_RECORDED | GW_SS7188SANF_STEWART |
| R16 | Ethernet.SchDoc | FRC0603J103TS | 10 kOhm; 5%; >= 3.3 V; tension de trabajo por verificar | GW_CAND_0603_res |
| R18 | Ethernet.SchDoc | FRC0603J103TS | 10 kOhm; 5%; >= 3.3 V; tension de trabajo por verificar | GW_CAND_0603_res |
| C51 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R12 | Ethernet.SchDoc | CRCW080575R0FKEA | 75 Ohm; 1%; NOT_RECORDED | MISSING |
| R14 | Ethernet.SchDoc | CRCW080575R0FKEA | 75 Ohm; 1%; NOT_RECORDED | MISSING |
| C46 | Ethernet.SchDoc | C1206C102KGRACAUTO | 1 nF; 10%; NOT_RECORDED | MISSING |
| R19 | Ethernet.SchDoc | CRCW080575R0FKEA | 75 Ohm; 1%; NOT_RECORDED | MISSING |
| R17 | Ethernet.SchDoc | CRCW080575R0FKEA | 75 Ohm; 1%; NOT_RECORDED | MISSING |
| C52 | Ethernet.SchDoc | C1206C102KGRACAUTO | 1 nF; 10%; NOT_RECORDED | MISSING |
| U7 | Ethernet.SchDoc | ATA6561-GAQW | ATA6561-GAQW; NOT_RECORDED; NOT_RECORDED | GW_SOIC8_1P27_5P4 |
| C53 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C54 | Ethernet.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| U8 | Field_IO.SchDoc | ISO1212DBQR | ISO1212DBQR; NOT_RECORDED; NOT_RECORDED | GW_DBQ0016A_TI |
| U9 | Field_IO.SchDoc | SN74LVC2T45DCTR | SN74LVC2T45DCTR; NOT_RECORDED; NOT_RECORDED | GW_DCT0008A_TI |
| U10 | Field_IO.SchDoc | BSP75NTA | BSP75NTA; NOT_RECORDED; NOT_RECORDED | MISSING |
| U11 | Field_IO.SchDoc | BSP75NTA | BSP75NTA; NOT_RECORDED; NOT_RECORDED | MISSING |
| C56 | Field_IO.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R23 | Field_IO.SchDoc | RC0603FR-07562RL | 562 Ohm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| R22 | Field_IO.SchDoc | MM204F1K00TKRTR3K0 | MM204F1K00TKRTR3K0; NOT_RECORDED; NOT_RECORDED | MISSING |
| C57 | Field_IO.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R20 | Field_IO.SchDoc | RC0603FR-07562RL | 562 Ohm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| R21 | Field_IO.SchDoc | MM204F1K00TKRTR3K0 | MM204F1K00TKRTR3K0; NOT_RECORDED; NOT_RECORDED | MISSING |
| C55 | Field_IO.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C58 | Field_IO.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R24 | Field_IO.SchDoc | FRC0603J103TS | 10 kOhm; 5%; >= 3.3 V; tension de trabajo por verificar | GW_CAND_0603_res |
| R25 | Field_IO.SchDoc | FRC0603J103TS | 10 kOhm; 5%; >= 3.3 V; tension de trabajo por verificar | GW_CAND_0603_res |
| C59 | Field_IO.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| U4 | MCU.SchDoc | STM32H723VET6 | STM32H723VET6; NOT_RECORDED; NOT_RECORDED | GW_LQFP100_ST_1L |
| C22 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C31 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C32 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C26 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C35 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C27 | MCU.SchDoc | C0805C475K4RACTU | 4.7 uF; 10%; 16 V; X7R | GW_CAND_0805_cap |
| C33 | MCU.SchDoc | C0603C225K8RACTU | 2.2 uF; 10% candidato; ST permite 20%; 10 V; X7R; ESR <100 mOhm | GW_CAND_0603_cap |
| C34 | MCU.SchDoc | C0603C225K8RACTU | 2.2 uF; 10% candidato; ST permite 20%; 10 V; X7R; ESR <100 mOhm | GW_CAND_0603_cap |
| C30 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C29 | MCU.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| C24 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C23 | MCU.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| C28 | MCU.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R11 | MCU.SchDoc | FRC0603J103TS | 10 kOhm; 5%; >= 3.3 V; tension de trabajo por verificar | GW_CAND_0603_res |
| SW1 | MCU.SchDoc | TBD | SPST-NO; TBD; TBD | MISSING |
| Y1 | MCU.SchDoc | KC2016Z25.0000C15XXK | KC2016Z25.0000C15XXK; NOT_RECORDED; NOT_RECORDED | GW_KC2016Z_KYOCERA |
| C25 | MCU.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| U2 | Power.SchDoc | LMR36015FBRNXR | LMR36015FBRNXR; NOT_RECORDED; NOT_RECORDED | GW_RNX0012A_TI;GW_RNX0012B_TI |
| L1 | Power.SchDoc | XAL4030-682MEC | 6.8 uH; 20%; Isat25C 3.6 A; Irms20C 3.0 A | MISSING |
| C6 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| C4 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| C5 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| R6 | Power.SchDoc | RC0603FR-07100KL | 100 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| R5 | Power.SchDoc | RC0603FR-0743K2L | 43.2 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| C7 | Power.SchDoc | C0805C475K4RACTU | 4.7 uF; 10%; 16 V; X7R | GW_CAND_0805_cap |
| C8 | Power.SchDoc | C0805C224K1RACTU | 220 nF; 10%; 100 V; X7R | GW_CAND_0805_cap |
| C9 | Power.SchDoc | C0805C224K1RACTU | 220 nF; 10%; 100 V; X7R | GW_CAND_0805_cap |
| C11 | Power.SchDoc | C0603C200J5GACTU | 20 pF; 5%; 50 V; C0G | GW_CAND_0603_cap |
| C10 | Power.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R7 | Power.SchDoc | RC0603FR-0743K2L | 43.2 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| C12 | Power.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| J1 | Power.SchDoc | TB002-500-02BE | *; NOT_RECORDED; NOT_RECORDED | CUI_TB002-500-02BE |
| L2 | Power.SchDoc | XAL4040-103MEC | 10 uH; 20%; Isat25C 3.0 A; Irms20C 2.2 A | MISSING |
| U3 | Power.SchDoc | LMR36015FBRNXR | LMR36015FBRNXR; NOT_RECORDED; NOT_RECORDED | GW_RNX0012A_TI;GW_RNX0012B_TI |
| C15 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| C13 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| C14 | Power.SchDoc | C3225X7R1C156M250AB | 15 uF por unidad; 45 uF nominal banco; 20%; 16 V; X7R | MISSING |
| R9 | Power.SchDoc | RC0603FR-07100KL | 100 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| R8 | Power.SchDoc | RC0603FR-0743K2L | 43.2 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| C16 | Power.SchDoc | C0805C475K4RACTU | 4.7 uF; 10%; 16 V; X7R | GW_CAND_0805_cap |
| C17 | Power.SchDoc | C0805C224K1RACTU | 220 nF; 10%; 100 V; X7R | GW_CAND_0805_cap |
| C18 | Power.SchDoc | C0805C224K1RACTU | 220 nF; 10%; 100 V; X7R | GW_CAND_0805_cap |
| C20 | Power.SchDoc | C0603C200J5GACTU | 20 pF; 5%; 50 V; C0G | GW_CAND_0603_cap |
| C19 | Power.SchDoc | C0603C104K5RACTU | 100 nF; 10%; 50 V; X7R; -55..125 C | GW_CAND_0603_cap |
| C21 | Power.SchDoc | CL10A105KB8NNNC | 1 uF; 10%; 50 V; X5R; -55..85 C | GW_CAND_0603_cap |
| R10 | Power.SchDoc | RC0603FR-0724K9L | 24.9 kOhm; 1%; 75 V max; limite sqrt(P*R) | GW_CAND_0603_res |
| F1 | Power.SchDoc | 0451002.MRL | 0451002.MRL; NOT_RECORDED; NOT_RECORDED | MISSING |
| D2 | Power.SchDoc | TDS3011P.C | TDS3011P.C; NOT_RECORDED; NOT_RECORDED | GW_TDS3011P_SEMTECH |
| D1 | Power.SchDoc | SS3P6L-M3/86A | SS3P6L-M3_86A; NOT_RECORDED; NOT_RECORDED | MISSING |
| U1 | Power.SchDoc | TPS26620DRCR | TPS26620DRCR; NOT_RECORDED; NOT_RECORDED | MISSING |
| C2 | Power.SchDoc | C5750X7R2A475K230KA | 4.7uF10%100VX7R; NOT_RECORDED; NOT_RECORDED | MISSING |
| C1 | Power.SchDoc | C0805C224K1RACTU | 220nF10%100VX7R; NOT_RECORDED; NOT_RECORDED | MISSING |
| R1 | Power.SchDoc | RC0603FR-07768KL | 768kOhm1%0.1W75V; NOT_RECORDED; NOT_RECORDED | MISSING |
| R3 | Power.SchDoc | RC0603FR-0733K2L | 33.2kOhm1%0.1W75V; NOT_RECORDED; NOT_RECORDED | MISSING |
| C3 | Power.SchDoc | C0603C103K1RACTU | 10 nF; 10%; 100 V; X7R; -55..125 C | GW_CAND_0603_cap |
| R4 | Power.SchDoc | RC0603FR-0730K1L | 30.1kOhm1%0.1W75V; NOT_RECORDED; NOT_RECORDED | MISSING |
| R2 | Power.SchDoc | RC0603FR-0713K3L | 13.3kOhm1%0.1W75V; NOT_RECORDED; NOT_RECORDED | MISSING |

No duplicate designators among106. No variants defined; conditionalDNP status cannot be assumed. Full [component CSV](evidence/native_schematic_audit/component_inventory.csv), [pin membership](evidence/native_schematic_audit/nets.json), [saved metadata](evidence/native_schematic_audit/placed_metadata.json), [library pin comparison](evidence/native_schematic_audit/pin_library_comparison.csv), [findings CSV](evidence/native_schematic_audit/findings_initial.csv). Source model availability is not an instance model assignment. Exact selected-versus-placed quantities are in the datasheet inventory; missing connectors/buttons/ESD/bank capacitors must not be hidden by total component count.

## Actual compilation/ERC and triage

Native proj_run_erc returned success and proj_get_erc_violations returned 105 total violations reported; only100 detailed entries returned (15 errors/85 warnings). Five details were not exposed by the tool and remain untriaged. This compiles/checks the actual project; it is not a clean ERC. Baseline snapshot unconnected_pins count0 is misleading because named single-pin nets exist: counted compiled memberships explicitly instead. Native compile-age metadata was inconsistent (uncached with very large age); no SaveAll/force_recompile was used during Phase1. ERC was run after inspection and before correction. [Actual detailed violations](evidence/native_schematic_audit/erc.json). No DRC was run;PCB routing/manufacturing is outside this audit.

| ERC category | Disposition |
|---|---|
| Missing child sheet for sheet symbol | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Missing component models | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Nets containing floating input pins | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Nets with no driving source | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Nets with only one pin | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Nets with possible connection problems | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Off-grid object | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |
| Unconnected objects in net | See specific electrical findings; no blanket suppression. Off-grid/possible-connection/model warnings remain; unusedMCUGPIO/PHYpins are not automatic functional defects. |

## Minimal authorized correction batch

After saving this baseline, correct only A01(sharedSW),A03(disconnectedVIN/EN alias),A09(TXlabel),A12(SWCLK label). Exact operations: four Power ePowerObject SW strings split by converter toB3_SW/B5_SW;two Vin powerport strings→existing24V;Ethernet label at9600,5000 TX+→TX-;MCU SWCLK label→PA14 electrical coordinate6400,4000. These preserve architectural power/ground boundaries, component inventories and all other pins. Verify each affected pin table and unchanged neighbors,save onlyproject,independently read saved records,then compile/ERC. No sheet regeneration or automatic routing. Other findings require local part replacement/additional wiring or explicit ground-boundary approval; document manual steps if safe editing cannot be demonstrated.


## Post-audit validation supplement (baseline findings unchanged)

Four findings A01/A03/A09/A12 were corrected after this baseline was saved; see [controlled log](schematic_correction_log_rev1.md). Remaining23 findings are open. Independent source/instance comparison found435 of437 pin names and electrical types match the current source symbols; J1's2 pins have no corresponding project-local source symbol. This is source consistency, not proof of all manufacturer pin functions. Eighty placed model records were examined:78 have matching source pad-designator sets;J2 has two additional mechanical mounting pads MP1/MP2 (not an electrical mapping fault), and J1 source is unavailable in the project library. Matching pad sets alone do not verify dimensions, orientation or custom mapping. [Electrical-type comparison](evidence/native_schematic_audit/electrical_type_comparison.json), [pin/pad sets](evidence/native_schematic_audit/pin_pad_set_comparison.json). No new footprints were generated.

The native save regenerated437 pin UniqueIds while preserving component/model/electrical records; further native edits stopped. Fresh native connectivity after save matches the intended corrected table exactly. Current PCB transfer status remains NO-GO. [Datasheet inventory](datasheet_inventory_rev1.md) covers44 placed identities and6 additional concrete required-BOM MPNs; unknown connector/button identities remain separately listed, not invented.
