# Academic Gateway Rev.1 — engineering closure,2026-11-08

> Actualización nativa 2026-11-10: ver [cierre y evidencia actual](closure_verification_rev1.md) y [BOM real por designador](assembly_bom_rev1.csv). Los pendientes de captura/modelos descritos debajo son históricos y quedan sustituidos por ese cierre; la validación del diálogo ECO sigue pendiente.


**Continue manual schematic completion;do not start full routing or manufacturing yet.**
The connection specification and source libraries were substantially completed.
The actual native circuit still contains the localized errors below. Altium became
unavailable after one backed-up wire repair;remaining native edits could not be
verified and were not attempted through a binary-file workaround.

Primary handoff: [construction guide,including exact completion sequence](schematic_construction_guide.md#15-exact-native-completion-sequence-and-connector-implementation).
Current [BOM](final_bom.csv),[passive BOM](passive_bom.csv),[CAD mapping](cad_library_mapping.csv).
Evidence and reproducible scripts: [autonomous_closure](evidence/autonomous_closure/WORKING_PLAN.md).
Academic assumptions remain nominal24V,current-limited regulated laboratory
supply,18–30V objective,supervised bring-up,no industrial certification gate.

## Actual baseline and preserved user work

Active project `hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb`;
Flat connectivity,`AllowPortNetNames=0`,`ConstraintManagerFlow=0`.
Native Electronics AI read all **108components/453pin memberships**,independently
paired with saved native component/parameter/model records. The five included
sheets are Power40components,MCU19,Ethernet34,Field_IO15,TopLevel0.
PCB1.PcbDoc exists and was not modified. No sheet count was assumed.

Compared with the earlier106-component audit,the user had already corrected
separate buckSW nets,VIN distribution,100k feedback uppers,TDS3311 identity,
RJ45TX- andMCU SWCLK;added J3 andTPD4E05U06;and linked the BSP footprints.
Those changes were preserved. New C7 TORCH15u100V is physically present but
does not have the exact-X7S/land/DCbias evidence of the selected TDK bank.
No new circuit is claimed merely because its source symbol exists.

The older [initial audit](schematic_audit_rev1.md) remains historical evidence;
its106/437 counts and already-repaired findings are not the current baseline.
[Native BOM](evidence/autonomous_closure/native_bom_before.json),
[all pin memberships](evidence/autonomous_closure/native_nets_before.json),
[instance metadata](evidence/autonomous_closure/metadata_before.json),
[backup hashes/paths](evidence/autonomous_closure/baseline_backups.json).

## Electrical decisions and source-backed implementation

| Issue | Closure implemented in resources | Evidence / practical limit |
|---|---|---|
| BSP physical mapping | Verified IN,D,S,S_TAB positions retained;SOURCE TAB is notDRAIN;existing verified foot unchanged | Diodes DS33016 Rev7-2 pp1/8;functional IDs intentionally retained |
| Translator loadedVOH | SN74LVC2T45DCTR superseded for this DO path,qty0;selected2xMMBT3904-7-F+2xDMP2035U-7 driver | TI SCES516N loadedVOH lacks4.5V assurance;Diodes saturation/RDS data;guide10 exact circuit |
| Reset/partial-power OFF | Existing10k GPIOdown;4.7k base;100ohm gate;4.7k gate-source;2.49k BSPinputdown | Low/HiZ GPIO ->NPNoff ->PMOSoff ->BSPoff. Firmware initializesLOW;verify sequencing before loads |
| Loaded BSP protection | Calculated minimumBSPinput4.812V with50mV ripple allowance;PMOS|VGS|4.514V | Engineering saturation/leakage/low-current assumptions explicitly identified;not a manufacturer-qualified full-temperature guarantee |
| DO load supply | External24Vpositive separate;BSP SOURCE/TAB share explicit non-isolated external/system return | Main electronicsTPS excludesDO current;not an isolatedDO architecture;initial0.5A resistive load tests |
| Input protection | Approved fuse/SS3P6L/TDS3311/TPS26620 chain retained;RTN separate | 13.3k ->0.498947A;UVLO15.759V,OVP33.142V;10nF ramp;TPS26620 latch-off |
| RNX compatibility | Both saved A/B maps reviewed;same functional positions,variant-specific mask/copper retained | TI SNVSB49D pp44–49;pin12SW,NC3externallytoSW;stencil/lot/process must match |
| MCU package |100pads/CCW numbering/pitch0.5/lands0.3x1.2/outer16.7mm independently checked | ST DS13313Rev5 Fig65 printed218/PDF219;native peripheral assignments preserved |
| ESD footprint | Rounded DQA lands and reducedGND paste windows implemented | TI SLVSBO7O pp29–30;GND3/8 paste0.565x0.36;R0.05 usingAltiumhalf-side50%/25% |
| Connectors | Same SkyTB002-500-02BE/03BE and Wurth613002/61300611121 selected/authored | Manufacturer hole patterns;project contact polarity explicit,not inferred from generic helpers |
| Bus-end terminations | CRCW1206120RFKEA120ohm1%0.25W and2pin headers prepared | Vishay20035p9 reflow;open-default;populate onlyatphysicalbusend |
| Reset/BOOT accessories | ActualJ3 custom pinout adopted;BOOT2pinheader selected | NoMCU reassignment. SW1 isBOOT recovery. Unselected onboardNRSTbuttonDNP;J3.4/.5 provides reset access |
| Common passives |20 existing symbol links repaired to verified Yageo/KEMET/TDK/Coilcraft/Samsung patterns | ExactMPNs,values,electrical pin types,origins/pin tips andcompact graphics preserved |

Independent5Vdriver calculation uses existing rail screen4.86249..5.17365V,
1%resistors,VCEsat0.20V engineering allowance,GPIOhigh>=2.4V androom-temperature
leakage conditions. Maximum VGS is well inside PMOS±10V;PMOS never sees24V.
Each BSP0.5A screening loss is0.16875W using0.675ohm. Thermal copper/load
and repetitive inductive energy still need the real prototype check;single-pulse
energy is not a repetitive-load rating. Full calculations/invariants are saved in
[verification.json](evidence/autonomous_closure/verification.json).

Existing2.81W electronics allocation and~0.217A input estimate are retained.
The new driver pair is budgeted12mA inside the existing5V0.1A allowance;
external load current remains excluded. Do not describe IC1.5A ratings as board
continuous-current capacity. Buck effective-C/startup assumptions remain those
in guide2/3;selected2xTDK4.7u100V per buck is retained instead of silently
approving nominally equivalent TORCH15u100V. No formal industrial gate is restored.

## Native findings still requiring action

| ID | Consequence / severity | Actual finding | Exact required action |
|---|---|---|---|
| N01 | CRITICAL if powered / pending verification | U1UVLO2/OVP3 andbothR3ends were oneOVP net | Saved localized wire/label repair;recompile and prove distinct ladder junctions before power |
| N02 | CRITICAL rating violation | C16=16V onprotected24V | SelectedTDK100V replacement;complete both2-capCIN banks |
| N03 | CRITICAL isolation/electrical error | R21/R22 field resistors terminate on ISOlogicOUT/MCU pins | Disconnect only R21.2/R22.2 fromOUTs;connect to respective field inputs;preserveOUT-to-MCU nets |
| N04 | MAJOR incomplete output | All U10/U11 BSP pins are unwired;translator remains | Implement guide10 discrete drivers,allBSP source/tab/drain nets andexternal supply/load connectors |
| N05 | MAJOR application mismatch | U2.3/U3.3 open;CVCC old1uF;selectedCIN quantities incomplete | NC3-to-ownSW12;2.2u50V CVCC;selected2x4.7u100V per converter |
| N06 | MAJOR boundary error | C46/C52 cable caps returnlogicGND;RJ45shieldsfloat | IndependentA/B caps toCHASSIS;J2.S1/S2 toCHASSIS;noDCGND bond |
| N07 | MAJOR missing bypass | C30.1floating;MCU native bank missing one1uF/one100nF | C30.1to3.3V;add the two selected bypass parts;guide15C |
| N08 | MAJOR incomplete interfaces | RS/CAN/DI/DO external terminals missing | Exact selected terminal/contact tables in guide15;no new bus architecture |
| N09 | MAJOR project-reference error |4TopLevel sheet symbols have placeholderFileName/Designator | Map toactual4children/uniqueIDs;retainFlat scope;checkcompiledcross-sheetnets |
| N10 | CAD/layout pending | D? unannotated;far-sideESD NC pads unassigned | Unique designator;selectedsame-netflow-throughpadpairs beforePCB. ExistingMDI signal nets are alreadycontinuous;NCfloatingalone is not an electricalopen |
| N11 | CRITICAL PGvoltage rating;CFF is separatepopulation issue | R6/R9 pullPG toward24V;TI PG operatingmax18V/absolute22V | Remove/DNP bothPGpullups beforepower;PG8intentionalopen. TI SNVSB49D p5. CFF separatelyDNP;no blanketvariant/libraryupdate |
| N12 | PCB CAD pending | Some nativeinstance model links are missing/stale | Local exact-MPN link migration/readback;source-library availability is notproof ofinstanceECO |

All native actions are written by designator,pin,net and source in guide15.
The current prepared BOM is a target,not a claim of equality with108placed parts.
[Selected/native reconciliation](evidence/autonomous_closure/bom_native_reconciliation.csv)
keeps aggregatequantity/MPN differences visible;source-current/thermal claims are
not inferred from that mechanical inventory.
[Per-designator native/model migration table](evidence/autonomous_closure/native_model_reconciliation.csv)
lists all108instances;model-name agreement is not electrical approval.

## Saved changes,backups and validation

Backups were made before edits in
`hardware/academic_rev1/backups/autonomous_20261108T195741Z/`;
the library backend also emitted timestamped `.bak` files for each write.
Recover exact locations from the JSON logs. Professor source libraries were
never write targets;their hashes and PCB1 hash match protected evidence.

The sole intentional native circuit edit was onPower:
wirePZUXORAP `(10100,7500)->(10000,7500)->(9700,7500)`mil was replaced by
`(10000,7500)->(9800,7500)` andUVLO label at `(10000,7700)`mil.
Altium also added the junction at9800,7500. Saved raw readback confirms these
records. Post-save net export still returned the old cachedOVP memberships;
forced recompile and project compile could not establish a native session.
Therefore this is **SAVED_GEOMETRY_ONLY;POST_COMPILE_NET_CHECK_PENDING**,
not an electrically verified correction.

Native `proj_save` also rewrote the other open SchDocs and project reference
cache. This is disclosed rather than claiming only one file changed:all108
component definitions,locations andidentities remained exact. Other-sheet
records changed only generated parameter/pin IDs orcontainer bytes;
TopLevel parsed records stayed exact. Project library-reference cache reordered;
projectscope/settings must retain their baseline values. [Saved-record diff](evidence/autonomous_closure/native_saved_diff.json).
No SchDoc was reconstructed or edited through a binary writer.

Final source inventory **76symbols/48footprints**;official backend readback
andvalidation performed after saving. SchLib:0errors/0warnings. PcbLib:0errors,
4overlap warnings confined to the unboundTPScompoundEP candidate.
All67original symbol pin arrays are exact;34unrelated symbols and36unrelated
footprints remain exact in parsed readback.33existing symbol updates affect
model/provenance/verification metadata only;existingDQA/TPS radii/paste were corrected;
9new symbols and10new footprints were added. R/C graphics and80mil pins remain.

CurrentBOM:140rows,99mandatoryrows/124units/50unique mandatoryMPNs.
98mandatoryrows have sourceCAD_VERIFIED;oneTPSrow remainsCAD_CANDIDATE. Every mandatory
MPN now has a saved model association;candidate is not fabrication-ready.
Active mapping rows remain specification-only withblankquantity;finalBOM carries
real placement quantities. Historical8-active/26-passive coverage figures are not
the current expanded design counts. DNP/conditional entries are separate.

Native bridge finalstate: `bridge_answering=false`,noactive document,
no native session;the tool explicitly refused a second script launch.
No Altium restart,installation orspeculative script repair was attempted.
**No post-edit native compilation,ERC,IntLib compilation,PCB DRC orlab test
was completed.** Existing IntLib is stale. Offline checks below do not replace them.

Reproduce from repository root with existingPython:

```powershell
C:/dev/tools/python/python.exe docs/hardware/evidence/autonomous_closure/prepare_closure_records.py
C:/dev/tools/python/python.exe docs/hardware/evidence/build_passive_deliverables.py
C:/dev/tools/python/python.exe docs/hardware/evidence/construction_sync/sync_guide.py
C:/dev/tools/python/python.exe docs/hardware/evidence/autonomous_closure/verify_closure.py
```

`prepare_models.py` produces source JSON only;it does not auto-write orduplicate
existing components. Model changes require the official library backend andfresh
readback. DQA authored correction is saved independently in its JSON.
Offline verification checks pin arrays,graphics/MPNs,model sets,source dimensions,
mandatoryquantities,19nativebaseline cross-sheetpairs/24MCUreservations,
return-domain separation,savedrecord scope and protectedhashes. BOM/guide
regeneration was checked for stable outputs;see finalverification record.

## Narrow CAD and fabrication dependencies

1. **TPS EP:** original fourunassigned copperregions remain unresolved;new
   `GW_DRC0010J_TI_TPS2662_EP11` uses central11+11A/B/C/D subpads. Native
   one-to-many symbol11 mapping toallfiveEF_RTN pads,or one genuine custompad11,
   must be validated before placement. Do not bind the alternate with default1:1map.
   OfficialAltium documents net inheritance for footprint primitives touchingpads:
   first test the existingfootprint in an isolatedECO;ifallfourregions inherit
   EF_RTN,no footprint replacement is needed. This is a native-transferverification
   hold,not absentmanufacturerdimensions or proof ofa defective footprint.
   [Altium routing-primitive behavior](https://www.altium.com/documentation/altium-designer/components-libraries/creating-pcb-footprint).
2. **Sourcegeometry closure:** PHY,ISO1212,transceivers,Kyocera,magnetics/RJ45,
   inductors andFirstohm lands were independently compared with the manufacturer
   drawings during thismission. Their geometry holds are closed;nativeinstance
   transfer,bodyenvelopes/courtyards andassembly-output checks remain separate.
   Samsung's officialMLCC_2401p159 resolved both remaining genericMLCCpatterns:
   CL10bodytolerance+/-0.10mm uses a=.68,b=.76,c=.85mm;CL21+/-0.20mm uses
   a=.88,b=.96,c=1.40mm. These are explicit midpoints in manufacturer ranges,
   not generic defaults. No missing-manufacturer-pinout claim is restored forBSP.
3. **Actual fabrication process:** newTH annuli are0.35/0.45mm;MCU/DQA mask
   bridges are approximately0.10mm. These are compatible with the published
   1oz/green-mask annular/bridge envelope,but a fabrication stack has not been
   created orapproved. The supplier's generic minimumSMTland0.25x0.25mm is
   larger thanTI DQA0.20mm andTPS0.24mm lead widths:obtain specificDFM acceptance
   before manufacturing;do not blindly enlarge officiallands. DQA uses theTI0.10mm
   stencil example;RNX/TPS examples need their selectedstencil treatment.
   [Official JLCPCB capability table](https://jlcpcb.com/capabilities/pcb-capabilities),
   Drilling/Traces/Soldermask sections,checked2026-11-08.
4. Controlledimpedance/layerstack androuting remain unimplemented. Set them
   from the actual chosen stack before Ethernet routing;RMII is single-ended.
   No arbitrary impedancewidth or industrialisolation spacing was invented.

## Per-subsystem readiness and exact handoff

“Connection spec ready” permits manualcapture under the documented prototype
assumptions;“native ready” requires the actual circuit fixes andfreshERC.

| Subsystem | Connection spec | CAD library | Native schematic ready | Placement | Routing | Manufacturing |
|---|---|---|---|---|---|---|
| Input |YES|CONDITIONAL,TPS EP map|NO,N01|NO|NO|NO|
|3.3V buck|YES|Sourcegeometry verified|NO,N05/N11|CONDITIONAL after repairs|NO|NO|
|5V buck|YES|same|NO,N02/N05/N11|CONDITIONAL after repairs|NO|NO|
| MCU |YES|Sourcegeometry verified|NO,N07/BOOT localmodel|CONDITIONAL|NO|NO|
|Ethernet PHY/clocks|YES,prototype clock-performance assumption|Sourcegeometry verified|CONDITIONAL,ESD/modeltransfer|CONDITIONAL|NO|NO|
|Magnetics/RJ45|YES|Sourcegeometry verified|NO,N06|CONDITIONAL|NO|NO|
|RS485|YES|Sourcegeometry verified|NO,N08|CONDITIONAL|NO|NO|
|CAN-FD|YES|same|NO,N08|CONDITIONAL|NO|NO|
|Two DI|YES|Sourcegeometry verified|NO,N03/N08|NO untilisolationrepair|NO|NO|
|Two DO|YES,newdriver selected|BSP/newdriver/connector geometry verified|NO,N04|NO untilmigration|NO|NO|

Next inAltium:reestablish one native session;back up currentwork;performguide15
power/DI corrections first;complete bypass/terminals/DO;fix childreferences andDNP;
compile/readnetmemberships/ERC;then resolveTPS EPmapping andcandidate assembly
checks,compileLibPkg andperform a reviewedPCB ECO. Keeploads unpowered until
rails/defaultOFF checks pass. No PCB,professor library,Rev.A orfirmware redesign
was performed;no remote push.
