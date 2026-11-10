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
