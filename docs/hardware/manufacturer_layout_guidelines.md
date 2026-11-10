# Manufacturer layout requirements - selected Academic capture configuration

<!-- AUTONOMOUS_CLOSURE_20261108_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- AUTONOMOUS_CLOSURE_20261108_END -->

Date: 2026-11-07. These are implementation requirements for the configuration in
[schematic_readiness_gate.md](schematic_readiness_gate.md), not a completed PCB
review. The existing academic `PCB1.PcbDoc` is preserved; no routing or stackup
was changed or qualified. The November6 rules audit remains historical evidence.

| Block | Selected source / exact locator | Placement, copper and return requirement | Remaining gate |
|---|---|---|---|
| MCU LDO | DS13313 fig5/table14; AN5419 table2/fig3 | Local100nF per five VDD pins; two2.2uF VCAP capacitors, ESR<100mohm, no external VCAP load. Keep VDDA/VREF decoupling returns short to VSSA/GND. No SMPS network on this H723 LQFP100 | Exact capacitor application ESR/bias, package escape, DFM |
| Active oscillators | Kyocera TNY1T-H1-DEX01-11 pp4,6/table2/fig4; ST table31; TI section7.6 | Two independent25MHz CMOS oscillators; local10nF at each VCC4/GND2; pin1 HIGH. Route output3 once to PH0 or XI9, with no branch/crystal loads. PH1 and PHY XO unconnected. Load includes pads/route/probe and receiver | <=15pF load budget; PHY phase-noise offsets; no shared-fanout approval |
| MCU reset/debug | AN5419 figures15/19, section6 |100nF NRST, accessible BOOT0/10k, SWD with adjacent returns and VTref. Own6pin header mapping is documented, not ARM-keyed standard. Keep reset away from SW | Exact header/switch drawings and commissioned option bytes |
| PHY supply/bias | SNLS647I table5-1/fig9-6 | Separate local VDDA3V3/VDDIO decoupling banks; RBIAS6.49k near10; CEXT2nF at2 (do not copy EVM100nF). Ground EP33 as specified; respect explicit paste windows | Supply ramp0.5-50ms and oscillator startup; package mask/paste/thermal vias |
| RMII/clock | SNLS647I sections7.6,9.2.5.2,9.4.1 | Single-ended50ohm intent; <50mm recommended/<150mm source ceiling; no arbitrary matching tolerance. Match TX and RX groups separately. PHY19->MCU PA1, uninterrupted return; no RMII differential pairs | Stack/geometry/timing budget. Reset LOW>=25us; SMI wait>=2ms after reset and>=50ms after power-up |
| MDI/transformer | SNLS647I sections9.2.5.3,9.4.1; EVM fig6-2/sheet3; Pulse HX1188FNL revB sheets2-3 |100ohm differential/50ohm single-ended intent, constant coupling, same layer, no stubs/unreviewed vias. Separate TX/RX pairs, exact winding map from readiness gate. **No metal beneath transformer on any layer.** No overlapping logic/chassis planes | Selected fab stack, reference-plane transition, exact all-layer keepout and insulation policy |
| Ethernet termination/shield | EVM sheet3 T2/J17/R43..46/C45..59; Cinch CT710001 B0 | Two parallel100nF per PHY CT2/7 to logic GND; four75ohm and two1nF/2kV cable-side AC returns to chassis. Shield S1/S2 to chassis. No automatic R51/C61 bridge to logic GND; selected DNP | HV capacitor safety class and land pattern; chassis/PE policy; connector copper annuli/holes/board edge |
| Ethernet ESD | EVM U13 and TI SLVSBO7O table4-2 | PHY-side TPD4E05U06 only, on MDI path with GND3/8 to logic GND. Preserve isolation; no cable-side return stitched into logic plane. No HDMI-derived topology | Actual low-inductance return/parasitics; board ESD test, not just diode rating |
| Buck hot loops | SNVSB49D sections12.1-12.2 figures12-1/12-2 |220nF at each opposite VIN/PGND pair; main CIN close; local VCC-GND and BOOT-SW; short/wide hot loops with minimal area. SW12->NC3. FB/RFB/CFF near FB/AGND, sense output away from SW/inductor. Internal ground reference and broad return paths | CIN effective count, COUT bias/ESR/transients, actual thermal model and RNX A/B mask/paste selection |
| XAL4030/XAL4040 | Coilcraft document806-1/806-4 | Exact .093in pad-center spacing, .038x.134in lands; connect high-dv/dt to marked end for lower EMI. Use correct3.1/4.1mm maximum height; do not substitute generic low-current inductors | Hot/fault inductance, core losses and nearby coupling.25C typical Isat is not hot guaranteed Isat |
| Power-input prototype | TI section11; TDK-Lambda figure5; Vishay88987; Littelfuse SMBJ table | One fuse then series reverse diode then TVS/local decoupling. Short clamp return to intended input GND; do not force surge/load current through PHY RBIAS/MCU VCAP/FB returns. No unreviewed input LC | Fuse/TVS/bulk/source/cable coordination.53.3V candidate clamp does not prove60V buck margin including overshoot or36V BSP fault protection |
| RS-485 | SLLSF78B figure8-5/table8-1, section10.1; Bourns SM712 pp1-3 | Selected basic3V3/115200baud circuit,100nF close. DE low/nRE high at reset. Protection positions at connector, short intentional return, only if qualified. Reference has TWO10ohm pulse resistors, one per line. End termination only at bus end, no default bias | SM712 clamp exceeds THVD1420 absmax without proven residual-current control; no transferred1kV rating. Cable/stub/termination/pulse/EMC review |
| CAN-FD | Microchip DS20005991B figure1-6/table2.0; EVKit DS50002649A sections3.5-3.8 |100nF each at VCC5V/VIO3V3; short CANH/L route to connector. Internal STBY/TXD pull-ups provide standby/recessive reset state. Conventional120ohm termination via end-only jumper; split option/choke/caps/TVS DNP |1M/2M cable-loop timing and component-level protection limitations; actual bus-end location |
| DO drive/switch | Diodes DS33016 pp1,3-8; TI SCES516N table5.5 | Source tab is NOT Drain. Preserve separate source/drain copper and keep1A aggregate load return out of quiet signal returns. DIR=VCCA, defined pull-downs on inputs/outputs, no OE assumed | Numbered Diodes terminal map; guaranteed>=4.5V loaded drive; rail-ramp OFF state; ambient/copper/inductive energy and repetition |
| DI Type3 | SLLSEY7G figures8-2/8-9/8-17/8-18, table4-2/8-1, section8.4; Firstohm MM p78 |562ohm SENSE-IN,1kohm MM204 series external input,10nF SENSE-FIELD_COM. Local logical100nF and EN=VCC1. Group FIELD_COM isolated from logic GND. External HV RTHR pad>=4mm from ISO/RSENSE/CIN pins for EMC flashover. Separate floating SUB1/SUB2 ownership; never ground/join |4mm is not universal creepage. MM204 normal operation does not establish surge. Optional FGND/PE capacitance must follow TI total<=500pF condition if later selected |

## Board-wide constraints

Preserve continuous logic return planes without arbitrary quiet/dirty ground
splits. Arrange current paths instead. The isolated field and Ethernet/chassis
boundaries remain real all-layer separations; identify approved coupling parts
before connecting domains. Do not use an unspecified safety distance.

Choose fab/assembler, stack, copper, drill/mask/paste limits, mechanical outline
and insulation standard/environment before configuring the proposed PCB rules.
The PHY recommends at least4 layers (6 if possible), and the buck guidance uses
an internal ground reference. No saved reference stack or trace width is adopted
as a gateway approval. See [the rules audit](pcb_design_rules_audit.md) and its CSV.

Native footprints retain explicit package geometry and stated limitations:
RNX SW12 is not GND; RHB EP33 uses explicit paste windows; DQA rectangular corners
remain a candidate approximation; RJ45 signal/shield copper annuli are engineering
choices around the official hole map. New footprints lack qualified courtyards
and3D height bodies; do not use them as collision/assembly proof. Global mask or
paste rules do not automatically override manual pad settings.

The MM204 reflow footprint is manufacturer-backed (two1.3x1.6mm lands,1.6mm inner
spacing); the surge claim is a separate electrical gate. Exact Bourns SM712 lands
are0.85mm squares with1.9mm bus-pad spacing and2mm row spacing. Source PDFs,
rendered drawings and readbacks are under `evidence/electrical_closure/` and
`hardware/academic_rev1/libraries/sources/electrical_closure/`.

No placement distance, impedance geometry, junction temperature, safety barrier
or industrial compliance result was verified on a routed gateway board here.

## TPS26620DRCR and academic input amendment

Use TI SLVSDT4F §§11–12 and DRC0010J4218878/B, not NIS3071 land/paste geometry.
Keep IN/OUT loops short, local input and buck bypass returns to GND_PWR; setting
resistors/dVdT and exposed pad11 return to EF_RTN. Never merge EF_RTN with GND_PWR.
Solder the EP and separately connect pin5; optional0.2mm thermal-via implementation
requires assembler review. Saved manufacturer-dimension candidate includes explicit
paste windows; its four EP copper tongues still need native custom-pad11/net
inheritance verification. No footprint placement/routing or native rules were changed.
See [input reference section10](input_protection_reference.md) for source links,
mask/paste details and prototype capacitor choices. No industrial compliance claim.


## BSP75NTA correction ? current physical closure (7 November 2026)

The earlier request for a manufacturer-numbered Type DN drawing is withdrawn. Diodes DS33016 pp1,8 identify physical functions and lands sufficiently. `BSP75NTA` now links to verified `GW_BSP75N_SOT223_DN_DIODES`: tab-up top view, lower IN/D/S, upper S_TAB=Source. Functional Altium pin/pad IDs are intentional; no generic numeric mapping is substituted. Physical CAD is **CAD_VERIFIED**; drive electrical approval remains pending separately. Current source libraries:66 symbols/38 footprints; structural validation0 errors/0 warnings,65 unrelated symbols and37 old footprints unchanged. Native compilation/ERC not run.

Use the [current physical closure and evidence](bsp75n_physical_closure.md) and [construction guide ?10](schematic_construction_guide.md#10-sn74lvc2t45-and-two-bsp75n-digital-outputs). Earlier blocked-numbering statements below/above are historical, superseded by this correction. Retain BSP as a functional smart-switch block, not a bare MOSFET.

## Current closure layout additions —2026-11-08

- TPS EP isEF_RTN,notGND. New compound candidate requires one-to-many symbol11mapping to11/11A/B/C/D orone nativecustompad;do not transfer it with1:1mapping. Thermalvias must stay onEF_RTN anduse agreedassembler treatment.
- Altium roundedrectangle percentage is ofhalf the shorter side. TI R0.05 corresponds toDQA50% for0.20mm leadlands,25% for0.40mm GNDlands;TPSlead42% givesR0.0504,central6% givesR0.0495,fingers40% givesR0.05. [Official Altium pad API definition](https://www.altium.com/documentation/altium-dxp-developer/pcb-api-design-objects-interfaces-reference). Initial incorrect percentage interpretation was corrected before finalreadback.
- RNX A/B share electricalpositions;pin12/NC3areSW. Keep bothVIN/PGND/HF loops compact,FBquiet andseparate switch nodes. Match the saved A/B copper/mask/stencil to the delivered package.
- ISO SUB12/13 eachget an independentfloating2x2mm copperisland;never join toFGND/GND/eachother. DI fieldresistors arefieldsideonly;fix actualR21/R22beforelayout.
- BSP lower-leftIN,lower-centreD,lower-rightS,upperSOURCE TAB. Route loadreturn separately fromquietlogic into the same systemGND;do not route it throughEF_RTN/FIELD_COM. Manufacturerthermal area relates toDRAINcopper;source-tab packages fromothermanufacturers are not substitutes.
- NPN/PMOSdriver transistors carry only5Vlogicinput current. Keep4.7kG-S and2.49kIN-S pull-down connections local;externalDOpositive must remain outside24V_ELEC. See guide10for the chosen circuit.
- Samsung MLCC_2401p159:CL10 +/-0.10mm row selects a=.68,b=.76,c=.85mm;CL21 +/-0.20mm row a=.88,b=.96,c=1.40mm. These are documented midpoints inside manufacturer ranges,not universal0603/0805 defaults. Mask+.05/paste1:1 are prototypechoices. Exact body tolerances come from the retained SamsungproductHTML.
- The connector andtransformerbody outlines/3D/courtyards are not universally implemented;manualplacement must use manufacturerbody envelopes andboardedge/access drawings,not onlypadhulls. Wurth/SameSkynewTH paste disabled. Inspect remainingTH/stencil outputs beforefabrication.
- CurrentJLCPCB1oz greenmask capability covers the chosenTHannuli and~0.10mm maskbridges. Publicgeneric minimumSMTland is0.25x0.25mm;obtain specificDFM acceptance forTI DQA0.20mm/TPS0.24mm leadlands beforemanufacturing. Do not enlarge verifiedlands blindly. [Official capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). This does not define orapprove a PCBstack.
