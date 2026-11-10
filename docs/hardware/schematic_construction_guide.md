# Academic Gateway Rev. 1 — manual schematic construction guide

Current baseline: **2026-11-08**. This is the primary construction reference for
manual drawing in Altium. Use the exact connections below and current
[BOM](final_bom.csv), [passive BOM](passive_bom.csv) and [CAD mapping](cad_library_mapping.csv).
Earlier recovery/qualification analysis is retained in [input_protection_reference.md](input_protection_reference.md)
sections1–9 and [the earlier readiness gate](schematic_readiness_gate.md); it does not
restore superseded selections. Source decisions and calculations are in input-reference
section 10, [TPS verification](evidence/tps26620/calculations.json) and
[academic freeze decisions](evidence/input_protection_freeze/bom_decisions.json).

Scope: supervised academic prototype; regulated, current-limited laboratory supply,
nominal24V,18–30V operating objective. No industrial certification gate is imposed.
Datasheet ratings, complete power connections and correct physical mapping still apply.
The user completes manual capture/placement/routing. This closure saved one localized Power-sheet wire/label repair; its compiled connectivity remains unverified. All other native findings below await local correction.

**Design selected** means a chosen architecture/MPN. **Schematic ready** means the
connections/passives are established (proposed TPS settings are identified explicitly).
**PCB ready** additionally requires verified lands, mapping and assembly implementation.
A saved candidate footprint is not PCB ready; no routed-board readiness is claimed.

| Subsystem | Selected design | Connection specification | Source CAD readiness | Native implementation dependency |
|---|---|---|---|---|
| Input |0451002.MRL/SS3P6L/TDS3311P/TPS26620|Defined,including RTN and startup|Connector resolved;TPS EP mapping candidate|Recompile saved UVLO repair;verify distinct UVLO/OVP|
|3.3V buck|LMR36015FBRNXR,6.8uH|Defined|RNX A/B/inductor/passive lands verified|NC3-to-SW;CIN/CVCC bank;DNP PG/CFF|
|5V buck|LMR36015FBRNXR,10uH|Defined|Same|Replace16V CIN before power;complete bank/CVCC|
|MCU|STM32H723VET6/internalLDO|Core/clock/boot/debug defined|MCU lands verified;exact SWD/BOOT headers saved;reset viaJ3|C30;one1uF/one100nF missing;BOOT model migration|
|Ethernet PHY/clocks|DP83826IRHBR + two independent Kyocera25MHz oscillators|RMII Leader and MCU bypass defined|PHY/clock/ESD/R/C source lands verified|Clock performance bringup;ESD flow-through/ECO;assembly review|
|Magnetics/RJ45|HX1188FNL/SS-7188S-A-NF|Defined;two separate chassis AC branches|Source lands/holes/orientation verified|Move cable-cap returns/shields toCHASSIS;mechanical envelope/edge placement|
|RS485|THVD1420DR/115200baud|Defined;end-only termination optional|Exact connector/header/120ohm model saved|Place/wire connector and optional jumper|
|CAN-FD|ATA6561-GAQW/1Mbit nominal,2Mbit data target|Defined|Same connector/termination resources|Place/wire connector;verify startup standby|
|Two DI|ISO1212DBQR/Type3|Defined;isolation unchanged|DBQ/Firstohm/connector source lands verified|Correct R21/R22 field-side connections;floating substrate islands|
|Two DO|BSP75NTA + two NPN/PMOS5V drivers|Defined with explicit engineering margin/bringup limits|BSP and new Diodes models verified|Migrate U9 locally;wire both BSPs and external supply/loads|

These are specification/library states,not a claim that the native sheets match them.
See [closure report](electrical_closure_rev1.md) and section15 for the actual remaining corrections.

Use project-local `hardware/academic_rev1/libraries/Gateway_Academic.SchLib` and
`.PcbLib` (saved readback: **76 symbols /48 footprints**). LibPkg source references remain project-local. Existing IntLib is stale and was not recompiled. File validation: SchLib0errors/0warnings; PcbLib0errors/4intentional TPS EP-subpad overlap warnings. No current native compilation,ERC,DRC,placement or electrical test is claimed. See [closure report](electrical_closure_rev1.md).

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

Ground/net policy: actual native **GND** is the common non-isolated electronics/source/DO return; GND_PWR describes its power-return role,not a separate isolated net. The native **24V** net is the protected electronics rail called24V_ELEC below; they must be one electrical net,never two disconnected aliases. Native **3.3V** is the logic rail;5V is separate. Keep existing flat-sheet ports consistent and verify compiled memberships after any label change. **EF_RTN** is a separate TPS reference (pins5/11);never short it toGND. **FIELD_COM** is the isolated DI return. **CHASSIS** is the RJ45 shield/cable-capacitor AC domain;no DC logic-ground bond is selected. External DO positive isDO_EXT_PLUS,not24V_ELEC. No ferrite/net-tie/impedance is added merely to rename grounds.

## 1. Single-input protection — current construction plan

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
Table 5/Table 6-1 p4 (variant/pins),Table 7.5 pp6–7,Eq 2 p18,Eq 5–7 p26,
Fig10-1 p25,§§9.3.8–9.4.1 pp23–24,§10.4 p32,DRC0010J pp43–45.
Diode: [Vishay88987](../../hardware/academic_rev1/libraries/sources/SS3P6L_88987.pdf),pp1/4.
Fuse: [Littelfuse land drawing](../../hardware/academic_rev1/libraries/sources/academic_freeze/fuse_manufacturer_drawing.pdf),printedp371.
TDS: [Semtech Rev2.4](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf),pp2,7–9;
local TDS3311 PDF is not claimed. Exact resistor/capacitor local links are in
[input reference section 10.5](input_protection_reference.md#105-sources-cad-readiness-and-actual-unfinished-work).

### C. Components to place

| BOM ID / quantity / function | MPN / value | Ratings / package | Symbol / footprint | Recorded electrical / CAD / population |
|---|---|---|---|---|
| IN_FUSE / 1 / Upstream physical fuse F1 | 0451002.MRL; 2 A | 125 VDC; Manufacturer fuse characteristic; Littelfuse451 SMD | `0451002.MRL` / `GW_0451_LITTELFUSE` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| IN_REVERSE / 1 / Bloqueo polaridad inversa | SS3P6L-M3/86A; 3 A Schottky | 60 V reverse; SMPC TO-277A | `SS3P6L-M3_86A` / `GW_SS3P6L_VISHAY_88987` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| IN_TVS / 1 / Supresion sobretension/transitorios | TDS3311P.C; 33 V working | 42 V maximum specified35A pulse; Manufacturer table; DFN6 1.6x1.6 | `TDS3311P.C` / `GW_TDS3311P_SEMTECH` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ACTIVE_TPS26620DRCR / 1 / Fixed architecture active specification | TPS26620DRCR | 4.5–60V; adjustable OV cutoff; latch-off; DRC10 + RTN EP | `TPS26620DRCR` / `GW_DRC0010J_TI_TPS2662` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| IN_RLIM / 1 / eFuse current-setting resistor | RC0603FR-0713K3L; 13.3 kOhm | 75 V; 1%; 0.1 W; 0603 | `RC0603FR-0713K3L` / `GW_RC0603_YAGEO_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_CDVDT / 1 / Optional eFuse slew capacitor | C0603C103K1RACTU; 10 nF | 100 V; X7R; 10%; 0603 | `C0603C103K1RACTU` / `GW_0603_KEMET_NOMINAL` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_UV_TOP / 1 / IN to UVLO divider top | RC0603FR-07768KL; 768 kOhm | 75 V; 1%; 0.1 W; 0603 | `RC0603FR-07768KL` / `GW_RC0603_YAGEO_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_UV_MID / 1 / UVLO to OVP divider middle | RC0603FR-0733K2L; 33.2 kOhm | 75 V; 1%; 0.1 W; 0603 | `RC0603FR-0733K2L` / `GW_RC0603_YAGEO_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_UV_BOTTOM / 1 / OVP to EF_RTN divider bottom | RC0603FR-0730K1L; 30.1 kOhm | 75 V; 1%; 0.1 W; 0603 | `RC0603FR-0730K1L` / `GW_RC0603_YAGEO_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_BULK / 1 / TPS26620 local input bypass | C5750X7R2A475K230KA; 4.7 uF | 100 V X7R; 10%; 2220 | `C5750X7R2A475K230KA` / `GW_C5750_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| IN_HF / 1 / TPS26620 input high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V X7R; 10%; 0805 | `C0805C224K1RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| IN_J / 1 / Conector entrada | TB002-500-02BE; 2 poles;5mm pitch | UL300V15A;IEC250V17.5A;academic circuit limits lower; TBD; TB002-500 2P TH | `TB002-500-02BE` / `GW_TB002_500_2P_SAMESKY` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| IN_RFAULT / 0 / FAULT pull-up | RC0603FR-0715KL; 15.0 kOhm | 75 V; 1%; 0.1 W; 0603 | `RC0603FR-0715KL` / `GW_RC0603_YAGEO_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; DNP |
| IN_SOUT / 0 / Reserved output-clamp footprint | SS3P6L-M3/86A; DNP negative-output clamp option | 60 V reverse; SMPC TO-277A | `SS3P6L-M3_86A` / `GW_SS3P6L_VISHAY_88987` | ELECTRICAL_VERIFIED; CAD_VERIFIED; DNP |

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
| TPS1 IN | VIN_CLAMP;4.7µF100V +220nF100V input bypass to GND_PWR/pin 6 |
| TPS2 UVLO | Junction of768kΩ from pin 1 and33.2kΩ to pin 3 |
| TPS3 OVP | Junction of33.2kΩ from pin 2 and30.1kΩ to EF_RTN |
| TPS4 SHDN_N | Open using internal weak pull-up/default enable; intentional NC. No24V tie |
| TPS5 RTN | EF_RTN; support-component returns; independently connected, not through EP only |
| TPS6 GND | GND_PWR, source/electronics return |
| TPS7 ILIM |13.3kΩ to EF_RTN |
| TPS8 dVdT |10nF to EF_RTN; populated, not the old NIS68pF option |
| TPS9 FLT_N | Unused/open with NC; no selected buck-EN/MCU fault connection |
| TPS10 OUT |24V_ELEC, both buck input banks |
| TPS11 RTN_EP | Solder EP to EF_RTN copper, not system ground |

Ladder order is exactly **IN—768k—UVLO—33.2k—OVP—30.1k—RTN**.
Never connect RTN/support components to GND_PWR. Never connect VCAP/3.3V/5V to RTN.
TPS26620 has **adjustable OV cutoff and overload/thermal latch-off**, not auto-retry
or the fixed-clamp behaviour of other variants. After removing a fault, reset by
cycling SHDN, UVLO or input power. Unused SHDN stays open; supervised input cycling
is the selected reset method. Buck EN pins remain tied to24V_ELEC, not FLT.

### E. Values, acceptance and remaining practical work

`I_LIMIT=6.636/13.3=0.49895A`; TI Table 7.5 gives0.47/0.50/0.52A at13.3kΩ
under its stated conditions, before resistor tolerance. The approximately0.217A
electronics budget (about0.218A with TPS screening losses) excludes external DO loads.
62kΩ is not reused: it would give only about0.107A by this equation.

| Threshold at IN relative RTN | Typical calculated value |
|---|---:|
| UVLO rising / enable |15.759V|
| UVLO falling / disable |14.446V|
| OVP rising / cutoff |33.142V|
| OVP falling / recovery |30.932V|

Total ladder831.3kΩ. Equations6/7 use Table 7.5's1.20V rising typical rather than
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

**TPS source CAD:** original `GW_DRC0010J_TI_TPS2662` remains a candidate because its four copper extensions have no proven pad-net inheritance. New `GW_DRC0010J_TI_TPS2662_EP11` has real central pad11 and aliases11A/11B/11C/11D;the union matches TI p44. Before binding it,Altium must map **one symbol pin11 to all five pads**,allEF_RTN,and verify that ECO/net readback transfers that net. Aliases are geometry segments,not extra manufacturer pins. Four overlap warnings are intentional only for this common-net construction. Do not use default1:1mapping. Existing symbol stays bound to the original candidate until that check. Alternative:make one native custom pad11 of the exact union. TI windowed paste is retained;thermal vias need explicit assembler treatment. Input connector is nowTB002-500-02BE,pin1positive/pin2GND by project convention;see section15.

Altium documents net inheritance for footprint routing primitives touching a mapped pad. Therefore first test the **existing**footprint in an isolatednativeECO:if allfourextensions acquireEF_RTN,no replacement is needed. This is a transfer-verification hold,not missing manufacturer dimensions or proof that the footprint is defective. For the alternate segmentedfootprint,PCBModel >PinMap >symbol11 >ModelPinDesignator uses `11,11A,11B,11C,11D`;keep allotherpins1:1. Altium21+ supports onepin-to-multiplepads;confirm actualECO/readback. [Official routing-primitive net behavior](https://www.altium.com/documentation/altium-designer/components-libraries/creating-pcb-footprint);[file-library PinMap procedure](https://www.altium.com/documentation/altium-designer/components-libraries/file-based-libraries/schematic).

### F. Construction verification

- [ ] F1 series, D_REV both anodes present, TDS shunt after diode.
- [ ] TPS pin 5 and EP11 on EF_RTN; pin 6 on GND_PWR; no external short between them.
- [ ]13.3kΩ pin 7-to-RTN;10nF pin 8-to-RTN; three-resistor ladder order correct.
- [ ] Local input bypass returns to GND_PWR; both buck input banks retained.
- [ ] FLT and SHDN intentionally open; latch-off/manual-reset behaviour recorded.
- [ ] Protected24V_ELEC feeds electronics only; DO supply and FIELD_COM stay separate.
- [ ] TPS pad-net transfer remains a native verification task;inputconnector1=positive/2=GND is defined in section15.


### G. Required net labels

VIN_FUSED,VIN_CLAMP,24V_ELEC,EF_RTN,GND_PWR; no VIN_PROT alias.

## 2. LMR36015FBRNXR 3.3-V buck.

### A. Selected configuration

Selected LMR36015FBRNXR,1MHz FPWM,6.8µH XAL4030-682MEC,100kΩ/43.2kΩ feedback;
3.3V allocation0.7A. Input and EN use **24V_ELEC** from TPS.
PG unused; no FLT-driven enable. Prototype capacitor network is now selected:
2×4.7µF100V CIN,2×220nF100V HF,1×2.2µF50V CVCC,1×100nF CBOOT,
3×15µF16V COUT. CFF20pF is conditional/DNP; no added damping bulk selected.
Capture can proceed; physical RNX/stencil and functional bring-up checks remain.

### B. Official manufacturer sources

- Main datasheet: `DS/lmr36015.pdf`, **SNVSB49D**, [TI LMR36015](https://www.ti.com/lit/ds/symlink/lmr36015.pdf). Use the pinned local revision for these locators: **Device Comparison Table p3**, **Figure 7-1 and Pin Functions p4**.
- Reference schematic: **Figure 10-1 p19**, and the **1000-kHz / 3.3-V row of Table 10-1 p19**. It gives 6.8 uH, nominal 3 x 15 uF COUT, 100 k/43.2 k, 4.7 uF plus 2 x 220 nF CIN, starting CFF 20 pF. It is an application example, not proof of our capacitor bank or layout.
- Application guidance within this datasheet: **section 10.1 p18** (effective capacitance unless stated otherwise); **10.2.1.2.2-.3 p20**, **equations 3-5 p21**; **10.2.1.2.5 pp21-22** (COUT/transients); **10.2.1.2.6-.9 p23** (CIN, CBOOT, CVCC, CFF); **10.2.1.2.10 p25** (thermal); **section 11 p33**. No separate buck application note/EVM is adopted as the final circuit. The datasheet's Figure 10-1 is the selected reference schematic.
- PCB guidance: **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**; RNX0012A package/board/stencil drawing **PDF pp44-46**, RNX0012B **pp47-49**. Both A/B copper/mask/stencil patterns were independently compared with the saved feet2026-11-08. The package lot and assembler process must match the selected variant.
- Inductor datasheet/layout: `EC/xal4000.pdf`, Coilcraft **document 806 Rev02/25/26**, **p1** XAL4030-682MEC row, **p4** Recommended Land Pattern and marked-end guidance. The 25-C typical saturation criterion is not a hot guarantee.
- Later source closure: [TDK exact input sheet](../../hardware/academic_rev1/libraries/sources/academic_freeze/TDK_exact.pdf),p1lands/p2bias, and [academic capacitor decisions](evidence/input_protection_freeze/bom_decisions.json) supersede the earlier403/missing-land statements. Output lands and exact saved model bindings are in the current mapping.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_LMR36015FBRNXR / 1 / 3.3-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_L / 1 / power inductor | XAL4030-682MEC; 6.8 uH | Isat25C 3.6 A; Irms20C 3.0 A; 20%; XAL4030 | `XAL4030-682MEC` / `GW_XAL4030_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| B3_CIN / 2 / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF | 100 V X7R; 10%; 2220 | `C5750X7R2A475K230KA` / `GW_C5750_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V X7R; 10%; 0805 | `C0805C224K1RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF | 16 V X7R; 20%; 1210 | `C3225X7R1C156M250AB` / `GW_C3225_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| B3_CVCC / 1 / local supply bypass | C0805C225K5RACTU; 2.2 uF | 50 V X7R; 10%; 0805 | `C0805C225K5RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_RFBB / 1 / lower feedback resistor | RC0603FR-0743K2L; 43.2 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0743K2L_a8308c0c` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; CONDITIONAL |
| B3_CDAMP / TBD / conditional input damping bulk | TBD; TBD | TBD; TBD; TBD | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |

Use the exact linked inductor and new exact-MPN capacitor symbols in the table.
Each CIN4.7µF part has about3.6µF on the saved30V bias curve; two give about6.48µF
after a10% allowance, supporting the4.7µF effective prototype target. CVCC is now
KEMET2.2µF50V X7R, not the former Samsung1µF part with0.656µF at5V. The selected
prototype assumption of60% retention and−10% tolerance gives1.188µF; confirm VCC
startup/ripple during bring-up. COUT45µF is **rated**, not effective capacitance
or a guarantee of stability. Keep CFF DNP unless application review selects it.

### D. Connection checklist

| IC pin | Required connection |
|---|---|
| 1 PGND | GND; local return of one VIN/HF-capacitor pair. |
| 2 VIN | 24V_ELEC; main CIN to GND and one local 220-nF bypass to PGND1. |
| 3 NC | Externally connect to **SW12**, per TI; not a generic leave-open NC. |
| 4 BOOT | 100 nF to SW, using the short SW3/12 connection. Never to GND. |
| 5 VCC | Dedicated `B3_VCC_INTERNAL`; qualified CVCC to GND. Internal nominal 5-V LDO output; no external load or tie to the 5-V buck rail. |
| 6 AGND | System GND; quiet FB-divider/CVCC reference. Preserve short local return, not an isolated floating ground. |
| 7 FB | Junction of RFBT 100 k from **3.3V after the inductor** and RFBB 43.2 k to AGND/GND. Neither VIN nor SW is the sense point. |
| 8 PG | Unused/open, deliberately marked NC. No pull-up is populated in this selected circuit. |
| 9 EN | 24V_ELEC directly; do not float. No external 18-V UVLO network selected. |
| 10 VIN | 24V_ELEC; second local 220-nF bypass to PGND11. |
| 11 PGND | GND and short local HF return. |
| 12 SW | XAL4030-682MEC switching end and NC3/CBOOT return. **Not a ground exposed pad.** |

Project inductorpin1(marked/shorted winding end) goes toSW;pin2 -> `3.3V`; three selected 15-uF COUT parts -> GND there. Optional CFF 20 pF, if later approved, goes **across RFBT**, output-to-FB. Main CIN bank is independent of the 5-V converter and must provide >=4.7 uF effective over actual bias/temperature. Table 10-1's **COUT columns explicitly say RATED CAPACITANCE**: retain 3 x 15 uF nominal without claiming 45 uF effective. Export `3.3V`/`GND` to MCU, PHY, RS-485, CAN VIO, ISO logic, oscillator supplies and MCU/DI/PHY logic. No output-enable/reset/boot pin exists on this regulator beyond EN; do not invent one.

### E. Remaining practical work

- Capture values/quantities are selected; no missing CIN count or CVCC replacement gate remains.
- RNX A/B terminal positions agree. Saved A uses solder-mask-defined copper for1/2/10/11/12;B uses the preferred NSMD pattern. Confirm purchased package and assembler mask/stencil capability;neither SW12 nor NC3 is ground.
- At bring-up verify eFuse/buck startup, VCC, rail ripple/load steps and temperature under the stated allocations. This is functional confirmation, not industrial qualification.

### F. Review checklist

- [ ] Exact FBRNXR identity matches 1-MHz FPWM, not a similarly named non-FPWM part.
- [ ] SW12 and NC3 are connected; neither is on GND.
- [ ] BOOT capacitor is BOOT-to-SW and VCC capacitor is VCC-to-GND.
- [ ] Internal VCC is neither externally loaded nor merged with the system 5-V rail.
- [ ] Divider is 100 k/43.2 k, sensed after the 6.8-uH inductor.
- [ ] Both opposite VIN/PGND pairs have their own 220-nF bypass.
- [ ] CIN has two4.7µF parts; COUT is three15µF rated parts; CVCC is selected2.2µF50V.
- [ ] CFF/PG/UVLO positions match selected population; no guessed pull-up or divider.
- [ ] Current, fault and thermal assumptions are recorded without claiming 1.5-A board capacity from IC rating alone.


### G. Required net labels

24V_ELEC,3.3V,B3_SW (pins3/12/BOOT return),B3_VCC_INTERNAL, B3_FB (pin 7),GND_PWR/GND.

## 3. LMR36015FBRNXR 5-V buck.

### A. Selected configuration

Selected LMR36015FBRNXR,1MHz FPWM,10µH XAL4040-103MEC,100kΩ/24.9kΩ feedback;
5V allocation0.1A. Input and EN use **24V_ELEC** from TPS.
PG unused; no FLT-driven enable. Prototype capacitor network is now selected:
2×4.7µF100V CIN,2×220nF100V HF,1×2.2µF50V CVCC,1×100nF CBOOT,
3×15µF16V COUT. CFF20pF is conditional/DNP; no added damping bulk selected.
Capture can proceed; physical RNX/stencil and functional bring-up checks remain.

### B. Official manufacturer sources

- `DS/lmr36015.pdf`, TI **SNVSB49D**, [official datasheet](https://www.ti.com/lit/ds/symlink/lmr36015.pdf): **Device Comparison Table p3**, **Figure 7-1/Pin Functions p4**, **Figure 10-1/Table 10-1 p19**, specifically **1000 kHz / 5 V** (10 uH, 100 k/24.9 k, nominal 3 x 15 uF).
- Application guidance: **section 10.1 p18**, **10.2.1.2.2-.3 p20**, **equations 3-5 p21**, COUT **pp21-22**, CIN/CBOOT/VCC/CFF **sections 10.2.1.2.6-.9 p23**, thermal **10.2.1.2.10 p25**, source/damping **section 11 p33**. Figure 10-1 is the reference schematic; no separate adopted EVM/application note is needed to infer a different mode.
- Layout: **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**, RNX A/B **PDF pp44-49**, as in section 2.
- `EC/xal4000.pdf`, Coilcraft document 806 Rev02/25/26, **p1 XAL4040-103MEC**, **p4** lands/marked winding end. TDK characterization/mounting files remain unavailable as detailed in section 2; do not invent curve/page references.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_LMR36015FBRNXR / 1 / 5-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_L / 1 / power inductor | XAL4040-103MEC; 10 uH | Isat25C 3.0 A; Irms20C 2.2 A; 20%; XAL4040 | `XAL4040-103MEC` / `GW_XAL4040_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| B5_CIN / 2 / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF | 100 V X7R; 10%; 2220 | `C5750X7R2A475K230KA` / `GW_C5750_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V X7R; 10%; 0805 | `C0805C224K1RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF | 16 V X7R; 20%; 1210 | `C3225X7R1C156M250AB` / `GW_C3225_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| B5_CVCC / 1 / local supply bypass | C0805C225K5RACTU; 2.2 uF | 50 V X7R; 10%; 0805 | `C0805C225K5RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_RFBB / 1 / lower feedback resistor | RC0603FR-0724K9L; 24.9 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0724K9L_10698e9e` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; CONDITIONAL |
| B5_CDAMP / TBD / conditional input damping bulk | TBD; TBD | TBD; TBD; TBD | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |

Use the exact linked inductor and new exact-MPN capacitor symbols in the table.
Each CIN4.7µF part has about3.6µF on the saved30V bias curve; two give about6.48µF
after a10% allowance, supporting the4.7µF effective prototype target. CVCC is now
KEMET2.2µF50V X7R, not the former Samsung1µF part with0.656µF at5V. The selected
prototype assumption of60% retention and−10% tolerance gives1.188µF; confirm VCC
startup/ripple during bring-up. COUT45µF is **rated**, not effective capacitance
or a guarantee of stability. Keep CFF DNP unless application review selects it.

### D. Connection checklist

| IC pin | Required connection |
|---|---|
| 1 PGND | GND/local return of VIN2 HF capacitor. |
| 2 VIN | 24V_ELEC, main local CIN and 220 nF to PGND1. |
| 3 NC | Externally join SW12. |
| 4 BOOT | 100 nF to SW3/12; no ground connection. |
| 5 VCC | Dedicated `B5_VCC_INTERNAL` with qualified CVCC to GND; **not system 5V**, not B3 VCC. |
| 6 AGND | GND, quiet lower-feedback/CVCC return. |
| 7 FB | 100 k from 5V output to FB; 24.9 k from FB to AGND/GND. |
| 8 PG | Unused/open with explicit NC. |
| 9 EN | 24V_ELEC; no divider or MCU drive selected. |
| 10 VIN | 24V_ELEC and second 220-nF bypass to PGND11. |
| 11 PGND | GND/local HF return. |
| 12 SW | XAL4040-103MEC switching end, BOOT-capacitor return and NC3; never GND. |

Project inductorpin1(marked/shorted winding end) goes toSW;pin2 -> `5V`; three selected 15-uF COUT to GND there. If later populated, 20-pF CFF parallels RFBT. Export `5V`/`GND` to CAN VCC and provisional translator VCCB. Maintain independent CIN/HF/VCC/BOOT banks and separate switching-node names for both converters. No buck oscillator synchronization pin or external frequency-setting network is selected.

### E. Remaining practical work

- Capture values/quantities are selected; no missing CIN count or CVCC replacement gate remains.
- RNX A/B terminal positions agree. Saved A uses solder-mask-defined copper for1/2/10/11/12;B uses the preferred NSMD pattern. Confirm purchased package and assembler mask/stencil capability;neither SW12 nor NC3 is ground.
- At bring-up verify eFuse/buck startup, VCC, rail ripple/load steps and temperature under the stated allocations. This is functional confirmation, not industrial qualification.

### F. Review checklist

- [ ] RFBB is **24.9 k**, not the 3.3-V sheet's 43.2 k.
- [ ] Inductor is **10 uH XAL4040**, using the linked exact symbol.
- [ ] SW3/12, BOOT4, VCC5 and GND pins are not interchanged.
- [ ] B3/B5 internal VCC and switching nodes remain separate from each other and system rails.
- [ ] Independent VIN decoupling includes two 220-nF HF parts.
- [ ] CVCC is2.2µF50V X7R; confirm the stated prototype retention assumption at bring-up.
- [ ] COUT and CFF population reflect conditional qualification, not nominal-only stability approval.
- [ ] The 5-V output powers CAN and the new DO input drivers, not the 0.5-A field loads.


### G. Required net labels

24V_ELEC,5V,B5_SW,B5_VCC_INTERNAL,B5_FB,GND_PWR/GND; never join B3/B5 internal nets.

## 4. STM32H723VET6 minimum hardware.

### A. Selected configuration

**ACCEPTED:** exact LQFP100 STM32H723VET6, internal LDO, 3.3-V VDD/VDDA/VREF+/VBAT, no backup battery, VREFBUF disabled; SWD, NRST, BOOT0 pull-down/recovery. **ACCEPTED topology / PROVISIONAL qualification:** its own KC2016Z25.0000C15XXK 25-MHz oscillator to PH0 in HSE bypass, PH1 unconnected; second independent oscillator belongs to PHY. PHY supplies the separate 50-MHz RMII reference to PA1. No shared oscillator fan-out is approved.

Exact source: gate **MCU connections and clock boundary**, BOM `MCU_*`, [capture_pin_bindings.csv](evidence/electrical_closure/capture_pin_bindings.csv) and [mcu_pin_reference.csv](../../hardware/academic_rev1/mcu_pin_reference.csv). Bindings reserve pins; this guide verifies AF choices without modifying firmware or approving a CPU/PLL frequency.

### B. Official manufacturer sources

- Main datasheet: `DS/DS_stm32h723zg.pdf`, ST **DS13313 Rev5**. The filename does not select a Z-package: use **Figure 5 p54**, **Table 7 pp57-71 LQFP100 column**, **Table 8 pp72-85** alternate functions; **Table 14 p92** VCAP; **Table 31 p111** HSE bypass. LQFP100 land pattern **Figure 65 printed p218 / PDF p219**.
- Relevant application note/reference schematics: [ST AN5419 Rev3](https://www.st.com/resource/en/application_note/an5419-getting-started-with-stm32h723733-stm32h725735-and-stm32h730-mcu-hardware-development-stmicroelectronics.pdf), **Table 2 pp7-8**, **Figure 3 p9** supply layout, **Figure 15 p20** reset, **section 3.1.1 p25** HSE bypass, **Figure 19 p30** boot, **section 6 pp31-33** debug. These are family diagrams: do not transfer absent SMPS/USB power pins or a different debug connector to LQFP100.
- Layout: AN5419 **section 7**, **Figure 22 p34** VDD/VSS layout; package-specific decoupling/VCAP rules above.
- Clock specification: `EC/KC2016Z25.0000C15XXK_e.pdf`, Kyocera **TNY1T-H1-DEX01-11**, **pp3-4** electrical/load/startup limits, **Table 2 p4**, **Figure 4 p6** terminal/land map and local **10-nF** bypass guidance. Exact nominal passive sheets are `SRC/passives/<MPN>.pdf`, except Samsung's retained HTML characterization; exact header drawings are referenced in section15;onboardNRST button is optionalDNP.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_STM32H723VET6 / 1 / LQFP100 MCU | STM32H723VET6 | 3.3-V selected supply; DS supply/voltage-scale/temperature limits; internal LDO | `STM32H723VET6` / `GW_LQFP100_ST_1L` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDD1 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDD2 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDD3 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDD4 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDD5 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CBULK / 1 / local bulk reserve | C0805C475K4RACTU; 4.7 uF | 16 V; X7R; 10%; 0805 | `GW_C0805C475K4RACTU_82374e08` / `GW_0805_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDDA1 / 1 / VDD local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_SAMSUNG_CL10_1608_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVDDA2 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVBAT1 / 1 / backup-supply bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_SAMSUNG_CL10_1608_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVBAT2 / 1 / backup-supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVREF1 / 1 / reference bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_SAMSUNG_CL10_1608_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVREF2 / 1 / reference bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVCAP1 / 1 / internal-LDO output capacitor | C0603C225K8RACTU; 2.2 uF | 10 V; X7R; ESR <100 mOhm; 10% candidato; ST permite 20%; 0603 | `GW_C0603C225K8RACTU_46503424` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CVCAP2 / 1 / internal-LDO output capacitor | C0603C225K8RACTU; 2.2 uF | 10 V; X7R; ESR <100 mOhm; 10% candidato; ST permite 20%; 0603 | `GW_C0603C225K8RACTU_46503424` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_CNRST / 1 / reset filter | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_RBOOT / 1 / BOOT0 pull-down | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| MCU_YHSE / 1 / MCU independent oscillator | KC2016Z25.0000C15XXK; 25 MHz active CMOS | 1.71..3.63 V supply; 3.3 V selected; load <=15 pF; total +/-30 ppm; 2.0x1.6 mm 4-pad | `KC2016Z25.0000C15XXK` / `GW_KC2016Z_KYOCERA` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| MCU_JSWD / 1 / six-position debug header | 61300611121; 6-position unkeyed custom SWD | See manufacturer source; TBD; 6x1 2.54mm TH | `61300611121` / `GW_WRPHD_6X1_254_WURTH` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| MCU_SRESET / 0 / normally-open reset button | TBD; SPST-NO | TBD; TBD; TBD | `GW_Sw_PUSH_4.5x4.5x5.0xmm_0f078dd9` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; DNP |
| MCU_JBOOT / 1 / boot recovery access | 61300211121; 2-position BOOT recovery | See manufacturer source; TBD; 2x1 2.54mm TH | `61300211121` / `GW_WRPHD_2X1_254_WURTH` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| MCU_COSC / 1 / oscillator bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |

CSV electrical statuses remain provisional for several nominal capacitors despite accepted connection functions. C0603C225K8RACTU VCAP capacitors require **ESR <100 mOhm** and application capacitance qualification. Samsung X5R parts are specified only to +85 C; do not infer that the conservative MCU current budget authorizes a hotter board. Header MPNs/hole patterns and project pin assignments are explicit. The unverified onboardNRST button placeholder isDNP;NRST is accessible at J3.4 and adjacentGND atJ3.5. Replace the existing BOOT SW1 locally with the verifiedBOOT header. The 10-k Yageo pull-down replaces the historical unqualified FOJAN identity. Crystal capacitors/resistor and LSE networks are DNP; no external analog ferrite is selected.

### D. Connection checklist

| LQFP100 pin(s) | Required connection |
|---|---|
| 11, 27, 50, 75, 100 VDD | 3.3V; separate 100-nF local bypass at each pin, plus selected 4.7-uF bulk. |
| 10, 26, 49, 74, 99 VSS | GND. All five must be connected. |
| 21 VDDA; 19 VSSA | VDDA to 3.3V analog branch; VSSA to GND. 1 uF + 100 nF from VDDA to its ground reference. No unselected ferrite inserted. |
| 20 VREF+ | VDDA/3.3V analog branch with its 1 uF + 100 nF bank; VREFBUF disabled. No independent VREF- pin is invented. |
| 6 VBAT | VDD/3.3V with selected 1 uF + 100 nF; no battery. |
| 48, 73 VCAP | Internal-core LDO output domain, joined as the selected VCAP net with one local 2.2-uF-to-GND at each pin. No external load; never connect to 3.3V. |
| 14 NRST | 100 nF to GND, SWD reset access. Optional onboard reset button isDNP;use debugger or a momentary externalcontact betweenJ3.4(NRST) andJ3.5(GND). Internal reset pull-up is used; no extra external pull-up selected. |
| 94 BOOT0 | 10 kOhm to GND and recovery access to 3.3V. BOOT header1=BOOT0,2=3.3V,normally open;never short3.3V directly toGND. Commission boot option bytes. |
| 12 PH0/OSC_IN | MCU oscillator OUT3; HSE bypass. |
| 13 PH1/OSC_OUT | Explicit NC in bypass configuration. |
| 72 PA13; 76 PA14 | SWDIO bidirectional and SWCLK input from debugger; reserve debug function. |

MCU oscillator: **1 STANDBY -> 3.3V; 2 GND -> GND; 3 OUT -> PH0 pin 12; 4 VCC -> 3.3V**, 10 nF directly between 4/2. No crystal load capacitors. HSI provides initial boot while the oscillator starts (specified up to 5 ms).

Debug header J3 is the **actual project-specific six-pin convention**: **1SWDIO,2GND,3SWCLK,4NRST,5GND,6VTref=3.3V sense**. This supersedes the older guide pin order;the existing user wiring is retained. Exact header `61300611121` / `GW_WRPHD_6X1_254_WURTH`;pin1 is the marked end,sequence+X in PCB TOP view. This is an unkeyed1x6 header,not the ARM standard. Wire the adapter to this table;VTref must not inject power. BOOT recovery header `61300211121`:pin1BOOT0,pin2=3.3V;normally OPEN,10k BOOT0-to-GND retained. SW1 currently performs BOOT recovery,not NRST reset;do not populate both a permanent boot shunt and a reset button under the same identity.

**Peripheral reservation and conflict check against this exact package:** Table 7 proves the package pins; Table 8 gives the AF below. Directions are from the MCU. No selected pin is assigned twice. Alternative functions sharing those pads remain disabled.

| MCU pin / pad | Selected role and direction | AF / verified Table 8 page | Other sheet endpoint |
|---|---|---|---|
| PA1 / 23 | ETH_RMII_REF_CLK input, 50 MHz | AF11 / p72 | PHY19 output; never PH0 |
| PA2 / 24 | ETH_MDIO bidirectional | AF11 / p72 | PHY11 |
| PC1 / 16 | ETH_MDC output | AF11 / p76 | PHY12 |
| PA7 / 31 | ETH_RMII_CRS_DV input | AF11 / p72 | PHY18 |
| PC4 / 32 | ETH_RMII_RXD0 input | AF11 / p76 | PHY16 |
| PC5 / 33 | ETH_RMII_RXD1 input | AF11 / p76 | PHY15 |
| PB11 / 47 | ETH_RMII_TX_EN output | AF11 / p75 | PHY23 |
| PB12 / 51 | ETH_RMII_TXD0 output | AF11 / p75 | PHY24 |
| PB13 / 52 | ETH_RMII_TXD1 output | AF11 / p75 | PHY25 |
| PD8 / 55 | USART3_TX output | AF7 / p78 | THVD4 D |
| PD9 / 56 | USART3_RX input | AF7 / p79 | THVD1 R |
| PD10 / 57 | RS485_DE output | GPIO, not USART3_CK / p79 | THVD3 |
| PD11 / 58 | RS485_nRE output | GPIO, not USART3_CTS/NSS / p79 | THVD2 |
| PD0 / 81 | FDCAN1_RX input | AF9 / p78 | ATA4 RXD |
| PD1 / 82 | FDCAN1_TX output | AF9 / p78 | ATA1 TXD |
| PE7 / 37 | CAN_STBY output | GPIO | ATA8 |
| PE4 / 3; PE5 / 4 | DI1/DI2 logic inputs | GPIO | ISO4/5 |
| PE6 / 5 | PHY_nRESET output | GPIO | PHY32, dedicated reset |
| PE2 / 1; PE3 / 2 | DO1/DO2 reservations only | GPIO; discrete5V driver selected | Channel1/2 base resistor,section10 |

PD10 is **not** USART3 hardware DE: the alternate function there is USART3_CK. PD11 is not an active UART flow-control input in this design. USART3 hardware RTS/CTS/synchronous clock are not selected. Keeping UART3 on PD8/9 avoids PB11/12/13 Ethernet conflicts. FDCAN1 is PD0/1, not the FDCAN2 functions on PB12/13. Do not enable MII, FMC, LCD, OCTOSPI or trace functions over reserved pads. PHY-facing MCU pins must remain HiZ through strap sampling; dedicated reset and initial clock sequencing require firmware review.

Remaining unused package pads (source Table 7; no new GPIO assignments): PC13 (7); PC14 (8); PC15 (9); PC0 (15); PC2_C (17); PC3_C (18); PA0 (22); PA3 (25); PA4 (28); PA5 (29); PA6 (30); PB0 (34); PB1 (35); PB2 (36); PE8 (38); PE9 (39); PE10 (40); PE11 (41); PE12 (42); PE13 (43); PE14 (44); PE15 (45); PB10 (46); PB14 (53); PB15 (54); PD12 (59); PD13 (60); PD14 (61); PD15 (62); PC6 (63); PC7 (64); PC8 (65); PC9 (66); PA8 (67); PA9 (68); PA10 (69); PA11 (70); PA12 (71); PA15 (77); PC10 (78); PC11 (79); PC12 (80); PD2 (83); PD3 (84); PD4 (85); PD5 (86); PD6 (87); PD7 (88); PB3 (89); PB4 (90); PB5 (91); PB6 (92); PB7 (93); PB8 (95); PB9 (96); PE0 (97); PE1 (98). Leave them unwired with explicit unused handling; firmware should select a defined low-power/analog state as appropriate, preserving SWD, oscillator and boot reservations. Do not add SMPS, VDDLDO, VDD50USB or VDD33USB pins absent from this package.

### E. Open engineering decisions

- **Does not prevent core initial capture:** VCAP ESR/bias and other capacitor effective values; MCU oscillator complete <=15-pF receiver/route/pad/probe budget. Clock startup/PLL/voltage-scale configuration is not implemented or approved here.
- **Prevents exact accessory completion:** reset-switch contact numbering/footprint, SWD/boot MPNs and orientation. Keep NRST and boot recovery accessible in the drawing; do not invent physical pairings.
- **Final electrical/physical approval:** rail/reset startup including PHY hold/release, BOOT option bytes, actual temperature/copper and decoupling geometry. PHY phase noise concerns the separate PHY oscillator; it does not block MCU power/debug capture.

### F. Review checklist

- [ ] Exactly the five VDD/five VSS pins and VDDA/VSSA/VREF+/VBAT are connected for LQFP100.
- [ ] VCAP48/73 have two local 2.2-uF parts, no 3.3V connection and no external load.
- [ ] Each VDD has its own bypass; analog/backup/reference banks are not silently omitted.
- [ ] PH0 receives its own 25-MHz CMOS oscillator; PH1 and crystal-load parts are unused.
- [ ] PHY's 50 MHz reaches PA1, without merging with the HSE net.
- [ ] AF11 RMII, PD8/9 AF7 and PD0/1 AF9 agree with the table; PD10/11 stay GPIO.
- [ ] BOOT0 is pulled low with recovery access; NRST filter/debug access remains usable.
- [ ] SWD header is labelled with its project pinout, VTref sense and mating orientation hold.
- [ ] No missing MCU package power pins have been inferred from a different STM32 variant.
- [ ] Blocked DO ports remain reservations, and PHY pads remain HiZ during bootstrap sampling.


### G. Required net labels

3.3V,GND,VCAP,NRST,BOOT0,SWDIO,SWCLK,MCU_HSE25 plus the peripheral reservation labels in the table.

## 5. DP83826I Ethernet PHY and clock.

### A. Selected configuration

**ACCEPTED:** DP83826IRHBR, ENHANCED mode, RMII **Leader**, PHY address 0, autonegotiation and Auto-MDIX; pin 19 outputs 50 MHz to MCU PA1. Independent 25-MHz KC2016Z oscillator drives XI9. **PROVISIONAL qualification:** oscillator load/phase noise, reset/ramp timing and physical layout. Basic connectivity is CONDITIONAL GO.

Exact source: gate **Ethernet - one complete termination implementation** and **MCU connections and clock boundary**; BOM `ETH_Y25`, `ETH_COSC`, `ETH_RRMII`, `ETH_CEXT`, `ETH_RBIAS` and local supply banks. Neither a shared oscillator nor RMII Follower/50-MHz input is selected.

### B. Official manufacturer sources

- `DS/dp83826i.pdf`, TI **SNLS647I**, [official datasheet](https://www.ti.com/lit/ds/symlink/dp83826i.pdf): **Table 5-1 pp5-6**, **p7** ground/EP; **section 7.6 pp15-17** clock/reset/ramp timing; **section 8.3.10 pp32-33**, especially **Figure 8-7 p33 RMII Leader**. Figures 8-5/8-6 describe Follower and are not our clock connections.
- Straps: **Figure 8-12/Table 8-6 p48**, **Figure 8-13/Table 8-7 p49**, **Tables 8-8/8-9/8-10 p50**. Application/reference: **Figure 9-1 p94**, **Figure 9-6 p99** supply decoupling.
- Evaluation-board reference: `SRC/DP83826EVM_snlu262a.pdf`, **SNLU262A Figure 6-2 p17**, **Table 7-1 pp21-26**; native reference `SRC/DP83826EVM_reference_schematic.pdf`, **sheet3 / PDF p3**, U12/U13 and T2/J17. Its old 100-nF CEXT is overridden by current Table 5-1 **2 nF**. The EVM is guidance, not permission to copy its MII/straps wholesale.
- Relevant application/layout guidance is the datasheet's **sections 9.2.5.2 p97, 9.4.1 pp99-101**; no separate ENHANCED-mode application note is selected. The datasheet's BASIC-mode SNLA338 reference is not a configuration authority here.
- Clock: `EC/KC2016Z25.0000C15XXK_e.pdf`, **pp3-4,6 / Table 2 / Figure 4**, as in section 4. Manufacturer RMS jitter alone does not verify TI's offset phase-noise mask.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_DP83826IRHBR / 1 / Ethernet PHY | DP83826IRHBR | 3.3-V analog and I/O supplies; RHB32+GND EP; RMII Leader 10/100 Ethernet | `DP83826IRHBR` / `GW_RHB0032M_TI` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDA3V3_HF / 1 / VDDA3V3 local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDA3V3_10N / 1 / VDDA3V3 local bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDA3V3_1U / 1 / VDDA3V3 local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_SAMSUNG_CL10_1608_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDA3V3_10U / 1 / VDDA3V3 local bypass | CL21A106KAYNNNE; 10 uF | 25 V; X5R; -55..85 C; 10%; 0805 | `GW_CL21A106KAYNNNE_c6e24382` / `GW_SAMSUNG_CL21_2012_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDIO_HF / 1 / VDDIO local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDIO_10N / 1 / VDDIO local bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDIO_1U / 1 / VDDIO local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_SAMSUNG_CL10_1608_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CVDDIO_10U / 1 / VDDIO local bypass | CL21A106KAYNNNE; 10 uF | 25 V; X5R; -55..85 C; 10%; 0805 | `GW_CL21A106KAYNNNE_c6e24382` / `GW_SAMSUNG_CL21_2012_REFLOW` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_CEXT / 1 / PHY external capacitor | C0603C202J5GACTU; 2 nF | 50 V; C0G; 5% seleccion; 0603 | `GW_C0603C202J5GACTU_fa733a70` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_RBIAS / 1 / PHY bias resistor | RC0603FR-076K49L; 6.49 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-076K49L_f42a9329` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_RRMII / 1 / RMII strap pull-up | RC0603FR-072K49L; 2.49 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-072K49L_b905c5f0` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_Y25 / 1 / PHY independent oscillator | KC2016Z25.0000C15XXK; 25 MHz active CMOS | 1.71..3.63 V supply; 3.3 V selected; load <=15 pF; total +/-30 ppm; 2.0x1.6 mm 4-pad | `KC2016Z25.0000C15XXK` / `GW_KC2016Z_KYOCERA` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_COSC / 1 / oscillator bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |

Each of VDDA3V3 and VDDIO retains **10 nF + 100 nF + 1 uF + 10 uF** locally; Samsung X5R upper temperature is +85 C. No analog ferrite or strap LEDs are selected. MDIO uses the device's internal 10-k pull-up unless a later rise-time review justifies a change; no external MDIO resistor is in the selected BOM. CEXT is the 2-nF C0G candidate, not the EVM's older 100 nF.

### D. Connection checklist

| PHY pin | Connection / reset handling |
|---|---|
| 1 ModeSelect | NC; internal HIGH selects ENHANCED. Not GND. |
| 2 CEXT | 2 nF to logic GND. |
| 3 VDDA3V3 | 3.3V and its own four-capacitor local bank to GND. |
| 4 RD_M; 5 RD_P | MDI_RXN / MDI_RXP to PHY-side ESD and magnetics8 / 6 respectively. |
| 6 TD_M; 7 TD_P | MDI_TXN / MDI_TXP to PHY-side ESD and magnetics3 / 1 respectively. |
| 8 XO | NC with active oscillator. |
| 9 XI | PHY oscillator OUT3, 25 MHz; not MCU HSE or 50-MHz reference. |
| 10 RBIAS | 6.49 kOhm, 1%, to logic GND. |
| 11 MDIO | MCU PA2/24 bidirectional; internal pull-up retained. |
| 12 MDC | MCU PC1/16 output -> PHY input. |
| 13 RX_D3 / strap7 | No external load; internal LOW retains CRS_DV selection. Unused data output in RMII. |
| 14 RX_D2 / strap8 | 2.49 kOhm to VDDIO, HIGH for RMII. Unused data output after strapping. |
| 15 RX_D1 / strap9 | PHY -> MCU PC5/33; default LOW strap enables Auto-MDIX. MCU HiZ at sampling. |
| 16 RX_D0 / strap0 | PHY -> MCU PC4/32; default LOW strap enables autonegotiation. MCU HiZ at sampling. |
| 17 VDDIO | 3.3V and its own four-capacitor bank to GND. |
| 18 RX_DV/CRS_DV / strap10 | PHY -> MCU PA7/31, combined CRS_DV. Retain default strap, no forced MDI/MDIX override. |
| 19 RX_CLK/50MHz_RMII | PHY 50-MHz output -> MCU PA1/23 only. |
| 20 RX_ER / strap6 | Unused output; leave externally unloaded, default LOW strap. No GPIO reassignment. |
| 21 PWRDN/INT | No interrupt selected; internal pull-up holds inactive power-down. Leave unconnected; do not ground. |
| 22 TX_CLK / strap5 | Unloaded/default LOW for **Leader**; unused clock output in RMII. |
| 23 TX_EN | MCU PB11/47 output -> PHY. |
| 24 TX_D0 | MCU PB12/51 output -> PHY. |
| 25 TX_D1 | MCU PB13/52 output -> PHY. |
| 26 TX_D2; 27 TX_D3 | RMII unused inputs; internal pull-downs retained, no MAC wiring. |
| 28 COL/LED2 / strap4 | Unloaded/default LOW, PHY address bit2=0. No LED. |
| 29 CRS/LED3 / strap3 | Unloaded/default LOW, PHY address bit1=0. No LED. |
| 30 LED0 / strap2 | Unloaded/default LOW, PHY address bit0=0. No LED. |
| 31 CLKOUT/LED1 / strap1 | Leave unloaded/default HIGH at POR; part of RMII-selection condition. Its default 25-MHz CLKOUT is unused. **Not the selected 50-MHz source.** |
| 32 RST_N | Dedicated `PHY_nRESET` from MCU PE6/5; internal pull-up. Keep separate from MCU NRST. |
| 33 exposed GND pad | Logic GND; must not be omitted as a mechanical-only pad. |

Oscillator **1 -> 3.3V, 2 -> GND, 3 -> XI9, 4 -> 3.3V**, with local 10 nF between 4/2. Both clocks remain independent. Reset LOW >=25 us; wait >=2 ms after release and >=50 ms after power-up before SMI, accommodating <=5-ms oscillator startup and 0.5-50-ms supply-ramp requirement. Do not assume RMII clock while reset is asserted. Read back straps during commissioning. Internal pulls are accepted only with all external/MCU loads respecting strap levels; add no guessed resistor network.

### E. Remaining practical work

Clock receiver/route load≤15pF; PHY clock performance and reset/supply timing require prototype confirmation. Preserve all straps and RMII pin reservations.

### F. Review checklist

- [ ] ModeSelect1 is NC, strap14 is pulled HIGH, TX_CLK22 remains default LOW, strap31 remains default HIGH.
- [ ] Address straps30/29/28 remain 000 without LED/MCU loading.
- [ ] PHY19 drives PA1 at 50 MHz; XI9 receives only its own 25-MHz oscillator.
- [ ] CEXT2 is 2 nF and RBIAS10 is 6.49 k/1%.
- [ ] Both 3.3-V supply banks and GND EP33 are present.
- [ ] RX/TX directions and D0/D1 mapping match the MCU AF11 reservation.
- [ ] Reset32 is separate from NRST and timing/SMI waits are documented.
- [ ] Unused pins do not defeat straps, power-down state or clock topology.


### G. Required net labels

3.3V,GND,PHY_XI25,PHY_nRESET,ETH_RMII_REF_CLK,ETH_MDIO,ETH_MDC and RMII data/control labels from section 4; PHY_XI25 is not MCU_HSE25.

## 6. HX1188FNL magnetics and SS-7188S-A-NF RJ45.

### A. Selected configuration

**ACCEPTED:** HX1188FNL with exact SS-7188S-A-NF shielded jack; complete transformer-coupled **TI EVM sheet3** termination variant; PHY-side TPD4E05U06DQAR. Two 100-nF capacitors in parallel per PHY center tap, four 75-Ohm resistors and two separate 1-nF/2-kV chassis AC returns. **PROVISIONAL/BLOCKED final insulation:** chassis/PE policy, HV-capacitor safety class/models and board ESD qualification. No automatic chassis-to-logic-GND bridge.

Exact source: gate **Ethernet - one complete termination implementation**, BOM `ETH_TMAG`, `ETH_CCT`, `ETH_RBOB`, `ETH_CBOB`, `ETH_JRJ45`, `ETH_DESD`. FNL is selected; FNLT is a packaging variant, not a reason to transfer a different winding map.

### B. Official manufacturer sources

- Main magnetics datasheet: `EC/HX1188FNL.pdf`, Pulse **RevB**, **sheet2 / PDF p2**, numbered winding schematic and electrical/isolation test limits (1:1, >=350 uH, 1500 Vrms/60 s); **sheet3 / PDF p3**, package and suggested land pattern. Exact drawing, not a generic 16-pin LAN transformer.
- Main connector drawing: `EC/SS-7188S-A-NF_drawing.pdf`, Cinch/Stewart **CT710001 B0**, **sheet1 / PDF p1**: numbered contact schematic, component-side recommended hole layout, shield and mechanical holes.
- ESD main datasheet: `EC/tpd4e05u06.pdf`, TI **SLVSBO7O**, **Table 4-2 p4**, DQA pinout; **DQA0010A board/stencil PDF pp29-30** (not another package's lands). Reference is **Ethernet EVM U13**, not the HDMI application drawing.
- Relevant application/reference/layout: `SRC/DP83826EVM_reference_schematic.pdf`, **sheet3 / PDF p3**, T2/J17/U13 and R43-R46/C45-C59; `SRC/DP83826EVM_snlu262a.pdf`, **Figure 6-2 p17**, **Table 7-1 pp21-26**. No separate jack/magnetics application note is selected. PHY datasheet `DS/dp83826i.pdf` **sections 9.2.5.3 pp97-98, 9.4.1 pp99-101**, notably **9.4.1.3 p100** transformer layout and **9.4.1.4 p101** metal pour, guides magnetics layout. Do not superpose the different **Figure 9-2 p95** termination network.
- Exact 75-Ohm/HV-capacitor application/model data are not closed. No safety-class certification is established by a 2-kV DC component rating.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ETH_TMAG / 1 / Ethernet transformer | HX1188FNL; 1:1; 350 uH candidato | HPOT >=1500 Vrms; limites tabla9-1; Relacion +/-2%; Pulse16 SMT 12.7x9.09 mm | `HX1188FNL` / `GW_HX1188FNL_PULSE` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_CCT / 4 / PHY-side center-tap bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_RBOB / 4 / cable-side termination | CRCW080575R0FKEA; 75 Ohm | 150 V limiting element; actual75Ohm continuous voltage limited bysqrt(P*R); 1%; 0.125 W at70C; derating applies; 0805 resistor | `CRCW080575R0FKEA` / `GW_CRCW0805_VISHAY_20035_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_CBOB / 2 / chassis AC return | C1206C102KGRACAUTO; 1 nF | 2000 V; X7R; safety class unverified; 10%; 1206 | `C1206C102KGRACAUTO` / `GW_C1206_KEMET_C1076_DENSITY_B` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_JRJ45 / 1 / shielded Ethernet jack | SS-7188S-A-NF; 8P8C shielded | TBD; TBD; CT710001 B0 through-hole | `SS-7188S-A-NF` / `GW_SS7188SANF_STEWART` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_DESD / 1 / PHY-side ESD array | TPD4E05U06DQAR; 4 canales baja C | TBD; TBD; DQA USON10 | `TPD4E05U06DQAR` / `GW_DQA0010A_TI` | PROVISIONAL; CAD_VERIFIED; REQUIRED |

75-Ohm parts are 1%, 0.125 W per current BOM; application pulse/safety limits remain to be checked. HV capacitors are 1 nF, 10%, 2 kV X7R candidates, not automatically Y-class. Both75Ω and1nF2kVDC models are now verified; the application does not acquire safety-Y certification from a voltage rating. Historical compiler warnings are not current validation. Jack holepattern/orientation isverified. Copperannuli areprototypechoices;body/boardedge placement andassemblystock still require the actualboard/assembler review. Contactratings are not independently requalified. No four external 49.9-Ohm MDI resistors, no C61/R51 logic/chassis coupling, no PoE implementation are selected.

### D. Connection checklist

| Exact endpoints | Connection |
|---|---|
| PHY7 TD+ -> magnetics1 | MDI_TXP, with ESD channel1 to logic GND. |
| PHY6 TD- -> magnetics3 | MDI_TXN, with ESD channel2. |
| PHY5 RD+ -> magnetics6 | MDI_RXP, with ESD channel4. |
| PHY4 RD- -> magnetics8 | MDI_RXN, with ESD channel5. |
| Magnetics2 PHY TX CT | Two parallel 100 nF to logic GND, no DC supply tie. |
| Magnetics7 PHY RX CT | Separate two parallel 100 nF to logic GND. |
| Magnetics16 -> RJ45 contact1 | Cable TX+. |
| Magnetics14 -> RJ45 contact2 | Cable TX-. |
| Magnetics11 -> RJ45 contact3 | Cable RX+. |
| Magnetics9 -> RJ45 contact6 | Cable RX-. |
| Magnetics15 and10 | Each through its own 75 Ohm to shared cable-CT node A; node A through one 1-nF/2-kV capacitor to chassis. |
| RJ45 contacts4+5 | Join this unused pair, then its own 75 Ohm to node B. |
| RJ45 contacts7+8 | Join this unused pair, then its own 75 Ohm to node B; node B through the second 1-nF/2-kV capacitor to chassis. |
| Magnetics4,5,12,13 | NC. |
| RJ45 S1/S2 | Chassis/shield. Project labels for unnumbered shield tabs, not signal contacts. MP1/MP2 are non-electrical mounting holes. |

Keep nodes A/B distinct; they meet only through their respective capacitors/chassis path. TPD4E05U06: **1=TXP, 2=TXN, 3=GND, 4=RXP, 5=RXN, 8=GND**. Its **10/9/7/6 are internal NC pads**; the EVM uses external continuous same-net copper **1-10, 2-9, 4-7, 5-6** for pass-through routing. Never assume internal series continuity through the device. If represented in the schematic, those same-net external connections must remain explicit; NC-pad pass-through does not create a cable-to-logic ground bridge.

Logic GND stays on PHY side; cable AC returns/shield reference chassis. Do not ground cable center taps directly or install an arbitrary DC chassis bond across the barrier. Preserve exact contact numbering from component-side versus mating views.

### E. Remaining practical work

The four75Ω positions now use saved CRCW080575R0FKEA / GW_CRCW0805_VISHAY_20035_REFLOW, C844859. The two C1206C102KGRACAUTO models are now saved: GW_C1206_KEMET_C1076_DENSITY_B, C600002. No remaining CAD model blocker for the termination resistors/capacitors. Resolve chassis/shield treatment and capacitor application rating; no arbitrary GND bond. Signal map can be drawn meanwhile.

### F. Review checklist

- [ ] Magnetics pin 1/3 and6/8 are PHY-side pairs;16/14 and11/9 reach the specified RJ45 contacts.
- [ ] Both PHY CTs each have two parallel 100-nF parts; neither CT is tied to a supply.
- [ ] Four 75-Ohm resistors and two separate chassis AC-return nodes are drawn exactly once.
- [ ] No external 49.9-Ohm MDI terminations or second datasheet termination variant has been added.
- [ ] ESD is PHY-side; both GND3/8 reference logic GND.
- [ ] ESD pass-through continuity is external copper, not an assumed internal NC connection.
- [ ] RJ45 shield/mechanical pads are distinguished; chassis and logic GND are not merged.
- [ ] Magnetics NC pins remain open; no PoE or extra field circuitry crosses the isolation barrier.
- [ ] No metal-under-magnetics and barrier/plane constraints are carried into later layout review.


### G. Required net labels

MDI_TXP,MDI_TXN,MDI_RXP,MDI_RXN, cable CT nodeA, unused-pair nodeB,CHASSIS. NodesA/B remain distinct.

## 7. THVD1420 RS-485.

### A. Selected configuration

**ACCEPTED:** one THVD1420DR, 3.3 V, nonisolated half-duplex, **115200 baud, 8N1** capture default; separate MCU GPIO DE/nRE, DE LOW and nRE HIGH at reset; built-in protection and receiver fail-safe, no external bias. **PROVISIONAL:** optional bus-end termination/connector mechanics. **BLOCKED optional surge circuit:** CDSOT23-SM712 plus **two** 10-Ohm pulse resistors; no transferred 1-kV rating.

Exact source: gate **RS-485, CAN, DI and DO decisions / RS-485**, `RS_*` BOM rows and USART3 reservations. Baud is an engineering default, not a confirmed field-bus contract.

### B. Official manufacturer sources

- `DS/thvd1400.pdf`, TI **SLLSF78B**, [official family datasheet](https://www.ti.com/lit/ds/symlink/thvd1400.pdf): **Table 4-1 p3** pins; **section 7.4/Table 7-2 p14** receive/fail-safe behavior; **Figure 8-1 p15** basic half-duplex bus; **sections 8.2.1.1-.4 pp15-16** topology/load/fail-safe.
- Protection reference: **Figure 8-5/Table 8-1 p19**, section 8.2.2; **Figure 8-6 p19** explicitly THVD1400, 500 kbps, 5 V. It is not a qualified THVD1420/3.3-V circuit. Application/layout guidance: **section 9 p19**, **section 10.1/Figure 10-1 p20**. No separate application note/EVM is adopted beyond these datasheet references.
- `EC/CDSOT23-SM712.pdf`, Bourns **pp1-3**, pin diagram, electrical clamp table, pulse curves and recommended footprint. The part has about 75-pF typical capacitance; its positive 19/20/26-V clamp at 1/5/17 A exceeds the THVD bus +/-16-V absolute limits without proven residual-current control.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_THVD1420DR / 1 / half-duplex bus transceiver | THVD1420DR | 3.3 V selected / 3.0-5.5 V recommended; bus common mode -7 to +12 V; bus absolute +/-16 V | `THVD1420DR` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| RS_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| RS_RT / 1 / conditional bus-end termination and open-default jumper | CRCW1206120RFKEA; 120 Ohm | 1%;0.25W at70C;200V or power-limited; 1%; 0.25W; 1206 | `CRCW1206120RFKEA` / `GW_CRCW1206_VISHAY_20035_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; CONDITIONAL |
| RS_RDE / 1 / DE reset pull-down | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| RS_RRE / 1 / nRE reset pull-up | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| RS_RPULSE / 2 / conditional bus-line pulse resistors | CRCW0603010RJNEAHP; 10 Ohm | Pulse-proof segun ficha exacta; 5%; Pulsos por verificar; 0603 | `GW_CRCW0603010RJNEAHP_c8eb51d2` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_TVS / 1 / transient clamp candidate | CDSOT23-SM712; Asimetrica -7/+12 V candidata | TBD; TBD; SOT23 | `CDSOT23-SM712` / `GW_SM712_BOURNS` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_J / 1 / field connector | TB002-500-03BE; 3 poles;5mm pitch | UL300V15A;IEC250V17.5A;academic circuit limits lower; TBD; TB002-500 3P TH | `TB002-500-03BE` / `GW_TB002_500_3P_SAMESKY` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |

Selected basic capture omits the optional SM712/10-Ohm network; conditional positions remain unqualified. Termination is **120 Ohm only at a physical cable end** if bus Z0 is 120 Ohm; target >=0.25 W at 70 C, 1%, with fault/ambient review and exact MPN/jumper selected in section15. Do not use a 0603 0.1-W resistor merely because 120 Ohm is available. UseTB002-500-03BE:1A,2B,3GND;project numbering/orientation in section15. No external bias is populated.

### D. Connection checklist

| THVD pin | Required connection |
|---|---|
| 1 R | Receiver output -> MCU PD9/56 USART3_RX. |
| 2 nRE | MCU PD11/58 GPIO; 10 kOhm pull-up to 3.3V holds receiver disabled at reset. |
| 3 DE | MCU PD10/57 GPIO; 10 kOhm pull-down to GND holds driver disabled at reset. |
| 4 D | MCU PD8/55 USART3_TX output -> driver input. |
| 5 GND | Logic/common bus-reference GND; no galvanic isolation claimed. |
| 6 A | Bus A connector functional terminal. |
| 7 B | Bus B connector functional terminal. |
| 8 VCC | 3.3V, local 100 nF to GND5. |

RS connectorTB002-500-03BE: **1A(U6.6),2B(U6.7),3COM=GND(U6.5)**. Label polarity on both PCB and cable. End-only 120-Ohm termination goes A-to-B through the open-default jumper. Basic selected line connections have no added series resistors. If the optional network is later qualified, use one 10-Ohm resistor in **each** line and SM712 bus pins1/2/reference3 per the exact source, with the intended return defined; do not silently insert it now. Transmit: assert DE, enable/disable receive deliberately, complete the final stop bit before releasing DE; receive: DE LOW, nRE LOW. MCU reset leaves both functions disabled. No mandatory external bias pull-up/down is missing because device fail-safe is retained.

### E. Remaining practical work

Connector numbering is defined. Optional end termination isCRCW1206120RFKEA,120ohm1%0.25W,with61300211121 two-pin jumper,normallyOPEN;see section15. Optional SM712/two10Ω network stays unpopulated and is not needed to draw the selected basic circuit.

### F. Review checklist

- [ ] R1 goes to MCU RX and D4 to MCU TX, not the reverse.
- [ ] DE has 10-k pull-down and nRE 10-k pull-up, with separate GPIO controls.
- [ ] PD10 is not configured as USART3 clock/hardware DE and PD11 is not CTS.
- [ ] VCC8 has local 100 nF to GND5 and no unintended isolation claim.
- [ ] Only actual cable ends carry termination; jumper defaults open at an intermediate node.
- [ ] No duplicate external bias or arbitrary 10-Ohm series part is populated.
- [ ] Optional surge network shows two resistors and remains visibly unqualified/unpopulated.
- [ ] COM/pin-number assumptions and field baud/cable constraints remain documented.


### G. Required net labels

RS485_TX (PD8),RS485_RX (PD9),RS485_DE (PD10),RS485_nRE (PD11),RS485_A,RS485_B,GND,3.3V.

## 8. ATA6561 CAN-FD.

### A. Selected configuration

**ACCEPTED:** ATA6561-GAQW SOIC8; VCC=5 V, VIO=3.3 V; startup standby and recessive TXD from internal pull-ups. MCU FDCAN1 on PD0/1. Engineering target **1 Mbit/s nominal / 2 Mbit/s data**, subject to cable timing. No external TVS, choke or bus shunt capacitors. Optional conventional 120-Ohm termination at a physical cable end only, open-default jumper at intermediate nodes; prior 62+62-Ohm/4.7-nF split alternative is DNP.

Exact source: gate **RS-485, CAN, DI and DO decisions / CAN**, `CAN_*` BOM and pin bindings. Basic-node capture GO does not mean interface compliance or an approved end termination.

### B. Official manufacturer sources

- Main: `DS/20005991B.pdf`, Microchip **DS20005991B**: **p1 package pinout**, **Figure 1-1 p4** operating modes; **Table 1-2 p8** pin functions, **Electrical Characteristics pp9-13**, especially **p11** internal STBY/TXD pull-ups; SOIC drawing **p19**.
- Relevant manufacturer application/evaluation guide: `SRC/ATA656x_EVKit_50002649A.pdf`, **DS50002649A**, **sections 3.3-3.8 pp17-18**, **Figure 4-1 p19** application for VIO devices, **Appendix A.2 p28** board schematic, **Table B-2 p32** ATA6561/3/6 BOM; **A.3-A.6 pp29-30** layout views. Select the **ATA6561 VIO** variant, not ATA6560 NSIL pin 5 or VDFN EP9.
- Locator correction only, no configuration change: the gate's **DS20005991B Figure 1-6** cannot be found in this exact local revision; its figures run 1-1 through 1-5 before section 2. Use verified **Figure 4-1 / Appendix A.2** in the EVKit guide. Likewise `table2.0` in the older report means **section 2.0 Electrical Characteristics**, not an identified numbered table. Do not perpetuate those unverified locators.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_ATA6561_GAQW / 1 / CAN-FD transceiver | ATA6561-GAQW | VCC 4.5-5.5 V; VIO 2.8-5.5 V; SOIC8; selected 1/2 Mbit/s | `ATA6561-GAQW` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| CAN_CVCC5 / 1 / 5-V bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| CAN_CVIO3V3 / 1 / 3.3-V I/O bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| CAN_CBULK / 1 / local bulk reserve | TBD; 47 uF | 10 V minimo EVM; TBD; 1210 candidato | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| CAN_J / 1 / field connector | TB002-500-03BE; 3 poles;5mm pitch | UL300V15A;IEC250V17.5A;academic circuit limits lower; TBD; TB002-500 3P TH | `TB002-500-03BE` / `GW_TB002_500_3P_SAMESKY` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| CAN_RT / 1 / conditional bus-end termination and open-default jumper | CRCW1206120RFKEA; 120 Ohm | 1%;0.25W at70C;200V or power-limited; 1%; 0.25W; 1206 | `CRCW1206120RFKEA` / `GW_CRCW1206_VISHAY_20035_REFLOW` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; CONDITIONAL |

Local bypasses are 100 nF each. End termination target is 120 Ohm/1%/>=0.25 W at 70 C with application/fault review; exact MPN/jumper/model selected in section15. The retained optional 47-uF/10-V bulk is an EVKit candidate, **not selected mandatory population**. The 5-V regulator/distribution transient response decides whether local bulk is necessary. No external STBY resistor or split network is selected.

### D. Connection checklist

| ATA6561 SOIC8 pin | Required connection |
|---|---|
| 1 TXD | MCU PD1/82 FDCAN1_TX -> transceiver; internal 20-50-kOhm pull-up to VIO retains recessive. |
| 2 GND | Logic/nonisolated bus-reference GND. |
| 3 VCC | 5V, 100 nF to GND2. Recommended VCC 4.5-5.5 V. |
| 4 RXD | Transceiver -> MCU PD0/81 FDCAN1_RX. |
| 5 VIO | 3.3V, separate 100 nF to GND2. This is **VIO, not NSIL**; do not tie to 5 V from an ATA6560 example. |
| 6 CANL | Connector functional CANL. |
| 7 CANH | Connector functional CANH. |
| 8 STBY | MCU PE7/37 GPIO; internal 75-175-kOhm pull-up to VIO holds standby while MCU HiZ. Drive LOW only after supplies/controller initialization. |

There is no exposed-pad 9 on the selected SOIC8 model. Optional 120 Ohm connects CANH-to-CANL through the open-default end-node jumper. CAN connectorTB002-500-03BE: **1CANH(U7.7),2CANL(U7.6),3COM=GND(U7.2)**. No external TVS/choke/shunt capacitors are populated; no galvanic isolation is claimed.

### E. Remaining practical work

Connector/end-termination models and exact connections are defined in section15. No additional TVS/filter or mandatory47µF bulk is selected. Confirm intended cable operation during functional tests.

### F. Review checklist

- [ ] Exact ATA6561 SOIC8 has VIO5=3.3V, VCC3=5V and no fictitious EP9/NSIL.
- [ ] TXD1 comes from FDCAN1_TX and RXD4 reaches FDCAN1_RX.
- [ ] Each supply has a separate local 100-nF capacitor.
- [ ] STBY defaults HIGH/standby and is driven LOW only after initialization.
- [ ] CANH7/CANL6 are not swapped at the connector.
- [ ] Termination appears only at a cable end; no simultaneous 120-Ohm and split network.
- [ ] Optional bulk, bus capacitors, choke and TVS have not become mandatory by copying the EVKit.
- [ ] Cable timing and connector/fault ratings remain distinct from basic-node capture approval.


### G. Required net labels

FDCAN1_TX (PD1),FDCAN1_RX (PD0),CAN_STBY (PE7),CANH,CANL,3.3V,5V,GND.

## 9. ISO1212 dual digital inputs.

### A. Selected configuration

**ACCEPTED:** one ISO1212DBQR, two **Type 3 sinking inputs** for normal 18-30-V sensing; each uses 562-Ohm RSENSE, 1-kOhm Firstohm MM204 RTHR and 10-nF CIN. Logic side 3.3 V, EN HIGH. FGND1/FGND2 share `FIELD_COM`: group isolation from logic, **not channel-to-channel isolation**. **PROVISIONAL/BLOCKED surge qualification:** MM204 resistor/system withstand. No default extra TVS or PE capacitor.

Exact source: gate **DI** decision, BOM `DI_*`. 10-nF Type 3 is retained; do not change to 330 nF or MM204P simply to copy a different surge example.

### B. Official manufacturer sources

- `DS/iso1212.pdf`, TI **SLLSEY7G**, [official datasheet](https://www.ti.com/lit/ds/symlink/iso1212.pdf): **Figure 4-2 and ISO1212 Pin Functions p4**; **section 5.9 p10** DC thresholds; **Figure 8-2 p20** sinking-input schematic; **section 8.2.1.2.1/equations 1-4 p21** thresholds/current; **Table 8-1/Figure 8-9 p25** surge modes/test fixture.
- Relevant application/reference and layout are in that datasheet: **section 8.2.1 pp19-28**, **sections 8.4.1-.2 pp30-31**, especially **Figure 8-18 p31 ISO1212 layout**. Figure 8-17 on the same page is **ISO1211**, not our pin map. No separate EVM/application note is adopted.
- Threshold resistor: `EC/Firstohm_MM.pdf`, manufacturer MM sheet **Rev08-March-2023**, **printed pp75-78 / PDF pp1-4**; MM204 rated/derating/surge curve (not MM204P) and **printed p78 / PDF p4** reflow lands. Manufacturer-authored document obtained from Alfatec; provenance is in [additional_documents.json](evidence/electrical_closure/additional_documents.json).
- Exact RSENSE: `SRC/ISO1212_RSENSE_RC0603FR07562RL.pdf`, **p1**; filter capacitor: `SRC/DI_CIN_C0603C103K1RACTU.pdf`, **p1** nominal properties. Their nominal sheets do not certify a system surge.
- Locator precision: the older report's `Table 4-2` is the **ISO1212 Pin Functions block beneath Figure 4-2**, and `table5.9` is **section 5.9**, not a numbered table. Use the verified locators above.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_ISO1212DBQR / 1 / two Type3 field inputs | ISO1212DBQR | VCC1 2.25-5.5 V; 3.3 V selected; normal input 18-30 V; isolation and surge limits separate | `ISO1212DBQR` / `GW_DBQ0016A_TI` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| DI_RSENSE1 / 1 / channel 1 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| DI_RTHR1 / 1 / channel 1 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| DI_CIN1 / 1 / channel 1 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| DI_RSENSE2 / 1 / channel 2 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_RC0603_YAGEO_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| DI_RTHR2 / 1 / channel 2 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |
| DI_CIN2 / 1 / channel 2 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_0603_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| DI_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| DI_CPE / 1 / unselected field-to-PE coupling | TBD; 500 pF candidato | 2 kV; seguridad por definir; TBD; TBD | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| DI_J / 1 / field connector | TB002-500-03BE; 3 poles;5mm pitch | UL300V15A;IEC250V17.5A;academic circuit limits lower; TBD; TB002-500 3P TH | `TB002-500-03BE` / `GW_TB002_500_3P_SAMESKY` | DERIVED_PENDING_REVIEW; CAD_VERIFIED; REQUIRED |

MM204 1 kOhm/1% is 0.25 W at 70 C, derated to zero at 125 C; maximum working voltage 200 V and overload/surge limits remain separate. At 2.75 mA and R+1%, RTHR power is 7.64 mW and RSENSE power 4.29 mW: normal dissipation is acceptable within derating, but **surge is not qualified**. MM204 is not the pulse-enhanced MM204P. CPE 500 pF/2 kV is an **unselected conditional candidate**, not a required placement; extra DI TVS is DNP. JDI physical/project numbering isdefined:1FIELD_DI1_PLUS,2FIELD_DI2_PLUS,3FIELD_COM;see section15.

### D. Connection checklist

| ISO1212 pin | Required connection |
|---|---|
| 1, 8 GND1 | Logic GND only. |
| 2 VCC1 | 3.3V; 100 nF locally to logic GND. |
| 3 EN | Tie to VCC1/3.3V; outputs continuously enabled. |
| 4 OUT1 | Logic output -> MCU PE4/3 DI1 input. |
| 5 OUT2 | Logic output -> MCU PE5/4 DI2 input. |
| 6, 7 NC | Leave individually unconnected. |
| 9 FGND2 | FIELD_COM, joined to FGND1 on field side only. |
| 10 IN2 | Low end of channel2 562-Ohm RSENSE; not the direct external 24-V terminal. |
| 11 SENSE2 | Field DI2 terminal through its 1-kOhm RTHR; 562 Ohm to IN2 and 10 nF to FIELD_COM. |
| 12 SUB2 | Independent floating substrate owner; never GND/FGND/SUB1. |
| 13 SUB1 | Independent floating substrate owner; never GND/FGND/SUB2. |
| 14 FGND1 | FIELD_COM. |
| 15 IN1 | Low end of channel1 562-Ohm RSENSE. |
| 16 SENSE1 | Field DI1 terminal through its 1-kOhm RTHR; 562 Ohm to IN1 and 10 nF to FIELD_COM. |

For each channel: external input -> **RTHR -> SENSE**, then **RSENSE from SENSE to IN**, and **CIN from SENSE to field COM**. RSENSE is not across the 24-V terminals; CIN does not return to logic GND. Field connector roles DI1/DI2/FIELD_COM await exact numbering. Optional separate 2 x 2-mm floating substrate copper islands must follow the source; no schematic net may merge their ownership. No PE coupling/extra field TVS is populated by default.

Use guaranteed DC threshold limits: VIH typical/max 10.4/10.95 V, VIL min/typical 8.7/9.2 V from section 5.9. Approximate equations giving 10.5/9.35 V are not guaranteed thresholds. Table 8-1's Type3/10-nF setup lists 1-kV line-PE/line-line but **500-V line-FGND**; 1-kV line-FGND uses 330 nF. None is assigned to the actual MM204 implementation.

### E. Remaining practical work

DI connectorTB002-500-03BE:1FIELD_DI1_PLUS,2FIELD_DI2_PLUS,3FIELD_COM. Keep SUB1/SUB2 floating separately and FIELD_COM isolated. Normal Type3 sensing is ready. No surge withstand is claimed or required by this academic task.

### F. Review checklist

- [ ] Both channels use 562-Ohm SENSE-IN and 1-kOhm series input resistors, not reversed positions.
- [ ] Each 10-nF capacitor returns to FIELD_COM, not logic GND.
- [ ] VCC1 bypass and EN=VCC1 are present; OUT1/2 go to PE4/5.
- [ ] FGND1/2 share only field COM; no channel-to-channel isolation claim.
- [ ] SUB1/2 are neither grounded nor joined; NC6/7 remain open.
- [ ] Exact MM204 is distinguished from MM204P and from generic 0603 resistors.
- [ ] Normal resistor dissipation is not presented as surge-energy qualification.
- [ ] Table 8-1 test modes and 10-nF versus 330-nF limits are not conflated.
- [ ] No arbitrary PE capacitor/TVS bypasses isolation or changes the selected threshold/filter circuit.


### G. Required net labels

DI1,DI2,FIELD_COM,DI1_SENSE,DI1_IN,DI2_SENSE,DI2_IN,3.3V,GND; do not share field/control returns.

## 10. Two BSP75N protected outputs with discrete 5-V input drivers

### A. Selected implementation and migration

Engineering selection,2026-11-08: keep both **BSP75NTA** protected low-side outputs,
MCU PE2/PE3 and the external24-V load supply. Replace the proposed
SN74LVC2T45DCTR interface with **two MMBT3904-7-F NPN + DMP2035U-7 PMOS
input-driver channels**. These small transistors switch only the BSP input current
from5V; they never carry24-V load current. This is an explicit driver revision,
not a silent equivalent substitution. U9 remains on the native sheet until the
local migration below is performed; the historical library component is retained.

The translator's loaded VOH row does not guarantee the BSP's4.5-V minimum for
overtemperature protection. The4.5-V condition is distinct from the lower ordinary
logic turn-on threshold. Do not connect an incomplete translator circuit to loads.

**Connection specification ready; native implementation pending.** The BSP,
NPN and PMOS source models have verified terminal positions and lands. No
bench waveform, thermal test, native ECO or ERC success is claimed.

### B. Manufacturer evidence and physical orientation

- [BSP75N Diodes DS33016 Rev7-2](../../hardware/academic_rev1/libraries/sources/bsp75n_closure/BSP75N.pdf),
  p1 TOP VIEW terminal identification,p3 ratings,p4 electrical characteristics,
  p6 inductive operation/thermal guidance,p8 Suggested Pad Layout.
- [MMBT3904 Diodes DS30036 Rev27-2 March2025](../../hardware/academic_rev1/libraries/sources/autonomous_closure/MMBT3904.pdf),
  p1 terminal positions/order code,p3 saturation/leakage,p6 suggested lands.
- [DMP2035U Diodes DS31830 Rev11-2 June2025](../../hardware/academic_rev1/libraries/sources/autonomous_closure/DMP2035U.pdf),
  p1 terminal positions/order code,p2 RDS(on),gate limits/leakage,p6 lands.
- Historical rejected driver: TI SCES516N electrical-characteristics VOH rows
  in the selected SN74LVC2T45 source. Do not treat the unloaded VOH row as a loaded guarantee.

BSP in TOP PCB view,wide tab above: lower-left=IN,lower-centre=DRAIN,
lower-right=SOURCE,upper tab=SOURCE. Actual Altium pin/pad IDs are
**IN,D,S,S_TAB**, not inferred numeric1/2/3/4. Footprint
`GW_BSP75N_SOT223_DN_DIODES`: lower centresx=-2.30,0,+2.30mm at y=-3.20mm,
lands1.20x1.60mm; SOURCE TAB centre(0,+3.20),land3.30x1.60mm.
Do not use a conventional drain-tab SOT223 footprint.

Both new SOT23 parts also use explicit functional Altium IDs. TOP view with
single lead above: lower-left=B(NPN)/G(PMOS),lower-right=E(NPN)/S(PMOS),
upper=C(NPN)/D(PMOS). Saved lands are0.80x0.90mm at(-0.95,-1.00),
(+0.95,-1.00),(0,+1.00)mm,from each exact Diodes drawing. No numeric
terminal assignment was borrowed from another vendor.

### C. Exact components and quantities for both channels

| Function | Quantity / exact MPN | Symbol / footprint |
|---|---|---|
| Protected low-side switches U10/U11 |2 BSP75NTA|`BSP75NTA` / `GW_BSP75N_SOT223_DN_DIODES`|
| Q_DO1_N,Q_DO2_N |2 MMBT3904-7-F|`MMBT3904-7-F` / `GW_MMBT3904_BEC_DIODES`|
| Q_DO1_P,Q_DO2_P |2 DMP2035U-7|`DMP2035U-7` / `GW_DMP2035U_GSD_DIODES`|
| Existing GPIO pull-downs R24/R25 |2 RC0603FR-0710KL,10k,1%,0.1W|`RC0603FR-0710KL` / `GW_RC0603_YAGEO_REFLOW`|
| R_DO1_BASE,R_DO2_BASE |2 RC0603FR-074K7L,4.7k,1%,0.1W|`RC0603FR-074K7L` / `GW_RC0603_YAGEO_REFLOW`|
| R_DO1_GS,R_DO2_GS |2 same4.7k MPN|same symbol/footprint|
| R_DO1_GATE,R_DO2_GATE |2 RC0603FR-07100RL,100ohm,1%,0.1W|`RC0603FR-07100RL` / `GW_RC0603_YAGEO_REFLOW`|
| R_DO1_OFF,R_DO2_OFF |2 RC0603FR-072K49L,2.49k,1%,0.1W|`GW_RC0603FR-072K49L_b905c5f0` / `GW_RC0603_YAGEO_REFLOW`|
| Local5V bypass |1 C0603C104K5RACTU,100nF50V|`GW_C0603C104K5RACTU_dc5e12a5` / `GW_0603_KEMET_NOMINAL`|
| DO_SUPPLY,DO1_LOAD,DO2_LOAD |3 TB002-500-02BE,2-pole5mm|`TB002-500-02BE` / `GW_TB002_500_2P_SAMESKY`|

R24/R25 may currently contain FOJAN5%10k: this is a BOM-identity mismatch,
not an automatic functional fault. The table selects the already documented
Yageo1% model. New4.7k/100ohm order codes use the documented Yageo RC0603
family and mounting pattern; distributor stock/JLC category has not been verified.

### D. Complete connection table: apply independently to channels1 and2

| Physical terminal / component | Channel1 net or endpoint | Channel2 net or endpoint |
|---|---|---|
| MCU output |U4 PE2/pad1=`DO1`|U4 PE3/pad2=`DO2`|
| Existing10k pull-down |DO1 toGND|DO2 toGND|
|4.7k base resistor |DO1 toQ_DO1_N.B|DO2 toQ_DO2_N.B|
| NPN E,lower-right |GND|GND|
| NPN C,upper lead |100ohm to`DO1_GATE`|100ohm to`DO2_GATE`|
| PMOS G,lower-left |DO1_GATE|DO2_GATE|
|4.7k gate-source resistor |DO1_GATE to5V|DO2_GATE to5V|
| PMOS S,lower-right |5V|5V|
| PMOS D,upper lead |DO1_DRIVE|DO2_DRIVE|
| BSP IN,lower-left |U10.IN=DO1_DRIVE|U11.IN=DO2_DRIVE|
|2.49k OFF resistor |DO1_DRIVE tolocalSOURCE/GND|DO2_DRIVE tolocalSOURCE/GND|
| BSP D,lower-middle |U10.D=`DO1_DRAIN`|U11.D=`DO2_DRAIN`|
| BSP S,lower-right |U10.S=GND/DO_EXT_RETURN|U11.S=GND/DO_EXT_RETURN|
| BSP S_TAB,upper tab |U10.S_TAB=sameSOURCE return|U11.S_TAB=sameSOURCE return|
| Load connector pin1 |DO_EXT_PLUS|DO_EXT_PLUS|
| Load connector pin2 |DO1_DRAIN|DO2_DRAIN|

`DO_SUPPLY.1=DO_EXT_PLUS` from a separate regulated24-V supply;
`DO_SUPPLY.2=DO_EXT_RETURN`,the **same non-isolated system GND**,with an explicit
high-current return route to the source connection. `DO_EXT_RETURN` is a role,
not a second disconnected ground. Do not connect any DO current to EF_RTN,
FIELD_COM or CHASSIS. Place the load between connector1(+) and2(switched negative).
The external DO supply positive must not be24V_ELEC or VIN_CLAMP. Main F1/TPS
does not limit this load current; set the external laboratory source current limit
for the actual test load. This is not a galvanically isolated DO architecture.

One100nF capacitor goes5V-to-GND near the driver pair. The former VCCA3.3V
capacitor is DNP in the selected DO BOM; a correctly connected existing instance
may remain as extra rail bypass. Remove U9 locally after preserving its MCU
ports and R24/R25 pull-downs. No global library update or wholesale sheet rewrite.

### E. Academic electrical estimate and required bring-up

The selected5V feedback network screens4.86249..5.17365V before ripple.
Allocate at most50mV negative ripple at the drivers. With1%4.7k/100ohm,
NPN VCE(sat)=0.20V engineering allowance and1mV gate-current allowance,
minimum PMOS |VGS| is about4.51V. The calculation uses the manufacturer's
45milliohm maximum RDS(on) specified already at-2.5V,so it does not depend on
a tight4.5-V gate-drive threshold. The35milliohm row at-4.5V is additional margin.
Using45milliohm for the room-temperature calculation and
5mA input load gives only0.225mV drop. BSP input remains about4.812V,
above4.5V. The2.7mA BSP input bound published at7V is used only as a
conservative engineering screen for the lower5V input,not a manufacturer
all-voltage current guarantee. Adding the2.49k pull-down gives under5mA.

With GPIO VOH>=2.4V and VBE(sat)<=0.85V screen,the4.7k base resistor
supplies about0.326mA versus about1.1mA static collector current. The
MMBT3904's0.20V maximum is specified at10mA/1mA; applying it here at much
lower forced beta is an engineering derating,not an exact manufacturer test row.
Driver pair allocation12mA from5V remains within the existing0.1A rail budget.
Do not describe these estimates as measured or full-temperature guarantees.

Reset/HiZ GPIO ->10k pull-down ->NPN OFF ->PMOS gate pulled tosource ->BSP
input pulled LOW. Missing3.3V or missing5V also commands OFF under the
supervised power sequencing. At room temperature,PMOS IDSS1uA through2.49k
is about2.5mV; gate leakage10uA through4.7k is47mV,below its0.4-V minimum
threshold. MCU deliberately HIGH during5V ramp can turn the load on; firmware
must initialize both GPIOs LOW. No false promise of autonomous startup sequencing.

First test without external load power: reset,debug halt,3.3V-only,5V-only,
normal power-up/power-down. Measure each BSP IN relative to **its localSOURCE**:
OFF close to0V;ON>=4.5V including ripple. Verify5V driver rail>=4.8125V.
Only then attach current-limited24V and a resistive load,initially<=0.5A/channel.
BSP0.675ohm maximum at the cited5V condition gives0.169W at0.5A;
208C/W minimal-board screening gives about35C rise. Real copper/ambient must
be checked; drain copper is the manufacturer thermal area,not a presumed drain tab.
Do not assume the single-pulse550mJ inductive figure permits repetitive loads.
Verify the real inductive energy/rate before such loads; no extra clamp is silently added.

### F. Practical verification checklist

- [ ] No SN74 translator remains in the populated DO path; both discrete channels match the table.
- [ ] Functional pin IDs and physical TOP-view positions match the three manufacturer drawings.
- [ ] SOURCE and SOURCE TAB share the external/common return; neither is DRAIN.
- [ ] Both GPIO10k pulls,base4.7k,gate100ohm,gate-source4.7k and output2.49k are present.
- [ ] External load positive and source-return connector are explicit; no FIELD_COM/EF_RTN bond.
- [ ] Native net readback/ERC after local migration; source-library availability alone is insufficient.
- [ ] Reset/partial-power OFF and loadedON>=4.5V verified before energizing loads.

Required nets: DO1,DO2,DO1_GATE,DO2_GATE,DO1_DRIVE,DO2_DRIVE,
DO1_DRAIN,DO2_DRAIN,DO_EXT_PLUS,5V,GND. FIELD_COM,EF_RTN andCHASSIS
are excluded from the DO return network.


## 11. Current closure and preserved history

Current decisions are the2026-11-08 sections above and the [closure report](electrical_closure_rev1.md). Earlier TPS/NIS recovery,discrete graphics,BSP physical closure,andEthernet75ohm/1nF reports remain historical evidence. They do not restore translator approval or a missing-BSP-pinout claim. FourETH_RBOB remainCRCW080575R0FKEA/C844859;twoETH_CBOB remainC1206C102KGRACAUTO/C600002. Their two AC return nodes stay separate. No FKEAC substitution or safety-Y certification is inferred. Conditional CFF,optional RS surge,CAN bulk and DI-PE positions are DNP in the selected basic prototype. Full inventory/readback and pending work are linked from the closure report.

## 15. Exact native completion sequence and connector implementation

This section describes required actions,**not completed native edits**. Latest
successful native read:5sheets,108components,453pins. Source snapshot and complete
pin memberships are in `evidence/autonomous_closure/`. Existing SWD/PHY ESD,
100k feedback uppers,separateB3_SW/B5_SW,correctRJ45 TX- and TDS3311 identity
are user changes already present;do not undo them using the older106-component audit.

### A. Before applying local corrections

Use `Industrial_Gateway_Academic.PrjPcb`,including Power,MCU,Ethernet,Field_IO,
TopLevel. Preserve a fresh copy of the sheets;the mission backup is
`hardware/academic_rev1/backups/autonomous_20261108T195741Z/`. Reopen/update
project-local libraries only after discarding no unsaved user work. No global
library update. The source R/C pins remain8units/80mil;new models must be placed
at their actual pin tips,not assumed to fit the older long-pin instances.

### B. Power.SchDoc: fix before any power test

| Existing item | Smallest required action | Verification |
|---|---|---|
| U1 UVLO2/OVP3/R3 previously allOVP | One wire was saved shorter and aUVLO label added. Recompile:768k R1 must beIN-to-UVLO;33.2k R3 UVLO-to-OVP;30.1k R4 OVP-to-EF_RTN. U1.2 and.3 must be different nets. Do not assume cachednet readback is fresh. | Distinct compiled memberships:U1.2+R1low+R3high;U1.3+R3low+R4high. |
| C16=4.7uF16V onprotected24V | Replace with selected C5750X7R2A475K230KA100V. | Read actualMPN/rating and pin nets after replacement. |
| C7=TORCH CC2220X7S100V156MN15u100V | Preserve its library symbol/history. Selected production-of-prototype BOM remains the verifiedTDK bank;replace this native instance locally with TDK,then add the secondTDK in parallel. TORCH exactX7S/land/DCbias evidence is incomplete. | Each buck has **two4.7u100V TDK** parts,not one unqualified nominal-equivalent. |
| Main input banks | Add one extraTDK4.7u100V in parallel at each buck (4total),plus existing separateTPS4.7u100V input bypass. | Both banks independently meet the documented effective-C screen. |
| C12/C21=Samsung1uF | Replace with C0805C225K5RACTU2.2uF50V X7R. | Each localVCC5-to-GND;never tosystem5V. |
| U2.3 andU3.3 open | U2.3-to-U2.12/B3_SW;U3.3-to-U3.12/B5_SW. | No sharedSW and noSW-to-GND. TI pin table explicitly requests thisNC connection. |
| R6/R9 PG pull-ups | **Remove/DNP before power.** They currently pullPG towardprotected24V. TI SNVSB49D p5 permits18V operating/22V absolute max onPG;nominal24V exceeds it despite100k series resistance. SelectedPG unused:remove the two instances or use an actualDNP variant;U2.8/U3.8 then intentionalopen. | No populatedPG-to24V pull-up. This is a real rating violation,not cosmetic. |
| C11/C20 feedforward | Selected captureDNP;retain only as explicitDNP positions or remove. |100k feedback top/43.2k and24.9k bottom preserved. |

R5/R8 are already100k in the current sheet. Both VIN2/10 andEN9 are already
on the protected native24V net. Do not repeat the obsolete sharedSW/isolatedVin
repair from the older audit. InputTPS13.3k/10nF/latch-off selection is unchanged.

### C. MCU.SchDoc: complete bypass/recovery without pin reassignment

1. C30.1 is currently a single-pin net;connect it to3.3V,retain C30.2=GND.
   Its saved electrical endpoint is(3200,4380)mil;use electrical pin readback,
   not a wire drawn near the body. Five existingVDD100nF capacitors C22,C31,
   C32,C26,C35 already span3.3V/GND.
2. Compared with the selected bank quantities,the MCU sheet has **two1uF
   instead ofthree** and **eight100nF instead ofnine**,includingNRST and the
   danglingC30. Add one CL10A105KB8NNNC1uF and one C0603C104K5RACTU100nF
   to3.3V/GND for the remaining VBAT/analog bank. Retain independent local
   placement at each relevant pin;shared net names do not replace decoupling.
3. Keep U4.48/.73=VCAP with C33/C34=2.2uF-to-GND;keep VCAP off3.3V.
4. Preserve actualJ3 pinout1SWDIO,2GND,3SWCLK,4NRST,5GND,6VTref.
   Assign exact61300611121/headerfoot after a local pin-map comparison.
5. SW1 is aBOOT0-to3.3V recovery switch,not NRST. For a verified PCB model,
   migrate that function to61300211121:1BOOT0,2=3.3V,normallyOPEN;retain R11
   10k pull-down. No permanent shunt during normalboot. Optional onboardNRST
   button isDNP;J3.4-to-J3.5 permits debugger or momentary external reset.
   Do not invent a four-pad tactile pin mapping or renameSW1 asreset.

### D. Ethernet.SchDoc: isolation,ESD and external buses

- C46 andC52 cable-termination return pins currently reach logicGND. Move
  those two return pins to **CHASSIS** and join J2.S1/S2 toCHASSIS. Their
  other ends remain independentA/B termination nodes. This implements the
  already selected cable/chassis boundary;do not add a DC logic-ground bond.
- D? TPD4E05U06DQAR is present,not missing. Annotate a unique designator.
  Explicit external feed-through pairing: **1/10=TXP,2/9=TXN,4/7=RXP,
  5/6=RXN;3/8=GND**. Datasheet Table4-2/flow-through application drawing:
  far-side pins calledNC are not assumed internally connected. These same-net
  assignments implement the selected flow-through PCB routing. PresentMDI
  nets already connect PHY andmagnetics;floatingNC pads alone do not prove
  a broken signal or absent shunt protection. Never use an internalNC connection
  as a wire. The rounded lands/reducedGND paste windows are now source-verified;
  confirm assembler DFM for0.20mm lead lands and the0.10mm stencil example.
- Preserve J2.2=TX- andT1.14=TX- (already corrected),notTX+.
- Place RS/CAN terminal blocks and optional bus-end jumper/resistor from the
  exact table below. Their bus pins are currently single-pin native nets.
- Do not reassign MCU RMII/UART/FDCAN ports. Verify existing flat cross-sheet
  memberships after any rename. CAN STBY internal pull-up holds standby;
  software releases it only after supplies/controller are ready.

### E. Field_IO.SchDoc: isolation and output completion

- **Critical:** disconnect only R21.2/R22.2 from ISO OUT1/OUT2/MCU DI nets.
  Keep ISO U8.4-to-U4.PE4/3 andU8.5-to-U4.PE5/4 connections intact.
  Connect R21.2 toexternalFIELD_DI1_PLUS andR22.2 toFIELD_DI2_PLUS.
  R21.1 staysSENSE1/U8.16;R22.1 staysSENSE2/U8.11.
  The saved free-end coordinates are(4430,5100)/(4430,5000)mil.
- R20=562ohm remainsIN1/U8.15-to-SENSE1;R23=562ohm remainsIN2/U8.10-to-SENSE2.
  Each10nF filter isSENSE-to-FIELD_COM. U8.9/.14=FIELD_COM;U8.1/.8=GND;
  U8.2/.3=3.3V;NC6/7 open. LabelSUB12=`ISO_SUB2`,SUB13=`ISO_SUB1`;use separate floating2x2mm islands,
  each connected only to its own substrate pin,not FGND/GND/eachother
  (TI SLLSEY7G Table4-2 p4). No galvanic-domain bridge.
- U10/U11 currently have all eight terminals unwired. Implement **all** of
  section10,including the four new transistors,external supply connector and
  both SOURCE TAB returns. DefaultOFF cannot be established by absent wires.

### F. Exact connector/contact assignments

All TB002 contacts use project pin1 atleft in PCB TOP view,wire-entryfront=-Y,
sequence+X. The manufacturer provides the5mm/1.30mm hole layout;numeric net
polarity is this project's convention and must be printed on silk/checked with
the physical connector. Saved2.20mm copper annuli/mask+.10mm are prototype
process choices;TH paste is disabled. Wurth headers have1.10mm holes at2.54mm
pitch,1.80mm copper pads,markedpin1 atleft/sequence+X;TH paste disabled.

| Role / exact MPN | Pin1 | Pin2 | Pin3 / treatment |
|---|---|---|---|
| J_IN TB002-500-02BE |external18..30V+ toF1|sourceGND|none;noPE terminal claimed|
| RS TB002-500-03BE |A/U6.6|B/U6.7|COM=GND/U6.5|
| CAN TB002-500-03BE |CANH/U7.7|CANL/U7.6|COM=GND/U7.2|
| DI TB002-500-03BE |FIELD_DI1_PLUS/R21.2|FIELD_DI2_PLUS/R22.2|FIELD_COM/U8.9/.14|
| DO_SUPPLY TB002-500-02BE |external24Vpositive|DO return=GND|outside electronics eFuse|
| DO1/DO2_LOAD TB002-500-02BE |DO_EXT_PLUS|respectiveBSP.D|external load between1/2|
| BOOT61300211121 |BOOT0/U4.94|3.3V|normallyOPEN|
| RS termination61300211121 |A|RT_RS.1|RT_RS.2 toB;normallyOPEN|
| CAN termination61300211121 |CANH|RT_CAN.1|RT_CAN.2 toCANL;normallyOPEN|

Both optional termination resistors: **CRCW1206120RFKEA**,120ohm1%,0.25W at70C,
symbol`CRCW1206120RFKEA`/foot`GW_CRCW1206_VISHAY_20035_REFLOW`.
Vishay20035p9 REFLOW1206:1.05x1.80mm lands atx=+/-1.275mm,innergap1.50mm,
body3.20x1.60mm. Enable only at a physical bus end;no permanent defaultshunt
or second split network. Header shunts are removable assembly accessories;
use an insulated2.54mm shunt with adequate contact rating,not a PCBfootprint.
5.174V full-rail differential screen gives0.226W at118.8ohm;normal differential
bus amplitude is lower. No24-V bus-fault withstand is inferred.

Sources: [Same Sky TB002 Rev1.04 pp1-2](../../hardware/academic_rev1/libraries/sources/autonomous_closure/tb002-500.pdf),
[Wurth61300211121 Rev003 p1](https://www.we-online.com/components/products/datasheet/61300211121.pdf),
[Wurth61300611121 Rev004 p1](https://www.we-online.com/components/products/datasheet/61300611121.pdf),
[Vishay20035 p9](../../hardware/academic_rev1/libraries/sources/ethernet_75ohm/C844859.pdf).
Wurth PDFs were inspected through the official web source;local downloads were
not available. No fake localPDF link is supplied.

### G. TopLevel/hierarchy,library transfer and release

Four sheet symbols still have placeholderFileName/Designator. Assign actual
Power.SchDoc,MCU.SchDoc,Ethernet.SchDoc,Field_IO.SchDoc and unique sheetIDs
after matching their displayed function. The project isFlat;do not switch it to
hierarchical to silence errors. Verify compiled port connectivity rather than
matching labels visually. Keep all accepted MCU pad reservations.

After local corrections:save,reopen,compile,runERC,and read actual pin/net
memberships for every modified circuit and cross-sheet interface. Verify exact
MPNs/DNP and model links before a PCB ECO. Compile LibPkg only when Altium
is available;existingIntLib must not be treated as the updated76/48 inventory.
TPS EP mapping and candidate package/assembly checks must precede placement
of those components. Full routing/manufacturing readiness is **NO** until these
native checks and the current circuit repairs are complete. No empty-boardDRC
or text-only validator can substitute for them.
