## 10. SN74LVC2T45 and two BSP75N digital outputs

### A. Selected configuration and readiness

Two **BSP75NTA** protected low-side switches, intended0.5A/channel, externally
powered loads. **Physical mapping and Diodes footprint are resolved.** Capture
the explicit connections below now; the existing SN74LVC2T45DCTR remains a
**drive candidate pending loaded-voltage/reset-OFF acceptance**. No automatic
electrical approval or component substitution is made.

The prior requirement for a manufacturer-numbered Type DN drawing was too strict:
Diodes identifies terminal **positions directly by function**. Its top-view pinout
plus its own suggested lands are sufficient; no other manufacturer's part was used.
The library deliberately retains `IN`, `D`, `S`, `S_TAB` pin/pad designators.
These are the actual Altium identifiers, not missing numbers. Do not relabel them
using a generic SOT223's numeric assignment. Existing symbol pin positions are unchanged.

### B. Exact manufacturer evidence and orientation

[Local Diodes BSP75N datasheet](../../hardware/academic_rev1/libraries/sources/bsp75n_closure/BSP75N.pdf),
**DS33016 Rev7-2 January2024**,p1 **Top View Pin Out** and Source-tab note;
p8 **SOT223(Type DN) Suggested Pad Layout**,p3 absolute/thermal limits and
p4 electrical table. [Official Diodes PDF](https://www.diodes.com/assets/Datasheets/BSP75N.pdf).
The p1 sketch has tab left and small leads right (top S,middle D,bottom IN).
Rotate that top view90° clockwise to match the p8 footprint: **tab above; lower
row left-to-right IN,D,S**. This is rotation, never a bottom-view mirror.

Native footprint `GW_BSP75N_SOT223_DN_DIODES` uses that tab-up top view:

| Altium pad | Physical position / coordinates(mm) | Manufacturer copper size(mm) |
|---|---|---|
|IN|Lower left,(-2.30,-3.20)|1.20×1.60|
|D|Lower center,(0,-3.20)|1.20×1.60|
|S|Lower right,(+2.30,-3.20)|1.20×1.60|
|S_TAB|Upper tab,(0,+3.20)|3.30×1.60|

Source p8 dimensions: C2.30,C1=6.40,X1.20,X1=3.30,Y1.60,Y1=1.60,Y2=8.00mm.
Manual mask+.05mm and1:1paste are explicit prototype process choices. Nominal
body outline6.50×3.50mm is on Mechanical1; no assumed3D height/courtyard approval.
Source tab and drain must remain electrically isolated. Diodes p1 recommends
significant **drain** copper for thermal performance; do not attach a drain heatsink
plane to the source tab by relying on a conventional SOT223 MOSFET footprint.

Translator: existing `DS/sn74lvc2t45.pdf`, **SCES516N June2024**,Table4-1 p2,
Table5.5 p6,§§7.4/8.3 for direction/startup; [official TI PDF](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf).
It has no OE pin. Keep DCTR/DCT8 and the current footprint `GW_DCT0008A_TI`.

### C. Components to place

__DO_COMPONENTS__

Population for the retained candidate: translator×1,BSP75NTA×2,100nF supply
bypass×2,and10kΩ pull-down×4 (one on each A input and each B/IN drive).
Use both translator channels; no unused channel or OE is invented. No series
input resistor or added external suppression is selected. The load connectors
remain2-way functional LOAD+/LOAD−; physical connector numbering still needs its
own drawing. Intended0.5A is a prototype load target, not an unconditional rating.

### D. Complete manual wiring checklist

| Translator DCT pin | Selected net / connection |
|---|---|
|1 VCCA|3V3;100nF to pin4/GND locally|
|2 A1|MCU PE2,pad1,net DO1;10kΩ pull-down to GND|
|3 A2|MCU PE3,pad2,net DO2;separate10kΩ pull-down to GND|
|4 GND|Logic GND/common GND_PWR return|
|5 DIR|VCCA/3V3 HIGH, A-to-B direction; not5V|
|6 B2|DO2_DRIVE → second BSP IN;10kΩ to return|
|7 B1|DO1_DRIVE → first BSP IN;10kΩ to return|
|8 VCCB|5V electronics rail; separate100nF to pin4/GND|

| BSP device / symbol pin = pad | Exact physical terminal | Required net |
|---|---|---|
|DO1 BSP / IN|Lower-left lead|DO1_DRIVE,from translator7(B1);B-side10kΩ to source/common return|
|DO1 BSP / D|Lower-center lead|DO1_LOAD−,first load negative / connector LOAD−|
|DO1 BSP / S|Lower-right lead|DO_EXT_RETURN,common with GND_PWR for this nonisolated control|
|DO1 BSP / S_TAB|Large upper tab|Same DO_EXT_RETURN; explicitly wire both S and S_TAB|
|DO2 BSP / IN|Lower-left lead|DO2_DRIVE,from translator6(B2);B-side10kΩ to source/common return|
|DO2 BSP / D|Lower-center lead|DO2_LOAD−,second load negative / connector LOAD−|
|DO2 BSP / S|Lower-right lead|DO_EXT_RETURN/common GND_PWR|
|DO2 BSP / S_TAB|Large upper tab|Same DO_EXT_RETURN; explicitly wire both S and S_TAB|

Each external load positive → **DO_EXT+**, not5V/3V3/24V_ELEC. External supply
negative → DO_EXT_RETURN,joined to the BSP source/translator common return for
the existing **nonisolated DO** architecture. Define this common connection
explicitly; do not leave the input-drive reference floating. Route high load
returns away from MCU analog/VCAP,PHY bias and buck FB returns. Do not merge
DO_EXT_RETURN into isolated DI FIELD_COM,chassis or EF_RTN. Main TPS electronics
eFuse does not carry the external DO load current. DO1/DO2 drain nets stay separate.

### E. Drive-voltage assessment and recommended prototype resolution

**Physical CAD blocker closed; drive guarantee remains unresolved.** Diodes p4
specifies input current max1.2mA **at VIN=5V** and VPROT minimum4.5V for
**overtemperature protection**. The lower input turn-on threshold does not prove
that protection is active. Prior wording calling4.5V the ordinary logic threshold
or a guarantee of every protection function was inaccurate.

Including10kΩ±1% pull-down, a screening load is1.2mA+5.174V/9.9kΩ≈**1.723mA**
per high output. The5V design's tolerance estimate is4.862–5.174V before ripple;
only0.362V at the low corner is available for output/return droop to retain4.5V.
The implied source-resistance budget≈210Ω is an **engineering target**, not a
guaranteed SN74 output resistance. The1.2mA limit is specified at5V,not a universal
bound at every rail voltage. Keep these calculations separate from manufacturer limits.

TI Table5.5 guarantees VOH≥3.8V at VCCO=4.5V,IOH=−32mA; near-rail VOH applies
at−100µA and listed supply conditions. Neither row establishes≥4.5V at our
asymmetric3.3V/5V supplies and approximately1.7mA load. Capacity to source current
is not the same as a guaranteed sufficiently high voltage. Typical curves cannot
be promoted into a guaranteed limit. **The existing candidate is plausible for
the supervised prototype, but the drive is not automatically approved.**

Recommended resolution within the approved academic scope: **retain the candidate
for capture and perform the following loaded-drive acceptance before powering
external loads**. No new component is required merely to draw these connections.

1. Leave DO_EXT+ unpowered; connect both actual BSP inputs and all four pull-downs.
   Power the3V3/5V electronics. Measure IN-to-**local S**,not remote bench ground.
2. Exercise each channel and both HIGH together. Verify both VIN≥4.5V,including
   output/source ripple; target near5V,not just at the threshold. Check the low
   end of the actual5V rail range. A separate bench supply must not fight a connected
   buck output; isolate the test fixture rail first if sweeping it externally.
3. Check reset,HiZ MCU,3V3-before5V,5V-before3V3 and power-down. Outputs must remain
   OFF as intended; record measured LOW voltage and actual load-OFF behaviour before
   connecting loads. No extra pull-up to5V is allowed: it could force ON while the
   translator is HiZ.
4. If acceptance passes, record **tested prototype operating conditions**,not a
   manufacturer family-wide guarantee. If it fails, keep DO loads disconnected and
   revise the drive stage separately. A guaranteed-design path requires a5V buffer/
   driver whose loaded VOH covers≥4.5V at≥1.8mA across the selected rail range,plus
   default-OFF startup behaviour; or explicit TI confirmation of the existing part
   at those conditions. No unverified replacement MPN is silently adopted here.

Remaining practical checks are reset-OFF/loaded drive,exact load-connector terminals,
and intended thermal/inductive operation. Resistive supervised0.5A bring-up comes
before inductive tests. The manufacturer's36V short-circuit rating at VIN=5V is
separate from its60V VDS absolute limit.550mJ is a single-pulse condition,not a
repetitive energy allowance. No industrial qualification task is reopened.

### F. Construction verification

- [ ] Select BSP75NTA with linked Diodes Type DN footprint,not an ordinary MOSFET symbol.
- [ ] Tab-up TOP VIEW: lower leads IN,D,S; large tab S_TAB=Source,never Drain.
- [ ] Both S and S_TAB of both devices connect to common external return/logic reference.
- [ ] Translator7/B1→DO1 IN;6/B2→DO2 IN;MCU PE2/PE3 unchanged.
- [ ] Two local100nF bypasses and four10kΩ pull-downs are present; DIR=3V3.
- [ ] External load positives use DO_EXT+,negative leads reach their separate drains.
- [ ] Physical CAD is ready; loaded-drive acceptance is visibly pending before energizing loads.

### G. Required net labels

DO1,DO2,DO1_DRIVE,DO2_DRIVE,DO1_LOAD−,DO2_LOAD−,DO_EXT+,DO_EXT_RETURN,
3V3,5V,GND_PWR/GND. FIELD_COM,CHASSIS and EF_RTN are separate domains.

