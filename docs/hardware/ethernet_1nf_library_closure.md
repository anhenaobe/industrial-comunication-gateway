# Ethernet1nF capacitor — saved library component

2026-11-07. **C1206C102KGRACAUTO**, KEMET1nF±10%,2000VDC,X7R,1206.
Downloaded [C600002.pdf](../../hardware/academic_rev1/libraries/sources/ethernet_1nf/C600002.pdf)
is KEMET family C1076_X7R_HV_AUTO_SMD,9/10/2019. Exact catalog
[C600002](https://jlcpcb.com/partdetail/C600002) confirms the MPN; the family
ordering table,p1,decodes1206/102=1000pF/K10%/G2000V/RX7R/A/C/AUTO.
Catalog observation2026-11-07: Extended,in_stock, exact quantity unknown.
Manufacturer-authored [exact part sheet](https://www.tme.eu/Document/9f223c0b8fcfe1557b113e7adc445409/C1206C102KGRACAUTO.pdf)
also confirms the MPN/rating/body. No alternate part selected.

| Saved object / property | Value |
|---|---|
|Symbol|`C1206C102KGRACAUTO`, conventional parallel plates, two passive terminals|
|Footprint|`GW_C1206_KEMET_C1076_DENSITY_B`|
|Pin mapping|Nonpolar project convention:1→left pad1,2→right pad2|
|Body,p4|3.20±0.20×1.60±0.20mm; termination bandwidth0.50±0.25mm|
|Manufacturer reflow,p10 Table3|1206 densityB nominal:C1.50,Y1.15,X1.80mm|
|Pads|Rectangles1.15×1.80mm at(−1.50,0)/(+1.50,0); centers3.00mm,inner gap1.85mm,overall4.15mm|
|Outline|Nominal3.20×1.60mm on Mechanical1; no invented3D height|
|Mask/paste|Manual+.05mm mask,0paste expansion/1:1. Explicit prototype process choices, not manufacturer-specified stencil|
|Courtyard reference|Manufacturer V1=4.70,V2=2.30mm; final board clearance/assembly review remains separate|

**ETH_CBOB quantity2:** one capacitor from common cable-CT nodeA to CHASSIS;
the second from unused-pair nodeB to CHASSIS. Nodes remain separate, and neither
is directly bonded to logic GND. Existing75Ω/magnetics/RJ45 topology is unchanged.

CAD status is **CAD_VERIFIED** for the saved source-backed symbol/land pattern.
Electrical application status remains **PROVISIONAL**, not electrically tested.
2000VDC and AEC-Q200 do not imply safety-Y certification. Family p2 does not
recommend X7R for AC-line filtering/pulse use; do not reinterpret this model as a mains safety or
surge-qualified component. The existing academic Ethernet AC-return circuit is
retained; no industrial certification requirement is introduced.

Readback and structural validation:66symbols/37footprints,0errors/0warnings.
Component diff: one symbol and one footprint added; all previous65/36 unchanged.
Evidence/backup/source hashes are under `evidence/ethernet_1nf/`.
Native compilation/ERC/placement were not performed; existing IntLib remains stale.
No native schematic/PCB or professor-library write operation was issued.

**No remaining CAD-model blocker for these two capacitors.** Chassis treatment,
board insulation/layout and functional prototype checks remain distinct tasks.
