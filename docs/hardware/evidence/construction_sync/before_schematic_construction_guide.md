# Industrial Gateway - schematic construction reference guide

Evidence date: 2026-11-07. Academic revision only. The user draws the schematic, places components and routes the PCB. This document supplies references and review criteria; it authorizes no CAD operations. Original Rev. A is preserved.

Decision authority: [schematic_readiness_gate.md](schematic_readiness_gate.md), especially **Final architecture and permitted capture** and **Accepted decisions and exact evidence**; [passive_component_selection.md](passive_component_selection.md), November 7 capture revision; current [passive_bom.csv](passive_bom.csv), [final_bom.csv](final_bom.csv) and [cad_library_mapping.csv](cad_library_mapping.csv). The November 7 update and gate supersede historical November 6 unresolved lists in [altium_library_preparation_report.md](altium_library_preparation_report.md). Older baseline files are provenance, not current selections.

**ACCEPTED** means accepted configuration/connections for manual capture within the stated limits. **PROVISIONAL** means a retained candidate or an application/physical qualification still open. **BLOCKED** means the dependent connection, selection or completed sheet cannot be approved. These are separate from CSV electrical/CAD fields: `ELECTRICAL_VERIFIED` does not imply `CAD_VERIFIED`, and a saved `CAD_CANDIDATE` is not a fabrication-qualified component. Active mapping rows sometimes retain older `PROVISIONAL` fields; use the gate for operating-configuration authority and the mapping for actual model bindings.

All relative repository paths expand under `C:/dev/7mo/design/industrial-linux-gateway/`. Manufacturer datasheet directory **DS** is exactly `C:/dev/7mo/design/Datasheets_industrial_gateway/`. **SRC** is exactly `C:/dev/7mo/design/industrial-linux-gateway/hardware/academic_rev1/libraries/sources/`; **EC** is its `electrical_closure/` subdirectory. Thus `DS/lmr36015.pdf`, for example, denotes an exact local file, not a search term. PDF page numbers below are **one-based file pages** unless explicitly called printed pages. An HTML page has no fixed document page number. No unavailable page, figure or application note is invented.

All library names in component tables refer to `hardware/academic_rev1/libraries/Gateway_Academic.SchLib` and `Gateway_Academic.PcbLib`; `MISSING` is literal absence. Use the current 46-symbol/23-footprint source set or its matching `Project Outputs for Gateway_Academic/Gateway_Academic.IntLib`. These counts and links are saved Electronics AI reader evidence, not a new live inspection. No connectivity test, native compile, ERC, DRC or full repository audit was repeated for this guide.

The [PCB rules audit](pcb_design_rules_audit.md) is historical and **not ready to apply**. The later [manufacturer layout guide](manufacturer_layout_guidelines.md) records the preserved academic PCB document; the older audit's absence-of-board statement must not be treated as current. Neither report establishes an approved stackup, impedance geometry or configured native rules. Manufacturer layout guidance below is a future review requirement, not an applied rule.

| First four sheets in this guide | Readiness for manual work |
|---|---|
| 1. Input/protection | Partial topology/reference capture only. Fuse/bulk/clamp coordination and missing library resources prevent a completed protected-input sheet. |
| 2. 3.3-V buck | Verified IC/inductor/feedback topology can be drawn with explicit unresolved capacitor banks. Completed power sheet/BOM blocked. |
| 3. 5-V buck | Same limit; retained 1-MHz FPWM FB variant and 10-uH inductor. Completed power sheet/BOM blocked. |
| 4. MCU minimum hardware | CONDITIONAL GO; recommended first sheet to draw. Core pin/power/debug/boot mapping is accepted; oscillator load, capacitor application and physical header/button qualification remain. |

Six compiler warnings: [compiler_messages.json](evidence/electrical_closure/compiler_messages.json) contains six unsuppressed `Missing Component Models` messages without component identifiers. The following attribution is an **inventory-based inference**, not a compiler cross-probe: [compiled_inventory.json](evidence/electrical_closure/compiled_inventory.json) independently lists exactly six retained symbols with zero footprint links.

| Unlinked symbol | Relevance to the first four sheets |
|---|---|
| `GW_C5750X7R2A475K230KA_5f18f946` | Both buck CIN banks: real missing 2220 footprint; symbol-only capture possible, CAD completion blocked. |
| `GW_C3225X7R1C156M250AB_bb412b42` | Both buck COUT banks: real missing 1210 footprint; symbol-only capture possible, CAD completion blocked. |
| `GW_Sw_PUSH_4.5x4.5x5.0xmm_0f078dd9` | MCU reset button: physical button unfinished; core NRST/SWD circuitry may be drawn without inventing switch terminal pairs. |
| `GW_XAL4030-682MEC_71dfd711` | Superseded old unlinked inductor symbol. Use linked `XAL4030-682MEC` / `GW_XAL4030_COILCRAFT`; no remaining missing-model blocker for the selected 3.3-V inductor. |
| `GW_XAL4040-103MEC_b36cb917` | Superseded old unlinked inductor symbol. Use linked `XAL4040-103MEC` / `GW_XAL4040_COILCRAFT`; same distinction for 5 V. |
| `BSP75NTA` | DO sheet only; no direct first-four-sheet model blocker. Its fault/load assumptions still affect input-fuse coordination. |

Other absent resources are **not additional members of those six warnings**: input fuse, series-diode and TVS models and bulk selection are absent/unselected; input terminal and debug/boot headers have candidate geometry but unverified exact drawings/ratings. Both RNX package variants remain candidates pending delivered-package/stencil confirmation. Missing unused/DNP rows do not block accepted core capture.

## 1. Industrial power input and protection.

### A. Selected configuration

**ACCEPTED scope:** one protected 18-30-V DC input; no redundant ORing and no added LC input filter. **PROVISIONAL implementation:** positive input -> fuse -> series SS3P6L -> shunt unidirectional SMBJ33A and bulk -> `VIN_PROT`, feeding both bucks. **BLOCKED:** final protection/fuse/bulk selection and any claim of fault or industrial surge qualification.

Exact configuration source: gate **Power - calculations completed, capacitor/fault gates retained** and `IN_FUSE`, `IN_REVERSE`, `IN_TVS`, `IN_BULK`, `IN_FILTER`, `IN_J` in the current BOM/decision overlay. The topology is selected for prototype reference; neither protection MPN is released. Do not substitute devices appearing in other historical source directories.

### B. Official manufacturer sources

- Application/reference topology: [TDK-Lambda, What external components are required for a DC-DC converter?](https://www.us.lambda.tdk.com/resources/blogs/20250102.html), January 2, 2025: **Figure 5**, series reverse diode/fuse; **Input fuse (F1) and the input capacitor (C1)** and **Reverse input protection** sections. HTML, no page number. This is a DC-DC module example, not a completed gateway TVS/fuse design; do not copy its SOC fuse recommendation.
- Main rectifier datasheet: `SRC/SS3P6L_88987.pdf`, Vishay document **88987**, revision 24-Apr-2020: **p1**, polarity/package sketch and Maximum Ratings; **p2**, Electrical Characteristics/thermal information; **pp3-4**, current/temperature curves and dimensions. [Official document](https://www.vishay.com/docs/88987/ss3p6l.pdf).
- Main TVS source: [Littelfuse SMBJ33A official product page](https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj33a). The manufacturer's historical [SMBJ series datasheet](https://www.littelfuse.com/~/media/electronics/datasheets/tvs_diodes/littelfuse_tvs_diode_smbj_datasheet.pdf.pdf), revised 06/03/20, has the **Electrical Characteristics, SMBJ33A row** and **Figures 3-4**, pulse derating/waveform. Cached text was recoverable, but the PDF endpoint redirects to a missing page; **page numbers/current downloadable PDF remain unverified**. This does not close the gate's current-datasheet requirement. No local `SMBJ33A_Littelfuse_datasheet.pdf` is claimed to exist.
- Converter interface and layout: `DS/lmr36015.pdf`, TI **SNVSB49D**, **section 11 p33** (source/cable ringing, damping and TVS considerations), **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**. No selected manufacturer evaluation board implements this complete protected-input circuit. No separate input-protection application note or fuse datasheet is selected because the fuse is unresolved.

### C. Components to place

Treat this as a candidate/hold list; do not label an incomplete protection circuit approved.

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| IN_FUSE / 1 / positive-input fuse | TBD; TBD | Electrical rating TBD - unverified | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| IN_REVERSE / 1 / series reverse-polarity diode | SS3P6L-M3/86A; TBD | Electrical rating TBD - unverified; SMPC TO-277A | `MISSING` / `MISSING` | PROVISIONAL; CAD_MISSING; REQUIRED |
| IN_TVS / 1 / transient clamp candidate | SMBJ33A; TBD | Electrical rating TBD - unverified; SMB DO-214AA | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| IN_BULK / TBD / input bulk/damping bank | TBD; TBD | Electrical rating TBD - unverified | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| IN_J / 1 / field connector | JL126-50002G01; 2 polos + politica PE | >=30 V continuo mas transitorios; corriente TBD | `GW_JL126-50002G01_16238e52` / `GW_CAND_CON_2x1_TH_5MM` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |

The series diode's source rating is 60-V VRRM, 3-A average under its specified cooling conditions; 150-A nonrepetitive 10-ms half-sine is not a continuous or repetitive rating. SMBJ33A historical limits are 33-V standoff and 53.3-V clamp at 11.3 A for the specified waveform, not a guaranteed board-node maximum. Fuse current, interrupt voltage/current, time-current/I-squared-t and bulk voltage/ripple/ESR remain **TBD**. A 35-V bulk capacitor is not approved at this clamp node. The input connector has no approved terminal-number-to-polarity assignment yet.

### D. Connection checklist

1. Mark connector functional terminals `VIN_RAW+` and input return. **Do not invent JL126 pin numbers**; its exact numbered drawing and the candidate pad-Y offset must be resolved before assigning polarity.
2. Positive lead -> the single series fuse -> diode **anode terminals 1 and 2**; Vishay p1 identifies both as anodes. Diode **K/cathode** -> `VIN_PROT`. Do not translate the cathode label into an unverified footprint pad number or use a generic two-pad diode for this package.
3. Unidirectional TVS **cathode -> VIN_PROT**, **anode -> input GND** after the series diode. No numbered TVS model has been selected. Avoid a reversed TVS that forward-conducts during normal power.
4. Bulk positive -> `VIN_PROT`, negative -> input GND; quantity/value/polarity marking and rating are unresolved. Keep both separate local buck CIN banks; a remote bulk capacitor does not replace them.
5. Export `VIN_PROT` and common nonisolated `GND` to both buck sheets. Output-load power comes from the field supply, not from either regulated rail; leave its final protected distribution/fault boundary flagged until coordination closes.
6. Keep chassis/PE and DI `FIELD_COM` distinct from logic/input `GND`. No default PE bond is selected. No second supply ORing, extra LC filter, guessed UVLO divider or sustained-overvoltage disconnect is approved.
7. The selected series diode blocks reverse polarity; the TVS is not a disconnect for sustained overvoltage. Do not infer an 18-V turn-on threshold from EN=VIN on the buck sheets.

### E. Open engineering decisions

- **Prevents completed initial protection capture:** source current limit/cable and required fault/surge envelope; fuse MPN/interrupt and I-squared-t coordination; diode cooling/package suffix; TVS energy/overshoot/temperature; input bulk C/ESR/voltage and inrush. Functional topology may be sketched with explicit holds.
- **Prevents component/pin completion:** input connector drawing/ratings and polarity numbering; fuse/diode/TVS/bulk CAD resources.
- **Prevents final electrical approval:** actual clamp including parasitics versus buck 60-V operating ceiling and BSP75N 36-V short-circuit-protection condition; sustained OV response; simultaneous output faults; chassis/PE policy. The nominal 6.7-V buck clamp margin proves none of these.

### F. Review checklist

- [ ] Fuse is in the positive input before the series diode/clamp, with no accidental unfused bypass.
- [ ] Both SS3P6L anode terminals and the cathode geometry agree with the exact package drawing.
- [ ] TVS polarity and its position after the diode are correct.
- [ ] No 35-V bulk or nominal-30-V-only component is represented as qualified for the clamp node.
- [ ] Each buck retains its own CIN/HF bank; no remote bulk-only decoupling.
- [ ] Field output current is excluded from buck-output current budgets but included in input/fault coordination.
- [ ] Chassis and DI FIELD_COM have not been merged into input GND by a symbol or global net label.
- [ ] Fuse, TVS, bulk and connector holds remain visible; no industrial immunity claim is attached.

## 2. LMR36015FBRNXR 3.3-V buck.

### A. Selected configuration

**ACCEPTED:** exact **LMR36015FBRNXR**, adjustable, **1 MHz FPWM**; 6.8-uH XAL4030-682MEC; upper/lower feedback 100 kOhm/43.2 kOhm; EN tied VIN, PG unused. Allocation 0.7 A; gate budget 619.2 mA. Nominal calculated output 3.31481 V, tolerance-only interval 3.21994-3.41200 V before ripple/line/load effects. **PROVISIONAL:** retained capacitor MPNs, CFF and thermal application. **BLOCKED:** completed CIN/COUT/CVCC selections and final power-sheet approval.

Exact source: gate **Final architecture**, **Power**; BOM `B3_*`; [electrical_calculations.json](evidence/electrical_closure/electrical_calculations.json). The letter F is the FPWM selection and B is the 1-MHz selection in the manufacturer's Device Comparison Table. Do not substitute LMR36015BRNXR, an A variant, or LMR51430.

### B. Official manufacturer sources

- Main datasheet: `DS/lmr36015.pdf`, **SNVSB49D**, [TI LMR36015](https://www.ti.com/lit/ds/symlink/lmr36015.pdf). Use the pinned local revision for these locators: **Device Comparison Table p3**, **Figure 7-1 and Pin Functions p4**.
- Reference schematic: **Figure 10-1 p19**, and the **1000-kHz / 3.3-V row of Table 10-1 p19**. It gives 6.8 uH, nominal 3 x 15 uF COUT, 100 k/43.2 k, 4.7 uF plus 2 x 220 nF CIN, starting CFF 20 pF. It is an application example, not proof of our capacitor bank or layout.
- Application guidance within this datasheet: **section 10.1 p18** (effective capacitance unless stated otherwise); **10.2.1.2.2-.3 p20**, **equations 3-5 p21**; **10.2.1.2.5 pp21-22** (COUT/transients); **10.2.1.2.6-.9 p23** (CIN, CBOOT, CVCC, CFF); **10.2.1.2.10 p25** (thermal); **section 11 p33**. No separate buck application note/EVM is adopted as the final circuit. The datasheet's Figure 10-1 is the selected reference schematic.
- PCB guidance: **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**; RNX0012A package/board/stencil drawing **PDF pp44-46**, RNX0012B **pp47-49**. A/B footprint choice and stencil remain provisional.
- Inductor datasheet/layout: `EC/xal4000.pdf`, Coilcraft **document 806 Rev02/25/26**, **p1** XAL4030-682MEC row, **p4** Recommended Land Pattern and marked-end guidance. The 25-C typical saturation criterion is not a hot guarantee.
- Exact TDK CIN/COUT bias/ESR characterization and mounting references are still missing: the gate records 403 responses for `c5750x7r2a475k230ka.pdf` and `c3225x7r1c156m250ab.pdf` under `https://product.tdk.com/info/en/documents/chara_sheet/`. No local successful acquisition or figure/page is claimed. Nominal KEMET/Yageo sheets are in `SRC/passives/`; Samsung's existing `CL10A105KB8NNN.html` and [bias calculations](evidence/passive_bias_calculations.json) do not qualify CVCC.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_LMR36015FBRNXR / 1 / 3.3-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | PROVISIONAL; CAD_CANDIDATE |
| B3_L / 1 / power inductor | XAL4030-682MEC; 6.8 uH | Isat25C 3.6 A; Irms20C 3.0 A; 20%; XAL4030 | `XAL4030-682MEC` / `GW_XAL4030_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| B3_CIN / TBD / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF por unidad; Ceff total >=4.7 uF objetivo conservador | 100 V; X7R; 10%; 2220 | `GW_C5750X7R2A475K230KA_5f18f946` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| B3_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V; X7R; 10%; 0805 | `GW_C0805C224K1RACTU_e16e52b8` / `GW_CAND_0805_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B3_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF por unidad; 45 uF nominal banco | 16 V; X7R; 20%; 1210 | `GW_C3225X7R1C156M250AB_bb412b42` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| B3_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B3_CVCC / 1 / local supply bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| B3_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B3_RFBB / 1 / lower feedback resistor | RC0603FR-0743K2L; 43.2 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0743K2L_a8308c0c` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B3_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; CONDITIONAL |
| B3_CDAMP / TBD / conditional input damping bulk | TBD; TBD | Electrical rating TBD - unverified | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |

Use the linked exact inductor symbol, not the retained older `GW_XAL4030-682MEC_71dfd711`. Feedback resistors are 1%, 0.1 W at 70 C, maximum 75 V subject to power/temperature. Required CBOOT is 100 nF, at least 16 V; retained 50-V part meets nominal voltage only. Required CVCC is **at least 1 uF effective, ceramic, at least 16 V**; the retained 1-uF/50-V X5R Samsung part is **blocked**: prior evidence gives about 0.656 uF typical at 5 V before other losses. Do not place that single candidate as a qualified solution. CIN quantity is not one by default. CFF is a conditional position, **DNP pending loop/transient review**. Input damping bulk is unselected, not an extra approved capacitor.

### D. Connection checklist

| IC pin | Required connection |
|---|---|
| 1 PGND | GND; local return of one VIN/HF-capacitor pair. |
| 2 VIN | VIN_PROT; main CIN to GND and one local 220-nF bypass to PGND1. |
| 3 NC | Externally connect to **SW12**, per TI; not a generic leave-open NC. |
| 4 BOOT | 100 nF to SW, using the short SW3/12 connection. Never to GND. |
| 5 VCC | Dedicated `B3_VCC_INTERNAL`; qualified CVCC to GND. Internal nominal 5-V LDO output; no external load or tie to the 5-V buck rail. |
| 6 AGND | System GND; quiet FB-divider/CVCC reference. Preserve short local return, not an isolated floating ground. |
| 7 FB | Junction of RFBT 100 k from **3V3 after the inductor** and RFBB 43.2 k to AGND/GND. Neither VIN nor SW is the sense point. |
| 8 PG | Unused/open, deliberately marked NC. No pull-up is populated in this selected circuit. |
| 9 EN | VIN_PROT directly; do not float. No external 18-V UVLO network selected. |
| 10 VIN | VIN_PROT; second local 220-nF bypass to PGND11. |
| 11 PGND | GND and short local HF return. |
| 12 SW | XAL4030-682MEC switching end and NC3/CBOOT return. **Not a ground exposed pad.** |

Inductor other end -> `3V3`; three provisional 15-uF COUT parts -> GND there. Optional CFF 20 pF, if later approved, goes **across RFBT**, output-to-FB. Main CIN bank is independent of the 5-V converter and must provide >=4.7 uF effective over actual bias/temperature. Table 10-1's **COUT columns explicitly say RATED CAPACITANCE**: retain 3 x 15 uF nominal without claiming 45 uF effective. Export `3V3`/`GND` to MCU, PHY, RS-485, CAN VIO, ISO logic, oscillator supplies and provisional translator VCCA. No output-enable/reset/boot pin exists on this regulator beyond EN; do not invent one.

### E. Open engineering decisions

- **Prevents a completed initial buck sheet/BOM:** CIN effective count, COUT effective capacitance/ESR/transient/loop suitability, and replacement/qualified bank for CVCC. Symbols with explicit holds may be drawn; no completed power release.
- **CAD completion:** missing CIN 2220/COUT 1210 footprints; delivered RNX A/B and stencil choice. Exact inductor model is available.
- **Final electrical approval:** source/clamp/damping coordination; hot/fault inductance and core loss; 1-MHz FPWM losses at light/full load; actual ambient, copper and enclosure. Standard datasheet RthetaJA is not the application thermal resistance.

### F. Review checklist

- [ ] Exact FBRNXR identity matches 1-MHz FPWM, not a similarly named non-FPWM part.
- [ ] SW12 and NC3 are connected; neither is on GND.
- [ ] BOOT capacitor is BOOT-to-SW and VCC capacitor is VCC-to-GND.
- [ ] Internal VCC is neither externally loaded nor merged with the system 5-V rail.
- [ ] Divider is 100 k/43.2 k, sensed after the 6.8-uH inductor.
- [ ] Both opposite VIN/PGND pairs have their own 220-nF bypass.
- [ ] CIN count and COUT nominal/effective wording remain correct; CVCC failure is not hidden by its 50-V rating.
- [ ] CFF/PG/UVLO positions match selected population; no guessed pull-up or divider.
- [ ] Current, fault and thermal assumptions are recorded without claiming 1.5-A board capacity from IC rating alone.

## 3. LMR36015FBRNXR 5-V buck.

### A. Selected configuration

**ACCEPTED:** independent LMR36015FBRNXR, **1 MHz FPWM**, XAL4040-103MEC 10 uH, RFBT/RFBB 100 k/24.9 kOhm, EN=VIN, PG unused. Allocation 0.1 A; gate budget 83.4 mA. Nominal calculated output 5.01606 V, tolerance-only interval 4.86249-5.17365 V before ripple/line/load. **PROVISIONAL/BLOCKED:** same capacitor and thermal gates as section 2. DO load current is not supplied by this rail.

Exact source: gate **Final architecture/Power**, BOM `B5_*`, electrical calculations. No LMR51430 substitution and no conversion to non-FPWM operation.

### B. Official manufacturer sources

- `DS/lmr36015.pdf`, TI **SNVSB49D**, [official datasheet](https://www.ti.com/lit/ds/symlink/lmr36015.pdf): **Device Comparison Table p3**, **Figure 7-1/Pin Functions p4**, **Figure 10-1/Table 10-1 p19**, specifically **1000 kHz / 5 V** (10 uH, 100 k/24.9 k, nominal 3 x 15 uF).
- Application guidance: **section 10.1 p18**, **10.2.1.2.2-.3 p20**, **equations 3-5 p21**, COUT **pp21-22**, CIN/CBOOT/VCC/CFF **sections 10.2.1.2.6-.9 p23**, thermal **10.2.1.2.10 p25**, source/damping **section 11 p33**. Figure 10-1 is the reference schematic; no separate adopted EVM/application note is needed to infer a different mode.
- Layout: **section 12.1 p34**, **Figure 12-1 p35**, **Figure 12-2 p36**, RNX A/B **PDF pp44-49**, as in section 2.
- `EC/xal4000.pdf`, Coilcraft document 806 Rev02/25/26, **p1 XAL4040-103MEC**, **p4** lands/marked winding end. TDK characterization/mounting files remain unavailable as detailed in section 2; do not invent curve/page references.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_LMR36015FBRNXR / 1 / 5-V synchronous buck | LMR36015FBRNXR | 4.2-60-V input operating range; 1.5-A device maximum; 1-MHz FPWM; board current/thermal limits separate | `LMR36015FBRNXR` / `GW_RNX0012A_TI` | PROVISIONAL; CAD_CANDIDATE |
| B5_L / 1 / power inductor | XAL4040-103MEC; 10 uH | Isat25C 3.0 A; Irms20C 2.2 A; 20%; XAL4040 | `XAL4040-103MEC` / `GW_XAL4040_COILCRAFT` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| B5_CIN / TBD / main input ceramic bank | C5750X7R2A475K230KA; 4.7 uF por unidad; Ceff total >=4.7 uF objetivo conservador | 100 V; X7R; 10%; 2220 | `GW_C5750X7R2A475K230KA_5f18f946` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| B5_CHF / 2 / VIN/PGND high-frequency bypass | C0805C224K1RACTU; 220 nF | 100 V; X7R; 10%; 0805 | `GW_C0805C224K1RACTU_e16e52b8` / `GW_CAND_0805_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B5_COUT / 3 / output ceramic bank | C3225X7R1C156M250AB; 15 uF por unidad; 45 uF nominal banco | 16 V; X7R; 20%; 1210 | `GW_C3225X7R1C156M250AB_bb412b42` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| B5_CBOOT / 1 / bootstrap capacitor | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| B5_CVCC / 1 / local supply bypass | CL10A105KB8NNNC; 1 uF | 50 V; X5R; -55..85 C; 10%; 0603 | `GW_CL10A105KB8NNNC_c3932faa` / `GW_CAND_0603_cap` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| B5_RFBT / 1 / upper feedback resistor | RC0603FR-07100KL; 100 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07100KL_ac663db8` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B5_RFBB / 1 / lower feedback resistor | RC0603FR-0724K9L; 24.9 kOhm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-0724K9L_10698e9e` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| B5_CFF / 1 / conditional feed-forward capacitor | C0603C200J5GACTU; 20 pF | 50 V; C0G; 5%; 0603 | `GW_C0603C200J5GACTU_c75b007a` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; CONDITIONAL |
| B5_CDAMP / TBD / conditional input damping bulk | TBD; TBD | Electrical rating TBD - unverified | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |

Use linked `XAL4040-103MEC`, not `GW_XAL4040-103MEC_b36cb917`. CBOOT >=16 V; CVCC >=1 uF **effective** and >=16 V. The listed single Samsung nominal 1-uF CVCC is blocked for this converter too. CFF remains DNP pending review; damping bulk is unselected. Three 15-uF COUT parts are nominal, not 45 uF effective. CIN count remains TBD independently of B3.

### D. Connection checklist

| IC pin | Required connection |
|---|---|
| 1 PGND | GND/local return of VIN2 HF capacitor. |
| 2 VIN | VIN_PROT, main local CIN and 220 nF to PGND1. |
| 3 NC | Externally join SW12. |
| 4 BOOT | 100 nF to SW3/12; no ground connection. |
| 5 VCC | Dedicated `B5_VCC_INTERNAL` with qualified CVCC to GND; **not system 5V**, not B3 VCC. |
| 6 AGND | GND, quiet lower-feedback/CVCC return. |
| 7 FB | 100 k from 5V output to FB; 24.9 k from FB to AGND/GND. |
| 8 PG | Unused/open with explicit NC. |
| 9 EN | VIN_PROT; no divider or MCU drive selected. |
| 10 VIN | VIN_PROT and second 220-nF bypass to PGND11. |
| 11 PGND | GND/local HF return. |
| 12 SW | XAL4040-103MEC switching end, BOOT-capacitor return and NC3; never GND. |

Inductor other end -> `5V`; three provisional 15-uF COUT to GND there. If later populated, 20-pF CFF parallels RFBT. Export `5V`/`GND` to CAN VCC and provisional translator VCCB. Maintain independent CIN/HF/VCC/BOOT banks and separate switching-node names for both converters. No buck oscillator synchronization pin or external frequency-setting network is selected.

### E. Open engineering decisions

- **Completed capture/BOM blocked:** independent CIN count; COUT bias/ESR/loop/load-step qualification and CVCC correction. Missing 2220/1210 footprints prevent completed CAD mapping.
- **Final approval:** delivered RNX/stencil; FPWM thermal losses at the small design load; actual hot/fault inductor limits; protected-input ringing and power-up/rail sequencing with CAN/DO. No schematic-only calculation closes these checks.

### F. Review checklist

- [ ] RFBB is **24.9 k**, not the 3.3-V sheet's 43.2 k.
- [ ] Inductor is **10 uH XAL4040**, using the linked exact symbol.
- [ ] SW3/12, BOOT4, VCC5 and GND pins are not interchanged.
- [ ] B3/B5 internal VCC and switching nodes remain separate from each other and system rails.
- [ ] Independent VIN decoupling includes two 220-nF HF parts.
- [ ] CVCC is still flagged blocked until effective-capacitance/internal-LDO compatibility is proven.
- [ ] COUT and CFF population reflect conditional qualification, not nominal-only stability approval.
- [ ] The 5-V output powers CAN/translator logic, not the 0.5-A field loads.

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
| ACTIVE_STM32H723VET6 / 1 / LQFP100 MCU | STM32H723VET6 | 3.3-V selected supply; DS supply/voltage-scale/temperature limits; internal LDO | `STM32H723VET6` / `GW_LQFP100_ST_1L` | PROVISIONAL; CAD_CANDIDATE |
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
| MCU_JSWD / 1 / six-position debug header | TBD; 6 posiciones | Electrical rating TBD - unverified | `GW_H_Male_6x1_TH_100mil_c0450d1e` / `GW_CAND_H_6x1_TH_100mil` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| MCU_SRESET / 1 / normally-open reset button | TBD; SPST-NO | Electrical rating TBD - unverified | `GW_Sw_PUSH_4.5x4.5x5.0xmm_0f078dd9` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; REQUIRED |
| MCU_JBOOT / 1 / boot recovery access | TBD; 2 posiciones | Electrical rating TBD - unverified | `GW_H_Male_2x1_TH_100mil_f89d9046` / `GW_CAND_H_2x1_TH_100mil` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
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

MCU oscillator: **1 STANDBY -> 3V3; 2 GND -> GND; 3 OUT -> PH0 pin12; 4 VCC -> 3V3**, 10 nF directly between 4/2. No crystal load capacitors. HSI provides initial boot while the oscillator starts (specified up to 5 ms).

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

## 5. DP83826I Ethernet PHY and clock.

### A. Selected configuration

**ACCEPTED:** DP83826IRHBR, ENHANCED mode, RMII **Leader**, PHY address 0, autonegotiation and Auto-MDIX; pin19 outputs 50 MHz to MCU PA1. Independent 25-MHz KC2016Z oscillator drives XI9. **PROVISIONAL qualification:** oscillator load/phase noise, reset/ramp timing and physical layout. Basic connectivity is CONDITIONAL GO.

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
| ACTIVE_DP83826IRHBR / 1 / Ethernet PHY | DP83826IRHBR | 3.3-V analog and I/O supplies; RHB32+GND EP; RMII Leader 10/100 Ethernet | `DP83826IRHBR` / `GW_RHB0032M_TI` | PROVISIONAL; CAD_CANDIDATE |
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

### E. Open engineering decisions

- **Final clock/timing approval, not a block on reference connectivity:** <=15-pF complete load; PHY phase-noise bounds at 1/10/100 kHz and 1 MHz offsets. Kyocera +/-30 ppm, 45-55% duty and <=2.5-ns edges do not establish that mask. Its p3 distinguishes 12-ps 1-sigma timing jitter from 36-ps phase jitter integrated over 12 kHz-20 MHz; do not conflate these metrics or use either as an offset-mask guarantee.
- **Final electrical/layout approval:** supply ramps, PHY reset sequence and RMII timing/return budget; physical decoupling and EP implementation. Cable/chassis/ESD issues are tracked in section 6.

### F. Review checklist

- [ ] ModeSelect1 is NC, strap14 is pulled HIGH, TX_CLK22 remains default LOW, strap31 remains default HIGH.
- [ ] Address straps30/29/28 remain 000 without LED/MCU loading.
- [ ] PHY19 drives PA1 at 50 MHz; XI9 receives only its own 25-MHz oscillator.
- [ ] CEXT2 is 2 nF and RBIAS10 is 6.49 k/1%.
- [ ] Both 3.3-V supply banks and GND EP33 are present.
- [ ] RX/TX directions and D0/D1 mapping match the MCU AF11 reservation.
- [ ] Reset32 is separate from NRST and timing/SMI waits are documented.
- [ ] Unused pins do not defeat straps, power-down state or clock topology.

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
| ETH_RBOB / 4 / cable-side termination | CRCW080575R0FKEA; 75 Ohm | Electrical rating TBD - unverified; 1%; 0.125 W; 0805 resistor | `MISSING` / `MISSING` | ELECTRICAL_VERIFIED; CAD_MISSING; REQUIRED |
| ETH_CBOB / 2 / chassis AC return | C1206C102KGRACAUTO; 1 nF | 2000 V; X7R; safety class unverified; 10%; 1206 | `MISSING` / `MISSING` | PROVISIONAL; CAD_MISSING; REQUIRED |
| ETH_JRJ45 / 1 / shielded Ethernet jack | SS-7188S-A-NF; 8P8C shielded | Electrical rating TBD - unverified; CT710001 B0 through-hole | `SS-7188S-A-NF` / `GW_SS7188SANF_STEWART` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| ETH_DESD / 1 / PHY-side ESD array | TPD4E05U06DQAR; 4 canales baja C | Electrical rating TBD - unverified; DQA USON10 | `TPD4E05U06DQAR` / `GW_DQA0010A_TI` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |

75-Ohm parts are 1%, 0.125 W per current BOM; application pulse/safety limits remain to be checked. HV capacitors are 1 nF, 10%, 2 kV X7R candidates, not automatically Y-class. Both have missing CAD models, separate from the six retained-library warnings. Jack contact/current ratings remain unqualified despite its accepted pin map; copper annuli/holes and assembly stock are not approved. No four external 49.9-Ohm MDI resistors, no C61/R51 logic/chassis coupling, no PoE implementation are selected.

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

### E. Open engineering decisions

- **Initial connectivity can be captured:** source pin/winding/contact map is closed. **Prevents complete component CAD:** missing four-resistor/two-HV-capacitor models and exact HV mounting evidence.
- **Prevents final insulation/EMC approval:** chassis/PE bond and accessible enclosure policy; HV capacitor safety class/working conditions; jack copper/hole/edge geometry; actual ESD current return/parasitics and board test. Component ESD/isolation tests alone are not gateway compliance.

### F. Review checklist

- [ ] Magnetics pin1/3 and6/8 are PHY-side pairs;16/14 and11/9 reach the specified RJ45 contacts.
- [ ] Both PHY CTs each have two parallel 100-nF parts; neither CT is tied to a supply.
- [ ] Four 75-Ohm resistors and two separate chassis AC-return nodes are drawn exactly once.
- [ ] No external 49.9-Ohm MDI terminations or second datasheet termination variant has been added.
- [ ] ESD is PHY-side; both GND3/8 reference logic GND.
- [ ] ESD pass-through continuity is external copper, not an assumed internal NC connection.
- [ ] RJ45 shield/mechanical pads are distinguished; chassis and logic GND are not merged.
- [ ] Magnetics NC pins remain open; no PoE or extra field circuitry crosses the isolation barrier.
- [ ] No metal-under-magnetics and barrier/plane constraints are carried into later layout review.

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
| ACTIVE_THVD1420DR / 1 / half-duplex bus transceiver | THVD1420DR | 3.3 V selected / 3.0-5.5 V recommended; bus common mode -7 to +12 V; bus absolute +/-16 V | `THVD1420DR` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_CANDIDATE |
| RS_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| RS_RT / 1 / conditional bus-end termination and open-default jumper | TBD; 120 Ohm si Z0=120 Ohm | >=3.3 V continuo; falla de bus aparte; 1%; >=0.25 W objetivo a70 C; 1206 candidato; no0603 0.1W | `MISSING` / `MISSING` | DERIVED_PENDING_REVIEW; CAD_BLOCKED; CONDITIONAL |
| RS_RDE / 1 / DE reset pull-down | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| RS_RRE / 1 / nRE reset pull-up | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| RS_RPULSE / 2 / conditional bus-line pulse resistors | CRCW0603010RJNEAHP; 10 Ohm | Pulse-proof segun ficha exacta; 5%; Pulsos por verificar; 0603 | `GW_CRCW0603010RJNEAHP_c8eb51d2` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_TVS / 1 / transient clamp candidate | CDSOT23-SM712; Asimetrica -7/+12 V candidata | Electrical rating TBD - unverified; SOT23 | `CDSOT23-SM712` / `GW_SM712_BOURNS` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; CONDITIONAL |
| RS_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos | Electrical rating TBD - unverified | `GW_MX126-5.0-03P-GN01-Cu-S-A_d57a488f` / `GW_CAND_CON_3x1_TH_5mm` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |

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

### E. Open engineering decisions

- **Does not prevent basic initial capture:** cable length/stubs/common reference, bus-end location and termination MPN/jumper, exact terminal drawing. They prevent completed connector/end-node approval.
- **Blocks optional protection/industrial release only:** surge waveform/source/repetition, SM712 clamp/residual current and two pulse-resistor energy/drop, board EMC tests. A 54-Ohm load plus 20-Ohm total series resistance gives only a first-order 54/74 amplitude factor, not qualification.

### F. Review checklist

- [ ] R1 goes to MCU RX and D4 to MCU TX, not the reverse.
- [ ] DE has 10-k pull-down and nRE 10-k pull-up, with separate GPIO controls.
- [ ] PD10 is not configured as USART3 clock/hardware DE and PD11 is not CTS.
- [ ] VCC8 has local 100 nF to GND5 and no unintended isolation claim.
- [ ] Only actual cable ends carry termination; jumper defaults open at an intermediate node.
- [ ] No duplicate external bias or arbitrary 10-Ohm series part is populated.
- [ ] Optional surge network shows two resistors and remains visibly unqualified/unpopulated.
- [ ] COM/pin-number assumptions and field baud/cable constraints remain documented.

## 8. ATA6561 CAN-FD.

### A. Selected configuration

**ACCEPTED:** ATA6561-GAQW SOIC8; VCC=5 V, VIO=3.3 V; startup standby and recessive TXD from internal pull-ups. MCU FDCAN1 on PD0/1. Engineering target **1 Mbit/s nominal / 2 Mbit/s data**, subject to cable timing. No external TVS, choke or bus shunt capacitors. Optional conventional 120-Ohm termination at a physical cable end only, open-default jumper at intermediate nodes; prior 62+62-Ohm/4.7-nF split alternative is DNP.

Exact source: gate **RS-485, CAN, DI and DO decisions / CAN**, `CAN_*` BOM and pin bindings. Basic-node capture GO does not mean interface compliance or an approved end termination.

### B. Official manufacturer sources

- Main: `DS/20005991B.pdf`, Microchip **DS20005991B**: **p1 package pinout**, **Figure 1-1 p4** operating modes; **Table 1-2 p8** pin functions, **Electrical Characteristics pp9-13**, especially **p11** internal STBY/TXD pull-ups; SOIC drawing **p19**.
- Relevant manufacturer application/evaluation guide: `SRC/ATA656x_EVKit_50002649A.pdf`, **DS50002649A**, **sections 3.3-3.8 pp17-18**, **Figure 4-1 p19** application for VIO devices, **Appendix A.2 p28** board schematic, **Table B-2 p32** ATA6561/3/6 BOM; **A.3-A.6 pp29-30** layout views. Select the **ATA6561 VIO** variant, not ATA6560 NSIL pin5 or VDFN EP9.
- Locator correction only, no configuration change: the gate's **DS20005991B Figure 1-6** cannot be found in this exact local revision; its figures run 1-1 through 1-5 before section 2. Use verified **Figure 4-1 / Appendix A.2** in the EVKit guide. Likewise `table2.0` in the older report means **section 2.0 Electrical Characteristics**, not an identified numbered table. Do not perpetuate those unverified locators.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_ATA6561_GAQW / 1 / CAN-FD transceiver | ATA6561-GAQW | VCC 4.5-5.5 V; VIO 2.8-5.5 V; SOIC8; selected 1/2 Mbit/s | `ATA6561-GAQW` / `GW_SOIC8_1P27_5P4` | PROVISIONAL; CAD_CANDIDATE |
| CAN_CVCC5 / 1 / 5-V bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| CAN_CVIO3V3 / 1 / 3.3-V I/O bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| CAN_CBULK / 1 / local bulk reserve | TBD; 47 uF | 10 V minimo EVM; 1210 candidato | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| CAN_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos | Electrical rating TBD - unverified | `GW_MX126-5.0-03P-GN01-Cu-S-A_d57a488f` / `GW_CAND_CON_3x1_TH_5mm` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
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

There is no exposed-pad9 on the selected SOIC8 model. Optional 120 Ohm connects CANH-to-CANL through the open-default end-node jumper. Connector roles CANH/CANL/COM are selected, but exact physical terminal numbering is pending. No external TVS/choke/shunt capacitors are populated; no galvanic isolation is claimed.

### E. Open engineering decisions

- **No core initial-capture block:** exact connector drawing, end-node position, termination resistor/jumper MPN; optional bulk depends on supply/distribution transient response.
- **Final interface approval:** bus cable/stub/loop-delay budget at 1/2 Mbit/s, voltage/fault environment, EMC immunity and rail startup. Component transient ratings do not establish board compliance.

### F. Review checklist

- [ ] Exact ATA6561 SOIC8 has VIO5=3V3, VCC3=5V and no fictitious EP9/NSIL.
- [ ] TXD1 comes from FDCAN1_TX and RXD4 reaches FDCAN1_RX.
- [ ] Each supply has a separate local 100-nF capacitor.
- [ ] STBY defaults HIGH/standby and is driven LOW only after initialization.
- [ ] CANH7/CANL6 are not swapped at the connector.
- [ ] Termination appears only at a cable end; no simultaneous 120-Ohm and split network.
- [ ] Optional bulk, bus capacitors, choke and TVS have not become mandatory by copying the EVKit.
- [ ] Cable timing and connector/fault ratings remain distinct from basic-node capture approval.

## 9. ISO1212 dual digital inputs.

### A. Selected configuration

**ACCEPTED:** one ISO1212DBQR, two **Type 3 sinking inputs** for normal 18-30-V sensing; each uses 562-Ohm RSENSE, 1-kOhm Firstohm MM204 RTHR and 10-nF CIN. Logic side 3.3 V, EN HIGH. FGND1/FGND2 share `FIELD_COM`: group isolation from logic, **not channel-to-channel isolation**. **PROVISIONAL/BLOCKED surge qualification:** MM204 resistor/system withstand. No default extra TVS or PE capacitor.

Exact source: gate **DI** decision, BOM `DI_*`. 10-nF Type 3 is retained; do not change to 330 nF or MM204P simply to copy a different surge example.

### B. Official manufacturer sources

- `DS/iso1212.pdf`, TI **SLLSEY7G**, [official datasheet](https://www.ti.com/lit/ds/symlink/iso1212.pdf): **Figure 4-2 and ISO1212 Pin Functions p4**; **section 5.9 p10** DC thresholds; **Figure 8-2 p20** sinking-input schematic; **section 8.2.1.2.1/equations 1-4 p21** thresholds/current; **Table 8-1/Figure 8-9 p25** surge modes/test fixture.
- Relevant application/reference and layout are in that datasheet: **section 8.2.1 pp19-28**, **sections 8.4.1-.2 pp30-31**, especially **Figure 8-18 p31 ISO1212 layout**. Figure 8-17 on the same page is **ISO1211**, not our pin map. No separate EVM/application note is adopted.
- Threshold resistor: `EC/Firstohm_MM.pdf`, manufacturer MM sheet **Rev08-March-2023**, **printed pp75-78 / PDF pp1-4**; MM204 rated/derating/surge curve (not MM204P) and **printed p78 / PDF p4** reflow lands. Manufacturer-authored document obtained from Alfatec; provenance is in [additional_documents.json](evidence/electrical_closure/additional_documents.json).
- Exact RSENSE: `SRC/ISO1212_RSENSE_RC0603FR07562RL.pdf`, **p1**; filter capacitor: `SRC/DI_CIN_C0603C103K1RACTU.pdf`, **p1** nominal properties. Their nominal sheets do not certify a system surge.
- Locator precision: the older report's `Table4-2` is the **ISO1212 Pin Functions block beneath Figure 4-2**, and `table5.9` is **section 5.9**, not a numbered table. Use the verified locators above.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_ISO1212DBQR / 1 / two Type3 field inputs | ISO1212DBQR | VCC1 2.25-5.5 V; 3.3 V selected; normal input 18-30 V; isolation and surge limits separate | `ISO1212DBQR` / `GW_DBQ0016A_TI` | PROVISIONAL; CAD_CANDIDATE |
| DI_RSENSE1 / 1 / channel 1 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RTHR1 / 1 / channel 1 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| DI_CIN1 / 1 / channel 1 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RSENSE2 / 1 / channel 2 SENSE-IN resistor | RC0603FR-07562RL; 562 Ohm | 75 V max; limite sqrt(P*R); 1%; 0.1 W @70 C; 0603 | `GW_RC0603FR-07562RL_a6fad8df` / `GW_CAND_0603_res` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_RTHR2 / 1 / channel 2 external-input threshold resistor | MM204F1K00TKRTR3K0; 1 kOhm | 200 V maximum working; DC applied drop <3 V; pulse gate separate; 1%; 0.25 W at70C, derated to0 at125C; MELF0204 MM204 | `MM204F1K00TKRTR3K0` / `GW_MM204_FIRSTOHM` | DERIVED_PENDING_REVIEW; CAD_CANDIDATE; REQUIRED |
| DI_CIN2 / 1 / channel 2 SENSE-FIELD_COM filter | C0603C103K1RACTU; 10 nF | 100 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C103K1RACTU_97f3ee33` / `GW_CAND_0603_cap` | ELECTRICAL_VERIFIED; CAD_CANDIDATE; REQUIRED |
| DI_CVCC / 1 / local supply bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DI_CPE / 1 / unselected field-to-PE coupling | TBD; 500 pF candidato | 2 kV; seguridad por definir | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; CONDITIONAL |
| DI_J / 1 / field connector | MX126-5.0-03P-GN01-Cu-S-A; 3 polos si COM comun | Electrical rating TBD - unverified | `GW_MX126-5.0-03P-GN01-Cu-S-A_8a7ef64c` / `GW_CAND_CON_3x1_TH_5mm` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |

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

### E. Open engineering decisions

- **No block on normal Type3 initial capture:** exact field-connector drawing and MM204 physical/pulse review remain visible. COM sharing is selected; it is not an unresolved topology choice.
- **Blocks surge/final immunity approval:** required coupling/waveform/source/repetition/ambient and actual voltage/current/energy across RTHR versus its non-P surge curve/400-V overload ceiling. TI's fixture-level voltage does not automatically appear wholly across RTHR. No supplied test establishes those stresses.
- **Final isolation/layout approval:** creepage/clearance, substrate islands and optional PE policy. Keep external HV RTHR terminal >=4 mm from device/RSENSE/CIN terminals per TI EMC layout guidance.

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

## 10. SN74LVC2T45 and two BSP75N digital outputs.

### A. Selected configuration

**ACCEPTED scope:** two low-side BSP75NTA outputs, intended 0.5 A each from field supply. **PROVISIONAL drive candidate:** SN74LVC2T45DCTR, VCCA=3.3 V, VCCB=5 V, DIR=VCCA (A-to-B), 10-k pull-downs on both A and B channels. **BLOCKED:** BSP75N manufacturer-numbered Type DN terminals/footprint and guaranteed loaded >=4.5-V drive for full protected behavior. Do not proceed with numbered BSP wiring or represent the translator as an approved driver.

Exact source: gate **DO**, BOM `DO_*`, active mapping `ACTIVE_SN74LVC2T45DCTR` / `ACTIVE_BSP75NTA`. Some passive rows still mention DCUR; the actual prepared/active candidate is **DCTR/DCT8**, not a silently interchangeable DCU8 package. This is a recorded inconsistency to resolve before physical placement, not authorization to change packages.

### B. Official manufacturer sources

- Translator main datasheet: `DS/sn74lvc2t45.pdf`, TI **SCES516N**, [official datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf): **Table 4-1 p2** numbered DCT/DCU pins, **section 5.5 p6** loaded VOH, **section 7.4 p15** direction; application/reference **Figure 8-1 p16**, **section 8.3 p19** power-up, **sections 8.4.1-.2 pp19-20 / Figure 8-3 p20** layout. DCT0008A drawing **PDF pp28-30**. No OE pin exists.
- Switch main datasheet: `DS/BSP75N.pdf`, Diodes **DS33016 Rev7-2**, **p1** functional pinout/Source tab, **pp3-4** electrical characteristics including input current/4.5-V protection condition, **pp5-6** current/thermal/inductive behavior, **p8** package dimensions. **No manufacturer-numbered terminal assignment is present.**
- Package supplement: `EC/SOT223-Type-DN.pdf`, exact Diodes drawing; it adds dimensions but still does not close terminal numbering. No Infineon BSP75N terminal map may be transferred.
- Relevant application/reference guidance is the above translator Figure 8-1 and Diodes switch functional/thermal material; **no complete manufacturer evaluation schematic qualifies this exact translator-plus-switch combination**. No separate application note or PCB reference with a verified Diodes numbered mapping is available. Do not invent a figure number for the switch role sketch or treat the package drawing as missing-number evidence.

### C. Components to place

| BOM ID / quantity / function | MPN or specified value | Required rating / tolerance | Library symbol / footprint | Verification |
|---|---|---|---|---|
| ACTIVE_SN74LVC2T45DCTR / 1 / candidate level translator | SN74LVC2T45DCTR | VCCA=3.3 V, VCCB=5 V; device supplies 1.65-5.5 V; loaded BSP drive NOT qualified | `SN74LVC2T45DCTR` / `GW_DCT0008A_TI` | ELECTRICAL_BLOCKED; CAD_CANDIDATE |
| ACTIVE_BSP75NTA / 2 / protected low-side switch candidate | BSP75NTA | intended 0.5 A/channel; IN>=4.5 V for protected operation; Source tab; numbered map blocked | `BSP75NTA` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED |
| DO_CVCCA3V3 / 1 / A-side bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DO_CVCCB5 / 1 / B-side bypass | C0603C104K5RACTU; 100 nF | 50 V; X7R; -55..125 C; 10%; 0603 | `GW_C0603C104K5RACTU_dc5e12a5` / `GW_CAND_0603_cap` | PROVISIONAL; CAD_CANDIDATE; REQUIRED |
| DO_RPDA / 2 / logic-side reset pull-downs | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| DO_RPDB / 2 / drive-side reset pull-downs | RC0603FR-0710KL; 10 kOhm | 75 V maximum; power-limited working voltage; 1%; 0.1 W at70C; 0603 | `RC0603FR-0710KL` / `GW_CAND_0603_res` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |
| DO_SUPPRESS / TBD / external inductive-load suppression if required | TBD; TBD | Electrical rating TBD - unverified | `MISSING` / `MISSING` | ELECTRICAL_BLOCKED; CAD_BLOCKED; TBD |
| DO_JLOAD / 2 / load connectors | JL126-50002G01; 2 polos por canal | >=30 V y0.5 A/canal mas fallas | `GW_JL126-50002G01_ddbad43f` / `GW_CAND_CON_2x1_TH_5MM` | ELECTRICAL_BLOCKED; CAD_CANDIDATE; REQUIRED |

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

For each BSP, **roles only, no numeric pins**: `IN` <- candidate drive; `DRAIN` -> load negative; load positive -> selected field-supply distribution; `SOURCE` and **SOURCE TAB** -> intended common field/input return compatible with nonisolated logic control. Do not automatically use isolated DI FIELD_COM. High-current return must not traverse MCU analog/VCAP/PHY bias/FB return paths. Keep Source tab separate from Drain copper. No numeric BSP wiring may be inferred from these role labels.

At 5 V each BSP input can require up to 1.2 mA plus B-side 10-k pull-down current. Full protected operation requires input >=4.5 V. SCES516N section 5.5 only gives 3.8-V minimum at the 4.5-V/-32-mA loaded test point; the near-rail specification is at 100 uA. Interpolating to this actual load is not a guarantee. Startup OFF during partial rails/MCU HiZ also needs validation despite the translator's supply-sequencing features. No fake OE or unused channel exists; both translator channels are used.

### E. Open engineering decisions

- **Prevents initial numbered DO capture/placement:** authoritative Diodes BSP75NTA terminal numbers/Source-tab mapping; guaranteed driver voltage >=4.5 V at worst rail/temperature/input-plus-pull-down load. A role-labelled concept is the current limit.
- **Prevents final electrical approval:** reset/partial-rail OFF behavior; two-channel hot current and copper; load resistance/inductance/duty/repetition and demagnetization; short-circuit supply voltage/energy coordination. Input TVS candidate clamp does not ensure the BSP 36-V protection condition.
- **Physical completion:** translator DCTR/DCUR row inconsistency; load connector drawings/ratings; external suppression selection if actual inductive envelope requires it. Minimum-copper 520-mA at 85-C datum and single-pulse 550-mJ figure are not universal two-channel ratings.

### F. Review checklist

- [ ] DO remains visibly blocked until exact Diodes terminal numbers and a footprint are proven.
- [ ] Source tab is never assumed Drain or copied from another manufacturer's BSP75N.
- [ ] Translator identity/package matches DCTR/DCT; DCUR row inconsistency is resolved before placement.
- [ ] DIR5 is VCCA HIGH for A-to-B; no OE pin is invented.
- [ ] Both supply bypasses and all four pull-downs are present in the candidate network.
- [ ] B1 drives output1 and B2 output2; both MCU pins remain the documented reservations.
- [ ] Guaranteed loaded drive, including pull-down current and rail tolerance, is checked against 4.5 V.
- [ ] Loads draw from the field supply; Source/current return does not merge isolated DI COM or quiet returns.
- [ ] Simultaneous thermal/inductive/fault conditions are bounded; no universal 0.5-A/550-mJ protection claim.
