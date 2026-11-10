# Industrial Communication Gateway - PCB design rules audit

Date: 2026-11-06. Scope: Academic Revision, read-only engineering audit.
**READY TO APPLY: NO.** The proposal is prepared; no rules, classes, stackup,
native CAD files or RUL exports were created or changed.

## 1. Current academic project and inspection boundary

The actual project is
`hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb`. Its two members are
`libraries/Gateway_Academic.SchLib` and `libraries/Gateway_Academic.PcbLib`.
There is **no academic PcbDoc**, RUL file, saved layer-stack file or separate
Constraints Manager configuration in the inspected academic directory. The
project has no `ConstraintManagerFlow` entry; absence of that key does not prove
a particular editor mode. No board-specific net classes, pair classes or
configured rules can be verified without a board or an authored constraint dataset.

**No project-specific PCB rules can yet be verified from a native board document.**
The libraries are evidence of package geometry only, not configured board rules.
The earlier library-preparation report remains Conditional and does not establish
an approved PCB stack or fabrication process.

Electronics AI schemas were discovered for `eda__proj_list_documents` and
`eda__pcb_get_design_rules`. The explicit academic-project document query returned:
`An EDA handler is still running. No new command was queued; inspect the previous
operation before retrying.` No native retry loop, repair, unrelated active-board
query, save, compile, DRC or desktop control followed. The static tool guide was
consulted; actual native rule evaluation remained unavailable. Disk records below
are **saved-file evidence, not a live native rule-query result**.

Searches were bounded to `C:/dev/7mo/design/` and its identified
`electronic-design-dc-dc/` and `PCB_Project/` engineering directories. Native
history inspection was restricted to their PCB/project history archives. No
unrestricted drive/user-profile search was performed. No software or files were
installed/downloaded. Official Altium documentation was read online without
saving downloaded documentation. No commit or push was made.

## 2. Buck/boost reference recovered

The exact requested **`DC-DC project.PrjPcb` was not found** in that bounded search.
The located alternative is:

- B1 project: `C:/dev/7mo/design/electronic-design-dc-dc/buck_boost_design/PCB_Project_1.PrjPcb`.
- B1 board: `C:/dev/7mo/design/electronic-design-dc-dc/buck_boost_design/PCB1.PcbDoc`.
- B2 copy: same project/board names beneath `buck_boost_design/Altium/`.
- B3 archive: `buck_boost_design/Altium.zip`, member `Altium/PCB1.PcbDoc`.

Both disk boards and the archive member are byte-identical:
`4d2fbd5df1bf612b34ea90b7d501099075eecb869f4e97a35d25ea0acbbb095f`.
Their Rules6/Data stream hash is
`a713470b64e8074ef0c6dac66472eca7e0114103a8864c4abe4c3d207d64511b`.
The saved Board6 metadata records October 16, 2026. This is not a live-save timestamp.
These are related buck/boost references; their identity as the specifically named
classroom project and the professor's exact instructions remain unconfirmed.

The board contains 43 rule records, 13 nets, 21 components, 268 tracks, 66 pads,
28 vias and 17 regions. No differential pairs or From-To objects are saved. Net
names include `3.3V`, `5V`, `12V`, `GND` and `FB`. The component class `buck_boost`
contains the 21 saved components. The other class records are built-in/automatic
classes; no custom power-net or differential-pair class was recovered. In
particular, a rule named `Width_POWER_NETS` is **not evidence of a power-net class**.

Both reference projects explicitly store `ConstraintManagerFlow=0`. An opaque
30-byte ConstraintManager stream is present in the boards, but no authored
Constraint Manager rule configuration was established from it. The Rules6 records
are the operative saved rule evidence used here.

The saved V9 stack lists Top Layer / FR-4 dielectric / Bottom Layer. Top and bottom
copper are each **1.4 mil (35.56um)**; the dielectric is **12.6 mil (0.32004mm)**
with stored Er **4.8**, and solder resist is **0.4 mil** per face. These are saved
reference values, not an approved manufacturing stack or a gateway stack. Generic
unused mid-layer fields are not additional actual copper layers. No controlled
impedance profile or fabrication impedance ticket was established. The Width
records' `MINIMP/MAXIMP/FAVIMP=50` fields do not prove such a profile is active.

No RUL export, classroom-rule screenshot/document or prior DRC result report was
found in the bounded reference resources. The DRC options record permits report
generation, has an empty report filename and caps violations at 500. It is a
configuration record, not a successful DRC report. The audit also read 75 nearby
native-history archives: 68 PCB members and 7 project members. Their four distinct
clearance/width/sliver configurations are retained in the evidence; no alternate
snapshot confirms the missing classroom values below.

### Historical values versus actual evidence

| Historical claim | Saved-file result | Audit disposition |
|---|---|---|
| Global clearance 8 mil | B1 has **10 mil**, All/All, DifferentNets, priority2, Rules6/Data@19951. All 68 history PCB members retain 10mil generic clearance | 8mil unconfirmed; do not label it a professor/fab requirement |
| Mask sliver 6 mil | B1 has **4 mil**, All/All, priority1, @5469. History has 4mil or 10mil, not 6mil | 6mil unconfirmed; neither historical number is universal for gateway fine pitch |
| Power width 60 mil | No Width record with 60mil recovered | Unconfirmed. 60mil testpoint sizes are not power routing widths |
| R1-to-C12 exception 10 mil | No such rule/From-To; B1 has R1 but no C12 | Cannot inspect its type, scope or priority; no reuse |
| Region-to-Pad clearance 1.5 mil | No such exception recovered. One early history state has a pad/region matrix override, but it does not establish 1.5mil | Unconfirmed; no broad Region-Pad relaxation proposed |
| Via-to-All 0 mil | **Confirmed**, `Clearance_vias`, IsVia/All, DifferentNets, priority1, @2899; generic gap0 | Dangerous positive-clearance suppression; reject unchanged reuse |
| Approximately 150 mil high-current case | **150mil preferred/max**, 10mil min, `Width_POWER_NETS`, priority1, `InNet('3.3V')`, @1369. Earlier history had scope All | Configuration confirmed; current capacity is not. No gateway current rating inferred |

If the named classroom reference is another file, the exact path to
`DC-DC project.PrjPcb`, its PcbDoc and any RUL/screenshots/DRC report remains input D1.
The audit continues using the explicitly identified alternative, without claiming
that its discrepancies disprove the user's recollection.

## 3. Complete saved-rule inventory and assessment

Each row below originates in **B1 `Rules6/Data` at its byte offset**; B2 and B3
duplicate the same content. Full per-layer fields, object-pair matrix values,
enabled flags, online/batch selections and exact source paths are in
[`actual_rules.csv`](evidence/pcb_rules_audit/actual_rules.csv) and
[`saved_board_records.json`](evidence/pcb_rules_audit/saved_board_records.json).

Classification is **suitability for unchanged gateway reuse**. It does not claim
the original buck board violates every condition. The result is 5 VALID reusable
logical/model definitions, 7 INCORRECT for unchanged reuse, 27
CONDITIONALLY_VALID and 4 BLOCKED. Actual native query evaluation is unavailable.

<!-- ACTUAL_RULES_START -->

| Rule / type | Saved scope1; scope2 / priority | Key parameters | Gateway reuse assessment | Exact record offset |
|---|---|---|---|---|
| Schematic Supply Nets_3 / SupplyNets | InNet('3.3V'); All / 1 | {"VOLTAGE":" 0.000"} | INCORRECT - 3.3V net has SI supply voltage0.000; not a usable 3.3V SI model. No physical isolation approval follows from this rule. | B1 Rules6/Data@0 |
| Schematic Supply Nets_2 / SupplyNets | InNet('12V'); All / 2 | {"VOLTAGE":" 0.000"} | INCORRECT - 12V net has SI supply voltage0.000; also a buck-specific rail, not an academic gateway supply selection. | B1 Rules6/Data@343 |
| Schematic Supply Nets_1 / SupplyNets | InNet('5V'); All / 3 | {"VOLTAGE":" 0.000"} | INCORRECT - 5V net has SI supply voltage0.000; correct voltage if SI modeling is adopted, otherwise omit unused SI model. | B1 Rules6/Data@685 |
| Prioridad_3.3V / RoutingPriority | InNet('3.3V'); All / 1 | {"ROUTINGPRIORITY":"0"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@1026 |
| Width_POWER_NETS / Width | InNet('3.3V'); All / 1 | {"MAXLIMIT":"150mil","MINLIMIT":"10mil","PREFEREDWIDTH":"150mil","MINIMP":"50.000000","MAXIMP":"50.000000","FAVIMP":"50.000000"} | CONDITIONALLY_VALID - 150mil preferred/max, 10mil min, scoped only to3.3V before generic Width. Current/copper/drop/thermal evidence absent; internal-layer cached max10mil must be revisited for multilayer gateway. | B1 Rules6/Data@1369 |
| MinimumAnnularRing / MinimumAnnularRing | All; All / 1 | {"MINIMUMRING":"3mil"} | CONDITIONALLY_VALID - 3mil radial ring is internally consistent with preferred18/12 via; acceptance class and drill/registration allowances remain unknown. | B1 Rules6/Data@2560 |
| Clearance_vias / Clearance | ISvia; All / 1 | {"GAP":"0mil","GENERICCLEARANCE":"0mil","IGNOREPADTOPADCLEARANCEINFOOTPRINT":"FALSE","OBJECTCLEARANCES":"ClearanceObj_SMDPad-ClearanceObj_Hole:50000;ClearanceObj_THPad-ClearanceObj_Hole:110000"} | INCORRECT - Priority1 DifferentNets IsVia-All has generic gap0; suppresses positive default via clearance. Replace with positive approved matrix; short-circuit checking is a separate gate. | B1 Rules6/Data@2899 |
| Schematic Supply Nets / SupplyNets | InNet('GND'); All / 4 | {"VOLTAGE":" 0.000"} | VALID - GND nominal0 is consistent as an SI supply reference; does not enforce ground return geometry. | B1 Rules6/Data@3394 |
| UnpouredPolygon / UnpouredPolygon | All; All / 1 | {} | VALID - All scope is a useful stale/unpoured-copper gate; require current actual pours during later validation. | B1 Rules6/Data@3734 |
| NetAntennae / NetAntennae | All; All / 1 | {"NETANTENNAETOLERANCE":"0mil"} | VALID - All scope and zero stub tolerance are a reusable release intent; investigate intended testpoints/NC structures rather than blanket waivers. | B1 Rules6/Data@4050 |
| SilkToBoardRegionClearance / SilkToBoardRegionClearance | All; All / 1 | {} | BLOCKED - No numeric parameter recovered and omitted from saved check lists. Not evidence of copper-to-board-outline clearance. | B1 Rules6/Data@4384 |
| SilkToSilkClearance / SilkToSilkClearance | All; All / 1 | {"SILKTOSILKCLEARANCE":"2mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@4722 |
| SilkToSolderMaskClearance / SilkToSolderMaskClearance | IsPad; All / 1 | {"MINSILKSCREENTOMASKGAP":"0.1mil","CLEARANCETOEXPOSEDCOPPER":"TRUE"} | INCORRECT - 0.1mil=.00254mm is not a supported fabrication print margin. IsPad and exposed-copper mode also do not establish a complete mask-opening check. | B1 Rules6/Data@5071 |
| MinimumSolderMaskSliver / MinimumSolderMaskSliver | All; All / 1 | {"MINSOLDERMASKWIDTH":"4mil"} | INCORRECT - 4mil=.1016mm exceeds MCU candidate nominal .100mm web; cannot reuse unchanged as a universal release rule. | B1 Rules6/Data@5469 |
| HoleToHoleClearance / HoleToHoleClearance | All; All / 1 | {"GAP":"14mil","ALLOWSTACKEDMICROVIAS":"TRUE"} | CONDITIONALLY_VALID - 14mil hole gap and ALLOWSTACKEDMICROVIAS=TRUE need actual drill process/approved via types. Do not inherit stacked-via permission. | B1 Rules6/Data@5825 |
| DiffPairsRouting / DiffPairsRouting | All; All / 1 | {"MAXLIMIT":"10mil","MINLIMIT":"10mil","MOSTFREQGAP":"10mil","TOPLAYER_MINWIDTH":"15mil","TOPLAYER_MAXWIDTH":"15mil","TOPLAYER_PREFWIDTH":"15mil","BOTTOMLAYER_MINWIDTH":"15mil","BOTTOMLAYER_MAXWIDTH":"15mil","BOTTOMLAYER_PREFWIDTH":"15mil","MAXUNCOUPLEDLENGTH":"500mil"} | BLOCKED - 15mil widths, 10mil gap, 500mil uncoupled limit are not tied to a qualified stack; zero differential-pair objects exist. No gateway impedance inference. | B1 Rules6/Data@6186 |
| Fanout_BGA / FanoutControl | IsBGA; All / 1 | {"BGADIR":"Out","BGAVIAMODE":"Centered","FANOUTSTYLE":"Auto","FANOUTDIRECTION":"Alternating","VIAGRID":"1mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@9076 |
| Fanout_LCC / FanoutControl | IsLCC; All / 2 | {"BGADIR":"Out","BGAVIAMODE":"Centered","FANOUTSTYLE":"Auto","FANOUTDIRECTION":"Alternating","VIAGRID":"1mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@9501 |
| Fanout_SOIC / FanoutControl | IsSOIC; All / 3 | {"BGADIR":"Out","BGAVIAMODE":"Centered","FANOUTSTYLE":"Auto","FANOUTDIRECTION":"Alternating","VIAGRID":"1mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@9926 |
| Fanout_Small / FanoutControl | (CompPinCount < 5); All / 4 | {"BGADIR":"Out","BGAVIAMODE":"Centered","FANOUTSTYLE":"Auto","FANOUTDIRECTION":"OutThenIn","VIAGRID":"1mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@10354 |
| Fanout_Default / FanoutControl | All; All / 5 | {"BGADIR":"Out","BGAVIAMODE":"Centered","FANOUTSTYLE":"Auto","FANOUTDIRECTION":"Alternating","VIAGRID":"1mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@10794 |
| HoleSize / HoleSize | All; All / 1 | {"ABSOLUTEVALUES":"TRUE","MAXLIMIT":"200mil","MINLIMIT":"12mil","MAXPERCENT":"80.000","MINPERCENT":"20.000"} | CONDITIONALLY_VALID - Absolute12..200mil drilling range has no fab/lead/NPTH qualification. | B1 Rules6/Data@11225 |
| LayerPairs / LayerPairs | All; All / 1 | {"ENFORCE":"TRUE"} | CONDITIONALLY_VALID - EnforcementTRUE is reasonable only after layer/via pairs are actually defined and this check is enabled where applicable. | B1 Rules6/Data@11614 |
| Height / Height | All; All / 1 | {"MINHEIGHT":"0mil","MAXHEIGHT":"1000mil","PREFHEIGHT":"500mil"} | BLOCKED - 0/500/1000mil limits have no gateway enclosure/connector evidence. | B1 Rules6/Data@11933 |
| ComponentClearance / ComponentClearance | All; All / 1 | {"GAP":"10mil","COLLISIONCHECKMODE":"3","VERTICALGAP":"10mil","SHOWDISTANCES":"FALSE"} | CONDITIONALLY_VALID - 10mil horizontal/vertical separation requires valid bodies/courtyards and assembly/mechanical limits; saved batch list omits kind24. | B1 Rules6/Data@12282 |
| AssemblyTestpoint / AssemblyTestpoint | All; All / 1 | {"TESTPOINTUNDERCOMPONENT":"TRUE","MINSIZE":"40mil","MAXSIZE":"100mil","PREFEREDSIZE":"60mil","MINHOLESIZE":"0mil","MAXHOLESIZE":"40mil","PREFEREDHOLESIZE":"32mil","TESTPOINTGRID":"1mil","USEGRID":"TRUE","GRIDTOLERANCE":"0.01mil","ALLOWSIDETOP":"TRUE","ALLOWSIDEBOTTOM":"TRUE"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@12673 |
| AssemblyTestPointUsage / AssemblyTestPointUsage | All; All / 1 | {} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@13221 |
| FabricationTestpoint / FabricationTestpoint | All; All / 1 | {"SIDE":"3","TESTPOINTUNDERCOMPONENT":"TRUE","MINSIZE":"40mil","MAXSIZE":"100mil","PREFEREDSIZE":"60mil","MINHOLESIZE":"0mil","MAXHOLESIZE":"40mil","PREFEREDHOLESIZE":"32mil","TESTPOINTGRID":"1mil","ALLOWSIDETOP":"TRUE","ALLOWSIDEBOTTOM":"TRUE","USEGRID":"TRUE","GRIDTOLERANCE":"0.01mil"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@13551 |
| FabricationTestPointUsage / FabricationTestPointUsage | All; All / 1 | {"VALID":"0","ALLOWMULTIPLE":"FALSE"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@14112 |
| RoutingTopology / RoutingTopology | All; All / 1 | {"TOPOLOGY":"Shortest"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@14476 |
| SolderMaskExpansion / SolderMaskExpansion | All; All / 1 | {"EXPANSION":"2mil","ISTENTINGTOP":"FALSE"} | CONDITIONALLY_VALID - 2mil radial expansion is historical only; local pad overrides can supersede this value and fine-pitch mask geometry must be checked. | B1 Rules6/Data@14810 |
| PasteMaskExpansion / PasteMaskExpansion | All; All / 1 | {"EXPANSION":"0mil"} | CONDITIONALLY_VALID - 0mil is1:1 only where rule-following pads apply. Cannot replace PHY EP/RNX windowed paste or manual overrides. | B1 Rules6/Data@15168 |
| RoutingVias / RoutingVias | All; All / 1 | {"HOLEWIDTH":"12mil","WIDTH":"18mil","VIASTYLE":"Through Hole","MINHOLEWIDTH":"12mil","MINWIDTH":"18mil","MAXHOLEWIDTH":"30mil","MAXWIDTH":"100mil"} | CONDITIONALLY_VALID - 18mil land/12mil hole preferred gives3mil nominal radial ring. Allowed independent ranges18..100/12..30mil need linked valid templates, tolerances and fab approval; batch list omits this kind. | B1 Rules6/Data@15505 |
| RoutingCorners / RoutingCorners | All; All / 1 | {"CORNERSTYLE":"45-Degree","MINSETBACK":"100mil","MAXSETBACK":"100mil"} | CONDITIONALLY_VALID - 45-degree style with100mil setback is an autorouter-oriented setting, not a general manufacturing validation or hot-loop constraint. | B1 Rules6/Data@15932 |
| RoutingLayers / RoutingLayers | All; All / 1 | {"TOP LAYER_V5":"TRUE","BOTTOM LAYER_V5":"TRUE"} | BLOCKED - Legacy flags permit Top/Bottom and 30 Mid layers although saved copper stack has only2 layers. Rebuild allowed layers from the future approved stack. | B1 Rules6/Data@16304 |
| RoutingPriority / RoutingPriority | All; All / 2 | {"ROUTINGPRIORITY":"0"} | CONDITIONALLY_VALID - Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation. | B1 Rules6/Data@17276 |
| Width / Width | All; All / 2 | {"MAXLIMIT":"150mil","MINLIMIT":"10mil","PREFEREDWIDTH":"10mil","MINIMP":"50.000000","MAXIMP":"50.000000","FAVIMP":"50.000000"} | CONDITIONALLY_VALID - 10/10/150mil min/preferred/max default; fabrication and fine-pitch escape/current capacity unqualified. MINIMP50 fields do not prove an active solved impedance profile. | B1 Rules6/Data@17610 |
| PolygonConnect / PolygonConnect | All; All / 1 | {"CONNECTSTYLE":"Relief","RELIEFCONDUCTORWIDTH":"10mil","RELIEFENTRIES":"4","POLYGONRELIEFANGLE":"90 Angle","AIRGAPWIDTH":"10mil"} | CONDITIONALLY_VALID - Relief4x10mil spokes/10mil gap not qualified for exposed pads, high-current paths or assembly. | B1 Rules6/Data@18779 |
| PlaneClearance / PlaneClearance | All; All / 1 | {"CLEARANCE":"20mil"} | CONDITIONALLY_VALID - 20mil negative-plane antipad is not universal clearance or creepage; only applicable if corresponding planes exist. | B1 Rules6/Data@19202 |
| PlaneConnect / PlaneConnect | All; All / 1 | {"PLANECONNECTSTYLE":"Relief","RELIEFEXPANSION":"20mil","RELIEFENTRIES":"4","RELIEFCONDUCTORWIDTH":"10mil","RELIEFAIRGAP":"10mil"} | CONDITIONALLY_VALID - Negative-plane thermal settings are inactive as a useful power-plane constraint on a simple2-signal-layer stack; future stack/process decides applicability. | B1 Rules6/Data@19532 |
| Clearance / Clearance | All; All / 2 | {"GAP":"10mil","GENERICCLEARANCE":"10mil","IGNOREPADTOPADCLEARANCEINFOOTPRINT":"FALSE","OBJECTCLEARANCES":""} | INCORRECT - 10mil=.254mm exceeds MCU candidate pad gap .200mm; pad-pad exclusion is FALSE. Not suitable as the unchanged universal gateway rule. | B1 Rules6/Data@19951 |
| UnRoutedNet / UnRoutedNet | All; All / 1 | {} | VALID - All scope is a useful completeness check on a populated, connected board; empty-board pass is meaningless. | B1 Rules6/Data@20354 |
| ShortCircuit / ShortCircuit | All; All / 1 | {"ALLOWED":"FALSE"} | VALID - All-All, ALLOWED=FALSE is a reusable logical check; preserve explicit approved net ties separately. | B1 Rules6/Data@20662 |

<!-- ACTUAL_RULES_END -->

### Rule syntax, scope and priority findings

The saved net scopes refer to existing reference nets. `All`, `IsVia`, `IsPad`,
package fanout predicates and the component-pin-count comparison have recognizable
Altium syntax; no unsupported syntax was identified by static review. This is
**not an Altium parser/Test Queries pass**. The gateway has no objects against
which to test proposed queries. Documented class functions use quoted class names.
[Altium membership queries](https://www.altium.com/documentation/altium-designer/pcb/query-functions/membership-checks).

Within each rule type, smaller priority numbers win. The saved Via clearance1
overrides clearance2, and 3.3V Width1 overrides Width2. The precedence structure
works against safety when the narrower rule has a zero clearance. Broad defaults
exist for the reference Clearance, Width and other basic types. They do not exist
in the academic board because that board does not exist. Matched-length rules
require special care because multiple applicable matching rules can apply.
[Altium rule scoping and priorities](https://www.altium.com/documentation/altium-designer/pcb/defining-scoping-managing-design-rules).

All 43 saved rule records have ENABLED=TRUE, but the DRC configuration does not
select every kind for every mode. For example, the batch kind list omits
ComponentClearance24, DiffPairsRouting51 and RoutingVias11; the online list omits
mask-sliver53 and annular-ring19. Some rule types are routing/output instructions,
not standalone DRC checks, so absence from a list is not automatically a defect.
Nevertheless, enabled-in-editor does not establish release-check coverage.
No DRC was run. [Altium DRC](https://www.altium.com/documentation/altium-designer/pcb/drc).

## 4. Incorrect/risky reuse and corrections

| Actual problem | PCB consequence | Proposed correction and evidence | Approval needed |
|---|---|---|---|
| `Clearance_vias` gap0, IsVia/All, highest clearance priority | Positive copper spacing is waived for applicable different-net via interactions. Arbitrarily close copper can pass this clearance rule. ShortCircuit=FALSE remains a separate check and may still catch actual cross-net shorts | Remove this broad exception from any gateway rule set; use the approved positive default/object matrix, with precise documented exceptions only. B1@2899; A1 | Later write authorization D0 plus fab D2; no edit authorized now |
| Generic 10mil clearance includes footprint pad-pad checking | MCU .5mm pitch minus .3mm pad width gives .200mm gap, below .254mm. A default that looks conservative can make the actual package impossible to pass | Choose fab-compatible default and, only if needed, per-singleton-IC pad-only rules supported by the exact land pattern. Keep barriers higher priority. B1@19951; M6 | D2,D4,D7 plus D0 |
| Universal 4mil mask sliver | MCU candidate web .5-.3-2x.05=.100mm is below4mil=.1016mm; 6mil=.1524mm is still more restrictive. PHY example .5-.25-2x.05=.150mm is below6mil | Approve mask registration/web process and package-specific mask/gang-mask strategy. Do not merely disable the sliver check. B1@5469; M6; A3 | D2,D7 plus D0 |
| Silk clearance .1mil with IsPad/exposed-copper mode | Unsupported 2.54um print margin; this does not establish checking against every mask opening. Ink may be clipped over pads or refdes rendered unreadable | Use fab-approved spacing and mask-opening mode with complete intended scope. Native applicability of the current IsPad query is unverified. B1@5071; A3 | D2 plus D0 |
| Nonzero named supplies have SI voltage0 | If used for SI, 3.3V/5V/12V are modeled incorrectly. They do not define physical voltage separation | Use actual nominal voltage if SI modeling is adopted; do not import obsolete12V. GND0 may be retained. B1@0,343,685 | D5,D6 plus D0 |
| 150mil preferred width on only3.3V, min10mil | Rule name can mislead a reviewer into thinking all power paths are covered; a10mil bottleneck remains permitted. No evidence supports the current/temperature rating | Split actual power/current paths; calculate width/via/polygon capacity from copper, layer, drop, rise, ambient and fault duration. B1@1369; M2,M5 | D2,D3,D6 plus D0 |
| Generic differential rule15mil width/10mil gap/500mil uncoupled | Zero saved pair objects means it may target nothing. It cannot establish100ohm on a different stack | Define the two MDI pairs and profile from the approved stack; keep RMII out of the pair class. B1@6186; M1 | D2,D3,D5 plus D0 |
| Via range and3mil ring without fabrication process | Preferred18/12mil gives3mil nominal ring, but independent diameter/hole ranges can offer incompatible combinations; drill tolerances can reduce ring further | Use approved linked templates/tuples satisfying minimum land diameter >= maximum hole diameter +2x required radial ring, with registration/tolerance allowance; constrain via spans in stack manager. B1@2560,15505; A2,A3 | D2,D3 plus D0 |
| No Board Outline Clearance rule recovered | SilkToBoardRegionClearance does not establish copper/hole-to-edge/cutout margins | Add an approved object-edge matrix, including slots and intentional connector overhang. B1 inventory; A3 | D2,D8 plus D0 |

The last five rows are risky or incomplete configurations, not all classified
INCORRECT in the inventory: unknown thermal/fab evidence is CONDITIONALLY_VALID
or BLOCKED rather than a fabricated numeric failure. The unlocated Region-Pad
and R1-C12 exceptions are not labeled verified errors; they simply must not be
copied without their missing source/context.

## 5. Interface and layout requirements

### Ethernet MDI, RMII and clocks

M1 specifies **100ohm differential and50ohm to ground** for PHY-to-transformer MDI,
same-layer routing, parallel length-matched members, constant coupling, minimized
discontinuities and continuous return. The two PHY-side pairs must not be extended
as one electrical pair through the transformer isolation barrier. There is no
requirement here to match total TX-pair length to total RX-pair length. No numerical
intra-pair skew tolerance is documented in the inspected material: it remains TBD.

**RMII is single-ended.** M1 specifies50ohm to ground, recommends less than50mm
and gives less than150mm as the maximum. TX signals form one matching group, RX
another. Tolerance and the clock relationship require the selected RMII mode and
the H723/PHY timing budget. Do not invent a universal +/-1mm tolerance. The
50MHz reference clock, externally driven XI clock, and crystal resonator loops
have different roles; crystal traces are compact parasitic-sensitive loops, not
members of an RMII differential-pair class. Clock source/topology remains open.

The nominal impedance targets are sourced, **physical widths/gaps and impedance
tolerances are not**. Profiles need dielectric heights, materials/Er at relevant
frequency, finished copper/plating, trace geometry/etch tolerances, reference
planes, mask assumptions and fab-controlled impedance acceptance/coupons. No
value is derived from the old board's Width fields.

Differential-routing gap controls routing; electrical Clearance rules supply the
DRC spacing check. The proposal therefore has both DP_MDI and
CLR_MDI_WITHIN_PAIR, using Same Differential Pair connectivity so it cannot waive
spacing between TX and RX pairs. Return Path checking requires the correct stack
profile; it cannot justify extending metal beneath the transformer.
[Altium routing constraints](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/routing),
[return and matching constraints](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/high-speed).

### CAN-FD and RS-485

Use separate CAN and RS-485 net classes. Both carry differential bus signaling,
but that fact does not make them Ethernet MDI or impose100ohm PCB routing.
The termination/cable nominal impedance is not automatically a PCB impedance
specification. Rates, edge times, cable/stub topology, connector/protection
segments and EMC target must be fixed before numeric skew, stub or controlled
impedance rules are approved. Pairwise symmetry and an appropriate return path
remain review obligations. RMII must not be placed in either bus pair class.

M7 places protection at the bus entry, along the signal path, with low-inductance
returns and local bypass. Its recommendation for at least two VCC/GND vias at
protection/decoupling connections is layout guidance, not a universal via diameter
or current rating. M4 requires review of the CAN termination option and timing
with optional choke/capacitance; no blanket CAN/RS485 length budget is invented.

### Buck loops, DO current paths and thermal behavior

M2 requires a small input hot loop, local input bypass at VIN/PGND, short/wide
VCC and BOOT paths, SW12-to-NC3 routing, compact SW copper and feedback sensing
away from SW. It recommends an internal ground plane and adequate thermal copper;
its outer copper guidance recommends2oz and not less than1oz. This is a design
input to reconcile with the fab/stack, not proof that the gateway has2oz copper.

Width/via/connection rules can limit individual geometry. They do not prove hot-loop
area, low inductance, good capacitor placement, an acceptable SW-node area, correct
feedback sensing or thermal performance. Those are explicit layout-review gates.
Thermal-via drilling, count, tenting/filling and plane connections depend on the
selected package, current and assembly process. In particular, RNX12 is SW, **not
a ground exposed pad**.

The existing engineering budget proposes3.3V capacity0.7A,5V capacity0.1A and
two0.5A DO channels. These remain candidate design loads. Confirm startup/inrush,
short-circuit clearing, duty, simultaneous loads and enclosure temperature. DO
load current is not part of the logic rail budget. The input and return paths
must cover actual aggregate currents;60mil/150mil history proves no rating.
BSP75N's Source tab must not be treated as Drain. Its datasheet thermal test
copper/board conditions do not establish a universal required copper area.

Do not split logic ground merely to label quiet and dirty returns. Keep the
required reference continuous and arrange load/surge-current paths so they do
not share narrow bottlenecks with RBIAS/VCAP/FB. The physically isolated field
domains are a different requirement and must remain separated on every layer.

### Manufacturing and fine-pitch packages

The general manufacturing limits remain **TBD**, including trace/space by copper
weight, drill and finished-hole ranges/tolerances, annular ring, hole-hole,
copper/holes-to-edge/slot, mask registration/web, silk print limits, assembly
spacing and stencil process. No named fabricator capability file was found.
No unlicensed/unsourced IPC numeric table is substituted for fabrication evidence.

The prior library report gives these particularly sensitive candidates:

| Package | Relevant geometry / rule risk | Required check |
|---|---|---|
| STM32 LQFP100 | .5mm pitch, .3mm lands; .200mm copper gap; .100mm nominal web with+.05mm mask | Pad-pad exception only if sourced and needed; approve mask/process registration, escape widths and paste |
| DP83826I RHB32 | .5mm pitch/.25mm pad dimension across pitch; GND EP33; four .94mm square paste windows at+/- .57mm | Preserve manual full-EP paste suppression/windows; verify stencil coverage and optional filled/plugged/tented vias |
| LMR36015 RNX A/B | Asymmetric pads, SW12, two .25x.812mm paste windows; different SMD/NSMD mask treatment | Confirm delivered package revision; do not apply one global mask/paste value; rectangular-window corner approximation remains unqualified |
| ISO1212 DBQ16 | Isolation boundary, NC6/7, distinct SUB1/SUB2 | Do not ground substrate pins; reconcile table4-2 optional separate floating2x2mm islands with section8.4 NC instruction in the approved layout |

Local pad mask/paste overrides can supersede board rules. Changing a global rule
alone cannot prove the generated apertures changed. Review actual plotted mask
and stencil geometry later. [Altium mask rules](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/mask).
Mask sliver measures the remaining web, not copper clearance. Annular ring is a
radial copper allowance, not a via diameter or hole-hole gap.
[Altium manufacturing rules](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/manufacturing).

### Isolation, chassis and industrial interfaces

No safety creepage/clearance value is approved. D4 must establish functional,
basic or reinforced isolation, group versus channel isolation, maximum working
and repetitive/transient voltages, impulse/overvoltage requirements, pollution
degree, altitude, CTI/material group, coating credit and the applicable equipment
standard. Component package creepage and hipot ratings alone do not set the
complete PCB barrier.

M3's **4mm** separation concerns the **external high-voltage RTHR terminal** versus
ISO121x/RSENSE/CIN pins for EMC flashover. It is not a universal isolation distance.
The proposal uses a dedicated pad class for only those external RTHR terminals;
its scope must not include both resistor pads. Separate safety-barrier rules
retain higher priority. No numeric creepage value is inferred from4mm.

Maintain GND1/logic, FGND1, FGND2, optional individual floating SUB islands,
Ethernet cable side and chassis as explicit domains until approved connections
are documented. Group-isolation approval may permit FGND sharing; the audit does
not assume it. SUB1/SUB2 must not be joined to each other or either ground.
Do not transfer the PHY's local no-floating-metal advice blindly to the optional
ISO1212 floating substrate islands.

M1 forbids metal beneath the transformer and overlapping circuit/chassis planes;
the selected magnetics drawing must define the all-layer keepout and boundary.
Shield-to-chassis connection, PE bonding and any safety-rated coupling capacitor
need an approved connection matrix. ESD/surge protection return destinations must
be deliberate and must not bridge isolation unintentionally.

## 6. Implementation-ready proposal and proposed classes

The full parameter table is [`pcb_rules_proposal.csv`](pcb_rules_proposal.csv):
**70 parameter rows /69 named constraints or review gates**. It records type,
both queries, class, min/preferred/max, units, priority, source, status, user
decision, connective mode, implementation method and native-scope verification.
These are proposal rows, not a native import format. Profile, pad-override,
keepout and manual-review rows are explicitly distinguished from native rules.
`target_configuration_status=MISSING` means an academic native rule is not
configured; `verification_status` separately assesses the proposed definition.

### Proposed class membership contract

**None of these GW_* classes currently exists on an academic board.** Resolve
membership by approved schematic pin roles/netlist, not by blindly matching net
name prefixes. Existing CAD mapping `design_reference=UNASSIGNED` is not native
PCB component membership.

| Class / object type | Intended membership and exclusions |
|---|---|
| GW_LOGIC_DOMAIN / net class | All galvanically connected logic/system-domain nets, including GND1, rails and nonisolated power paths; review input/DO topology explicitly |
| GW_FIELD1_DOMAIN, GW_FIELD2_DOMAIN / net classes | Each channel's external input, RTHR/IN/SENSE/filter/FGND nets; include all connected protection segments. Keep distinct until group/channel decision |
| GW_ETH_CABLE_DOMAIN / net class | Transformer cable-side conductors toward RJ45, excluding PHY-side MDI and shield |
| GW_CHASSIS / net class | Approved shield/chassis/PE conductors only; do not automatically include logic GND or field returns |
| GW_EXT24, GW_VIN24 / net classes | High-voltage external/input/DO portions and the approved converter-input supply; overlapping role classes are allowed but safety rules outrank functional exceptions |
| GW_3V3, GW_5V, GW_GND_LOGIC / net classes | Respective actual rails/return. Review local low-current escapes separately; one ground class does not enforce quiet-current paths |
| GW_DO1_DRAIN, GW_DO2_DRAIN / net classes | Each load/drain conductor and protection segments; include simultaneous current in aggregate input/return analysis |
| GW_BUCK3_SW, GW_BUCK5_SW / net classes | SW12, NC3, corresponding inductor switching terminal and bootstrap-return connection; no VOUT/FB inclusion |
| GW_LOGIC_IO / net class | MCU/control digital signals; exclude analog feedback, resonator loops, MDI and external buses |
| GW_RMII_TX / net class | MCU TXD0, TXD1, TX_EN to PHY; add any mode-required member explicitly |
| GW_RMII_RX / net class | PHY RXD0, RXD1, CRS_DV to MCU; mode-dependent optional signals only after timing review |
| GW_RMII_CLK / net class | Actual50MHz reference-clock path for selected leader/follower/source topology; not HSE or a crystal loop |
| GW_MDI_PHY / net class | RD_P/RD_M and TD_P/TD_M electrical paths from PHY to transformer PHY-side terminals, including any series protection segments |
| GW_MDI_RX, GW_MDI_TX / differential pairs | RD_P/RD_M and TD_P/TD_M respectively, positive/negative mapping verified from pin roles; GW_MDI_PAIRS pair class contains these two pairs only |
| GW_CAN_BUS, GW_RS485_BUS / net classes | CANH/CANL and A/B respectively, including approved protection/filter segments. No100ohm profile or numeric matching budget inferred |
| GW_ESCAPE_ROUTES / net class | Explicit reviewed nets requiring bounded neck-down; apply only with a validated maximum neck length/current analysis, not an unrestricted narrow Width rule |
| GW_MCU, GW_PHY, GW_BUCK3V3, GW_BUCK5V / singleton component classes | Exactly one respective IC per class; source for the explicit pad-class memberships below. A shared multi-component fine-pitch class would relax unrelated pad pairs and is not proposed |
| GW_MCU_PADS, GW_PHY_PADS, GW_BUCK3V3_PADS, GW_BUCK5V_PADS / pad classes | All pads of exactly one respective IC instance (expected100,33,12,12). Native pad-only clearance queries use InPadClass directly, without assuming component-class queries include child primitives |
| GW_ISO_DI, GW_DI_SENSE_FILTER / component classes | ISO1212 and the two channels' RSENSE/CIN components, for the sourced flashover check |
| GW_DI_EXTERNAL_HV_PADS / pad class | Only the external high-voltage terminal of each selected RTHR; actual numbered pads await exact MPN selection |
| GW_DI_SENSITIVE_PADS / pad class | All ISO1212, RSENSE and CIN pads, explicitly enumerated after component binding; expected24 pads for the present16-pin/two-channel arrangement |
| GW_MAGNETICS / component class | Selected transformer for keepout/placement review; an EVM candidate is not a selected physical part |

Management MDIO/MDC and other low-current signals initially receive the approved
signal fallback, with any high-speed/clock requirements added from their actual
edge-rate/source documentation. ISO substrate islands require distinct intentional
floating ownership; do not sweep them into broad ground/plane classes.

### Rule structure and priority contract

Priorities in the CSV are within each native rule type, not global across types.
Create all applicable rules, then rank them; do not rely on creation order.
Specific barrier rules must remain ahead of package/routing exceptions. If a
conditional rule is omitted, retain the documented relative order among the rest.

| Family | Scope/priority order | Numeric disposition / status |
|---|---|---|
| Clearance | 1 logic-field;2 Ethernet barrier;3 DI channels;4 logic-chassis;5 field/cable-chassis;6 RTHR flashover;7 external24-to-LV;8 same MDI pair;9-12 singleton package pads;13 All/All | Safety/fab numbers TBD; only the narrowly scoped4mm flashover recommendation is sourced. Pair gap awaits stack |
| Creepage | Separate five barrier definitions, ranks1-5 | BLOCKED by D4; no borrowed IPC/4mm default |
| Width | 1 buckSW;2/3 DO drains;4 VIN;5/6 logic rails;7 GND;8 RMII;9 MDI;10 CAN;11 RS485;12 All | All physical widths TBD after fabrication/current/impedance inputs |
| Neck-down | Explicit reviewed route class, bounded length | TBD; validate interaction with Width before enabling |
| Vias / drill / ring | All catch-alls, approved linked tuples and stack via spans | TBD; no unqualified18/12mil template imported |
| Routing Layers | MDI-specific rank1; approved default rank2 | Stack/layers TBD; same-layer MDI intent supported |
| MDI profiles/routing | Pair class and corresponding net-width/clearance rules |100ohm nominal target supported; W/S/tolerance/uncoupled length TBD |
| RMII profile / length | Single-ended TX/RX/clock classes; separate TX/RX matched groups |50ohm nominal target; prefer<50mm, source ceiling<150mm; native max needs margin, skew TBD |
| Return Path / via count | Approved MDI/RMII profiles; MDI no-via plan | Reference geometry TBD; proposed zero MDI vias is conditional planning guidance |
| Masks/paste | Global fallback plus inspected object/package overrides | Fab values TBD; preserve explicit RHB/RNX stencil geometry |
| Assembly/edges | Silk, board-edge matrix, component clearance and height | All process/mechanical values TBD |
| Copper connections | Polygon settings; negative-plane settings only if applicable | Thermal/direct choices and numeric dimensions TBD |
| Logical release gates | Shorts prohibited; opens, stale pours and antennae reviewed | Definitions reusable after real PCB/netlist exists; intentional NC pin policy separate |
| Manual/object gates | Transformer all-layer keepout, buck/thermal review, protection entry, clock placement | Require geometry/engineering review; cannot be replaced by width/clearance DRC |

## 7. Fabrication, stack and user decisions

| ID | Exact decision/input | Rules blocked |
|---|---|---|
| D0 | Authorize a later implementation task after a real target PcbDoc/netlist is identified. This audit grants no write authorization | Every native change |
| D1 | Provide the exact location of `DC-DC project.PrjPcb` and its board/export/classroom screenshots if different from recovered PCB_Project_1 | Unconfirmed8/6/60mil, R1-C12 and1.5mil Region-Pad history |
| D2 | Select fab/assembler and supply actual DFM capabilities: finished copper/etch, trace-space by layer, drill/finished-hole/registration tolerances, ring, hole/slot/edge spacing, mask registration/minimum web, print/assembly rules, stencil thickness and via fill/tent process | All general physical numeric defaults, mask/sliver/paste, vias and assembly |
| D3 | Approve layer count/order, ground-reference continuity, dielectric materials/heights/Er, copper/plating, mask geometry, total thickness, via types/spans and fab impedance/tolerance/coupon agreement | Width-gap solutions, controlled impedance, allowed layers, return-path checking and via geometry |
| D4 | Approve domain/connection matrix: group versus channel DI isolation, insulation type/standard, working/impulse/transient voltages, pollution/altitude/material CTI/coating assumptions, Ethernet barrier and chassis/PE/coupling policy | Creepage, isolation clearances, plane gaps/keepouts and approved cross-domain connections |
| D5 | Freeze PHY MII/RMII mode/clock topology and timing budget; select magnetics/RJ45; specify CAN-FD/RS485 rates, edge/cable/stub/topology/termination and EMC environment | Pair/class membership, skew/length tolerances, clock routing, bus constraints, magnetics geometry |
| D6 | Confirm normal/peak/inrush/fault current and duty for rails and both DOs, simultaneous aggregate return current, temperature/enclosure, allowed voltage drop and protection clearing behavior | Power widths, neck bottlenecks, via count/cross-section, thermal copper and connection style |
| D7 | Close source CAD issues: BSP75N terminal numbering, RNX A/B, exact inductors/high-voltage capacitors, DI pulse-MELF MPN and pad roles, connector/reset footprints and intentional NC/substrate policy | Pin-accurate scopes, escapes, mask/paste details and isolation/high-current layout |
| D8 | Approve outline, cutouts/slots, mounting holes, enclosure/height, connector overhang/mating and assembly/rework envelope | Edge clearance, height/component spacing and mechanical zones |

A four-layer stack is a **proposal**, not a saved/approved fact. M1 recommends at
least four layers and six where possible; M2 needs an internal ground reference.
Do not copy the reference's two-layer Er4.8/12.6mil stack. Choose construction with
the manufacturer before calculating50/100ohm geometries. IPC-2152 or another
agreed current/thermal method may support D6 once its inputs and acceptance
conditions are defined; no unsourced current-to-mil conversion is used here.

## 8. Rules suitable for reuse, missing rules and next implementation

Reusable **definitions** are the broad short-circuit prohibition, unrouted-net
check, stale/unpoured polygon check and antenna review. The reference GND0 supply
definition is coherent if SI modeling is required. None is currently configured
on an academic board. Other reference values require process/topology review.

Do not reuse the zero Via-All exception, generic10mil clearance over fine-pitch
lands, universal4/6mil mask-web assumptions, .1mil silk margin, zero-volt nonzero
SI supplies, or unverified60/150mil current rules. Do not copy empty/default pair
rules, old12V membership, all-layer routing flags or missing classroom exceptions.

**MISSING in the academic native PCB context:** the target PcbDoc and real netlist;
approved stack/profiles/via types; class memberships; catch-all copper clearance,
width/via/drill/mask/manufacturing constraints; isolation/chassis barrier rules;
MDI and single-ended RMII constraints; return-path/thermal/edge/assembly checks;
and release DRC configuration. This is an absence of configured PCB context, not
a claim that a nonexistent board has passed or failed DRC.

Later implementation procedure, after the decisions above:

1. Identify the real populated target board and approved schematic/netlist. Save
   authorized recovery copies, record target identity and chosen legacy Rules versus
   Constraint Manager workflow. Do not mix competing constraint sources silently.
2. Instantiate only approved explicit classes/pairs. Check member counts and pin
   roles. Resolve every applicable TBD in the CSV; skip nonapplicable conditional
   rows with a recorded reason rather than enabling placeholder values.
3. Create approved rules with the stated scopes/connective modes; rank within
   each type and read back actual values. Inspect the complete object-pair matrix,
   not only the simple displayed clearance.
4. Run native Test Queries/applicable-rule checks on representative objects:
   ordinary track/pad/via/region; a different-net via near a pad; TX/RX MDI members
   versus different pairs; MCU pad pairs within and between components; domain
   boundaries; and the exact external RTHR pad. Unexpected zero matches or extra
   matches block acceptance. Inspect effective pad mask/paste override state.
5. Inspect actual return paths, hot loops, SW area, feedback, magnetics keepout,
   barrier geometry, load/ESD returns and thermal bottlenecks. Polygon and negative
   plane settings have different purposes; one cannot stand in for the other.
6. Configure relevant online/batch checks explicitly and perform DRC only on the
   actual design, with adequate violation reporting. Review generated mask/paste,
   drill and board-edge output. Retain live readback, scope results, DRC messages,
   exceptions and fab/assembly approval. Only then consider an authorized RUL export.

The first logical definitions are ready to specify, and the table is ready for
decision review. **No complete numeric manufacturing rule set is ready to apply.**

## 9. Sources, evidence and verification

Official Altium documentation consulted on2026-11-06 is current documentation
for the installed AD26-era workflow; its pages are not a frozen versioned26
reference. Native script applicability on this installation remains untested.

| ID | Supporting source |
|---|---|
| A1 | [Electrical rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/electrical): copper clearance, connective scope and logical checks |
| A2 | [Routing rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/routing): Width, neck-down, vias/layers and differential routing |
| A3 | [Manufacturing rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/manufacturing): ring, holes, sliver, silk and board outline |
| A4 | [Mask rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/mask): expansion and local overrides |
| A5 | [High-speed rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/high-speed): length/matching/return path |
| A6 | [Placement rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/placement): placement/clearance/height |
| A7 | [Plane rule types](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/plane): negative-plane versus polygon connection constraints |
| A8 | [DRC](https://www.altium.com/documentation/altium-designer/pcb/drc), [scoping/priorities](https://www.altium.com/documentation/altium-designer/pcb/defining-scoping-managing-design-rules), [rule categories](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types) |
| A9 | [Membership queries](https://www.altium.com/documentation/altium-designer/pcb/query-functions/membership-checks): InNetClass, InComponentClass, InPadClass, InDifferentialPairClass |
| B1-B3 | Exact saved buck project/board/archive paths and Rules6 offsets in sections2-3 and evidence JSON; classroom authorship not independently established |
| M1 | Local DP83826I SNLS647I PDF, sections9.2.5.2-.3 p97,9.4.1 pp99-101; RHB0032M drawing/stencil pages112-113 |
| M2 | Local LMR36015 SNVSB49D PDF, section12.1 pp34-35, RNX0012A/B drawing and stencil pages44-49 |
| M3 | Local ISO1212 SLLSEY7G PDF, table4-2 p4, safety table/notes p7 and section8.4 pp30-32 |
| M4 | Local Microchip DS20005991B and `libraries/sources/ATA656x_EVKit_50002649A.pdf`, sections3.5-3.8 and appendixA |
| M5 | Local Diodes BSP75N DS33016 Rev7-2, pin roles p1 and thermal/board-test conditions pp3-8; not a universal current-width formula |
| M6 | [Library preparation report](altium_library_preparation_report.md), saved official-reader snapshots and exact local manufacturer package drawings; candidates remain unqualified |
| M7 | Local THVD1400/THVD1420 SLLSF78B PDF, section10.1 p20 |
| F1 | **Missing input**, not a fabricated source: selected fabricator/assembler capability and process acceptance document |

The exact local manufacturer-text evidence is
[M1 DP83826I](evidence/library_preparation/dp83826i.pdf.txt),
[M2 LMR36015](evidence/library_preparation/lmr36015.pdf.txt),
[M3 ISO1212](evidence/library_preparation/iso1212.pdf.txt),
[M4 ATA6561](evidence/library_preparation/20005991B.pdf.txt),
[M5 BSP75N](evidence/library_preparation/BSP75N.pdf.txt) and
[M7 THVD1420](evidence/library_preparation/thvd1400.pdf.txt).
The M4 evaluation-kit source is
[`ATA656x_EVKit_50002649A.pdf`](../../hardware/academic_rev1/libraries/sources/ATA656x_EVKit_50002649A.pdf).
These existing extracts are used with the section/page locators above; they were
not newly downloaded for this audit.

The existing [readiness assessment](cad_readiness_assessment.md),
[passive selection](passive_component_selection.md),
[manufacturer layout guidelines](manufacturer_layout_guidelines.md) and
[library preparation report](altium_library_preparation_report.md) were inspected.
The newer library report supersedes older claims that no academic PrjPcb exists;
none of those files establishes a PCB rule set.

Read-only extraction uses the existing local `olefile` dependency, parses complete
length-delimited records and checks rule/class/net/component counts against saved
stream headers. The DRC-options header is metadata rather than an object count.
The parser does not resolve native query applicability, decode all CAD geometry
or certify fabrication. Evidence is beneath `evidence/pcb_rules_audit/`:

- `saved_board_records.json`: exact saved rules, classes, nets, Board6 stack metadata and DRC options.
- `actual_rules.csv`: all43 rules with source offsets, assessment and check-selection flags.
- `reference_archive_inventory.json`, `reference_history_records.json`: archive member/hash identity and bounded history evidence.
- `native_query_result.json`: actual blocked Electronics AI call result.
- `native_files_hashes_before.json`, `verification.json`: native-file preservation and deliverable checks.

Validation: proposal schema/unique parameter keys, explicit units/TBDs, per-type
priorities, complete43-rule coverage, source locators, and native hash preservation
were checked. `git diff --check` and `git status --short` were run. No PCB, project,
library, history archive or native rule file was modified. No DRC readiness claim
is based on an empty board.

CURRENT RULES: no academic PcbDoc; no project-specific native rules verified.

BUCK REFERENCE: PCB_Project_1 recovered,43 saved rules; exact DC-DC project filename missing.

VALID RULES: five reusable saved definitions; no qualified academic physical rule set.

INCORRECT RULES: seven definitions unsuitable for unchanged gateway reuse; critical Via-All0mil.

MISSING RULES: target PCB/netlist, approved manufacturing/stack, domain/interface rules and check configuration.

BLOCKING DECISIONS: D2-D8; D1 for the specifically named classroom reference.

READY TO APPLY: NO.

NEXT ACTION: approve fabrication/stack, isolation, topology, load and package inputs; then authorize a separate scoped native implementation using the CSV.
