# Academic gateway: recovered 24 V input protection

Prepared 2026-11-07. **CONDITIONAL for manual capture of supported connections; the complete input protection sheet is not electrically released.** The agreed architecture remains one 18–30 V input, two LMR36015 bucks and two low-side outputs. No schematic, PCB, Rev. A source or professor library was edited.

Recommendation: retain **one NIS3071MT4TWG channel** as a reuse candidate; evaluate **one TDS3011P.C** after a series reverse-polarity diode. Keep both LTC4414 controllers and both DMP6023LSS-13 ORing MOSFETs excluded. An upstream conventional fuse is proposed for uncontrolled sources, with its rating pending fault/inrush coordination. None of these proposals silently changes the current BOM.

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
