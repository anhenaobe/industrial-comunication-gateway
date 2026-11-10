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
| MCU output |U4 PE2/pad1=`DO1_CMD`|U4 PE3/pad2=`DO2_CMD`|
| Existing10k pull-down |DO1_CMD toGND|DO2_CMD toGND|
|4.7k base resistor |DO1_CMD toQ_DO1_N.B|DO2_CMD toQ_DO2_N.B|
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

Required nets: DO1_CMD,DO2_CMD,DO1_GATE,DO2_GATE,DO1_DRIVE,DO2_DRIVE,
DO1_DRAIN,DO2_DRAIN,DO_EXT_PLUS,5V,GND. FIELD_COM,EF_RTN andCHASSIS
are excluded from the DO return network.
