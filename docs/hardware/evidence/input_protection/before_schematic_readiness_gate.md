# Academic Revision - schematic capture gate

Date: Saturday, November 7, 2026. **CONDITIONAL GO for the independently defined
sheets below.** Complete power-input, buck-capacitor and DO closure is still
required. This is a capture gate, not approval for purchase, PCB fabrication,
industrial immunity or connection to uncontrolled field wiring.

## Final architecture and permitted capture

| Subsystem | Selected operating configuration | Capture status / remaining gate |
|---|---|---|
| MCU | STM32H723VET6, LQFP100, internal LDO; 3.3 V VDD/analog/backup supplies; no battery, VREFBUF disabled; SWD, BOOT0 recovery and NRST | CONDITIONAL GO. Connections and package pin numbers closed; VCAP capacitor ESR/bias and physical reset/header selections need qualification |
| Clocks | Two independent KC2016Z25.0000C15XXK oscillators at 3.3 V: one to MCU HSE bypass, one to PHY XI. PHY RMII Leader supplies the MAC's 50 MHz reference | CONDITIONAL GO. Shared fan-out rejected as unproven; oscillator/PCB load and PHY phase-noise mask remain open |
| Ethernet | DP83826IRHBR, ENHANCED/RMII Leader, address 0, autonegotiation/Auto-MDIX; HX1188FNL and SS-7188S-A-NF; complete EVM transformer-coupled termination variant; PHY-side TPD4E05U06 | CONDITIONAL GO. Pin/winding/termination map closed; clock qualification, chassis safety policy and HV-passive CAD remain |
| 3.3 V buck | LMR36015FBRNXR, 1 MHz FPWM, 6.8 uH XAL4030-682MEC, 100 k / 43.2 k feedback; 0.7 A design allocation | NO-GO for final power-sheet closure: CIN effective-capacitance quantity and COUT bias/ESR/transient/thermal checks open |
| 5 V buck | LMR36015FBRNXR, 1 MHz FPWM, 10 uH XAL4040-103MEC, 100 k / 24.9 k feedback; 0.1 A allocation | Same power gate. Retained part is the FB variant; no LMR51430 substitution |
| Single input | Fused positive input, series reverse diode, shunt TVS after diode, local buck decoupling; no redundant ORing, no added LC filter | NO-GO for protected-input completion. SS3P6L and SMBJ33A are bounded prototype candidates; fuse/bulk and fault coordination remain unselected |
| RS-485 | One THVD1420DR at 3.3 V, half duplex, **115200 baud, 8N1** capture default; internal protection; DE low and nRE high at reset; no external bias | CONDITIONAL GO for this limited configuration. SM712 + two 10-ohm resistors retained as unqualified optional network, not an approved surge circuit |
| CAN-FD | ATA6561-GAQW: VCC 5 V, VIO 3.3 V; startup standby; nominal 1 Mbit/s / data 2 Mbit/s design target; no external TVS/choke/shunt filter | GO for basic-node capture. Cable timing/EMC qualification remains; optional conventional 120-ohm termination only at a physical bus end |
| DI | One ISO1212DBQR, two Type 3 inputs, 562 ohm RSENSE / 1 kohm MM204 RTHR / 10 nF CIN per channel; group-isolated FIELD_COM | CONDITIONAL GO for normal 18-30 V sensing. No MM204/system surge rating established |
| DO | Two BSP75NTA low-side protected switches, intended 0.5 A each, SN74LVC2T45 3.3-to-5 V drive candidate | NO-GO: authoritative Diodes terminal numbering and guaranteed >=4.5 V protected drive remain unresolved; thermal/inductive envelope also conditional |

The baud/bit rates above are selected engineering defaults, not a previously
confirmed field-bus contract. Changing them reopens timing and protection review.
The two DI channels share field COM in the selected TI group-input topology;
channel-to-channel isolation is not claimed. Logic GND, FIELD_COM and chassis are
distinct domains. No additional interfaces or redundant input were restored.

**P0 closure accounting: 5/8 specific capture decisions closed:** MCU pin/power/
reset/boot connections; PHY mode/straps/reset; magnetics/RJ45/MDI topology;
regulator identity/feedback/ripple calculations; main P0 IC pin-to-pad models
(MCU, PHY, regulator). The three open gates are clock qualification, buck
capacitance/stability/thermal closure and protected input coordination.
"Closed" here does not approve their subsequent PCB layout or hardware tests.

**P1: 3/4 subsystems may begin capture** (RS-485, CAN, DI), with the limits in the
table; DO remains blocked. This does not mean three surge-qualified interfaces.

## Accepted decisions and exact evidence

### MCU connections and clock boundary

DS13313 Rev 5 figure 5/table 7 gives VDD 11/27/50/75/100; VSS
10/26/49/74/99; VDDA 21; VSSA 19; VREF+ 20; VBAT 6; VCAP 48/73;
PH0 12; PH1 13; NRST 14; BOOT0 94; SWDIO PA13 72; SWCLK PA14 76.
All 100 numbered symbol pins and the LQFP100 footprint remain available.
[The pin-role reservation table](evidence/electrical_closure/capture_pin_bindings.csv)
records the selected Ethernet, USART3, FDCAN1, GPIO, oscillator and IC pin bindings;
it is documentation, not an emitted schematic or compiled netlist.
Do not add SMPS, VDD50USB or VDD33USB pins absent from this package.

Adopt AN5419 table 2/figures 3, 15, 19 and section 6: one 100 nF per VDD,
the existing bulk/analog/backup decoupling, two local 2.2 uF VCAP capacitors
for LDO mode, no external VCAP load, NRST 100 nF to GND and BOOT0 10 kohm
to GND with recovery access to 3.3 V. VREF+ follows VDDA with VREFBUF disabled;
VBAT follows VDD. VCAP ESR must be below 100 mohm (DS table 14); the selected
KEMET nominal part is retained subject to that application check. HSI boots the
MCU while the external oscillator starts. No new MCU clock-frequency/firmware
configuration was applied.

SWD six-position **project pinout**: 1=VTref, 2=SWDIO, 3=GND, 4=SWCLK,
5=NRST, 6=GND. This is not an ARM-standard keyed connector. VTref does not
power VDD. The existing pushbutton footprint remains unfinished; NRST is still
available through SWD. Check BOOT option bytes during commissioning.

[Kyocera specification](https://ele.kyocera.com/assets/products/crystal-device/specification/KC2016Z25.0000C15XXK_e.pdf),
TNY1T-H1-DEX01-11, pp3-4,6/table2/figure4: pins 1=standby,2=GND,3=OUT,4=VCC;
tie standby HIGH. Each oscillator gets a local **10 nF** bypass. No crystal load
capacitors or crystal drive resistor are populated. Its 15 pF output-load limit
includes receiver, route, pads and measurement loading. It specifies total
frequency error +/-30 ppm, 45-55% duty and 2.5 ns maximum edges at 3.3 V.

ST DS table31 / AN5419 section3 allow 25 MHz on PH0 in HSE bypass; PH1 is
unconnected. At 25 MHz, 45% duty gives an 18 ns shortest HIGH/LOW interval,
above ST's 7 ns minimum. Kyocera 0.9/0.1 VCC output limits clear ST's
0.7/0.3 VDD thresholds on the common rail. PHY section7.6 allows +/-50 ppm,
5 ns edges and 50 ps RMS jitter. The oscillator's 12 ps RMS figure supports
the jitter comparison, but does not establish the separate PHY phase-noise
limits at 1/10/100 kHz and 1 MHz offsets. Obtain that mask evidence or test it.

Direct sharing remains **unverified**: ST lists 5 pF and TI lists XI 1 pF as
typical values, not a bounded total fan-out specification. The independent
topology adds one oscillator and one bypass relative to sharing and eliminates
the branch stub. Each output still needs a <=15 pF load check. PHY pin19 drives
only MCU PA1/ETH_RMII_REF_CLK, not PH0. RMII clock/data setup, hold and return-path
closure remain layout/timing tasks; a frequency match alone is not approval.

### Ethernet - one complete termination implementation

Use TI DP83826EVM SNLU262A figure6-2 / native-reference **sheet3**, T2/J17/U13 and
table7-1, with the current SNLS647I pin requirements. The EVM's CEXT=100 nF
conflicts with current table5-1: **retain 2 nF on CEXT2**, not the EVM value.
RBIAS10 remains 6.49 kohm/1%. Both PHY supplies use the existing local banks.

Freeze ModeSelect1 NC/internal HIGH=ENHANCED, strap1/CLKOUT31 internal1,
RX_D2/strap8 pin14 HIGH through 2.49 kohm, TX_CLK/strap5 pin22 default0=Leader.
Keep PHY address straps pins30/29/28 at000; default Auto-MDIX/autonegotiation
and CRS_DV configuration. No strap LEDs/load are selected. MCU pads must be HiZ
at POR; strap1's POR-only behavior is retained. Sources: tables8-6 through8-10,
figure8-13. Read back strap status during commissioning.

RESET32 is a dedicated MCU-controlled signal; do not casually merge it with
NRST. TI section7.6 requires reset LOW >=25 us, >=2 ms after release before
SMI, and >=50 ms after power-up before SMI. Accommodate oscillator startup
up to5 ms and TI's specified supply-ramp window. RMII clock after reset is
specified separately; firmware must not assume it exists while PHY reset is LOW.

[Pulse HX1188FNL revB](https://productfinder.pulseeng.com/doc_type/WEB301/doc_num/HX1188FNL/doc_part/HX1188FNL.pdf),
sheets2-3, establishes 1:1 windings, 350 uH minimum, 1500 Vrms/60 s isolation
and exact terminal polarity. This is the same family used in the TI EVM.

| Connection | Exact endpoints |
|---|---|
| PHY TD+ / TD- | PHY7/6 -> magnetics1/3 |
| PHY RD+ / RD- | PHY5/4 -> magnetics6/8 |
| PHY-side taps | magnetics2 and7; **two parallel100 nF to logic GND per tap**, four total |
| Cable TX | magnetics16/14 -> RJ451/2 |
| Cable RX | magnetics11/9 -> RJ453/6 |
| Cable taps | magnetics15 and10 each through75 ohm to shared node ->1 nF/2 kV ->chassis |
| Unused cable pairs | RJ454+5 and7+8 each through75 ohm to second node ->second1 nF/2 kV ->chassis |
| NC magnetics | 4,5,12,13 unconnected |
| Shield | RJ45S1/S2 ->chassis; no default direct logic-GND tie |

The Bob Smith network is **selected as the TI EVM recommendation**, not claimed
mandatory for every Ethernet product. Do not superpose datasheet figure9-2's
different RC network or add four external49.9-ohm MDI terminations. Retain two
separate cable-side AC-return nodes as the EVM draws them. Confirmed BOM:
4 x CRCW080575R0FKEA, 2 x C1206C102KGRACAUTO; the HV capacitors' application
safety class and CAD remain unqualified. Logic/chassis EVM C61/R51 coupling is
DNP until a PE/insulation policy exists; an arbitrary resistor must not bridge
the Ethernet barrier.

[Cinch drawing CT710001 B0](https://www.cinch.com/media/drawings/products/ethernet-usb/dr-stw-ss-7188s-a-nf-ss-7188s-a-nf-50.pdf)
confirms contact numbering and distinct mounting/shield holes. The footprint
uses its component-side hole map; copper-land sizes are documented engineering
candidates requiring fabrication review. No other RJ45 footprint is substituted.
The exact jack remains selected despite unknown assembly stock.

The [TPD4E05U06](https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf)
SLVSBO7O table4-2 plus **Ethernet EVM U13** justify PHY-side placement: TD+/TD-
to1/2, RD+/RD- to4/5, GND3/8 to logic GND. NC10/9/7/6 permit straight-through
routing in that example. This is not an HDMI circuit transfer or a cable-side
surge protector. Preserve the magnetics barrier and low-inductance intended
return. Component ESD ratings do not certify this board.
The NC pads are not internally wired series terminals: straight-through use
requires continuous external copper joining the corresponding same-net pads.

### Power - calculations completed, capacitor/fault gates retained

The machine-readable [calculations](evidence/electrical_closure/electrical_calculations.json)
separate source bounds from engineering allowances. The 3.3 V budget is
**619.2 mA**: MCU430, PHY70, THVD output60 plus quiescent1.8, ISO logic1.9,
CAN VIO0.5, oscillator allowance20, other allowance35. The MCU bound is the
DS13313 table20 550 MHz/all-peripherals/Tj105 C case, conservatively retained
without approving that operating temperature or clock speed. The PHY bound is
SNLS647I section7.5 100%-traffic Leader. THVD's60 mA is an output bound, not
its no-load ICC. The 5 V budget is **83.4 mA**, including CAN dominant70,
two BSP inputs2.4, two pull-downs1 and allowance10. Allowances are not measured
maxima. Both fit the prior0.7/0.1 A allocations and the1.5 A converters; actual
temperature/layout still limits capacity. DO load current comes directly from
the field input, not either buck output.

SNVSB49D equations3-5 and table10-1 yield:

| Derived quantity | 3.3 V design | 5 V design |
|---|---:|---:|
| Feedback nominal output |3.31481 V|5.01606 V|
| FB/reference/resistor tolerance interval, before ripple/line/load |3.21994-3.41200 V|4.86249-5.17365 V|
| Ripple at30 V, nominal L/1 MHz |0.432 A|0.417 A|
| Ripple at f=0.85 MHz,L=-20% |0.635 A|0.613 A|
| Peak at0.7/0.1 A design load |1.018 A|0.406 A|
| RMS at that corner |0.724 A|0.203 A|
| I-squared-DCR loss at25 C |0.039 W|0.0038 W|

[Coilcraft document806](https://www.coilcraft.com/getmedia/6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf),
pp1,4 supports the exact inductors and lands. Isat25 C is a typical30%-drop
criterion, not a hot guaranteed limit; fault-current/core-loss review remains.
Use independent CIN banks, two220 nF VIN-PGND HF capacitors per converter,
100 nF BOOT-SW and1 uF/16 V minimum VCC-GND. VCC is not the load5 V rail.
EN=VIN and unused PG are the selected minimum configuration. Join NC3 to SW12
per TI; pin12 is not a ground exposed pad. CFF20 pF remains conditional.
The ideal minimum on-times at30 V/fmax are95.7/144.9 ns for3.3/5 V,
above the83 ns maximum minimum-on-time specification; this is a calculation,
not a transient or hardware test.

**Capacitance wording resolved:** section10.1 generally means effective
capacitance, while **table10-1 explicitly labels its COUT columns RATED
CAPACITANCE**. Retain the table's3x15 uF nominal COUT example; do not call it
45 uF effective or guaranteed stable. CIN>=4.7 uF is an effective requirement.
Official TDK bias/ESR characterizations could not be retrieved locally (403),
so CIN count remains unknown and COUT bias/ESR/transient qualification is open.
No invented bias percentage, generic inductor or nominal-only stability claim
was used. TI section10.2.1.2.10 explicitly warns against using its standard
thermal-table RthetaJA as a board-design guarantee; thermal closure needs actual
losses, copper, ambient and enclosure.
An additional concrete failure is **CVCC**: the retained Samsung nominal1 uF
candidate has about0.656 uF typical at the internal5 V rail in the existing P9
bias evidence, before tolerance/temperature/aging. A single part therefore does
not establish TI's1 uF effective requirement. Both CVCC BOM rows are blocked
until a qualified capacitor/bank and internal-LDO compatibility are established;
they are not approved merely because their voltage rating is high enough.

The selected prototype input topology follows
[TDK-Lambda figure5 and input-protection discussion](https://www.us.lambda.tdk.com/resources/blogs/20250102.html)
and TI section11. It is **not released**. Vishay88987 supports the SS3P6L
series diode candidate. The Littelfuse SMBJ33A row gives33 V standoff and53.3 V
clamp at11.3 A for its specified waveform, leaving only6.7 V to the buck's60 V
limit before parasitics/temperature. It does not hold a DO drain below the
BSP75N's36 V short-circuit-protection condition, nor disconnect sustained OV.
Fusing, inrush, TVS energy, hot-plug ringing, bulk ESR and source current limits
must be coordinated before this sheet is finalized. No IEC surge level is
claimed. Do not substitute a35 V professor bulk capacitor on this clamp node.

### RS-485, CAN, DI and DO decisions

**RS-485:** SLLSF78B figure8-5/table8-1 has **R1 AND R2**, each10 ohm
CRCW0603010RJNEAHP; one resistor per line. THVD1400/1420 share the same bus
recommended common-mode -7..+12 V and +/-16 V absolute limits. The
[Bourns SM712](https://www.bourns.com/pdfs/CDSOT23-SM712.pdf) pp1-3 has75 pF
typical capacitance and positive clamp19/20/26 V at1/5/17 A. Resistance can limit
residual current, but those clamps alone do not prove a safe THVD1420 pin voltage.
At a54-ohm differential load, two10-ohm series resistors give a first-order
54/74=0.730 voltage factor;10 ohm x75 pF=0.75 ns is only a lumped estimate.
Neither calculation transfers the reference's1 kV test. The pictured waveforms
are500 kbaud/THVD1400/5 V, not a qualification of our115200/THVD1420/3.3 V.
Selected capture uses the manufacturer's basic device circuit and internal
protection; optional surge network remains blocked. No industrial surge claim
is accepted. Pins1R,2nRE,3DE,4D,5GND,6A,7B,8VCC; SM7121/2 bus,3 reference.

**CAN:** DS20005991B figures1-1/1-6 and table2.0 support VCC4.5-5.5 V and
VIO2.8-5.5 V. Use100 nF at each supply. STBY internal75-175 kohm pull-up selects
standby while MCU isHiZ; TXD internal20-50 kohm pull-up keeps recessive. Pull
STBY low only after supplies/configuration are valid. Adopt optional conventional
120-ohm termination with an open default jumper at an intermediate node;
populate only at the cable end. The previous split62+62-ohm/4.7 nF option is DNP.
The device supports CAN-FD up to5 Mbit/s; the selected1/2 Mbit/s target still
needs cable/loop-delay validation. Built-in ESD/transient test conditions are not
board compliance. No external CAN TVS or filter was selected.

**DI:** SLLSEY7G section8.2.1.2.1/equations1-4/table5.9/figure8-2 give the
adopted562-ohm/1-kohm Type3 network. Approximate equations give10.5/9.35 V;
the authoritative DC table gives VIH typical/max10.4/10.95 V and VIL minimum/
typical8.7/9.2 V. Use table limits rather than treating approximate equations as
guaranteed thresholds. At2.75 mA and resistor+1%, calculated RTHR/RSENSE powers
are7.64/4.29 mW. The Firstohm MM2040.25 W part has ample normal dissipation
margin under its temperature derating, but **MM204 is not MM204P**. Its actual
non-repetitive surge curve and400 V overload ceiling do not prove TI's system
surge tests. Compare the voltage/current waveform across RTHR, integral I²Rdt,
repetition and temperature with that curve. No waveform/system test is supplied.
For scale only, an assumed exponential500 V pulse actually across1 kohm with
50 us half-voltage decay gives250 W peak and9.02 mJ;1000 V gives1000 W/36.07 mJ.
These peaks exceed the MM204 curve's tens-of-watts region around tens of
microseconds. This is not the voltage automatically appearing across RTHR in
TI's common-mode test fixture. The exact coupling and resistor waveform are
needed; MELF geometry and0.25 W alone do not qualify it.

TI table8-1 for Type3/10 nF distinguishes1 kV line-PE/line-line from500 V
line-FGND;1 kV line-FGND uses330 nF instead. Neither rating is assigned to our
MM204 implementation. VCC1 bypass100 nF; EN tied to VCC1. Field CIN returns to
FIELD_COM, not logic GND. SUB1/SUB2 remain separate unconnected/floating owners,
never grounded or joined; any optional separate copper islands follow table4-2
and layout review. No extra TVS or FGND/PE capacitor populated by default.

**DO:** DS33016 Rev7-2 pp1,3-8 confirms the Source tab and protected-switch
behavior. The exact Diodes SOT223 Type DN drawing was obtained but still does
not number the terminals; no Infineon pinout was transferred. The role-labelled
symbol stays blocked without a numbered footprint. At5 V the input draws up
to1.2 mA and full thermal-protection operation requires>=4.5 V. SCES516N table5.5
guarantees only3.8 V at its4.5 V/-32 mA test point; its near-rail specification
is at100 uA. Interpolation to our load is not a guarantee. Thus the translator
remains selected as a candidate, not an approved BSP driver.

DIR=VCCA, A-side and B-side10-kohm pull-downs define reset OFF intent; the part
has no OE, so rail ramp/startup still needs checking. Cold0.5 A loss is0.169 W,
but the datasheet's minimum-copper table gives only520 mA at85 C; cold RDS and
nominal current-limit ratings are insufficient thermal approval. Inductive
operation needs load L/current, repetition and temperature: the published
550/200 mJ single-pulse conditions must not be made repetitive ratings. No
unverified external suppression network was invented.

## Final BOM and CAD resources

[Final BOM](final_bom.csv) contains **122 requirement rows**:114 retained/new
passive/auxiliary rows plus8 unique active specifications. Active quantities:
MCU1, PHY1, THVD1, ATA1, ISO1, translator1, BSP2 and LMR2. All111 previous
requirement IDs remain. Every changed quantity/MPN/assembly state is recorded
in [the decision overlay](evidence/electrical_closure/bom_decisions.json).
The passive table has78 known mandatory placements, three unresolved mandatory
quantity groups (two CIN banks and input bulk), and8 conditional placements.
It is not a final purchasing total. There are24 ordinary mandatory passive
specifications; clocks/magnetics are separate auxiliary categories. The earlier
26-specification inventory included their unresolved requirements and remains
historical evidence. Physical-package compatibility is recorded separately.

JLCPCB Basic/Preferred status is **unknown** for unobserved parts; no substitution
was made for a lower price. Public JLC evidence identified MM204/C233005 as
Extended and reported out_of_stock without a quantity. This is incomplete public
catalog evidence, not a reservation or proof of zero LCSC inventory. The confirmed
RJ45 remains in the academic BOM with separate unknown sourcing risk.

Project-local files: `hardware/academic_rev1/libraries/Gateway_Academic.SchLib`,
`.PcbLib`, `.LibPkg`, and `Project Outputs for Gateway_Academic/Gateway_Academic.IntLib`.
They now contain **46 symbols /23 footprints**, including nine added symbols and
eight footprint candidates: oscillator, magnetics, both inductors, SM712, DQA ESD,
exact RJ45 and MM204; Yageo10k reuses the documented candidate0603 resistor lands.
Every addition was saved through Electronics AI and independently read back.
No original professor library was changed. Existing37/15 objects were retained.

Altium compilation completed and regenerated IntLib. The actual message query
returns **six unsuppressed warnings, all `Missing Component Models`, source
`Gateway_Academic.SchLib`; no errors returned**. It does not identify components.
Independent file inventory finds six unlinked retained symbols: BSP75N, reset,
two TDK capacitors and the two superseded older inductor symbols. The new exact
inductor symbols are linked; do not select their older unlinked variants.

The final IntLib's compressed embedded SchLib/PcbLib source bytes match the
current source libraries exactly; the official file reader reads46/23 components.
Its SHA256 is `358fbb2931b64476f4cd528cf62790ce388a69cd66b4a5e30af3139d3360aca4`.
The earlier native Extract Sources call reported an Open Integrated Library modal;
disk inspection found45/23 extracted sources afterward, without replaying the
operation. The final46/23 inventory instead uses the current artifact's own
embedded bytes. This distinction and actual compiler results are retained in
`evidence/electrical_closure/`. No global registration was performed.

Backup before library edits:
`hardware/academic_rev1/libraries/backups/closure_20261107T052419Z/`;
backend timestamped backups also remain. The scripting engine was detached with
`engine_release_confirmed=true`. No repair of the previous script issue was attempted.

CAD_CANDIDATE means useful, source-backed editable model, **not fully qualified
manufacturing geometry**. RJ45 copper annuli, DQA rectangular corner approximation,
mask/paste and courtyards still need DFM review. BSP remains CAD_BLOCKED. Native
representative placement/ERC/hardware tests were not performed in this task.

## Remaining blockers and exact inputs

| Blocker / owner input | Exact requirement or file and destination |
|---|---|
| Clock qualification | Kyocera output phase-noise bounds versus SNLS647I section7.6, plus receiver/route load budget. Save manufacturer response as `hardware/academic_rev1/libraries/sources/electrical_closure/KC2016Z_phase_noise_load.pdf`; no invented pin-capacitance maximum |
| Buck capacitor closure | TDK `c5750x7r2a475k230ka.pdf` and `c3225x7r1c156m250ab.pdf` official characterization PDFs from `https://product.tdk.com/info/en/documents/chara_sheet/`, and exact mounting drawings, into the same directory. Need Ceff/ESR over bias/T/aging, load-step/ripple acceptance and ambient/copper;403 is recorded |
| Input/DO fault environment | Supply current limit and cable, inrush, simultaneous load/fault current, required sustained OV behavior and surge waveform/source impedance/repetition. Then select fuse, bulk and coordinated clamp/disconnect;18-30 V alone does not define these |
| Current TVS source | Obtain `SMBJ33A_Littelfuse_datasheet.pdf` from the [official SMBJ33A product page](https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj33a) into the same source directory before release; the historical manufacturer table supports the candidate, but the old PDF URL now redirects to a missing page |
| BSP mapping/drive | Exact **Diodes BSP75NTA** numbered Type DN symbol/pad drawing or verified editable model proving Source-tab mapping, plus guaranteed loaded driver voltage>=4.5 V. Save as `BSP75NTA_numbered_Type_DN.pdf` or exact `.SchLib/.PcbLib` in the source directory. The fetched `SOT223-Type-DN.pdf` alone does not close numbering |
| DI surge, only if required | Required line-FGND/line-line/PE test levels, coupling/source impedance, repetition and ambient; supplier confirmation/test evidence for exact MM204F1K00TKRTR3K0 or a separately reviewed alternative. Normal sensing can be captured now |
| Mechanical/interface assembly | Exact terminal/reset/header drawings; selected bus-end jumper/connector hardware and chassis/PE policy. These block final connector/insulation completion, not MCU or CAN core capture |

Use the exact sources already saved under `sources/electrical_closure/` before
requesting them again. Firstohm's manufacturer-authored March2023 MM sheet was
obtained from its distributor Alfatec, with URL/hash retained; its pp75-78
contain the actual MM204 curve and reflow lands. Do not substitute the P-series
surge plot. The Cinch, Pulse, Bourns, Coilcraft, Kyocera and TI protection drawings
are already local; they do not need another download.

Start MCU power/debug/reset/boot, CAN basic node, normal Type3 DI and basic
RS-485 sheets using the selected modes. Ethernet connectivity may be captured
with the documented clock/insulation review flags. Hold DO connections and final
protected-input/buck BOM completion. No full schematic, PCB routing, rule import,
stackup change, Rev.A edit, commit or push was performed.

## Verification record

Validation scope: escalated native-CAD/artifact validation. Commands executed:

```text
C:/dev/tools/python/python.exe docs/hardware/evidence/build_passive_deliverables.py
C:/dev/tools/python/python.exe docs/hardware/evidence/validate_passive_deliverables.py
C:/dev/tools/python/python.exe docs/hardware/evidence/electrical_closure/build_capture_bindings.py
C:/dev/tools/python/python.exe docs/hardware/evidence/electrical_closure/verify_closure.py
git diff --check
git status --short
```

Passed: BOM/MPN/quantity change authorization, ID conservation, generator
idempotence, saved pin/pad/link readback for9 symbols/8 footprints, official
source/compiled inventories, compiled-source byte identity and source protection.
Of2782 baseline-hashed files,2779 remained byte-identical; the only changed
baseline native files are the two intended Gateway libraries and their IntLib.
All original37 symbols/15 footprints remain semantically unchanged. Rev.A,
the academic Sheet1/PcbDoc/project, professor sources and firmware were preserved.
`git diff --check` passed; pre-existing firmware line-ending warnings are unrelated.

Remaining unverified: the electrical/application and CAD/DFM gates above.
No full-design ERC/DRC, representative placement, power-loop/thermal test or
industrial compliance test was run. Actual checks and hashes are in
[validation.json](evidence/electrical_closure/validation.json), with the full
compiler warnings and generated inventory retained alongside it.
