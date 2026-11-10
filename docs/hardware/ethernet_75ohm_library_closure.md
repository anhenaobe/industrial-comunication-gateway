# Ethernet75Ω model closure — Academic Rev.1

2026-11-07. **Retained original Vishay CRCW080575R0FKEA,75Ω ±1%,0805,0.125W.**
ETH_RBOB remains one specification with **four populated instances**, not four
new specification IDs. No native schematic/PCB or professor library was changed.

| Candidate / source | Identity and disposition |
|---|---|
|Uniroyal0603WAF750JT5E / C4275|Confirmed by supplied MPN and current JLC catalog. [Local family sheet](../../hardware/academic_rev1/libraries/sources/ethernet_75ohm/C4275.pdf), Feb12,2019 V3,p2 decodes0603/WA=0.1W/F=1%/750J=750×0.1=75Ω/T5E=tape5000lead-free. Body1.60±0.10×0.80±0.10×0.45±0.10mm,p4. **Not adopted**: smaller package and20% lower nominal power than original; Basic status alone does not justify changing the EVM-based selection.|
|VishayCRCW080575R0FKEA / C844859|**Selected.** The filename alone does not establish identity: supplied PDF is generic D/CRCW e3,document20035,Rev18-Jun-2018. Exact JLC catalog identifies this code as FKEA. Ordering p3 decodes0805/75R0/F1%/K100ppm/K/EA packaging; p1 gives0.125W at70°C,150V element limit. Existing TI EVM BOM selects this exact MPN.|
|VishayCRCW080575R0FKEAC / C1511836|Exact catalog identity verified, but final **C means commodity**, not just reel/cut-tape suffix. Manufacturer [document28773](https://www.vishay.com/docs/28773/crcwce3.pdf),p2, identifies the special code. Same nominal75Ω/1%/0.125W and2012 case; body tolerance/height and recommended lands differ from document20035. **Not adopted or silently assigned the original footprint**. A procurement substitution needs its own land/process review.|

Catalog observations: [C844859](https://jlcpcb.com/partdetail/C844859) and
[C1511836](https://www.lcsc.com/product-detail/C1511836.html) identify different MPNs;
both JLC Extended. [C4275](https://jlcpcb.com/partdetail/C4275) is Basic. Observed
2026-11-07 via Electronics AI public JSON-LD; stock status says in_stock but exact
assembly quantities are unavailable. This is not an inventory reservation.
Evidence is saved under `evidence/ethernet_75ohm/supply_*.json`.

For this non-PoE, transformer-coupled cable termination, retain the original
reference-design0805. Both candidates offer75Ω/1% electrically, but no cost/stock
need currently warrants changing package/power/pulse behaviour. No resistor is
placed directly across24V.150V is an element limit, **not** permissible continuous
voltage across75Ω: sqrt(0.125×75)=3.06Vrms at the rated-power condition before
derating; for0.1W it is2.74Vrms. Actual waveform/temperature limits still apply;
no industrial surge claim or PoE compatibility is added.

## Saved model and exact geometry

Source: [supplied C844859.pdf](../../hardware/academic_rev1/libraries/sources/ethernet_75ohm/C844859.pdf),
Vishay20035 pp1/3/9; [official manufacturer URL](https://www.vishay.com/docs/20035/dcrcwe3.pdf).
The provided archive was used for geometry; current distributor power-rating
changes do not authorize silently increasing our0.125W design rating.

| Property | Saved value / evidence |
|---|---|
|Symbol|`CRCW080575R0FKEA`, conventional IEC resistor, visible lead graphics; both physical pins retained|
|Footprint|`GW_CRCW0805_VISHAY_20035_REFLOW`|
|Mapping|Nonpolar project convention pin1→left pad1,pin2→right pad2; manufacturer does not assign polarity|
|Body|L2.0+0.20/−0.10,W1.25±0.15,H0.45±0.05mm; T1=0.3+0.20/−0.10,T2=0.3±0.20mm|
|REFLOW table,p9|G=1.00mm inner gap;Y=0.95mm pad length along resistor axis;X=1.45mm transverse pad width;Z=2.90mm overall|
|Explicit pads|Rectangles0.95×1.45mm at(−0.975,0) and(+0.975,0);1.95mm center spacing; no drills|
|Body outline|Nominal2.0×1.25mm on Mechanical1; not a claimed qualified courtyard/3D model|
|Mask|Manual+0.05mm each edge: openings1.05×1.55mm, gap0.90mm. Prototype process choice; manufacturer does not prescribe mask expansion|
|Paste|Manual0expansion,1:1copper openings0.95×1.45mm. Prototype process choice, no unsupported manufacturer stencil claim|

These are manufacturer **REFLOW**, not WAVE, lands. Structural validity and source
geometry do not replace final fabrication-output/assembly review.

## Four connections — unchanged topology

| Logical instance, within ETH_RBOB quantity4 | Pin1 → pin2 |
|---|---|
|Magnetics CT branch1|HX1188FNL pin15 → nodeA|
|Magnetics CT branch2|HX1188FNL pin10 → nodeA|
|Unused cable pair1|RJ45 contacts4+5 joined → nodeB|
|Unused cable pair2|RJ45 contacts7+8 joined → nodeB|

NodeA → its own1nF high-voltage capacitor → CHASSIS; nodeB → its separate1nF
high-voltage capacitor → CHASSIS. Never short nodesA/B together or directly to
logic GND. Instance descriptions are functional identifiers, not assigned native
reference designators. All four use the same exact resistor symbol/footprint.

## Validation and remaining dependencies

New saved symbol/footprint read back through Electronics AI file backend.
Libraries contain65symbols/36footprints; structural validation0errors/0warnings.
Backup and per-component diff evidence are in `evidence/ethernet_75ohm/`.
Native compilation/ERC/placement were **not run**; no new Altium automation session
was started. Existing IntLib is stale. The preceding64/35 TPS report remains
historical evidence, not current inventory.

Concurrent disk changes were observed in academic `Ethernet.SchDoc`, `MCU.SchDoc`,
`Power.SchDoc` and `Industrial_Gateway_Academic.PrjPcb` between the initial and final
hash checks. This task issued no schematic/project/PCB write operation; those
changes were preserved and not reverted. Therefore byte-preservation of those
four files cannot be claimed. Professor and other original libraries retain their
hashes. Native compilation remains unperformed by this task.

**No remaining blocker for the four75Ω resistor models.** The two high-voltage
Ethernet capacitor models/chassis treatment remain separate open tasks. TPS EP,
BSP numbering/drive and other previously recorded issues are not closed here.
