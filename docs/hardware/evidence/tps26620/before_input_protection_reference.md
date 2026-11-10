# Academic gateway: recovered 24 V input protection

Prepared 2026-11-07. **CONDITIONAL for manual capture of supported connections; the complete input protection sheet is not electrically released.** The agreed architecture remains one 18–30 V input, two LMR36015 bucks and two low-side outputs. No schematic, PCB, Rev. A source or professor library was edited.

Latest review: propose **one TDS3311P.C** in place of TDS3011P.C, after a series reverse-polarity diode, with **one NIS3071MT4TWG channel feeding electronics only**. DO loads use an external supply under the assumptions in section9. Keep both LTC4414 controllers and both DMP6023LSS-13 ORing MOSFETs excluded. Fuse, startup and fault coordination remain conditional. **Section9 is the current manual connection plan; sections1–8 retain the recovery record and earlier conditional load cases.** No proposal silently changes the BOM or CAD.

## 1. Recovered decisions and diagrams

The original electrical reasoning is in [master requirements §§6.1–6.5, §8 and source register D6–D9](../industrial_gateway_requirements.md). Its power tree is also preserved in [the original architecture drawing](../figures/industrial_gateway_architecture.drawio), nodes `p_tdsa`, `p_tdsb`, `p_or`, `p_efuse` and `p_sys`. These are architecture diagrams, not a verified native protection schematic. No additional detailed protection schematic was found in the relevant repository documentation/project records inspected.

```text
HISTORICAL Rev. A — two independent positive inputs, common return

Input A+ ----o---- LTC4414 + DMP6023LSS ideal-diode path ----+
            |                                             |
          TDS A                                           +--24V_OR--NIS CH1--24V_SYS--+--3V3 buck
            |                                             |                         +--5V buck
GND --------+                                             |
                                                          |
Input B+ ----o---- LTC4414 + DMP6023LSS ideal-diode path ----+
            |
          TDS B                 TDS elements are SHUNT devices, not series regulators.
            |
GND --------+
```

| Item | Recovered decision and current disposition | Status |
|---|---|---|
| Two independent inputs | Rev. A redundancy, now replaced by one input under the agreed academic scope | SUPERSEDED |
| Two TDS3011P.C | Shunt suppression before the original ORing controllers; reduce to one, with placement changed as below | HISTORICALLY_SELECTED → PROPOSED_FOR_REUSE |
| Two LTC4414 + two DMP6023LSS-13 | Low-loss source ORing, not necessary for one input | HISTORICALLY_SELECTED → SUPERSEDED |
| One NIS3071MT4TWG, CH1 | Auto-retry main-rail breaker; three channels unused | HISTORICALLY_SELECTED → PROPOSED_FOR_REUSE |
| R_LIM 43.2 kΩ E96 | Historical Fig.5 estimate ITH≈1.4 A, ICB≈2.8 A; not guaranteed thresholds | PROPOSED_FOR_REUSE; final setting BLOCKED |
| Two LMR36015FBRNXR | Existing 1 MHz FPWM 3.3/5 V selection; no change here | CURRENTLY_APPROVED selection; existing capacitor/thermal qualifications remain open |
| Single input, no ORing | Explicit user architecture and [academic README simplification](../../hardware/academic_rev1/README.md), power section | CURRENTLY_APPROVED architecture |
| SS3P6L series diode + TDS/eFuse | Earlier academic simplification already proposed this combination; never fully approved | PROPOSED_FOR_REUSE |
| Later fuse → SS3P6L → SMBJ33A draft | [Readiness gate](schematic_readiness_gate.md) / [passive BOM](passive_bom.csv) retain this **unreleased** draft; SMBJ33A did not establish continuous overvoltage or fault coordination | BLOCKED; replacement by recovered TDS/eFuse is proposed, not adopted |

Original LTC4414 reasoning: 36 V operating ceiling, 40 V VIN/SENSE absolute maximum, gate clamp approximately 8–9 V, typical forward regulation approximately 20 mV. The 40 V maximum TDS clamp already reached the controller's absolute maximum before trace overshoot. Its limited reverse-battery rating is only −14 V, not a demonstrated −30 V input capability. See local LTC datasheet pp2–3,6–8 and Fig.4 p10. The original DMP MOSFET is conventional SO-8, no exposed pad; 33 mΩ maximum is specified at VGS=−4.5 V, ID=−4 A, TA=25°C, not a hot-board guarantee. The historical 1.2 A calculation gave 47.5 mW MOSFET loss. Removing ORing removes that controller bottleneck without reintroducing a redundant supply.

## 2. Component and local datasheet index

All linked local PDF targets below exist. Five exact existing manufacturer PDFs were copied from `C:/dev/7mo/design/Datasheets_industrial_gateway/`; the existing Vishay PDF was reused in place. [Manifest](evidence/input_protection/datasheet_manifest.json) records original paths and SHA-256 values. Page numbers below refer to the saved PDF, which remains the evidence baseline even when a manufacturer page advertises a later release.

| Exact MPN / manufacturer | Purpose; relevant pages | Local PDF | Official manufacturer source | CAD / electrical status |
|---|---|---|---|---|
| TDS3011P.C — Semtech | Shunt EOS suppressor; Rev2.0 16-Jun-2021 p2 ratings, p4 leakage/slew curves, p5 Figs2–3 pin/layout, p6 land pattern, p7 order code | [TDS3011P.pdf](../../hardware/academic_rev1/libraries/sources/input_protection/TDS3011P.pdf#page=2) | [Semtech product and datasheet portal](https://www.semtech.com/products/circuit-protection/surgeswitch/tds3011p) | New symbol + footprint CAD_CANDIDATE; PROPOSED_FOR_REUSE |
| NIS3071MT4TWG — onsemi | Four-channel eFuse; Rev3 Apr2026 Table1 p2, Table3 p3, pp5–6 application, Fig5 p7, Figs9–11 p8, ordering p11, CASE510CM p12 | [NIS3071-D.PDF](../../hardware/academic_rev1/libraries/sources/input_protection/NIS3071-D.PDF#page=2) | [onsemi datasheet](https://www.onsemi.com/pdf/datasheet/nis3071-d.pdf) | New symbol + footprint CAD_CANDIDATE; PROPOSED_FOR_REUSE |
| LTC4414 — Analog Devices | Historical ideal-diode controller; RevC pp2–3 limits/order options, pp6–8 operation, Fig4 p10, MS8 drawing p11 | [4414fc.pdf](../../hardware/academic_rev1/libraries/sources/input_protection/4414fc.pdf#page=2) | [ADI datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/4414fc.pdf) | Absent from target; excluded, no new model. Historical suffix/temperature grade not recovered; base name is not an exact order code |
| DMP6023LSS-13 — Diodes Incorporated | Historical external PFET; DS37198 Rev2-2 Jan2015 p1 pinout/order, p2 ratings, p5 package and pad layout | [DMP6023LSS.pdf](../../hardware/academic_rev1/libraries/sources/input_protection/DMP6023LSS.pdf#page=1) | [Diodes datasheet](https://www.diodes.com/datasheet/download/DMP6023LSS.pdf) | Absent from target; excluded, no new model; saved document marked ADVANCE INFORMATION |
| SS3P6L-M3/86A — Vishay | Series reverse-polarity candidate; 88987 Rev24-Apr-2020 p1 terminal functions, p2 ratings/thermal, p4 mounting lands | [SS3P6L_88987.pdf](../../hardware/academic_rev1/libraries/sources/SS3P6L_88987.pdf#page=4) | [Vishay product / document88987](https://www.vishay.com/en/product/88987/) | New corrected mapping CAD_CANDIDATE; PROPOSED_FOR_REUSE |
| LMR36015FBRNXR — Texas Instruments | Existing two bucks; SNVSB49D p4 pins, §10.2.1.2.6 p23 input capacitors, §11 layout; RNX package appendices | [lmr36015.pdf](../../hardware/academic_rev1/libraries/sources/input_protection/lmr36015.pdf#page=23) | [TI datasheet](https://www.ti.com/lit/ds/symlink/lmr36015.pdf) | Existing symbol and RNX-A/B footprints preserved; use existing variant-selection gate |
| 0451002.MRL — Littelfuse | Proposed upstream fuse; 451/453 Rev01-Dec-2025 pp1–4 | **Missing locally; no fake PDF link** | [Official 451/453 datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1) | Symbol only, CAD_BLOCKED footprint; PENDING_USER_APPROVAL |

The Semtech product portal advertises a 2023-12-05 release and a different headline surge test than the saved 2021 document. This task uses the saved revision's exact electrical/package tables and makes no system compliance claim. Obtain/reconcile that later PDF before making a surge qualification claim. The onsemi web PDF returned403 in this environment; its complete local Rev3 document was available and inspected. Fuse downloads from official global, legacy and regional endpoints were denied403; web text was readable, but the mounting sketch was not reliably inspectable.

## 3. Proposed single-input implementation

This is a **proposal for review**, not a manufacturer reference design reproduced unchanged. Element behavior is documented; complete system coordination is still unverified.

```text
SERIES POSITIVE PATH
J_IN+ -- F1? -- VIN_FUSED -- D_REV -- VIN_CLAMP -- NIS IN1[2] / OUT1[1] -- 24V_SYS
                           A1,A2 -> K                                    |-- 3V3 buck
                                                                        |-- 5V buck
                                                                        +-- DO load supply? [decision]

SHUNT ELEMENTS AND RETURNS
VIN_CLAMP -- TDS IN[4,5,6] / GND[1,2,3] -- GND_PWR
VIN_CLAMP -- C_IN_LOCAL / C_BULK_PRE? ---- GND_PWR
24V_SYS   -- C_BULK_POST? --------------- GND_PWR
NIS GND[8] + exposed PAD[EP] ------------ GND_PWR
J_IN- ---------------------------------- GND_PWR

NIS ILIM[7] -- R_LIM (43.2k candidate) --- GND_PWR
NIS dvdt[6] -- C_DVDT? ------------------ GND_PWR   [or open, documented default]
NIS FAULT[5] -- R_FAULT 15k -- 3V3        [optional MCU status]
```

`F1?` is pending approval. Bulk location/value and whether DO loads are powered through this channel are decisions, not finalized connections. No chassis/PE or isolated-input ground is silently tied to GND_PWR. TDS surge return is a short local path to connector return and appropriate ground copper, away from sensitive feedback and isolated-domain boundaries.

Reverse-polarity protection remains necessary if swapped field wires are an allowed fault: neither the eFuse nor the bucks establishes a guaranteed −30 V reverse-input specification. Put D_REV **before** the unidirectional TDS. A TDS directly across a reversed connector can forward-conduct; the original before-ORing placement therefore cannot be copied as complete reverse-polarity protection. Vishay explicitly lists polarity-protection use. Both small anodes go to VIN_FUSED, large cathode K to VIN_CLAMP.

SS3P6L's 60 V repetitive reverse rating must cover retained output voltage plus reversed input, not merely 30 V: a charged +30 V downstream rail and −30 V source already total60 V before overshoot. Its typical VF at1.5 A is0.464 V at25°C (about0.56 W using1.208 A as a screening estimate, not a guaranteed loss). Its150 A/10 ms half-sine rating does not prove compatibility with every TDS surge pulse. Verify hot loss, pulse waveform and reverse envelope before release; otherwise select a separately justified stage. Do not restore LTC4414 simply to avoid this check.

## 4. Suppressor, eFuse and fault coordination

**TDS:** the 30 V working rating includes exactly30 V, with zero tolerance headroom. Leakage at30 V and25°C is0.05 µA typical,1 µA maximum; p4 temperature curves are typical, not an all-temperature guaranteed maximum. At1 µA, static power is30 µW. A supply nominally set to30 V with +5% tolerance reaches31.5 V and is outside the working rating. The series diode's typical drop is not a guaranteed tolerance allowance. Confirm the maximum steady/ripple voltage **at VIN_CLAMP**, source tolerance, temperature and hot-plug envelope.

The saved datasheet specifies breakdown34–39 V at1 mA and clamp38 V typical/40 V maximum at35 A for its stated1.2/50 µs voltage and8/20 µs current combination, RS=2Ω. This gives20 V nominal static headroom to the NIS/buck60 V ceiling under those test conditions, before parasitic overshoot and temperature qualification. It is not continuous overvoltage regulation. A sustained high supply may overheat a shunt suppressor; downstream NIS cannot disconnect a short in the TDS branch ahead of itself. A40 V clamp also exceeds BSP75N's separately documented36 V short-protection condition, so it does not close that DO fault case. Neither a larger standoff TVS nor an eFuse without OVP fixes this automatically.

**NIS:** Table2 lists steady VIN/OUT limits up to60 V under its absolute-maximum/thermal heading; the65 V transient allowance is only≤100 µs. These are not universal surge guarantees. Eighteen–30 V is within the device's stated industrial application range. MT4 is Auto-Retry, not MT3 latch-off. It trips after current exceeds ITH for approximately1.5 ms, or at ICB=2×ITH with approximately6 µs response; current is not continuously regulated at ITH. Table3's1.9–2.1 A threshold bound is for30 kΩ under its specified conditions, **not** a tolerance guarantee for43.2 kΩ. Fig5 gives only the historical approximate1.4/2.8 A values; hot variation is shown in Fig7. Auto-retry repeatedly energizes a persistent fault and requires system-level acceptance.

Use one channel as originally intended; tie unused IN2/3/4 and EN2/3/4 to ground, leave their OUT pins unconnected. This uses only one quarter of the available switches, but is electrically supported and avoids changing selected silicon solely for utilization. The datasheet permits channel paralleling; it is unnecessary here and not proposed. ILIM/dvdt are common controls, not one set per channel.

Current screening from the [existing rail budget](evidence/electrical_closure/electrical_calculations.json): design allocations3.3 V×0.7 A +5 V×0.1 A =2.81 W. Assuming75% conversion efficiency **only as an engineering allowance** at18 V gives0.208 A, plus1.0 A if both0.5 A DO loads use this rail: approximately1.208 A, before front-end losses, added loads and charging. This is not measured consumption or a proven worst case. Thus the historical1.4 A curve setting cannot yet be released. If DO loads are externally powered, do not count their drain currents through the eFuse. At1.208 A, I²R is approximately0.134 W using92 mΩ at25°C or0.226 W using155 mΩ at150°C; add bias/switching/startup loss and verify the actual copper thermal path. The25°C resistance result is not a hot rating.

**Capacitors and inrush:** NIS Table3's100 µF CIN/COUT are characterization conditions, not an instruction to fit two100 µF capacitors. Local input bypass is needed to control inductance; bulk C/ESR, voltage/ripple rating and location remain TBD from cable/source impedance, hot-plug and load transients. Front-end capacitance must tolerate the actual clamped voltage plus overshoot; the professor's35 V100 µF part is not qualified for a40 V clamp. Do not select it merely because CAD exists.

Default NIS ramp is approximately1.5 ms with dvdt open. Use Figs9–11 for a low-leakage ceramic C_DVDT if necessary; no `CDVDD` pin exists. Check `I_start ≈ I_load_start + C_downstream·dV/dt` against the minimum trip threshold and timer. For illustration only,100 µF charged to24 V in1.5 ms requires1.6 A before load, showing why a curve-based1.4 A threshold and unanalysed bulk can conflict. Pre-eFuse bulk does not benefit from its soft start. Numerical C_DVDT and bulk selections remain blocked until the real load and source are defined.

Retain each buck's own input bank: TI §10.2.1.2.6 requires at least4.7 µF ceramic input capacitance and close220 nF bypass; its example uses two220 nF capacitors at the two VIN/PGND locations. Existing BOM retains100 V X7R candidates, with effective capacitance and exact main-capacitor footprint still unresolved. An upstream bulk capacitor does not replace those local banks. TI also discusses an electrolytic's ESR damping for long input leads; no arbitrary filter inductor or undamped LC was added.

NIS pp5–6 warns of positive IN spikes and negative OUT spikes during current interruption. Place the TDS at the IN-side path with short return, verify interconnect inductance, and evaluate whether an additional OUT-to-GND Schottky is required (anode GND, cathode OUT). That conditional recommendation does not select an MPN or prove the candidate input diode can serve both roles. No extra output diode is silently populated. Validate input/output waveforms during hot-plug, short, release and repeated retry.

## 5. Conventional fuse inventory and decision

No physical fuse, PTC or holder MPN was selected in the master, academic worklist or current BOM (`IN_FUSE=TBD`). Electronics AI inspected177 objects across the Gateway/professor symbol and footprint libraries; relevant-name search found no fuse or these historical protection ICs. The professor symbol metadata/inventory also contains no physical fuse/PTC/holder. The separate SS3P6L libraries contain a diode, not a fuse. The eFuse model was absent before this task.

An upstream fuse is desirable for an uncontrolled24 V source: shorts before NIS and semiconductor failures bypass its protection. A supervised current-limited bench prototype can instead rely on documented external current limiting and suitably rated wiring, but its source settings/fault behavior have not been supplied. Fuse omission is therefore not approved.

**Candidate: Littelfuse0451002.MRL, PENDING_USER_APPROVAL.** Manufacturer451/453 tables give2 A,125 VDC,50 A interruption at125 VDC and300 A at32 VDC; package6.10×2.69 mm, surface-mount, very fast acting. Nominal melting I²t=0.530 A²s is not total clearing energy. The standard25% continuous-current derating gives1.5 A before temperature rerating, above the conditional1.208 A budget. Inrush, ambient, available fault current and wiring/TDS coordination remain unverified. The2 A part's200% opening limit is5 s; it cannot guarantee immediate semiconductor protection or selectivity with an auto-retrying eFuse. Its manufacturer p4 pad drawing must be inspected before authoring the footprint. [Official datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1).

JLCPCB classification/stock is UNKNOWN for the TDS, NIS and fuse: the connected supply query returned dynamic-catalog-unavailable on2026-11-07, not zero stock. No Basic/Preferred status is claimed. Do not substitute a PTC or unspecified fuse to fill this slot.

## 6. Supported pin-by-pin construction checklist

These are documented connections for the **proposed** topology; use them only after deciding the power/fault policy above. All symbol pins are visible and numbered; no hidden global supply nets were added.

| Component pin(s) | Net / connection | Evidence and limitation |
|---|---|---|
| TDS4,5,6 IN | VIN_CLAMP; connect all three with the protected positive path | Semtech p5 Figs2–3; all IN pins required for surge capability |
| TDS1,2,3 GND | GND_PWR; all three, short/wide return, multiple ground vias in board design | Semtech p5; do not use isolated DI return or a long signal-ground trace |
| NIS2 IN1 | VIN_CLAMP, local bypass return to GND_PWR | Table1 p2; transient discussion pp5–6 |
| NIS1 OUT1 | 24V_SYS, then separately bypassed buck branches | Table1 p2; total downstream/startup current pending |
| NIS8 GND and PAD | GND_PWR; exposed ground pad must connect | Table1; project terminal name `EP` maps unnumbered manufacturer `PAD`; not manufacturer pin17 |
| NIS7 ILIM | R_LIM to GND_PWR | Table1 / Fig5;43.2 kΩ historical candidate only; existing `GW_RC0603FR-0743K2L_a8308c0c` symbol can represent that exact resistor; shared0603 footprint remains CAD_CANDIDATE |
| NIS6 dvdt | Open for documented default, or low-leakage capacitor to GND_PWR | Table1, p5, Figs9–11; no chosen C_DVDT value |
| NIS16 EN1 | Floating enables by internal pull-up; external LOW disables | p5 Enable. Default-on suits the original always-on supply, but auto-retry/default-on policy needs acceptance. Do not connect EN to24 V;6 V absolute maximum. High-inductance output case recommends driven-high EN; resolve before that use |
| NIS5 FAULT_N | Optional15 kΩ pull-up to3V3 and MCU status input; alternatively leave open | Table1 and p5; open-drain, active-low. Pull-up sinks≈0.22 mA, within Table3's0.5 mA test/current limit. Not a power-good signal; UVLO can report HIGH |
| NIS3 IN2,11 IN3,10 IN4 | GND_PWR | p5 unused-channel instruction |
| NIS15 EN2,14 EN3,13 EN4 | GND_PWR | p5 unused-channel instruction |
| NIS4 OUT2,12 OUT3,9 OUT4 | Unconnected; show intentional NC in manual schematic | Unused channels; do not short outputs to ground |
| D_REV1 and2 | Both anodes to VIN_FUSED | Vishay p1:1/2 are anodes, not anode/cathode pair |
| D_REV K | Cathode to VIN_CLAMP | Vishay p1/p4; `K` terminal retained in CAD |
| F1 END1 / END2 | Series J_IN+ to VIN_FUSED, only if approved | Nonpolar project terminal labels1/2; candidate symbol only, no footprint |

If FAULT is monitored, the logic supply appears only after the bucks start; it does not supply EN's startup function. The controller may subsequently pull EN low, but must not create a dependency that prevents powering itself. External connections/backfeed, including debugger power, need checking before claiming reverse isolation.

## 7. Saved native library resources and verification

Targets: [Gateway_Academic.SchLib](../../hardware/academic_rev1/libraries/Gateway_Academic.SchLib), [Gateway_Academic.PcbLib](../../hardware/academic_rev1/libraries/Gateway_Academic.PcbLib), [Gateway_Academic.LibPkg](../../hardware/academic_rev1/libraries/Gateway_Academic.LibPkg). The package already references these two local libraries and was preserved unchanged.

| Saved symbol | Linked footprint | Source geometry / mapping | Readiness |
|---|---|---|---|
| `TDS3011P.C` | `GW_TDS3011P_SEMTECH` | Six0.30×0.65 mm lands;0.50 mm pitch, rows1.45 mm apart,0.80 mm inside gap,2.10 mm outside extent. Top row6/5/4 IN, bottom1/2/3 GND per p5 Fig3; rotated from Fig2 top view | Pin map and copper checked; CAD_CANDIDATE pending mask/stencil/DFM |
| `NIS3071MT4TWG` | `GW_NIS3071_510CM_ONSEMI` |16 perimeter lands plus `EP`;1.05 mm pitch. Side lands0.71×0.35, end lands0.52×0.70, outside5.30×6.30; EP2.85×4.75 mm. Side x=±2.295, end y=±2.80; side y/end x=±1.575,±0.525. Top-view counterclockwise numbering starts at upper left-side pin1 | Pin map and recommended copper checked; CAD_CANDIDATE. EP paste, thermal copper/vias and stencil not finalized |
| `SS3P6L-M3_86A` | `GW_SS3P6L_VISHAY_88987` | Exact MPN parameter retains slash. Large K4.80×4.72 mm at0,0; small1/2 lands1.40×1.27 at(+1.22,−3.805)/(−1.22,−3.805);1.04 mm gap,6.80 mm total extent. Minimum manufacturer mounting dimensions | New mapping checked; CAD_CANDIDATE pending thermal/mask/stencil review |
| `0451002.MRL` | None | Two passive terminals; project1/2 convention for nonpolar fuse | Symbol persisted; CAD_BLOCKED footprint; PENDING_USER_APPROVAL |

**Do not use the supplied SS3P6L model unchanged.** Its source symbol maps1=Anode,2=Cathode,3=Anode while its `SS3P6L-M386A_VIS` footprint makes pad1 the large land. Vishay instead identifies the large land asK and the small terminals as1/2 anodes. This mismatch was recorded in [source readback](evidence/input_protection/ss3_source_readback.json). The source files remain unchanged; the newly authored symbol and footprint use matching manufacturer identifiers1,2,K. No other provider variant was automatically accepted.

All newly authored pads are explicit SMD rectangles, not generic package-helper output. TDS/NIS body outlines are on Mechanical1. The asymmetric SS3 footprint omits a body outline because body registration to the mounting lands was not explicitly dimensioned; its copper pattern is preserved. No placeholder3D models or thermal drill patterns were inserted. Mask/paste expansions currently defer to board rules; in particular the NIS exposed-pad stencil must be reviewed before assembly output. A readable land pattern establishes copper geometry, not a complete assembly process.

Electronics AI file-backend readback confirmed all4 added symbols and3 footprints after save. Structural validation returned **0 errors /0 warnings** for50 symbols and26 footprints. Independent library comparison confirmed all46 old symbols and23 old footprints unchanged, with no removals. [Final readback, validation and comparisons](evidence/input_protection/final_readback_validation.json); [source-dimensional inputs](evidence/input_protection/cad_assets.json).

Backup: [input_protection_20261107T152230Z](../../hardware/academic_rev1/libraries/backups/input_protection_20261107T152230Z/) contains both libraries and LibPkg with [SHA-256 manifest](evidence/input_protection/library_backup.json). The first symbol write rejected the slash in the SS3 stream name; disk hash and46-component readback were checked before retrying with the underscore stream name. No existing objects were changed by that rejection.

**Compilation:** no new native session was launched and no native compile was attempted, per task constraint. File validation is successful; native open/placement/compilation of these additions is unverified. The prior IntLib is unchanged and **STALE for these additions**: it contains the earlier46-symbol/23-footprint source inventory. Its earlier six Missing Component Models warnings are historical results, not new compiler output. Use the editable libraries for review, then manually compile this LibPkg when Altium is idle. Do not mistake the older IntLib for the newly populated source libraries.

The current BOM and earlier generator inputs remain unchanged; these CAD candidates are separately indexed here and in `evidence/input_protection/cad_assets.json`. That avoids silently replacing IN_TVS/IN_FUSE or approving the recovered chain. After approval, update the BOM/generator overlay together and bind the exact saved names above.

Final [verification record](evidence/input_protection/verification.json):28 symbol contacts and26 footprint pads read back;6 local PDF links and all other local report links resolve;26 baseline native/source files remain hash-identical, including professor libraries, existing IntLib, project, schematic and PCB documents. Only the two intended Gateway source libraries changed. `git diff --check` passed; [final Git status](evidence/input_protection/git_status_final.txt) retains the pre-existing firmware work. [Library release status](evidence/input_protection/library_release_status.json) explicitly records that the IntLib is stale.

## 8. Remaining decisions and next manual steps

Electrical blockers for a released complete input sheet:

1. **Source contract:** maximum continuous/ripple voltage including tolerance atVIN_CLAMP, source current-limit behavior and prospective short-circuit current; cable length/inductance, ambient and allowed reverse voltage. TDS30 V working and diode60 V reverse margins cannot be approved from “18–30 V” alone.
2. **Fault/load contract:** confirm whether both DO loads are supplied through24V_SYS, actual continuous/startup load, permitted auto-retry/default-on behavior and maximum acceptable fault energy. Then close R_LIM tolerance, C_DVDT and bulk capacitance/ESR. Historical43.2 kΩ is not a verified current setting for today's load.
3. **Fuse choice:** approve or reject the proposed2 A part after derating, inrush and source-fault coordination; an eFuse downstream cannot protect a suppressor/input short upstream. For a bench-only omission, document the external supply's current limit and fault/wiring bounds instead.
4. **Transient/overvoltage requirement:** waveform, source impedance, polarity, repetitions and required system test level. TDS pulse capability does not establish industrial compliance or continuous OV disconnect. Resolve the DO36 V short-protection condition separately if that rail sees the clamp. No numerical IEC withstand was invented.

Documentation/CAD/sourcing tasks, separate from those electrical decisions:

- Save the official **451/453 datasheet with its readable p4 recommended pad layout** as `hardware/academic_rev1/libraries/sources/input_protection/Littelfuse_451_453.pdf`, using the official link above. That exact missing file blocks only the candidate fuse footprint. Do not use a similarly sized generic2410 pattern without checking the drawing.
- Retrieve/reconcile the Semtech product portal's later TDS datasheet before claiming surge compliance; preserve the existing2021 PDF and compare pin/land/rating revisions.
- Review board mask/stencil and NIS exposed-pad thermal connection with the fabricator/assembler. Confirm input capacitor effective capacitance and voltage/temperature behavior from the existing buck-closure blockers.
- Manually open the project-local source libraries in an idle Altium session, inspect the new models, and compile `Gateway_Academic.LibPkg`; do not depend on the old IntLib. No computer control or software installation is needed from this agent.
- Obtain supplier C-codes/current stock if JLCPCB assembly is intended. Unknown catalog results are sourcing issues, not reasons to substitute components silently.

**Ready now:** manually capture the sourced TDS and NIS pin groups and existing independent buck logic, with these candidate/status notes visible. **Not ready:** release final input protection values, select all bulk capacitors, claim coordinated fault/surge protection, or order a board using the missing fuse footprint. Overall manual schematic-capture readiness is **CONDITIONAL**.

## 9. Academic Revision — Approved Schematic Connection Plan

Review date:2026-11-07. The requested section title does **not** confer approval on provisional parts or values. **SCHEMATIC_READY = CONDITIONAL / CONNECTIONS_ONLY. ELECTRICALLY_APPROVED = NO for the complete input circuit.** Pin connections below can be drawn manually; explicitly unresolved values remain TBD. No native CAD, schematic or PCB was edited in this review.

### 9.1 Operating contract and scope change

Review basis: one regulated18–30 V input, nominal24 V; no ORing; the main eFuse supplies only the two bucks and their electronics. The existing allocations remain0.7 A at3.3 V and0.1 A at5 V. The BSP driver/input currents remain in the5 V budget; **external DO drain/load currents do not pass through this eFuse**. No IEC immunity level or continuous overvoltage disconnect is claimed.

This differs from Rev. A's24V_SYS load distribution and the earlier conditional1.208 A calculation that included two0.5 A loads. It is an explicit new **review assumption**, not evidence that the historical wiring was approved for external DO power. It resolves the main-channel DO-current ambiguity only if implemented as specified: external supply+ → load → BSP drain; BSP source → DO_RETURN → external supply−. Define one low-impedance bond between DO_RETURN and the logic/driver ground reference. Keep load and fault return currents out of MCU, eFuse sense/reference and input-suppressor return traces. External supply+ must never connect to24V_ELEC. FIELD_COM and chassis remain separate domains unless separately justified. External DO power still needs its own fault/inductive-load protection review; F1/NIS do not protect that feed. Common-ground voltage offset, alternate debugger/communication returns and any backfeed remain required checks.

### 9.2 Final proposed topology and normal/fault behavior

```text
SERIES POSITIVE PATH — electronics only

J_IN+ -- F1 -- VIN_FUSED -- D_REV(A1+A2 -> K) -- VIN_CLAMP -- U_EF.IN1[2]
                                                              U_EF.OUT1[1] -- 24V_ELEC --+-- 3V3 buck
                                                                                       +-- 5V buck

SHUNT BRANCHES — each returns to local GND_PWR / J_IN-

VIN_CLAMP -- D_TDS.IN[4,5,6] / GND[1,2,3] -- GND_PWR      [TDS3311P.C proposed]
VIN_CLAMP -- C_EF_IN ---------------------- GND_PWR      [value/MPN TBD]
24V_ELEC  -- C_EF_OUT? -------------------- GND_PWR      [extra bulk conditional]
GND_PWR   -- D_SOUT.anode / cathode ------- 24V_ELEC     [separate output clamp; MPN TBD]

CONTROL
U_EF.ILIM[7] -- R_LIM -- GND_PWR                          [62.0k 1% starting proposal]
U_EF.dvdt[6] -- C_DVDT? -- GND_PWR                        [value or DNP not yet approved]
U_EF.FAULT[5] -- R_FAULT15k -- 3V3                       [optional status]
U_EF.EN1[16] open: internal pull-up gives default ON      [documented low-inductance case]
U_EF.GND[8], PAD[EP] -- GND_PWR
```

**D_REV is a series reverse-polarity blocker. D_SOUT is a shunt negative-output clamp. They are different devices/functions and neither substitutes for the other.** Do not connect the series diode's anodes to ground. D_SOUT follows [AND90248 §3.2, p3](../../hardware/academic_rev1/libraries/sources/input_protection/AND90248-D.pdf#page=3); the existing SS3P6L is not automatically suitable for it. Its datasheet does not guarantee≤0.3 V forward drop at the relevant fault current/temperature. Select D_SOUT against pulse current, reverse voltage, VF plus interconnect overshoot, and the NIS negative-voltage limit; absent those bounds, its exact part is BLOCKED. Include this distinct function in the connection plan; a DNP decision requires a quantified/measured output-inductance case.

| Condition | Required relationship and remaining limitation |
|---|---|
| Normal positive input | F1/D_REV carry electronics input current; TDS and D_SOUT are normally off; enabled CH1 feeds both bucks. Buck input banks stay local to their VIN/PGND pins |
| Reversed source | D_REV blocks the positive path before the unidirectional TDS. Check retained downstream charge plus negative input against D_REV reverse rating; a30 V charged rail and−30 V source already reach its60 V rating |
| Positive pulse | TDS diverts current at VIN_CLAMP. F1 and D_REV are upstream and must survive/coordinate with that pulse. Clamp42 V is conditional on the TDS test waveform, not an arbitrary surge limit |
| Electronics overload/short | NIS opens CH1 after its specified trip behavior and MT4 later retries. F1 is backup protection, not guaranteed to clear during NIS retries |
| TDS/input-cap short or NIS shorted failure | A downstream eFuse cannot isolate a shunt fault ahead of it. F1 or the source must safely clear/limit it; source fault current is still unknown |
| Output inductance at turn-off | D_SOUT provides the local negative-current path. Output capacitor and diode selection depend on energy/current and ringing |
| Sustained overvoltage | Neither TDS nor NIS is a continuous OV disconnect. Outside the agreed regulated-source contract, protection is not approved |

### 9.3 Component decisions, values and independent statuses

| Element | Proposed part/value and evidence | SCHEMATIC_READY | ELECTRICALLY_APPROVED |
|---|---|---|---|
| U_EF | NIS3071MT4TWG; one CH1; April2026 Rev3 Tables1–4, Figs4–5,7,9–11; MT4 ordering p11 | YES for documented pins | CONDITIONAL: startup/fault/thermal envelope open |
| D_TDS | **TDS3311P.C preferred replacement**, not adopted in BOM; comparison below | YES for sourced pin functions; exact CAD MPN absent | NO: source/transient bounds and revision reconciliation |
| D_REV | SS3P6L-M3/86A, both anodes toVIN_FUSED, K toVIN_CLAMP; Vishay88987 pp1–4 | YES, corrected project model exists | CONDITIONAL: reverse/retained-charge and pulse/thermal bounds |
| D_SOUT | Separate Schottky, anodeGND_PWR/cathode24V_ELEC; exact MPN TBD | CONNECTIONS_ONLY | NO: pulse/VF/negative-excursion verification missing |
| F1 | 0451002.MRL2 A candidate remains PENDING_USER_APPROVAL; reassessment below | Symbol only; footprint missing | NO: source clearing/interrupt/inrush coordination |
| R_LIM | **62.0 kΩ1% engineering starting proposal**, replacing the historical43.2 kΩ only after review; derivation below | CONNECTIONS_ONLY; value provisional | NO: nominal curve point is not a guaranteed threshold |
| R_FAULT |15 kΩ, if monitored;3V3 pull-up; NIS Table1/AND90248 §1.2 | YES for value/connection; exact resistor MPN/CAD not selected here | YES for static pull-up calculation; MCU pad/power-state check remains |
| C_DVDT | Low-leakage ceramic toGND; value TBD, or DNP only after startup check | CONNECTIONS_ONLY | NO: C_total,max and permitted inrush missing |
| C_EF_IN | One local bypass network on the one active input rail; C/ESR/ripple/MPN TBD; AND90248 §2.2 | CONNECTIONS_ONLY | NO: source impedance/droop target unknown |
| C_EF_OUT | No extra bulk value is prescribed; use required buck input banks, then assess extra damping/storage; AND90248 §2.3 | CONNECTIONS_ONLY | NO: C_total,max/inductive energy unknown |
| Buck input banks | Per buck≥4.7 µF effective ceramic plus existing2×220 nF bypass; TI §10.2.1.2.6; retain100 V X7R candidates | Existing connections available; principal cap footprint blocked | NO: actual bank count, Ceff/max C and ESR remain open |
| EN network | Default-on internal pull-up, no24 V connection; optional later external LOW inhibit | YES for documented low-inductance default | CONDITIONAL on always-on/retry policy and external control behavior |

### 9.4 TDS3011P versus TDS3311P

The [Semtech-authored TDS3311P Rev2.4,23-Mar-2021 PDF](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf) is readable through the distributor-hosted web viewer; a local download timed out. [Semtech's official portal](https://www.semtech.com/products/circuit-protection/surgeswitch/tds3311p) corroborates the33 V part and advertises a later2023-12-05 release. Do not represent the distributor copy as that later revision.

| Quantity | Saved TDS3011P Rev2.0 p2 | TDS3311P Rev2.4 p2 |
|---|---|---|
| Working voltage |30 V |33 V |
| Breakdown,1 mA |34–39 V |36–41 V,39 V typical |
| Clamp,35 A |38 V typical/40 V max |40.5 V typical/42 V max |
| Clamp,24 A | Not separately tabulated in saved table |40.3 V typical/41 V max |
| Leakage at rated working voltage,25°C |0.05 µA typical/1 µA max |0.13 µA typical/0.60 µA max |
| Package / pins | DFN1.6×1.6×0.55 mm, six leads;1–3 GND,4–6 IN | Same dimensions/functions, p7 pin table; all six connect |
| Reference lands | p6:0.30×0.65 mm,0.50 pitch,1.45 row centers | p8: same listed dimensions,0.80 inside gap/2.10 outside extent |

Clamp entries use the specified1.2/50 µs voltage,8/20 µs current combination with2 Ω source; they do not cover sustained OV or all-temperature system overshoot. Recommend3311 for the regulated30 V maximum:3 V working headroom, versus zero for3011. If30 V is a setpoint with+5% tolerance,31.5 V fits33 V before ripple;33 V is not permission to ignore additional tolerance. The tradeoff is2 V higher maximum clamp and18 V arithmetic headroom to the60 V NIS/buck ceiling. All-temperature leakage and actual clamp-plus-layout overshoot still require checking. This proposed substitution affects the **electronics supply**, not the external DO rail; it does not certify BSP short protection.

### 9.5 NIS3071 pin checklist and MT4 policy

Use [April2026 Table1 p2](../../hardware/academic_rev1/libraries/sources/input_protection/NIS3071-D.PDF#page=2), Basic Operation/Enable pp5–6 and Table4. `EP` is the project's identifier for the manufacturer's unnumbered ground PAD.

| Pin | Function | Manual connection |
|---|---|---|
|1 | OUT1 |24V_ELEC, only the two buck input branches |
|2 | IN1 |VIN_CLAMP with local C_EF_IN return |
|3 | IN2 unused |GND_PWR |
|4 | OUT2 unused |Intentional NC |
|5 | FAULT active-low open-drain |Optional15 kΩ to3V3 and MCU input; otherwise NC |
|6 | dvdt |C_DVDT toGND_PWR, value TBD; do not hard-ground; DNP not yet released |
|7 | ILIM |R_LIM toGND_PWR, candidate62.0 kΩ; no open/short substitute |
|8 | GND |GND_PWR |
|9 | OUT4 unused |Intentional NC |
|10 | IN4 unused |GND_PWR |
|11 | IN3 unused |GND_PWR |
|12 | OUT3 unused |Intentional NC |
|13 | EN4 unused |GND_PWR |
|14 | EN3 unused |GND_PWR |
|15 | EN2 unused |GND_PWR |
|16 | EN1 |Open for documented internal-pull-up default ON; external LOW can inhibit. Do not tie toVIN. Driven-high recommendation for high output inductance requires a separately bounded startup-capable logic source |
|PAD / EP | Ground pad |GND_PWR and board thermal copper; never NC |

R_FAULT gives at most3.3/15k≈0.220 mA and0.726 mW at nominal3.3 V, below Table3's0.5 mA output-sink limit; use actual rail/resistor tolerances for final ERC/current check. FAULT is not power-good: UVLO can produce HIGH with an external pull-up. **AND90248 §4.2 contains a polarity wording conflict; the current datasheet's active-low truth table governs.** Its older figure references also map to Figs9–11 in Rev3 for Cdvdt.

MT4 Auto-Retry is confirmed by ordering p11 and Fig4 p7. ITH overcurrent starts an approximately1.5 ms timer; ICB=2×ITH trips in approximately6 µs. Thermal shutdown is approximately175°C with27°C hysteresis; normal operation must remain within150°C. Do not infer a fixed retry period that is not bounded in the table. Auto-retry is suitable in principle for restarting **electronics**, provided repeated startup/fault heating is acceptable and DO control remains safely off through each reset. That DO reset/drive guarantee remains blocked in the existing readiness gate. No hazardous load is permitted to restart merely because this review proposes MT4; the choice is conditional, not a fault-latching guarantee.

### 9.6 Input-current budget and RLIM derivation

The existing [rail allocation calculation](evidence/electrical_closure/electrical_calculations.json) gives `P_load =3.3×0.7 +5×0.1 =2.81 W`. This already includes BSP logic input/translator allowances. The former extra1 A DO drain current is excluded. At18 V and an **assumed**, not proven,75% buck efficiency, bare input current is0.208 A. A screening calculation allowing0.60 V series drop,0.155 Ω hot NIS resistance and1.2 mA bias gives approximately**0.217 A**. The0.60 V and1.2 mA are engineering allowances based on limited datasheet conditions, not guaranteed cold-diode or one-channel-loaded limits. Therefore this is a usable design estimate, not a final worst-case current. [Reproducible calculation](evidence/input_protection_final_review/calculations.json).

Rev3 Fig5 has a typical≈1 A ITH curve near60 kΩ; Fig7 explicitly characterizes62 kΩ. **Propose62.0 kΩ1% as a starting value**, giving roughly1 A ITH and2 A ICB typically, about4.6× the screening running current. This retains startup allowance without reusing the earlier DO-sized1.4 A setting. It does not derive an exact guaranteed threshold by assuming `60/R` is a manufacturer equation. MT4 cannot be assigned an arbitrary0.2–0.3 A threshold just because the electronics running current is small; the datasheet's settable lower-range limitations apply.

To release R_LIM, establish `I_run,max + I_cap,max + I_start,extra < ITH,min(R,T,V)` or explicitly validate the allowed trip-time excursion; also check the upper ICB bound against downstream copper/connector/fault ratings. Table3 only gives1.9–2.1 A bounds at30 kΩ under its test conditions. It gives **no equivalent guaranteed tolerance for62 kΩ or43.2 kΩ**. Obtain supplier/manufacturer bounds or qualify the actual startup/fault envelope. The original43.2 kΩ exact resistor CAD remains available but is not automatically the new value; no62 kΩ MPN or model was added here. Final R_LIM is **proposed62.0 kΩ / electrically unapproved**, not a claimed1 A limiter.

### 9.7 Capacitance, ramp calculation and passive closure

AND90248 §2 does not prescribe universal100 µF capacitors. It calls for input filtering per independent rail and output capacitance suited to inductive energy. For this one-channel circuit there is one independent input/output; unused grounded channels do not receive duplicate bypass networks. Rev3 Table3's100 µF CIN/COUT entries remain characterization conditions. C_EF_IN must be located onVIN_CLAMP/IN1; it does not replace the two local buck banks downstream.

For startup, bound the **maximum charge drawn**, not merely the DC-biased minimum capacitance. Include both buck input banks, added24V_ELEC bulk, tolerance/low-bias capacitance, attached equipment and converter startup current. TI's minimum two-bank effective ceramic total is `2×(4.7+2×0.220)=10.28 µF`. That is a **minimum operating requirement**, not C_total,max: the principal bank quantities are still blank in the current BOM. The3.3 V/5 V output capacitors are not simply parallel24 V capacitors; their charging appears through the converters as additional input/startup demand.

For an approximately linear input-voltage ramp:

```text
I_charge = C_total,max × (dV_ELEC/dt)_max
t_ramp,required >= C_total,max × V_ELEC,max / I_charge,budget
I_charge,budget <= ITH,min - I_run_during_start,max - I_start,extra,max
```

At the illustrative1.5 ms typical default ramp and30 V, just10.28 µF would require≈0.206 A charging; adding the0.217 A screening load gives≈0.423 A. That does **not** approve leaving dvdt open: ramp time is not a guaranteed minimum, actual C_total,max and converter startup are unknown, and the actual dV/dt must be bounded. Neither “Cdvdt required” nor “DNP is safe” can be closed numerically yet.

Worked example **only**, not a selected capacitor bank: if C_total,max=100 µF and a0.30 A charging budget were justified, the required ramp at30 V is≥10 ms. AND90248 §2.1's24 V/25°C example reads approximately65 pF for11 ms. It illustrates curve selection; it is not proof that65 pF guarantees10 ms over18–30 V,−40…125°C, tolerances and real loading. Use Rev3 Figs9–11 with the **fastest** applicable ramp corner, capacitor/stray capacitance and startup tests. No exact final C_DVDT can be calculated until C_total,max and charging-current budget are supplied; do not populate68 pF merely by rounding the example.

C_EF_IN sizing additionally needs permitted droop and source-response time (`C >= ΔI·Δt/ΔV` as an engineering approximation), ESR/ripple limits and cable impedance. Extra C_EF_OUT/damping depends on output interconnect energy (`E_L=½LI²`) and allowable voltage excursion; this may be unnecessary beyond buck banks, but DNP needs evidence. Rate every capacitor onVIN_CLAMP/24V_ELEC for the **actual** clamp plus overshoot/temperature, not30 V alone. A35 V bulk part is unsuitable against the42 V candidate clamp; even a nominal50 V part needs margin review. Existing100 V X7R candidates remain subject to Ceff/MPN/footprint qualification. No new bulk value, inductor filter, output-clamp MPN or capacitor MPN was invented.

### 9.8 Fuse, voltage and thermal release checks

**0451002.MRL remains a candidate, not approved.** Its125 VDC rating covers normal30 V. Manufacturer451/453 Rev01-Dec-2025 pp1–3 specify50 A interruption at125 VDC and300 A at32 VDC; the2 A row additionally lists10,000 A at75 VDC. Apply a documented rating/test condition, not an interpolated breaking-current curve. Standard25% continuous derating gives1.5 A before temperature rerating, ample for the0.217 A running estimate. It is therefore not too small in normal service, but is oversized as a precise electronics limiter. It remains backup for upstream/failed-semiconductor faults only if source clearing current, wiring withstand and startup/pulse coordination support it. A source limited below2 A may never open it. Melting I²t0.530 A²s is not total clearing energy; at4 A the specified opening limit is5 s, not immediate semiconductor protection. [Official fuse datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1).

Normal input is within the NIS8–60 V application range and both bucks' input range. NIS Table2 limitsVIN/OUT to60 V steady andIN to65 V for≤100 µs; the buck60 V ceiling is stricter than that NIS transient allowance. The42 V TDS table entry leaves18 V arithmetic headroom, but only verified waveform/temperature/layout limits can establish an actual maximum. EN must remain−0.3…6 V, and negativeOUT excursion needs the separate clamp assessment. Retained-charge reverse stress, source overshoot and the external DO rail remain distinct checks.

At the0.217 A screening current, hot NIS conduction loss is≈7.3 mW; adding an illustrative30 V×1.2 mA bias term gives≈43 mW. D_REV loss using the0.60 V allowance is≈0.13 W. These are favorable screening results, **not complete thermal approval**: bias conditions, cold/hot VF, ambient, actual copper θJA, startup linear-mode energy and repeated retry dissipation remain unknown. Check `Tj=Ta+P·θJA` using the actual board thermal path. Do not use175°C shutdown as the allowable operating target. TDS pulse energy/repetition and fuse temperature derating require their own checks.

### 9.9 Exact remaining inputs, references and CAD disposition

| Needed input | Decision it closes |
|---|---|
| Supply exact MPN; maximum setting+tolerance+ripple; current-limit/hiccup behavior; prospective short current and upstream protection | TDS33 V working margin; F1 interruption/clearing; sustained OV assumptions |
| Allowed reversed-input voltage and hot-swap while downstream charge is retained; source/cable length and inductance | D_REV60 V margin; input clamp/overshoot and local bypass |
| Final buck CIN counts/MPNs and C(V,T,tolerance) curves; any extra24V_ELEC bulk and attached equipment | C_total,max, C_DVDT versus DNP and startup energy |
| Guaranteed/minimum buck efficiency and startup demand over the intended operating range; allowable input charging current and startup time | Final running-current bound, R_LIM margin and ramp selection |
| Ambient range, copper/stackup/thermal path; acceptable fault energy/retry policy | Diode/NIS/fuse thermal release and MT4 suitability |
| External DO supply/return connection and offset/fault current; verified reset-off behavior | Valid exclusion of drain current, return routing and safe electronics retry; no main-input fuse protection claim for DO feed |
| Output connection L/current and negative-excursion limit/measurements | D_SOUT MPN/current/VF and optional output bulk |

References used for this section:

- **NIS3071/D April2026 Rev3**: local PDF linked above; Tables1–4 pp2–5, Fig4 p7, Fig5 p7, Fig7/Figs9–11 p8, ordering p11. [Official current endpoint](https://www.onsemi.com/download/data-sheet/pdf/nis3071-d.pdf) is readable; this resolves only the earlier web-access issue, not any electrical gate.
- **AND90248/D September2023 Rev0**: [saved official PDF](../../hardware/academic_rev1/libraries/sources/input_protection/AND90248-D.pdf), [official endpoint](https://www.onsemi.com/download/application-notes/pdf/and90248-d.pdf); §§1.1–1.2 p2, §§2.1–2.3 and3.1–3.2 p3. Current datasheet governs the polarity/figure-reference discrepancies noted above.
- **Semtech TDS3011P Rev2.0**: saved local PDF pp2,5–6. **TDS3311P Rev2.4**: manufacturer-authored distributor-hosted PDF p2 ratings, p7 Fig6 pin table/layout, p8 lands, p9 ordering. Semtech portal links a later release; obtain that exact official PDF as `hardware/academic_rev1/libraries/sources/input_protection/TDS3311P.pdf` and reconcile before final release. No fake local3311 link was created.
- **Vishay88987 Rev24-Apr-2020**: saved SS3P6L PDF pp1–2 ratings/terminal functions and p4 land pattern. **Littelfuse451/453 Rev01-Dec-2025**: official web PDF pp1–4; local retrieval still denied403. Existing exact fuse PDF/footprint request remains open.

Read-only Electronics AI inventory still shows**50 symbols/26 footprints**. NIS and corrected SS3 models exist; TDS3011 exists, **TDS3311 does not**. Compatible pin functions and listed lands make3311 a plausible reuse candidate, but do not rename3011's MPN or claim a new verified symbol. Fuse remains symbol-only. D_SOUT and the proposed62 kΩ resistor have no exact prepared model; the current mapping still lists the earlierSMBJ33A draft and43.2 kΩ resources. This review changes **only the connection reference**, not those selections. Prior native compile is stale for the last library additions; no compile or native session was started here.

**Release decision:** manually draw the defined series/shunt structure, NIS pin groups, grounds and15 kΩ optional status pull-up. Keep TDS3311,62 kΩ, F1 and all TBD/DNP choices visibly provisional. **SCHEMATIC_READY: CONDITIONAL for documented connectivity; not a fully valued released sheet. ELECTRICALLY_APPROVED: NO** until the specific current, capacitance, source-fault, return and thermal inputs above are closed. This is the exact remaining dependency; the external-DO assumption alone cannot supply those numbers.
