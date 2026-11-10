# Academic Gateway Rev. 1 — manual schematic construction guide

Current baseline: **2026-11-07**. This is the primary construction reference for
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
|Magnetics/RJ45|HX1188FNL + SS-7188S-A-NF|Signal map ready; chassis policy open|Resistor/capacitor models saved|Chassis treatment; physical layout |
|RS-485|THVD1420DR,115200baud|Basic circuit ready|Saved model; connector candidate|Exact connector; end termination only if required |
|CAN-FD|ATA6561-GAQW,1/2Mbit/s|Basic node ready|Saved model; connector candidate|Exact connector; optional end termination |
|Two DI|ISO1212DBQR,Type3|Normal18–30V sensing ready|Saved candidate models|Connector; preserve substrate/isolation domains |
|Two DO|BSP75NTA + translator candidate|Role diagram only; numbered circuit held|BSP footprint missing|Diodes terminal numbering and guaranteed loaded drive≥4.5V |

Use project-local `hardware/academic_rev1/libraries/Gateway_Academic.SchLib` and
`.PcbLib` (saved readback: **66 symbols /37 footprints**). LibPkg references these
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
External DO load supply is not `24V_ELEC`,3V3 or5V; see section 10.

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
| IN_J / 1 / Conector entrada | JL126-50002G01; 2 polos + politica PE | >=30 V continuo mas transitorios; corriente TBD; TBD; TBD | `GW_JL126-50002G01_16238e52` / `GW_CAND_CON_2x1_TH_5MM` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
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
Never connect RTN/support components to GND_PWR. Never connect VCAP/3V3/5V to RTN.
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

**CAD unfinished:** candidate `GW_DRC0010J_TI_TPS2662` has0.5mm lead pitch,
0.60×0.24mm lead lands, central1.65×2.40mm EP and four0.25×0.50mm extensions.
The extensions remain separate unassigned copper regions; library pads normally
have no net, but these regions do not yet have proven pad 11 net inheritance.
Finish native custom-pad 11 conversion or verified EF_RTN assignment, R0.05 corners
and mask/paste review before PCB use. EP is never GND_PWR. Use windowed paste;
TI's stencil example is approximately80% coverage at0.125mm thickness. Optional
thermal vias need assembler treatment, not automatic insertion. This does not block
source-backed symbol connections. Input terminal exact numbered polarity is also pending.

### F. Construction verification

- [ ] F1 series, D_REV both anodes present, TDS shunt after diode.
- [ ] TPS pin 5 and EP11 on EF_RTN; pin 6 on GND_PWR; no external short between them.
- [ ]13.3kΩ pin 7-to-RTN;10nF pin 8-to-RTN; three-resistor ladder order correct.
- [ ] Local input bypass returns to GND_PWR; both buck input banks retained.
- [ ] FLT and SHDN intentionally open; latch-off/manual-reset behaviour recorded.
- [ ] Protected24V_ELEC feeds electronics only; DO supply and FIELD_COM stay separate.
- [ ] TPS footprint candidate and connector numbering remain visible practical tasks.


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
- PCB guidance: **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**; RNX0012A package/board/stencil drawing **PDF pp44-46**, RNX0012B **pp47-49**. A/B footprint choice and stencil remain provisional.
- Inductor datasheet/layout: `EC/xal4000.pdf`, Coilcraft **document 806 Rev02/25/26**, **p1** XAL4030-682MEC row, **p4** Recommended Land Pattern and marked-end guidance. The 25-C typical saturation criterion is not a hot guarantee.
- Later source closure: [TDK exact input sheet](../../hardware/academic_rev1/libraries/sources/academic_freeze/TDK_exact.pdf),p1lands/p2bias, and [academic capacitor decisions](evidence/input_protection_freeze/bom_decisions.json) supersede the earlier403/missing-land statements. Output lands and exact saved model bindings are in the current mapping.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_LMR36015FBRNXR / 1 / 3.3-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B3_L / 1 / power inductor | XAL4030-682MEC; 6.8 uH | Isat25C 3.6 A; Irms20C 3.0 A; 20%; XAL4030 | `XAL4030-682MEC` / `GW_XAL4030_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| B3_CIN / 2 / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF | 100 V X7R; 10%; 2220 | `C5750X7R2A475K230KA` / `GW_C5750_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V X7R; 10%; 0805 | `C0805C224K1RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF | 16 V X7R; 20%; 1210 | `C3225X7R1C156M250AB` / `GW_C3225_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B3_CVCC / 1 / local supply bypass | C0805C225K5RACTU; 2.2 uF | 50 V X7R; 10%; 0805 | `C0805C225K5RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B3_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B3_RFBB / 1 / lower feedback resistor | RC0603FR-0743K2L; 43.2 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0743K2L_a8308c0c` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B3_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; CONDITIONAL |
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
| 7 FB | Junction of RFBT 100 k from **3V3 after the inductor** and RFBB 43.2 k to AGND/GND. Neither VIN nor SW is the sense point. |
| 8 PG | Unused/open, deliberately marked NC. No pull-up is populated in this selected circuit. |
| 9 EN | 24V_ELEC directly; do not float. No external 18-V UVLO network selected. |
| 10 VIN | 24V_ELEC; second local 220-nF bypass to PGND11. |
| 11 PGND | GND and short local HF return. |
| 12 SW | XAL4030-682MEC switching end and NC3/CBOOT return. **Not a ground exposed pad.** |

Inductor other end -> `3V3`; three selected 15-uF COUT parts -> GND there. Optional CFF 20 pF, if later approved, goes **across RFBT**, output-to-FB. Main CIN bank is independent of the 5-V converter and must provide >=4.7 uF effective over actual bias/temperature. Table 10-1's **COUT columns explicitly say RATED CAPACITANCE**: retain 3 x 15 uF nominal without claiming 45 uF effective. Export `3V3`/`GND` to MCU, PHY, RS-485, CAN VIO, ISO logic, oscillator supplies and provisional translator VCCA. No output-enable/reset/boot pin exists on this regulator beyond EN; do not invent one.

### E. Remaining practical work

- Capture values/quantities are selected; no missing CIN count or CVCC replacement gate remains.
- Confirm delivered RNX0012A/B package and stencil before PCB use; neither SW12 nor NC3 is ground.
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

24V_ELEC,3V3,B3_SW (pins3/12/BOOT return),B3_VCC_INTERNAL, B3_FB (pin 7),GND_PWR/GND.

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
| ACTIVE_LMR36015FBRNXR / 1 / 5-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B5_L / 1 / power inductor | XAL4040-103MEC; 10 uH | Isat25C 3.0 A; Irms20C 2.2 A; 20%; XAL4040 | `XAL4040-103MEC` / `GW_XAL4040_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| B5_CIN / 2 / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF | 100 V X7R; 10%; 2220 | `C5750X7R2A475K230KA` / `GW_C5750_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V X7R; 10%; 0805 | `C0805C224K1RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF | 16 V X7R; 20%; 1210 | `C3225X7R1C156M250AB` / `GW_C3225_TDK_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B5_CVCC / 1 / local supply bypass | C0805C225K5RACTU; 2.2 uF | 50 V X7R; 10%; 0805 | `C0805C225K5RACTU` / `GW_0805_KEMET_NOMINAL` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| B5_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B5_RFBB / 1 / lower feedback resistor | RC0603FR-0724K9L; 24.9 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0724K9L_10698e9e` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B5_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; CONDITIONAL |
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

Inductor other end -> `5V`; three selected 15-uF COUT to GND there. If later populated, 20-pF CFF parallels RFBT. Export `5V`/`GND` to CAN VCC and provisional translator VCCB. Maintain independent CIN/HF/VCC/BOOT banks and separate switching-node names for both converters. No buck oscillator synchronization pin or external frequency-setting network is selected.

### E. Remaining practical work

- Capture values/quantities are selected; no missing CIN count or CVCC replacement gate remains.
- Confirm delivered RNX0012A/B package and stencil before PCB use; neither SW12 nor NC3 is ground.
- At bring-up verify eFuse/buck startup, VCC, rail ripple/load steps and temperature under the stated allocations. This is functional confirmation, not industrial qualification.

### F. Review checklist

- [ ] RFBB is **24.9 k**, not the 3.3-V sheet's 43.2 k.
- [ ] Inductor is **10 uH XAL4040**, using the linked exact symbol.
- [ ] SW3/12, BOOT4, VCC5 and GND pins are not interchanged.
- [ ] B3/B5 internal VCC and switching nodes remain separate from each other and system rails.
- [ ] Independent VIN decoupling includes two 220-nF HF parts.
- [ ] CVCC is2.2µF50V X7R; confirm the stated prototype retention assumption at bring-up.
- [ ] COUT and CFF population reflect conditional qualification, not nominal-only stability approval.
- [ ] The 5-V output powers CAN/translator logic, not the 0.5-A field loads.


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
- Clock specification: `EC/KC2016Z25.0000C15XXK_e.pdf`, Kyocera **TNY1T-H1-DEX01-11**, **pp3-4** electrical/load/startup limits, **Table 2 p4**, **Figure 4 p6** terminal/land map and local **10-nF** bypass guidance. Exact nominal passive sheets are `SRC/passives/<MPN>.pdf`, except Samsung's retained HTML characterization; no exact reset/header MPN drawing is available.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_STM32H723VET6 / 1 / LQFP100 MCU | STM32H723VET6 | 3.3-V selected supply; DS supply/voltage-scale/temperature limits; internal LDO | `STM32H723VET6` / `GW_LQFP100_ST_1L` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDD1 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDD2 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDD3 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDD4 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDD5 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CBULK / 1 / local bulk reserve | C0805C475K4RACTU; 4.7 uF | 16 V; X7R; 10%; 0805 | `GW_C0805C475K4RACTU_82374e08` / `GW_CAND_0805_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDDA1 / 1 / VDD local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVDDA2 / 1 / VDD local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVBAT1 / 1 / backup-supply bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVBAT2 / 1 / backup-supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVREF1 / 1 / reference bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVREF2 / 1 / reference bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVCAP1 / 1 / internal-LDO output capacitor | C0603C225K8RACTU; 2.2 uF | 10 V; X7R; ESR <100 mOhm; 10% candidato; ST permite 20%; 0603 | `GW_C0603C225K8RACTU_46503424` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CVCAP2 / 1 / internal-LDO output capacitor | C0603C225K8RACTU; 2.2 uF | 10 V; X7R; ESR <100 mOhm; 10% candidato; ST permite 20%; 0603 | `GW_C0603C225K8RACTU_46503424` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_CNRST / 1 / reset filter | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_RBOOT / 1 / BOOT0 pull-down | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| MCU_YHSE / 1 / MCU independent oscillator | KC2016Z25.0000C15XXK; 25 MHz active CMOS | 1.71..3.63 V supply; 3.3 V selected; load <=15 pF; total +/-30 ppm; 2.0x1.6 mm 4-pad | `KC2016Z25.0000C15XXK` / `GW_KC2016Z_KYOCERA` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| MCU_JSWD / 1 / six-position debug header | TBD; 6 posiciones | TBD; TBD; TBD | `GW_H_Male_6x1_TH_100mil_c0450d1e` / `GW_CAND_H_6x1_TH_100mil` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| MCU_SRESET / 1 / normally-open reset button | TBD; SPST-NO | TBD; TBD; TBD | `GW_Sw_PUSH_4.5x4.5x5.0xmm_0f078dd9` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| MCU_JBOOT / 1 / boot recovery access | TBD; 2 posiciones | TBD; TBD; TBD | `GW_H_Male_2x1_TH_100mil_f89d9046` / `GW_CAND_H_2x1_TH_100mil` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| MCU_COSC / 1 / oscillator bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |

CSV electrical statuses remain provisional for several nominal capacitors despite accepted connection functions. C0603C225K8RACTU VCAP capacitors require **ESR <100 mOhm** and application capacitance qualification. Samsung X5R parts are specified only to +85 C; do not infer that the conservative MCU current budget authorizes a hotter board. Header/button MPNs, mating orientation and exact terminal pairs are unresolved. The 10-k Yageo pull-down replaces the historical unqualified FOJAN identity. Crystal capacitors/resistor and LSE networks are DNP; no external analog ferrite is selected.

### D. Connection checklist

| LQFP100 pin(s) | Required connection |
|---|---|
| 11, 27, 50, 75, 100 VDD | 3V3; separate 100-nF local bypass at each pin, plus selected 4.7-uF bulk. |
| 10, 26, 49, 74, 99 VSS | GND. All five must be connected. |
| 21 VDDA; 19 VSSA | VDDA to 3V3 analog branch; VSSA to GND. 1 uF + 100 nF from VDDA to its ground reference. No unselected ferrite inserted. |
| 20 VREF+ | VDDA/3V3 analog branch with its 1 uF + 100 nF bank; VREFBUF disabled. No independent VREF- pin is invented. |
| 6 VBAT | VDD/3V3 with selected 1 uF + 100 nF; no battery. |
| 48, 73 VCAP | Internal-core LDO output domain, joined as the selected VCORE_CAP net with one local 2.2-uF-to-GND at each pin. No external load; never connect to 3V3. |
| 14 NRST | 100 nF to GND, SWD reset access. Normally-open reset button would short NRST to GND only after exact contact-pair model is known. Internal reset pull-up is used; no extra external pull-up selected. |
| 94 BOOT0 | 10 kOhm to GND and recovery access to 3V3. Header terminal numbering remains provisional; do not short 3V3 directly to GND. Commission boot option bytes. |
| 12 PH0/OSC_IN | MCU oscillator OUT3; HSE bypass. |
| 13 PH1/OSC_OUT | Explicit NC in bypass configuration. |
| 72 PA13; 76 PA14 | SWDIO bidirectional and SWCLK input from debugger; reserve debug function. |

MCU oscillator: **1 STANDBY -> 3V3; 2 GND -> GND; 3 OUT -> PH0 pin 12; 4 VCC -> 3V3**, 10 nF directly between 4/2. No crystal load capacitors. HSI provides initial boot while the oscillator starts (specified up to 5 ms).

Debug header is the **project-specific six-pin convention**: 1 VTref=3V3 sense, 2 SWDIO, 3 GND, 4 SWCLK, 5 NRST, 6 GND. VTref is not a power input. This is not an ARM-standard keyed pinout; exact header/mating orientation is still unqualified.

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
| PE2 / 1; PE3 / 2 | DO1/DO2 reservations only | GPIO; **BLOCKED DO implementation** | Translator2/3 candidate |

PD10 is **not** USART3 hardware DE: the alternate function there is USART3_CK. PD11 is not an active UART flow-control input in this design. USART3 hardware RTS/CTS/synchronous clock are not selected. Keeping UART3 on PD8/9 avoids PB11/12/13 Ethernet conflicts. FDCAN1 is PD0/1, not the FDCAN2 functions on PB12/13. Do not enable MII, FMC, LCD, OCTOSPI or trace functions over reserved pads. PHY-facing MCU pins must remain HiZ through strap sampling; dedicated reset and initial clock sequencing require firmware review.

Remaining unused package pads (source Table 7; no new GPIO assignments): PC13 (7); PC14 (8); PC15 (9); PC0 (15); PC2_C (17); PC3_C (18); PA0 (22); PA3 (25); PA4 (28); PA5 (29); PA6 (30); PB0 (34); PB1 (35); PB2 (36); PE8 (38); PE9 (39); PE10 (40); PE11 (41); PE12 (42); PE13 (43); PE14 (44); PE15 (45); PB10 (46); PB14 (53); PB15 (54); PD12 (59); PD13 (60); PD14 (61); PD15 (62); PC6 (63); PC7 (64); PC8 (65); PC9 (66); PA8 (67); PA9 (68); PA10 (69); PA11 (70); PA12 (71); PA15 (77); PC10 (78); PC11 (79); PC12 (80); PD2 (83); PD3 (84); PD4 (85); PD5 (86); PD6 (87); PD7 (88); PB3 (89); PB4 (90); PB5 (91); PB6 (92); PB7 (93); PB8 (95); PB9 (96); PE0 (97); PE1 (98). Leave them unwired with explicit unused handling; firmware should select a defined low-power/analog state as appropriate, preserving SWD, oscillator and boot reservations. Do not add SMPS, VDDLDO, VDD50USB or VDD33USB pins absent from this package.

### E. Open engineering decisions

- **Does not prevent core initial capture:** VCAP ESR/bias and other capacitor effective values; MCU oscillator complete <=15-pF receiver/route/pad/probe budget. Clock startup/PLL/voltage-scale configuration is not implemented or approved here.
- **Prevents exact accessory completion:** reset-switch contact numbering/footprint, SWD/boot MPNs and orientation. Keep NRST and boot recovery accessible in the drawing; do not invent physical pairings.
- **Final electrical/physical approval:** rail/reset startup including PHY hold/release, BOOT option bytes, actual temperature/copper and decoupling geometry. PHY phase noise concerns the separate PHY oscillator; it does not block MCU power/debug capture.

### F. Review checklist

- [ ] Exactly the five VDD/five VSS pins and VDDA/VSSA/VREF+/VBAT are connected for LQFP100.
- [ ] VCAP48/73 have two local 2.2-uF parts, no 3V3 connection and no external load.
- [ ] Each VDD has its own bypass; analog/backup/reference banks are not silently omitted.
- [ ] PH0 receives its own 25-MHz CMOS oscillator; PH1 and crystal-load parts are unused.
- [ ] PHY's 50 MHz reaches PA1, without merging with the HSE net.
- [ ] AF11 RMII, PD8/9 AF7 and PD0/1 AF9 agree with the table; PD10/11 stay GPIO.
- [ ] BOOT0 is pulled low with recovery access; NRST filter/debug access remains usable.
- [ ] SWD header is labelled with its project pinout, VTref sense and mating orientation hold.
- [ ] No missing MCU package power pins have been inferred from a different STM32 variant.
- [ ] Blocked DO ports remain reservations, and PHY pads remain HiZ during bootstrap sampling.


### G. Required net labels

3V3,GND,VCORE_CAP,NRST,BOOT0,SWDIO,SWCLK,MCU_HSE25 plus the peripheral reservation labels in the table.

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
| ACTIVE_DP83826IRHBR / 1 / Ethernet PHY | DP83826IRHBR | 3.3-V analog and I/O supplies; RHB32+GND EP; RMII Leader 10/100 Ethernet | `DP83826IRHBR` / `GW_RHB0032M_TI` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDA3V3_HF / 1 / VDDA3V3 local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDA3V3_10N / 1 / VDDA3V3 local bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDA3V3_1U / 1 / VDDA3V3 local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDA3V3_10U / 1 / VDDA3V3 local bypass | CL21A106KAYNNNE; 10 uF | 25 V; X5R; -55..85 C; 10%; 0805 | `GW_CL21A106KAYNNNE_c6e24382` / `GW_CAND_0805_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDIO_HF / 1 / VDDIO local bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDIO_10N / 1 / VDDIO local bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDIO_1U / 1 / VDDIO local bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CVDDIO_10U / 1 / VDDIO local bypass | CL21A106KAYNNNE; 10 uF | 25 V; X5R; -55..85 C; 10%; 0805 | `GW_CL21A106KAYNNNE_c6e24382` / `GW_CAND_0805_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_CEXT / 1 / PHY external capacitor | C0603C202J5GACTU; 2 nF | 50 V; C0G; 5% seleccion; 0603 | `GW_C0603C202J5GACTU_fa733a70` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_RBIAS / 1 / PHY bias resistor | RC0603FR-076K49L; 6.49 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-076K49L_f42a9329` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_RRMII / 1 / RMII strap pull-up | RC0603FR-072K49L; 2.49 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-072K49L_b905c5f0` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_Y25 / 1 / PHY independent oscillator | KC2016Z25.0000C15XXK; 25 MHz active CMOS | 1.71..3.63 V supply; 3.3 V selected; load <=15 pF; total +/-30 ppm; 2.0x1.6 mm 4-pad | `KC2016Z25.0000C15XXK` / `GW_KC2016Z_KYOCERA` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| ETH_COSC / 1 / oscillator bypass | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |

Each of VDDA3V3 and VDDIO retains **10 nF + 100 nF + 1 uF + 10 uF** locally; Samsung X5R upper temperature is +85 C. No analog ferrite or strap LEDs are selected. MDIO uses the device's internal 10-k pull-up unless a later rise-time review justifies a change; no external MDIO resistor is in the selected BOM. CEXT is the 2-nF C0G candidate, not the EVM's older 100 nF.

### D. Connection checklist

| PHY pin | Connection / reset handling |
|---|---|
| 1 ModeSelect | NC; internal HIGH selects ENHANCED. Not GND. |
| 2 CEXT | 2 nF to logic GND. |
| 3 VDDA3V3 | 3V3 and its own four-capacitor local bank to GND. |
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
| 17 VDDIO | 3V3 and its own four-capacitor bank to GND. |
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

Oscillator **1 -> 3V3, 2 -> GND, 3 -> XI9, 4 -> 3V3**, with local 10 nF between 4/2. Both clocks remain independent. Reset LOW >=25 us; wait >=2 ms after release and >=50 ms after power-up before SMI, accommodating <=5-ms oscillator startup and 0.5-50-ms supply-ramp requirement. Do not assume RMII clock while reset is asserted. Read back straps during commissioning. Internal pulls are accepted only with all external/MCU loads respecting strap levels; add no guessed resistor network.

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

3V3,GND,PHY_XI25,PHY_nRESET,ETH_RMII_REF_CLK,ETH_MDIO,ETH_MDC and RMII data/control labels from section 4; PHY_XI25 is not MCU_HSE25.

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
| ETH_TMAG / 1 / Ethernet transformer | HX1188FNL; 1:1; 350 uH candidato | HPOT >=1500 Vrms; limites tabla9-1; Relacion +/-2%; Pulse16 SMT 12.7x9.09 mm | `HX1188FNL` / `GW_HX1188FNL_PULSE` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_CCT / 4 / PHY-side center-tap bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_RBOB / 4 / cable-side termination | CRCW080575R0FKEA; 75 Ohm | 150 V limiting element; actual75Ohm continuous voltage limited bysqrt(P*R); 1%; 0.125 W at70C; derating applies; 0805 resistor | `CRCW080575R0FKEA` / `GW_CRCW0805_VISHAY_20035_REFLOW` | ELECTRICAL_VERIFIED; CAD_VERIFIED; REQUIRED |
| ETH_CBOB / 2 / chassis AC return | C1206C102KGRACAUTO; 1 nF | 2000 V; X7R; safety class unverified; 10%; 1206 | `C1206C102KGRACAUTO` / `GW_C1206_KEMET_C1076_DENSITY_B` | PROVISIONAL; CAD_VERIFIED; REQUIRED |
| ETH_JRJ45 / 1 / shielded Ethernet jack | SS-7188S-A-NF; 8P8C shielded | TBD; TBD; CT710001 B0 through-hole | `SS-7188S-A-NF` / `GW_SS7188SANF_STEWART` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_DESD / 1 / PHY-side ESD array | TPD4E05U06DQAR; 4 canales baja C | TBD; TBD; DQA USON10 | `TPD4E05U06DQAR` / `GW_DQA0010A_TI` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |

75-Ohm parts are 1%, 0.125 W per current BOM; application pulse/safety limits remain to be checked. HV capacitors are 1 nF, 10%, 2 kV X7R candidates, not automatically Y-class. Both75Ω and1nF2kVDC models are now verified; the application does not acquire safety-Y certification from a voltage rating. Historical compiler warnings are not current validation. Jack contact/current ratings remain unqualified despite its accepted pin map; copper annuli/holes and assembly stock are not approved. No four external 49.9-Ohm MDI resistors, no C61/R51 logic/chassis coupling, no PoE implementation are selected.

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
| ACTIVE_THVD1420DR / 1 / half-duplex bus transceiver | THVD1420DR | 3.3 V selected / 3.0-5.5 V recommended; bus common mode -7 to +12 V; bus absolute +/-16 V | `THVD1420DR` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| RS_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| RS_RT / 1 / conditional bus-end termination and open-default jumper | TBD; 120 Ohm si Z0=120 Ohm | >=3.3 V continuo; falla de bus aparte; 1%; >=0.25 W objetivo a70 C; 1206 candidato; no0603 0.1W | `MISSING` / `MISSING` | DERIVED_PENDING_REVIEW; CAD_BLOCKED; CONDITIONAL |
| RS_RDE / 1 / DE reset pull-down | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| RS_RRE / 1 / nRE reset pull-up | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| RS_RPULSE / 2 / conditional bus-line pulse resistors | CRCW0603010RJNEAHP; 10 Ohm | Pulse-proof segun ficha exacta; 5%; Pulsos por verificar; 0603 | `GW_CRCW0603010RJNEAHP_c8eb51d2` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_TVS / 1 / transient clamp candidate | CDSOT23-SM712; Asimetrica -7/+12 V candidata | TBD; TBD; SOT23 | `CDSOT23-SM712` / `GW_SM712_BOURNS` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos | TBD; TBD; TBD | `GW_MX126-5.0-03P-GN01-Cu-S-A_d57a488f` / `GW_CAND_CON_3x1_TH_5mm` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |

Selected basic capture omits the optional SM712/10-Ohm network; conditional positions remain unqualified. Termination is **120 Ohm only at a physical cable end** if bus Z0 is 120 Ohm; target >=0.25 W at 70 C, 1%, with fault/ambient review and exact MPN/jumper still unselected. Do not use a 0603 0.1-W resistor merely because 120 Ohm is available. Connector physical pin numbers/ratings are unresolved. No external bias is populated.

### D. Connection checklist

| THVD pin | Required connection |
|---|---|
| 1 R | Receiver output -> MCU PD9/56 USART3_RX. |
| 2 nRE | MCU PD11/58 GPIO; 10 kOhm pull-up to 3V3 holds receiver disabled at reset. |
| 3 DE | MCU PD10/57 GPIO; 10 kOhm pull-down to GND holds driver disabled at reset. |
| 4 D | MCU PD8/55 USART3_TX output -> driver input. |
| 5 GND | Logic/common bus-reference GND; no galvanic isolation claimed. |
| 6 A | Bus A connector functional terminal. |
| 7 B | Bus B connector functional terminal. |
| 8 VCC | 3V3, local 100 nF to GND5. |

Connector roles A/B/COM are selected; **numbered connector assignments await the exact drawing**. End-only 120-Ohm termination goes A-to-B through the open-default jumper. Basic selected line connections have no added series resistors. If the optional network is later qualified, use one 10-Ohm resistor in **each** line and SM712 bus pins1/2/reference3 per the exact source, with the intended return defined; do not silently insert it now. Transmit: assert DE, enable/disable receive deliberately, complete the final stop bit before releasing DE; receive: DE LOW, nRE LOW. MCU reset leaves both functions disabled. No mandatory external bias pull-up/down is missing because device fail-safe is retained.

### E. Remaining practical work

Finish connector physical numbering. If used at a cable end, select the120Ω termination MPN/jumper. Optional SM712/two10Ω network stays unpopulated and is not needed to draw the selected basic circuit.

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

RS485_TX (PD8),RS485_RX (PD9),RS485_DE (PD10),RS485_nRE (PD11),RS485_A,RS485_B,GND,3V3.

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
| ACTIVE_ATA6561_GAQW / 1 / CAN-FD transceiver | ATA6561-GAQW | VCC 4.5-5.5 V; VIO 2.8-5.5 V; SOIC8; selected 1/2 Mbit/s | `ATA6561-GAQW` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| CAN_CVCC5 / 1 / 5-V bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| CAN_CVIO3V3 / 1 / 3.3-V I/O bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| CAN_CBULK / 1 / local bulk reserve | TBD; 47 uF | 10 V minimo EVM; TBD; 1210 candidato | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| CAN_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos | TBD; TBD; TBD | `GW_MX126-5.0-03P-GN01-Cu-S-A_d57a488f` / `GW_CAND_CON_3x1_TH_5mm` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| CAN_RT / 1 / conditional bus-end termination and open-default jumper | TBD; 120 Ohm si Z0=120 Ohm | >=3.3 V continuo; falla de bus aparte; 1%; >=0.25 W objetivo a70 C; 1206 candidato; no0603 0.1W | `MISSING` / `MISSING` | DERIVED_PENDING_REVIEW; CAD_BLOCKED; CONDITIONAL |

Local bypasses are 100 nF each. End termination target is 120 Ohm/1%/>=0.25 W at 70 C with application/fault review; exact MPN, jumper and model unresolved. The retained optional 47-uF/10-V bulk is an EVKit candidate, **not selected mandatory population**. The 5-V regulator/distribution transient response decides whether local bulk is necessary. No external STBY resistor or split network is selected.

### D. Connection checklist

| ATA6561 SOIC8 pin | Required connection |
|---|---|
| 1 TXD | MCU PD1/82 FDCAN1_TX -> transceiver; internal 20-50-kOhm pull-up to VIO retains recessive. |
| 2 GND | Logic/nonisolated bus-reference GND. |
| 3 VCC | 5V, 100 nF to GND2. Recommended VCC 4.5-5.5 V. |
| 4 RXD | Transceiver -> MCU PD0/81 FDCAN1_RX. |
| 5 VIO | 3V3, separate 100 nF to GND2. This is **VIO, not NSIL**; do not tie to 5 V from an ATA6560 example. |
| 6 CANL | Connector functional CANL. |
| 7 CANH | Connector functional CANH. |
| 8 STBY | MCU PE7/37 GPIO; internal 75-175-kOhm pull-up to VIO holds standby while MCU HiZ. Drive LOW only after supplies/controller initialization. |

There is no exposed-pad 9 on the selected SOIC8 model. Optional 120 Ohm connects CANH-to-CANL through the open-default end-node jumper. Connector roles CANH/CANL/COM are selected, but exact physical terminal numbering is pending. No external TVS/choke/shunt capacitors are populated; no galvanic isolation is claimed.

### E. Remaining practical work

Finish connector physical numbering and optional bus-end120Ω termination/jumper. No additional TVS/filter or mandatory47µF bulk is selected. Confirm intended cable operation during functional tests.

### F. Review checklist

- [ ] Exact ATA6561 SOIC8 has VIO5=3V3, VCC3=5V and no fictitious EP9/NSIL.
- [ ] TXD1 comes from FDCAN1_TX and RXD4 reaches FDCAN1_RX.
- [ ] Each supply has a separate local 100-nF capacitor.
- [ ] STBY defaults HIGH/standby and is driven LOW only after initialization.
- [ ] CANH7/CANL6 are not swapped at the connector.
- [ ] Termination appears only at a cable end; no simultaneous 120-Ohm and split network.
- [ ] Optional bulk, bus capacitors, choke and TVS have not become mandatory by copying the EVKit.
- [ ] Cable timing and connector/fault ratings remain distinct from basic-node capture approval.


### G. Required net labels

FDCAN1_TX (PD1),FDCAN1_RX (PD0),CAN_STBY (PE7),CANH,CANL,3V3,5V,GND.

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
| ACTIVE_ISO1212DBQR / 1 / two Type3 field inputs | ISO1212DBQR | VCC1 2.25-5.5 V; 3.3 V selected; normal input 18-30 V; isolation and surge limits separate | `ISO1212DBQR` / `GW_DBQ0016A_TI` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DI_RSENSE1 / 1 / channel 1 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RTHR1 / 1 / channel 1 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| DI_CIN1 / 1 / channel 1 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RSENSE2 / 1 / channel 2 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RTHR2 / 1 / channel 2 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| DI_CIN2 / 1 / channel 2 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DI_CPE / 1 / unselected field-to-PE coupling | TBD; 500 pF candidato | 2 kV; seguridad por definir; TBD; TBD | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| DI_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos si COM comun | TBD; TBD; TBD | `GW_MX126-5.0-03P-GN01-Cu-S-A_8a7ef64c` / `GW_CAND_CON_3x1_TH_5mm` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |

MM204 1 kOhm/1% is 0.25 W at 70 C, derated to zero at 125 C; maximum working voltage 200 V and overload/surge limits remain separate. At 2.75 mA and R+1%, RTHR power is 7.64 mW and RSENSE power 4.29 mW: normal dissipation is acceptable within derating, but **surge is not qualified**. MM204 is not the pulse-enhanced MM204P. CPE 500 pF/2 kV is an **unselected conditional candidate**, not a required placement; extra DI TVS is DNP. No exact connector terminal numbering is approved.

### D. Connection checklist

| ISO1212 pin | Required connection |
|---|---|
| 1, 8 GND1 | Logic GND only. |
| 2 VCC1 | 3V3; 100 nF locally to logic GND. |
| 3 EN | Tie to VCC1/3V3; outputs continuously enabled. |
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

Finish connector physical numbering; keep SUB1/SUB2 floating separately and FIELD_COM isolated. Normal Type3 sensing is ready. No surge withstand is claimed or required by this academic task.

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

DI1,DI2,FIELD_COM,DI1_SENSE,DI1_IN,DI2_SENSE,DI2_IN,3V3,GND; do not share field/control returns.

## 10. SN74LVC2T45 and two BSP75N digital outputs.

### A. Selected configuration

**ACCEPTED scope:** two low-side BSP75NTA outputs, intended 0.5 A each from field supply. **PROVISIONAL drive candidate:** SN74LVC2T45DCTR, VCCA=3.3 V, VCCB=5 V, DIR=VCCA (A-to-B), 10-k pull-downs on both A and B channels. **BLOCKED:** BSP75N manufacturer-numbered Type DN terminals/footprint and guaranteed loaded >=4.5-V drive for full protected behavior. Do not proceed with numbered BSP wiring or represent the translator as an approved driver.

Exact source: gate **DO**, BOM `DO_*`, active mapping `ACTIVE_SN74LVC2T45DCTR` / `ACTIVE_BSP75NTA`. The prepared/active candidate is **DCTR/DCT8**. The two bypass parent labels were corrected from historical DCUR text; no package substitution or drive approval occurred.

### B. Official manufacturer sources

- Translator main datasheet: `DS/sn74lvc2t45.pdf`, TI **SCES516N**, [official datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf): **Table 4-1 p2** numbered DCT/DCU pins, **section 5.5 p6** loaded VOH, **section 7.4 p15** direction; application/reference **Figure 8-1 p16**, **section 8.3 p19** power-up, **sections 8.4.1-.2 pp19-20 / Figure 8-3 p20** layout. DCT0008A drawing **PDF pp28-30**. No OE pin exists.
- Switch main datasheet: `DS/BSP75N.pdf`, Diodes **DS33016 Rev7-2**, **p1** functional pinout/Source tab, **pp3-4** electrical characteristics including input current/4.5-V protection condition, **pp5-6** current/thermal/inductive behavior, **p8** package dimensions. **No manufacturer-numbered terminal assignment is present.**
- Package supplement: `EC/SOT223-Type-DN.pdf`, exact Diodes drawing; it adds dimensions but still does not close terminal numbering. No Infineon BSP75N terminal map may be transferred.
- Relevant application/reference guidance is the above translator Figure 8-1 and Diodes switch functional/thermal material; **no complete manufacturer evaluation schematic qualifies this exact translator-plus-switch combination**. No separate application note or PCB reference with a verified Diodes numbered mapping is available. Do not invent a figure number for the switch role sketch or treat the package drawing as missing-number evidence.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_SN74LVC2T45DCTR / 1 / candidate level translator | SN74LVC2T45DCTR | VCCA=3.3 V, VCCB=5 V; device supplies 1.65-5.5 V; loaded BSP drive NOT qualified | `SN74LVC2T45DCTR` / `GW_DCT0008A_TI` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| ACTIVE_BSP75NTA / 2 / protected low-side switch candidate | BSP75NTA | intended 0.5 A/channel; IN>=4.5 V for protected operation; Source tab; numbered map blocked | `BSP75NTA` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| DO_CVCCA3V3 / 1 / A-side bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DO_CVCCB5 / 1 / B-side bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DO_RPDA / 2 / logic-side reset pull-downs | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| DO_RPDB / 2 / drive-side reset pull-downs | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| DO_SUPPRESS / TBD / external inductive-load suppression if required | TBD; TBD | TBD; TBD; TBD | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; TBD |
| DO_JLOAD / 2 / load connectors | JL126-50002G01; 2 polos por canal | >=30 V y0.5 A/canal mas fallas; TBD; TBD | `GW_JL126-50002G01_ddbad43f` / `GW_CAND_CON_2x1_TH_5MM` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |

The BSP role-only symbol is an unfinished reference, excluded from numbered placement. Two 100-nF supply bypasses and four 10-k pull-downs are the retained candidate network. External inductive suppression, terminal ratings and any series input resistance are unselected; `DO_RSER` is DNP because arbitrary series resistance could further reduce drive. The rated 0.5-A design intention does not guarantee hot, simultaneous, repetitive or inductive operation.

### D. Connection checklist

**Reference-only translator pins; downstream protected-drive acceptance remains BLOCKED:**

| Translator pin | Intended connection |
|---|---|
| 1 VCCA | 3V3, local 100 nF to GND. |
| 2 A1 | MCU PE2/1 reserved DO1 output; 10-k pull-down to GND. |
| 3 A2 | MCU PE3/2 reserved DO2 output; separate 10-k pull-down. |
| 4 GND | Logic/nonisolated output-control return. |
| 5 DIR | VCCA/3V3 HIGH for A-to-B, not 5 V. |
| 6 B2 | Candidate DO2_DRIVE with 10-k pull-down -> switch2 IN role only. |
| 7 B1 | Candidate DO1_DRIVE with 10-k pull-down -> switch1 IN role only. |
| 8 VCCB | System 5V, separate local 100 nF to GND. |

For each BSP, **roles only, no numeric pins**: `IN` <- candidate drive; `DRAIN` -> load negative; load positive -> external DO supply positive (DO_EXT+); `SOURCE` and **SOURCE TAB** -> DO_EXT_RETURN connected to BSP source/logic GND_PWR return for the nonisolated control stage. Do not automatically use isolated DI FIELD_COM. High-current return must not traverse MCU analog/VCAP/PHY bias/FB return paths. Keep Source tab separate from Drain copper. No numeric BSP wiring may be inferred from these role labels.

At 5 V each BSP input can require up to 1.2 mA plus B-side 10-k pull-down current. Full protected operation requires input >=4.5 V. SCES516N section 5.5 only gives 3.8-V minimum at the 4.5-V/-32-mA loaded test point; the near-rail specification is at 100 uA. Interpolating to this actual load is not a guarantee. Startup OFF during partial rails/MCU HiZ also needs validation despite the translator's supply-sequencing features. No fake OE or unused channel exists; both translator channels are used.

### E. Remaining practical work

Hold numbered BSP capture until exact Diodes terminal numbering/Source-tab map and a required footprint exist. Loaded translator drive≥4.5V remains unproven. Define actual external load/return terminals; verify reset-OFF and intended thermal/inductive operation before energizing those loads.

### F. Review checklist

- [ ] DO remains visibly blocked until exact Diodes terminal numbers and a footprint are proven.
- [ ] Source tab is never assumed Drain or copied from another manufacturer's BSP75N.
- [ ] Translator identity/package matches the current DCTR/DCT BOM and mapping; no DCU substitute.
- [ ] DIR5 is VCCA HIGH for A-to-B; no OE pin is invented.
- [ ] Both supply bypasses and all four pull-downs are present in the candidate network.
- [ ] B1 drives output1 and B2 output2; both MCU pins remain the documented reservations.
- [ ] Guaranteed loaded drive, including pull-down current and rail tolerance, is checked against 4.5 V.
- [ ] Loads draw from the field supply; Source/current return does not merge isolated DI COM or quiet returns.
- [ ] Simultaneous thermal/inductive/fault conditions are bounded; no universal 0.5-A/550-mJ protection claim.

### G. Required net labels

DO1 (PE2),DO2 (PE3),DO1_DRIVE,DO2_DRIVE,DO_EXT+,DO_EXT_RETURN,3V3,5V,GND_PWR. External DO return is not FIELD_COM/CHASSIS/EF_RTN.

## 11. Construction closure and correction record

The old guide's SMBJ33A/VIN_PROT circuit, unselected fuse/bulk and missing
2220/1210 land statements are replaced by the selected TDS3311/TPS chain and
current exact-MPN capacitor models. NIS62kΩ/68pF settings are historical, not TPS
connections. TPS pin assignments/ladder were checked against Table 6-1/Eq 5–7;
no pin reversal was found in the latest TPS proposal. The1.19V application-prose
versus1.20V electrical-table discrepancy is explicitly resolved in section 1.

MCU power/VCAP/debug/boot/oscillator and peripheral pin tables were preserved;
there is no reassignment or added VDDLDO pin. Old compilation messages remain
historical evidence, not validation of current64/35 sources. No new ERC/DRC is claimed.

Remaining work that affects full component construction: exact connector/header/
button mechanics and numbered assignments; optional bus-end resistor/jumper selections only where termination is used;
BSP numbering/footprint and guaranteed driver voltage. TPS custom thermal pad and
RNX/other candidate assembly checks affect PCB completion, not the established
symbol wiring. Normal laboratory startup/ripple/temperature checks are bring-up
tasks; absent industrial certification is not a blocker.

Current source-record discrepancy: conditional CFF rows carry quantity1 as reserved
positions, while selected capture leaves them DNP pending application review.
Likewise optional RS surge, CAN bulk and DI-PE candidate rows are not mandatory
population. No BOM selection/quantity was silently changed in this documentation task.
Current75Ω CAD status is VERIFIED: retain CRCW080575R0FKEA, C844859, four instances. See [resistor closure](ethernet_75ohm_library_closure.md) for exact reflow geometry, sources and supplier-suffix distinction.

Metadata corrections only: IN_BULK/IN_HF descriptions now name TPS26620 instead
of NIS; DO supply bypass parent references now name the selected DCTR rather
than the obsolete DCUR text. MPNs, values, quantities and drive approval did not change.

Before marking a manually drawn sheet complete, check every power/ground/NC,
symbol-to-pad mapping, passive quantity and cross-sheet label against its section.
Run native ERC and compile libraries when actually performed; save actual results.
Do not propagate library edits to schematic/PCB automatically.

## 12. Ethernet75Ω library closure

Four ETH_RBOB instances use `CRCW080575R0FKEA` / `GW_CRCW0805_VISHAY_20035_REFLOW`, verified catalog code C844859. C1511836 is the different commodity C-suffix part and is not adopted. Conventional resistor pins1/2 map to pads1/2 (nonpolar). Copper lands0.95×1.45mm, inner gap1.00mm, centers1.95mm per Vishay20035p9 REFLOW. Mask+.05mm and1:1paste are explicit prototype process choices. Topology and all MCU/interface pins remain unchanged. [Local datasheet](../../hardware/academic_rev1/libraries/sources/ethernet_75ohm/C844859.pdf). Native compilation has not been performed for the current66/37 sources.

## 13. Ethernet1nF capacitor library closure

Both ETH_CBOB instances use `C1206C102KGRACAUTO` / `GW_C1206_KEMET_C1076_DENSITY_B`, C600002:1nF,10%,2000VDC,X7R,1206. KEMET C1076p10 Table3 densityB reflow pads1.15×1.80mm atx±1.50mm; body3.20×1.60mm. Pin1-to-pad1 and pin2-to-pad2 are nonpolar project conventions. Mask+.05mm and1:1paste are explicit process choices. Connect one instance nodeA-to-CHASSIS and the other nodeB-to-CHASSIS; do not join nodesA/B or logic GND. [Capacitor evidence](ethernet_1nf_library_closure.md). No safety-Y or industrial pulse/insulation certification is claimed.
