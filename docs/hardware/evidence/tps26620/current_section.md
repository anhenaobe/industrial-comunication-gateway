## 10. Academic Revision — Approved Schematic Connection Plan

**Current baseline, 2026-11-07; supersedes the NIS3071 circuit proposals in sections1–9.**
The user approved TPS26620DRCR as the eFuse replacement and retained the fuse,
series diode and TDS3311P.C. Component approval is separate from application-setting
review, saved CAD verification and physical testing. The external settings below are
**PROPOSED_APPLICATION_VALUES**, calculated for the supervised academic prototype.
No native schematic or PCB was changed. Earlier industrial release gates are historical,
not prerequisites for beginning the supported manual schematic connections here.

### 10.1 Operating assumptions and topology

Nominal24V, regulated current-limited laboratory supply;18–30V design target,
supervised bring-up at24V, short local wiring, no IEC/EMC or industrial surge claim.
The two bucks retain3.3V/0.7A and5V/0.1A allocations. External DO drain currents are
excluded. No redundant input, LTC4414 or DMP6023LSS stage is restored.

```text
SERIES: J_IN+ -- F1 2A -- D_REV (anodes1 AND2 -> cathodeK) -- VIN_CLAMP
                                                               |
                                                           TPS pin1 IN
                                                           TPS pin10 OUT --24V_ELEC--+--3V3 buck
                                                                                   +--5V buck
SHUNT:  VIN_CLAMP -- TDS3311P.C (IN4/5/6; GND1/2/3) -- GND_PWR
BYPASS: VIN_CLAMP -- [4.7uF100V || 220nF100V] -- GND_PWR
RETURN: J_IN- ------------------------------------------ GND_PWR -- TPS pin6 GND

SETTING LADDER (series resistors, separate reference):
VIN_CLAMP --768k-- UVLO pin2 --33.2k-- OVP pin3 --30.1k-- EF_RTN
TPS pin7 ILIM --13.3k-- EF_RTN
TPS pin8 dVdT --10nF-- EF_RTN
TPS pin5 RTN and thermal pad11 --------------------------- EF_RTN
EF_RTN IS NOT DIRECTLY CONNECTED TO GND_PWR.
```

**Retain SS3P6L.** TPS26620 already provides input reverse-polarity protection, but
removing the series diode would expose the upstream unidirectional TDS to reverse
input and forward conduction. Removing it requires a separately reviewed TDS/fuse
arrangement; that simplification is not implemented. Input reverse protection,
reverse-current blocking and surge suppression remain different functions.

F1 provides approved backup protection for wiring/front-end faults; a laboratory
current limit below2A may prevent it opening, which is expected. It does not provide
instant semiconductor protection. D_REV blocks ordinary reversed input; TDS shunts
specified transient pulses; TPS provides adjustable UV/OV cutoff, current limiting
and overload/thermal latch-off for the electronics. TDS is not a continuous OV regulator.
Keep the positive suppressor return short to GND_PWR; never use EF_RTN as its return.

### 10.2 Exact component and capacitor selections

| Function / quantity | Exact MPN / value | Connection and status |
|---|---|---|
| F1 ×1 | Littelfuse0451002.MRL,2A | APPROVED prototype selection;125VDC, manufacturer interruption table applies, not guaranteed coordination with all sources |
| D_REV ×1 | VishaySS3P6L-M3/86A | APPROVED;60V Schottky;1/2anodes to VIN_FUSED,K to VIN_CLAMP; footprint and terminal map unchanged |
| D_TDS ×1 | SemtechTDS3311P.C | APPROVED;33V working,42V specified maximum clamp at the stated35A pulse condition; not universal overshoot limit |
| U_EF ×1 | TI TPS26620DRCR | APPROVED COMPONENT SELECTION; adjustable OV cutoff, **latch-off**, not auto-retry |
| R_ILIM ×1 | YageoRC0603FR-0713K3L,13.3kΩ1%,0.1W,0603 | Proposed0.50A setting; replaces62kΩ NIS setting only |
| R_UV_TOP ×1 | RC0603FR-07768KL,768kΩ1%,0.1W,0603 | IN to UVLO |
| R_UV_MID ×1 | RC0603FR-0733K2L,33.2kΩ1%,0.1W,0603 | UVLO to OVP |
| R_UV_BOTTOM ×1 | RC0603FR-0730K1L,30.1kΩ1%,0.1W,0603 | OVP to EF_RTN |
| C_DVDT ×1 | KEMETC0603C103K1RACTU,10nF10%,100V X7R,0603 | Proposed populated timing capacitor; replaces historical68pF/DNP NIS option |
| Front-end bypass ×1 each | TDKC5750X7R2A475K230KA,4.7µF10%,100V X7R,2220; KEMETC0805C224K1RACTU,220nF10%,100V X7R,0805 | IN to GND_PWR. Retain bulk plus close HF capacitor; do not return them to EF_RTN |
| Each buck input ×2 each | Same4.7µF100V and220nF100V MPNs | Per buck9.84µF nominal input bank to GND_PWR; preserve LMR local placement |
| Each buck VCC bypass ×1 | KEMETC0805C225K5RACTU,2.2µF10%,50V X7R,0805 | VCC to local power ground; replaces undersized1µF choice; bring-up confirms VCC stability |
| Each buck output ×3 | TDKC3225X7R1C156M250AB,15µF20%,16V X7R,1210 |45µF rated per rail, matching TI1MHz example; not for24V; effective C/transient behaviour confirmed during prototype tests |
| R_FLT ×0 | RC0603FR-0715KL,15kΩ | DNP historical pull-up resource; FLT unused in this simple configuration |
| Optional SOUT ×0 | SS3P6L-M3/86A | DNP only; anodes1/2GND_PWR,K24V_ELEC if later justified. A Schottky forward drop does **not** guarantee OUT≥−0.3V |
| Historical eFuse ×0 | NIS3071MT4TWG | SUPERSEDED; symbol and both footprints retained; do not place in Rev1 |

All stock/JLC Basic/Preferred classifications remain UNKNOWN unless independently
recorded. These are exact design selections, not stock reservations. The separate
[input BOM](input_protection_bom.csv), [final BOM](final_bom.csv) and
[CAD mapping](cad_library_mapping.csv) carry quantities and independent statuses.

### 10.3 Pin-by-pin manual capture checklist

Source: [TI SLVSDT4F](../../hardware/academic_rev1/libraries/sources/tps26620/tps2662.pdf),
Table6-1/Figure6-1 p4, §§9.3.2,9.3.8,9.4.1,10.2 and10.4.

| Pad | Pin / symbol ERC type | Manual connection |
|---|---|---|
|1|IN / power|VIN_CLAMP after D_REV; front-end bypass to pin6/GND_PWR |
|2|UVLO / input|768k/33.2k junction. Never tie directly to24V; pin is low-voltage |
|3|OVP / input|33.2k/30.1k junction |
|4|SHDN_N / input|Leave open for internal weak pull-up/default enable, as in simple Fig10-14. NC marker is intentional. Optional local reset test access may pull to EF_RTN; never tie to VIN or GND_PWR |
|5|RTN / power|EF_RTN; divider bottom, ILIM and dVdT returns. Separate conductor to pad11; pad11 must not be its only connection |
|6|GND / power|GND_PWR/source negative and electronics return |
|7|ILIM / analog I/O|13.3kΩ to EF_RTN; not historical62kΩ or NIS pin net |
|8|dVdT / analog I/O|10nF to EF_RTN; do not connect to system ground |
|9|FLT_N / open collector|Unused, leave open with explicit NC marker. If later monitored, TI10–100k pull-up to a suitable logic rail requires a separate powered/unpowered interface review |
|10|OUT / power|24V_ELEC to both buck local input banks; no external DO load supply feed |
|11|RTN_EP / power|Solder thermal pad to EF_RTN copper; **not GND_PWR**. Native custom-pad extension check still pending |

RTN-to-GND is handled inside the IC. A direct external short defeats reverse-input
protection and is prohibited by TI. Avoid assigning a global GND symbol to EF_RTN.
SHDN is0–6V recommended relative RTN; its weak pull-up is2.39–3.1V at the stated
0.1µA condition. Overload/thermal latch resets by cycling SHDN low/high or by power
cycling below POR after the fault is removed. UV/OV cutoff and latch behaviour are
not interchangeable; follow §§9.3.4–9.3.7. TPS26620 does not have TPS26624/25's
negative-output-polarity capability.

DO loads remain externally powered under the established assumption: external
DO+ connects to the load positive; load negative goes to the BSP drain. The external
DO supply return must connect to the established BSP source/driver return for this
non-isolated low-side stage. Do not connect it to FIELD_COM, chassis or EF_RTN.
This records the required return relationship; BSP75 terminal numbering remains
unfinished in the wider project and no DO schematic or isolation design was changed.

### 10.4 Calculations and prototype limits

See [reproducible calculations](evidence/tps26620/calculations.json). The2.81W rail
allocation and75% efficiency allowance give about0.217A in the earlier screening.
Using TPS hot RON0.8Ω,0.482mA bias and0.6V series-diode allowance gives approximately
**0.218A at18V**. These are engineering allowances, not measured/worst-case load.

TI Eq5: `R_ILIM(kΩ)=6.636/I_LIM(A)`.13.3kΩ gives0.49895A. Table7.5 explicitly
specifies0.47/0.50/0.52A at13.3kΩ and VIN−VOUT=1V; allowing resistor+1% gives a
screening lower limit≈0.465A. This is not a guaranteed0.50A limit under every fault.
The former62kΩ would give only≈0.107A by this equation and is unsuitable here.

The two local buck input banks total19.68µF nominal,21.648µF at+10% before bias
derating. No additional eFuse output bulk is selected. This exceeds TI's0.01µF
minimum and is close to Fig10-1's22µF application. Nominal capacitance is used for
an upper charging-current estimate, not as effective capacitance for buck stability.

Default24V/660µs slew would charge this upper bank at≈0.787A, above the proposed
limit. **Populate10nF.** TI Eq2 gives `t_ramp=20.5e3 × VIN × C_DVDT`:3.69/4.92/6.15ms
at18/24/30V locally. With TI1.98µA and24.6V/V, charging current≈0.105A; a screening
corner using2.33µA,25.2V/V and9nF gives≈0.141A. Adding0.218A gives≈0.359A, below
0.465A. This bounds a constant-current startup assumption; full constant-power buck
loading during the low-voltage ramp can differ. Hold MCU reset during initial
bring-up and observe24V_ELEC,3V3/5V and input current; adjust only if startup latches
or rails oscillate. TI Fig10-1 also uses13.3kΩ/10nF/22µF, but its96Ω load is not
proof for every gateway startup state. No automatic industrial startup gate remains.

The proposed UV ladder uses Eq6/7 with **Table7.5's1.20V typical**, rather than the
application prose's1.19V. Local IN-to-RTN rising thresholds are15.759V UV and33.142V OV;
falling typical values14.446V/30.932V. Independent1% resistor and1.18–1.23V comparator
corners give15.21–16.45V UV and31.97–34.63V OV before leakage. Divider current at18V
is21.65µA, above20× the combined200nA maximum leakage; allow approximately0.1–0.2V
additional threshold error. This intentionally permits18V source operation after
the series drop and30V operation below cutoff. Thresholds are not a precision
18V/30V source specification. At30V the largest divider voltage is about2.28V,
within the4V recommended pin range; resistor dissipation is well below0.1W.

Normal input30V is below33V TDS working rating,60V TPS/LMR operating ceilings and
60V D_REV reverse rating. TDS's specified42V pulse clamp also lies below those IC
ceilings; wiring overshoot is not universally bounded by that number.100V input
capacitors provide practical margin. Estimated TPS dissipation at0.217A is≈33mW
including nominal bias at30V,≈52mW with0.8Ω/maximum bias screening; verify actual
temperature and soldered thermal path. These estimates do not justify sustained
fault dissipation. The IC's latch/thermal protection and current-limited supply
support supervised tests; neither replaces correct layout or absolute ratings.

### 10.5 Sources, CAD readiness and actual unfinished work

| Source | Local file / exact evidence | Official web reference |
|---|---|---|
| TI TPS2662 | [SLVSDT4F](../../hardware/academic_rev1/libraries/sources/tps26620/tps2662.pdf), Dec2021; Table5 p4 variant,Table6-1 p4 pins,Table7.5 pp6–7,Eq2 p18,Eq5–7 p26,Fig10-1 p25,§10.4 p32,§11 pp33–34,§12 pp35–36,DRC0010J pp43–45 | [TI datasheet](https://www.ti.com/lit/ds/symlink/tps2662.pdf), [exact part](https://www.ti.com/product/TPS2662/part-details/TPS26620DRCR) |
| Yageo current resistor | [13.3k exact spec](../../hardware/academic_rev1/libraries/sources/tps26620/RC0603FR-0713K3L.pdf), p1 | [manufacturer spec](https://yageogroup.com/download/specsheet/RC0603FR-0713K3L) |
| Yageo UV/OV resistors | [768k](../../hardware/academic_rev1/libraries/sources/tps26620/RC0603FR-07768KL.pdf), [33.2k](../../hardware/academic_rev1/libraries/sources/tps26620/RC0603FR-0733K2L.pdf), [30.1k](../../hardware/academic_rev1/libraries/sources/tps26620/RC0603FR-0730K1L.pdf), each p1 | [768k](https://yageogroup.com/download/specsheet/RC0603FR-07768KL), [33.2k](https://yageogroup.com/download/specsheet/RC0603FR-0733K2L), [30.1k](https://yageogroup.com/download/specsheet/RC0603FR-0730K1L) |
| Timing capacitor | [KEMET10nF exact spec](../../hardware/academic_rev1/libraries/sources/DI_CIN_C0603C103K1RACTU.pdf),p1; mechanically matching1608 lands from [KEMET Table3 p12](../../hardware/academic_rev1/libraries/sources/academic_freeze/KEMET_family.pdf) | [KEMET/Yageo specification](https://yageogroup.com/download/specsheet/C0603C103K1RACTU) |
| Resistor land pattern | [Yageo Mounting2018 p4 Fig4/Table1](../../hardware/academic_rev1/libraries/sources/academic_freeze/YAGEO_mount.pdf);0603 lands0.9×0.8mm,0.8mm inner gap | [Yageo](https://www.yageo.com/en/Chart/Download) |
| Fuse land pattern | [manufacturer drawing](../../hardware/academic_rev1/libraries/sources/academic_freeze/fuse_manufacturer_drawing.pdf), printedp371;6.86overall,2.95gap,3.15height | [Littelfuse451/453](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1) |
|4.7µF input /15µF output | [exact4.7µF TDK sheet](../../hardware/academic_rev1/libraries/sources/academic_freeze/TDK_exact.pdf),p1land/p2bias;100V input,16V output kept separate | [4.7µF](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R2A475K230KA), [15µF](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1C156M250AB) |

Existing local suppressor, diode and historical NIS/ORing references remain in
section5. No false local link is supplied for the missing Semtech TDS3311 PDF;
its manufacturer-authored [Rev2.4 pp7–9](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf)
supports the six-pin model. The input symbol convention and graphics verification
are in [symbol_library_verification.md](symbol_library_verification.md).

Saved symbol: `TPS26620DRCR`; saved footprint candidate:`GW_DRC0010J_TI_TPS2662`.
Pins1–10 map identically; thermal terminal11 maps to RTN_EP. DRC0010J has0.5mm
pitch,0.60×0.24mm lead lands at x±1.4mm, central1.65×2.40mm thermal land and four
0.25×0.50mm tongues. The file backend refused same-number compound pad11.
The candidate retains one central pad11 and four adjoining copper regions with
explicit solder/paste openings. **Native conversion of the tongues into custom
pad11, or verified net assignment/inheritance, remains unfinished.** Rectangular
region/stencil corners also need final R0.05 drawing review. No invented pad numbers
or unverified generic package substitutes were used.

NSMD expansion0.05mm is within TI's0.07mm maximum. Lead-to-lead mask bridge≈0.16mm;
lead-to-EP gap≈0.275mm before mask. Main EP automatic paste is suppressed; two
1.50×1.06mm windows and four0.25×0.34mm tongue windows reproduce TI's approximate
80% stencil example for0.125mm stencil. Optional thermal vias are not embedded:
TI example0.2mm drill locations(0,±0.95),(±0.575,0); if used under paste, fill/plug/tent
as required by assembler. EP must be soldered to EF_RTN copper; never merge into
the ordinary GND plane. Final Gerber/stencil and fabricator checks remain later work.

**SCHEMATIC_READY: CONDITIONAL YES** for manual capture with this explicit pin plan.
**ELECTRICALLY_APPROVED:** TPS component selection approved; external settings
proposed and calculated, not electrically tested. **PCB MODEL RELEASE: NO**, pending
the native thermal-pad check. No electrical contradiction is presently identified
under the stated supervised conditions. The only new library blocker is that
custom-pad/net check; native compilation/ERC/placement was not performed and the
existing IntLib is stale. The separate BSP numbering/drive issues remain outside
this input-only closure. No industrial qualification item is used as an automatic blocker.

### 10.6 Minimal functional bring-up

1. With power off, verify polarity, no VIN/GND short, both diode anodes wired,
   EF_RTN not directly shorted to GND_PWR and no external DO current path through TPS.
2. Start at24V with laboratory limit0.5A and MCU held reset; use short leads.
   Observe VIN_CLAMP,24V_ELEC,3V3,5V and input current. Verify a monotonic few-ms
  24V_ELEC ramp, stable buck VCC/rails and no latch-off or oscillation.
3. Release reset, exercise intended electronics loads and record current/temperature.
   Verify the approximately0.22A budget before adding optional loads. If startup
   fails, inspect buck constant-power behaviour before changing R_ILIM or C_DVDT.
4. With a controlled electronic load on the protected rail, verify current limiting
   and latch-off without stressing downstream circuitry; remove fault and power-cycle.
   Do not intentionally short the TDS or rely on F1 to open at the0.5A bench setting.
5. Check18V and30V operation after nominal bring-up. Test any reversed-input case
   only unpowered/discharged first; do not hot-reverse stored output energy.

Future industrial surge/EMC qualification, source/fuse coordination and optimized
reverse protection are separate improvements, not prerequisites for this prototype.
