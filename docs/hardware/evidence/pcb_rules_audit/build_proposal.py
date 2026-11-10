"""Emit an audit proposal only. Never writes CAD, RUL, stackup or classes."""
import csv
import json
from pathlib import Path

ROOT=Path.cwd()
OUT=Path(__file__).parent
DOC=ROOT/'docs/hardware'
rows=[]
def add(name,typ,scope,parameter,minimum='TBD',preferred='N/A',maximum='N/A',units='mm',priority=1,
        scope2='N/A',classes='N/A',source='A1; F1',status='BLOCKED',decision='D2',connective='N/A',
        method='NATIVE_RULE',notes='',ready='NO'):
    rows.append(dict(rule_name=name,altium_rule_type=typ,parameter=parameter,
        intended_scope_query=scope,second_scope_query=scope2,net_or_component_class=classes,
        minimum_value=minimum,preferred_value=preferred,maximum_value=maximum,units=units,
        priority=priority,supporting_source=source,verification_status=status,required_user_decision=decision,
        connective_check=connective,implementation_method=method,implementation_notes=notes,
        scope_verification='DOCUMENTED_SYNTAX_ONLY; target PCB/classes absent; native Test Queries pending',
        ready_after_target_exists=ready))

logic="InNetClass('GW_LOGIC_DOMAIN')"
field="(InNetClass('GW_FIELD1_DOMAIN') Or InNetClass('GW_FIELD2_DOMAIN'))"
chassis="InNetClass('GW_CHASSIS')"
cable="InNetClass('GW_ETH_CABLE_DOMAIN')"
barriers=[('ISO_LOGIC_FIELD',logic,field,'GW_LOGIC_DOMAIN;GW_FIELD1_DOMAIN;GW_FIELD2_DOMAIN','D4'),
          ('ETH_BARRIER',logic,cable,'GW_LOGIC_DOMAIN;GW_ETH_CABLE_DOMAIN','D4;D5'),
          ('DI_CHANNELS',"InNetClass('GW_FIELD1_DOMAIN')","InNetClass('GW_FIELD2_DOMAIN')",'GW_FIELD1_DOMAIN;GW_FIELD2_DOMAIN','D4'),
          ('LOGIC_CHASSIS',logic,chassis,'GW_LOGIC_DOMAIN;GW_CHASSIS','D4'),
          ('FIELD_CHASSIS',field+' Or '+cable,chassis,'GW_FIELD1_DOMAIN;GW_FIELD2_DOMAIN;GW_ETH_CABLE_DOMAIN;GW_CHASSIS','D4')]
for rank,(name,a,b,cc,d) in enumerate(barriers,1):
    add('CLR_'+name,'Clearance',a,'Copper clearance',priority=rank,scope2=b,classes=cc,source='A1; M1; M3',decision=d,connective='Any Net',notes='Barrier always outranks functional/escape exceptions. DI_CHANNELS applies only if channel isolation is required. Set no numeric value until isolation matrix and standard calculation approved.')
for rank,(name,a,b,cc,d) in enumerate(barriers,1):
    add('CRP_'+name,'Creepage Distance',a,'Surface creepage',priority=rank,scope2=b,classes=cc,source='A1; M1; M3',decision=d,notes='Independent of copper clearance; validate surface path, slots and all-layer barrier. Do not substitute the ISO1212 4mm EMC recommendation.')
add('CLR_DI_EXTERNAL_PIN','Clearance',"IsPad And InPadClass('GW_DI_EXTERNAL_HV_PADS')",'EMC flashover pin spacing',minimum='4',priority=6,
    scope2="IsPad And InPadClass('GW_DI_SENSITIVE_PADS')",
    classes='GW_DI_EXTERNAL_HV_PADS;GW_DI_SENSITIVE_PADS',source='M3 section8.4.1 pp30-31',
    status='CONDITIONALLY_VALID',decision='D4;D7',connective='Any Net',
    notes='Only the external high-voltage pad of each RTHR is in the pad class. Never both RTHR pads. Target every ISO1212/RSENSE/CIN pad. Higher-priority isolation constraints still win.')
add('CLR_EXT24_LV','Clearance',"InNetClass('GW_EXT24')",'Non-isolated 24V to low-voltage copper clearance',priority=7,
    scope2="(InNetClass('GW_3V3') Or InNetClass('GW_5V') Or InNetClass('GW_LOGIC_IO'))",classes='GW_EXT24;GW_3V3;GW_5V;GW_LOGIC_IO',
    source='A1; project18-30V; F1',decision='D2;D4;D6',connective='Different Nets',notes='Functional/non-isolated voltage spacing; not a safety-isolation rule. Include maximum transients and IC pad geometry in approval.')
add('CLR_MDI_WITHIN_PAIR','Clearance',"InNetClass('GW_MDI_PHY')",'Minimum within-pair gap',priority=8,
    scope2="InNetClass('GW_MDI_PHY')",classes='GW_MDI_PHY;GW_MDI_PAIRS',source='A1; A2; M1',decision='D2;D3',
    connective='Same Differential Pair',notes='Set the approved impedance-solved minimum gap; does not relax clearance between different MDI pairs. Diff Pairs Routing gap alone is not the DRC clearance check.')
for rank,cc in enumerate(['GW_MCU','GW_PHY','GW_BUCK3V3','GW_BUCK5V'],9):
    add('CLR_PACKAGE_'+cc,'Clearance',"IsPad And InPadClass('"+cc+"_PADS')",'Package-internal pad clearance',priority=rank,
        scope2="IsPad And InPadClass('"+cc+"_PADS')",classes=cc+';'+cc+'_PADS',source='A1; M6; package drawings',decision='D2;D7',
        connective='Different Nets',notes='Optional only if global clearance conflicts with the verified land pattern. Each class must contain exactly ONE IC so this cannot relax pad clearance between unrelated packages. No track/via/region relaxation.')
add('CLR_DEFAULT','Clearance','All','All copper-pair matrix minima',priority=13,scope2='All',source='A1; F1',decision='D2;D7',connective='Different Nets',notes='Positive approved copper clearance for all relevant pairings including Via-All and Region-Pad. Review full matrix; no inherited 0mil exception.')

for name,cc,load in [('VIN24','GW_VIN24','Aggregate regulator input plus DO loads/transients: TBD'),('3V3','GW_3V3','0.7A candidate rail capacity; current/temperature confirmation required'),('5V','GW_5V','0.1A candidate rail capacity; current/temperature confirmation required'),('DO1','GW_DO1_DRAIN','0.5A/channel proposed; inrush/short circuit/duty TBD'),('DO2','GW_DO2_DRAIN','0.5A/channel proposed; inrush/short circuit/duty TBD'),('GND','GW_GND_LOGIC','Aggregate return paths and local escape bottlenecks: TBD')]:
    add('W_'+name,'Width',"InNetClass('"+cc+"')",'Track width',preferred='TBD',maximum='TBD',priority={'VIN24':4,'3V3':5,'5V':6,'DO1':2,'DO2':3,'GND':7}[name],
        classes=cc,source='A2; M2; M5; project current budget',decision='D2;D3;D6',notes=load+'. Calculate from finished copper, layer, length, allowable drop/rise, enclosure, protection clearing time; width alone does not qualify polygons/vias.')
add('W_BUCK_SW','Width',"InNetClass('GW_BUCK3_SW') Or InNetClass('GW_BUCK5_SW')",'Switch-node track width',preferred='TBD',maximum='TBD',priority=1,classes='GW_BUCK3_SW;GW_BUCK5_SW',source='M2 section12.1',decision='D2;D3;D6',notes='Short/wide connections with minimum node AREA; not a requirement to flood the node. Does not encode hot-loop inductance.')
add('W_RMII','Width',"InNetClass('GW_RMII_TX') Or InNetClass('GW_RMII_RX') Or InNetClass('GW_RMII_CLK')",'Impedance-derived track width',preferred='TBD',maximum='TBD',priority=8,classes='GW_RMII_TX;GW_RMII_RX;GW_RMII_CLK',source='A2; M1 sections9.2.5.2,9.4.1',decision='D2;D3;D5',notes='Associate an approved 50ohm single-ended impedance profile; min/max physical widths and tolerance come from approved stack/fab. RMII is not differential.')
add('W_MDI','Width',"InNetClass('GW_MDI_PHY')",'Impedance-derived member track width',preferred='TBD',maximum='TBD',priority=9,classes='GW_MDI_PHY',source='A2; M1',decision='D2;D3;D5',notes='Make physical Width limits consistent with the approved differential-pair profile and DP_MDI; do not let the general signal Width rule contradict the pair widths.')
add('W_BUS_CAN','Width',"InNetClass('GW_CAN_BUS')",'Bus track width',preferred='TBD',maximum='TBD',priority=10,classes='GW_CAN_BUS',source='M4; F1',decision='D2;D5',notes='Choose using timing, edge rate, bus topology and surge current; do not infer a PCB impedance target from a 120ohm termination resistor.')
add('W_BUS_RS485','Width',"InNetClass('GW_RS485_BUS')",'Bus track width',preferred='TBD',maximum='TBD',priority=11,classes='GW_RS485_BUS',source='M7; F1',decision='D2;D5',notes='Review A/B symmetry and protection/resistor segments; no automatic Ethernet 100ohm pair rule.')
add('W_SIGNALS_DEFAULT','Width','All','Track width',preferred='TBD',maximum='TBD',priority=12,source='A2; F1; M6',decision='D2;D7',notes='Lowest-priority catch-all including low-current signals. Verify MCU/PHY/RNX escape corridors; do not copy 10mil or 60mil by habit.')
add('NECK_FINEPITCH','Routing Neck-Down',"InNetClass('GW_ESCAPE_ROUTES')",'Neck width and maximum neck length',preferred='TBD',maximum='TBD',classes='GW_ESCAPE_ROUTES',source='A2; M6',decision='D2;D6;D7',notes='Optional. Bind only reviewed routes, set bounded neck length/current capacity. Verify actual Width/Neck-Down interaction in AD26; never relax a complete power net to solve one pad escape.')

add('VIA_DEFAULT','Routing Via Style','All','Via diameter',preferred='TBD',maximum='TBD',source='A2; F1',decision='D2;D3',notes='Only approved via types/templates. Link diameter/drill/ring and drill tolerance; do not permit independent invalid combinations.')
add('VIA_DEFAULT','Routing Via Style','All','Drill diameter',preferred='TBD',maximum='TBD',source='A2; F1',decision='D2;D3',notes='Drilled tool size versus finished hole must be explicit; approved through-hole span comes from stack manager.')
add('ANNULAR_RING','Minimum Annular Ring','All','Minimum radial ring',source='A3; F1',decision='D2',notes='Use fabrication/acceptance class requirement, worst-case pad/hole tolerances. No unverified IPC-class numeric default.')
add('HOLE_TO_HOLE','Hole To Hole Clearance','All','Edge-to-edge hole clearance',scope2='All',source='A3; F1',decision='D2;D3',notes='Review plated/nonplated holes and mechanical slots. Disable stacked microvia permission unless an approved via process actually needs it.')
add('HOLE_SIZE','Hole Size','All','Hole diameter',maximum='TBD',source='A3; F1',decision='D2;D7',notes='Approved mechanical drills and component lead-hole drawings; min/max distinct from annular ring.')
add('LAYERS_DEFAULT','Routing Layers','All','Permitted signal layers',units='layer names',priority=2,source='A2; M1; M2',decision='D3',notes='Populate only approved active signal layers. Do not copy all 32 legacy flags. Via Z spans belong to approved stack via types.')
add('LAYERS_MDI','Routing Layers',"InNetClass('GW_MDI_PHY')",'One common routing layer',units='layer name',classes='GW_MDI_PHY',source='M1 sections9.2.5.3,9.4.1.1',decision='D3;D5',notes='One selected layer with uninterrupted reference between PHY and transformer; exact layer TBD.')

add('ZP_MDI','Layer Stack Manager impedance profile','N/A - profile; referenced by MDI rules','Differential impedance target',minimum='N/A',preferred='100',maximum='TBD',units='ohm',classes='GW_MDI_PAIRS',source='M1 sections9.2.5.3,9.4.1.1',status='CONDITIONALLY_VALID',decision='D2;D3',method='STACK_PROFILE_PLAN',notes='100ohm nominal is manufacturer-sourced. Tolerance, single-ended constituent behavior and W/S solutions TBD; profile not created.')
add('ZP_RMII','Layer Stack Manager impedance profile','N/A - profile; referenced by Width rule','Single-ended impedance target',minimum='N/A',preferred='50',maximum='TBD',units='ohm',classes='GW_RMII_TX;GW_RMII_RX;GW_RMII_CLK',source='M1 sections9.2.5.2,9.4.1.1',status='CONDITIONALLY_VALID',decision='D2;D3',method='STACK_PROFILE_PLAN',notes='50ohm nominal is manufacturer-sourced, not a solved width; impedance tolerance TBD.')
add('DP_MDI','Differential Pairs Routing',"InDifferentialPairClass('GW_MDI_PAIRS')",'Width and gap',preferred='TBD',maximum='TBD',classes='GW_MDI_PAIRS',source='A2; M1',decision='D2;D3;D5',notes='Bind 100ohm profile; set min/preferred/max W and S plus max uncoupled length; no copied 15mil/10mil/500mil defaults.')
add('MATCH_MDI','Matched Lengths',"InDifferentialPairClass('GW_MDI_PAIRS')",'Within-pair skew tolerance',maximum='TBD',classes='GW_MDI_PAIRS',source='A5; M1 section9.4.1.1 p100',decision='D3;D5',notes='Within Differential Pair mode only; do not group-match TX pair to RX pair without a requirement. Derive tolerance, do not invent +/-1mm.')
for name,cc in [('TX','GW_RMII_TX'),('RX','GW_RMII_RX')]:
    add('MATCH_RMII_'+name,'Matched Lengths',"InNetClass('"+cc+"')",'Group skew tolerance',maximum='TBD',priority=2 if name=='TX' else 3,classes=cc,source='A5; M1 section9.4.1.1 p100',decision='D3;D5',notes='Group matching within this direction. Define reference-clock relation from selected RMII mode and MCU/PHY setup/hold budgets. Do not combine TX and RX into one universal group.')
add('LEN_RMII','Length',"InNetClass('GW_RMII_TX') Or InNetClass('GW_RMII_RX') Or InNetClass('GW_RMII_CLK')",'Routed length',minimum='N/A',preferred='50',maximum='TBD',units='mm',classes='GW_RMII_TX;GW_RMII_RX;GW_RMII_CLK',source='M1 section9.2.5.2 p97',status='CONDITIONALLY_VALID',decision='D5',notes='TI recommends LESS THAN 50mm and requires LESS THAN 150mm. Set native maximum below 150mm using agreed margin; 50mm is a preferred planning limit, not a second Length-rule field.')
add('VIA_COUNT_MDI','Maximum Via Count',"InNetClass('GW_MDI_PHY')",'Via count',minimum='N/A',maximum='0',units='count',classes='GW_MDI_PHY',source='M1 section9.4.1.1 p100',status='CONDITIONALLY_VALID',decision='D3;D5',notes='No-via planning policy from TI same-layer/no-crossover guidance. Any unavoidable exception requires documented SI/return review, not a blanket waiver.')
add('RETURN_HS','Return Path',"InNetClass('GW_MDI_PHY') Or InNetClass('GW_RMII_TX') Or InNetClass('GW_RMII_RX') Or InNetClass('GW_RMII_CLK')",'Reference coverage and return-via distance',maximum='TBD',classes='GW_MDI_PHY;GW_RMII_TX;GW_RMII_RX;GW_RMII_CLK',source='A5; M1 section9.4.1.2',decision='D3;D5',notes='Bind approved profiles/reference layers. Edge margin and stitching distance TBD. Do not extend a reference plane through the magnetics keepout/isolation boundary.')

add('MASK_DEFAULT','Solder Mask Expansion','All','Radial expansion',minimum='N/A',preferred='TBD',source='A4; F1; M6',decision='D2;D7',notes='Fallback only; existing pad-level manual overrides take precedence and must be inspected. Do not overwrite package-specific SMD/NSMD mask definitions.')
add('MASK_SLIVER','Minimum Solder Mask Sliver','All','Mask web minimum',scope2='All',source='A3; F1; M6',decision='D2;D7',notes='TBD after fab registration/web approval. MCU candidate has 0.100mm nominal web with +0.05mm mask; both 4mil and 6mil universal limits can conflict. Approve package exception/gang-mask strategy explicitly.')
add('PASTE_DEFAULT','Paste Mask Expansion','All','Radial/percent expansion',minimum='N/A',preferred='TBD',source='A4; F1; M6',decision='D2;D7',notes='Select absolute vs percent deliberately; do not expand thermal-pad full paste over explicit windows. Through-hole/no-paste objects require correct object settings.')
for name,cc in [('PHY_EP','GW_PHY'),('BUCK3_SW12','GW_BUCK3V3'),('BUCK5_SW12','GW_BUCK5V')]:
    add('PASTE_'+name,'Package-specific pad overrides and explicit paste windows',"InComponentClass('"+cc+"')",'Stencil apertures',minimum='N/A',preferred='TBD',classes=cc,source='M6; exact RHB/RNX stencil drawing',decision='D2;D7',method='OBJECT_OVERRIDE_REVIEW',notes='Review manual paste suppression and window primitives in Gerber/stencil output. PHY EP33 uses four .94mm square windows. RNX SW12 uses two .25x.812mm windows; A/B mask revision and corner approximation require assembly approval.')
add('SILK_MASK','Silk To Solder Mask Clearance','All','Silk to mask-opening clearance',scope2='All',source='A3; F1',decision='D2',notes='Check solder-mask openings, not only exposed copper. Retain readable refdes after DFM clipping; do not copy 0.1mil.')
add('SILK_SILK','Silk To Silk Clearance','All','Silk-to-silk clearance',scope2='All',source='A3; F1',decision='D2',notes='Set from printable line/font/registration capabilities; 2mil history is not qualification.')
add('BOARD_EDGE','Board Outline Clearance','All','Copper/hole/silk to edge and cutout matrix',source='A3; F1',decision='D2;D8',notes='Define object-edge matrix including routed slots, copper layers, overlays, connector overhang exceptions. Legacy SilkToBoardRegionClearance is not evidence of this rule.')
add('COMPONENT_CLEARANCE','Component Clearance','All','Horizontal and vertical clearance',scope2='All',source='A6; F1',decision='D2;D8',notes='Approve assembly/courtyard/rework spacing; reliable 3D body coverage required for vertical check. Do not blindly copy 10mil.')
add('HEIGHT','Height','All','Component height envelope',maximum='TBD',source='A6; mechanical envelope',decision='D8',notes='Use enclosure/connector/inductor maxima, not 1000mil default.')
add('POLYGON_DEFAULT','Polygon Connect Style','All','Thermal spoke width/gap/count',preferred='TBD',maximum='TBD',source='A7; M2; F1',decision='D2;D6;D7',notes='Default assembly connections; separately review direct high-current/thermal-pad connections and return bottlenecks. No global direct-connect policy.')
add('PLANE_CONNECT','Power Plane Connect Style','All','Plane thermal/direct settings',preferred='TBD',maximum='TBD',source='A7; M2; F1',decision='D2;D3;D6',notes='Conditional on using negative power-plane layers; positive ground polygons use Polygon Connect Style instead.')
add('PLANE_CLEARANCE','Power Plane Clearance','All','Negative-plane antipad clearance',source='A7; F1',decision='D2;D3;D4',notes='Applies only where negative planes exist; neither 20mil legacy plane clearance nor copper clearance proves creepage.')
for name,typ,param in [('SHORTS','Short-Circuit','Allow shorts'),('OPENS','Un-Routed Net','Permitted unrouted connections'),('POLYGON_FRESH','Modified Polygon / UnpouredPolygon','Require current pours'),('ANTENNAE','Net Antennae','Dangling-stub tolerance')]:
    add(name,typ,'All',param,minimum='N/A',preferred='FALSE' if name=='SHORTS' else '0',units='boolean' if name=='SHORTS' else 'count' if name in ['OPENS','POLYGON_FRESH'] else 'mm',
        source='B1 Rules6; A1; A8',status='VALID',decision='D0',ready='YES - definitions only',notes='Reusable logical gate after real netlist/board exists. Open/pour counts are release acceptance, not invented editable numeric fields. No empty-board DRC as evidence.')
add('MAGNETICS_KEEP_OUT','All-layer copper keepout','N/A - approved transformer-body/isolation polygon','No metal beneath transformer',minimum='N/A',units='geometry',classes='GW_MAGNETICS',source='M1 section9.4.1.3 p100',status='CONDITIONALLY_VALID',decision='D4;D5;D7',method='BOARD_OBJECT_LAYOUT_GATE',notes='Object geometry, not a native query-based design rule. Derive boundary from chosen transformer drawing; copper keepout on every relevant layer, no RMII path across the void.')
add('BUCK_LAYOUT_REVIEW','Placement/loop review','N/A - B3/B5 source pin-role mapping','Hot-loop/SW/FB/thermal geometry',minimum='N/A',units='engineering review',source='M2 section12.1 pp34-35',status='CONDITIONALLY_VALID',decision='D3;D6;D7',method='MANUAL_LAYOUT_GATE',notes='Place CHF at each VIN-PGND pair; local VCC/BOOT, FB away from SW, SW12-NC3, minimal hot loop/node area, broad ground/thermal paths. Track-width DRC cannot prove these.')
add('ESD_ENTRY_REVIEW','Protection placement review','N/A - approved external-interface paths','Connector/protection/return ordering',minimum='N/A',units='engineering review',source='M1; M4; M7',status='CONDITIONALLY_VALID',decision='D4;D5;D6',method='MANUAL_LAYOUT_GATE',notes='Protection at entry with short intended surge return; prevent dirty return crossing quiet FB/RBIAS/VCAP or isolation. No arbitrary placement-distance number.')
add('CLOCK_PATH_REVIEW','Clock placement/return review','N/A - selected XI/HSE/RMII clock topology','Clock topology and coupling',minimum='N/A',units='engineering review',source='M1 sections9.2.4,9.4.1; ST AN2867 via manufacturer_layout_guidelines.md',status='CONDITIONALLY_VALID',decision='D3;D5;D7',method='MANUAL_LAYOUT_GATE',notes='Separate 50MHz RMII reference, externally driven PHY XI and crystal resonator loops. Extend the 50ohm single-ended profile to an externally driven XI route when selected; do not force a crystal loop into an RMII matching group. Keep clocks away from SW/inductors and preserve return path.')
add('UNCONNECTED_PINS','Un-Connected Pin','All','Pin-intent consistency',minimum='N/A',units='check enable',source='A1; approved schematic NC intent',status='CONDITIONALLY_VALID',decision='D7',notes='Separate from Un-Routed Net. Enable/review only after intentional NC/unused MCU pins are documented; never create dummy nets to clear this check.')

for row in rows:
    row['target_configuration_status']='MISSING - academic PcbDoc absent' if row['implementation_method']=='NATIVE_RULE' else 'NOT_CREATED / NOT_REVIEWED'

with (DOC/'pcb_rules_proposal.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Proposal parameter rows:',len(rows),'unique named constraints:',len({r['rule_name'] for r in rows}))

# Complete inventory of the actual saved buck rules, with a source locator on
# every row. Classifications are for gateway reuse, not proof of native DRC.
b=json.loads((OUT/'saved_board_records.json').read_text())[0]
options=b['extracted']['Design Rule Checker Options6'][0]['fields']
batch=set(options['RULESETTOCHECK'].split(','))
online=set(options['ONLINERULESETTOCHECK'].split(','))
specific={
 'Clearance_vias':('INCORRECT','Priority1 DifferentNets IsVia-All has generic gap0; suppresses positive default via clearance. Replace with positive approved matrix; short-circuit checking is a separate gate.'),
 'Clearance':('INCORRECT','10mil=.254mm exceeds MCU candidate pad gap .200mm; pad-pad exclusion is FALSE. Not suitable as the unchanged universal gateway rule.'),
 'MinimumSolderMaskSliver':('INCORRECT','4mil=.1016mm exceeds MCU candidate nominal .100mm web; cannot reuse unchanged as a universal release rule.'),
 'SilkToSolderMaskClearance':('INCORRECT','0.1mil=.00254mm is not a supported fabrication print margin. IsPad and exposed-copper mode also do not establish a complete mask-opening check.'),
 'Schematic Supply Nets_3':('INCORRECT','3.3V net has SI supply voltage0.000; not a usable 3.3V SI model. No physical isolation approval follows from this rule.'),
 'Schematic Supply Nets_2':('INCORRECT','12V net has SI supply voltage0.000; also a buck-specific rail, not an academic gateway supply selection.'),
 'Schematic Supply Nets_1':('INCORRECT','5V net has SI supply voltage0.000; correct voltage if SI modeling is adopted, otherwise omit unused SI model.'),
 'Schematic Supply Nets':('VALID','GND nominal0 is consistent as an SI supply reference; does not enforce ground return geometry.'),
 'ShortCircuit':('VALID','All-All, ALLOWED=FALSE is a reusable logical check; preserve explicit approved net ties separately.'),
 'UnRoutedNet':('VALID','All scope is a useful completeness check on a populated, connected board; empty-board pass is meaningless.'),
 'UnpouredPolygon':('VALID','All scope is a useful stale/unpoured-copper gate; require current actual pours during later validation.'),
 'NetAntennae':('VALID','All scope and zero stub tolerance are a reusable release intent; investigate intended testpoints/NC structures rather than blanket waivers.'),
 'Width_POWER_NETS':('CONDITIONALLY_VALID','150mil preferred/max, 10mil min, scoped only to3.3V before generic Width. Current/copper/drop/thermal evidence absent; internal-layer cached max10mil must be revisited for multilayer gateway.'),
 'Width':('CONDITIONALLY_VALID','10/10/150mil min/preferred/max default; fabrication and fine-pitch escape/current capacity unqualified. MINIMP50 fields do not prove an active solved impedance profile.'),
 'DiffPairsRouting':('BLOCKED','15mil widths, 10mil gap, 500mil uncoupled limit are not tied to a qualified stack; zero differential-pair objects exist. No gateway impedance inference.'),
 'RoutingLayers':('BLOCKED','Legacy flags permit Top/Bottom and 30 Mid layers although saved copper stack has only2 layers. Rebuild allowed layers from the future approved stack.'),
 'Height':('BLOCKED','0/500/1000mil limits have no gateway enclosure/connector evidence.'),
 'SilkToBoardRegionClearance':('BLOCKED','No numeric parameter recovered and omitted from saved check lists. Not evidence of copper-to-board-outline clearance.'),
 'RoutingVias':('CONDITIONALLY_VALID','18mil land/12mil hole preferred gives3mil nominal radial ring. Allowed independent ranges18..100/12..30mil need linked valid templates, tolerances and fab approval; batch list omits this kind.'),
 'MinimumAnnularRing':('CONDITIONALLY_VALID','3mil radial ring is internally consistent with preferred18/12 via; acceptance class and drill/registration allowances remain unknown.'),
 'SolderMaskExpansion':('CONDITIONALLY_VALID','2mil radial expansion is historical only; local pad overrides can supersede this value and fine-pitch mask geometry must be checked.'),
 'PasteMaskExpansion':('CONDITIONALLY_VALID','0mil is1:1 only where rule-following pads apply. Cannot replace PHY EP/RNX windowed paste or manual overrides.'),
 'HoleToHoleClearance':('CONDITIONALLY_VALID','14mil hole gap and ALLOWSTACKEDMICROVIAS=TRUE need actual drill process/approved via types. Do not inherit stacked-via permission.'),
 'HoleSize':('CONDITIONALLY_VALID','Absolute12..200mil drilling range has no fab/lead/NPTH qualification.'),
 'ComponentClearance':('CONDITIONALLY_VALID','10mil horizontal/vertical separation requires valid bodies/courtyards and assembly/mechanical limits; saved batch list omits kind24.'),
 'RoutingCorners':('CONDITIONALLY_VALID','45-degree style with100mil setback is an autorouter-oriented setting, not a general manufacturing validation or hot-loop constraint.'),
 'LayerPairs':('CONDITIONALLY_VALID','EnforcementTRUE is reasonable only after layer/via pairs are actually defined and this check is enabled where applicable.'),
 'PolygonConnect':('CONDITIONALLY_VALID','Relief4x10mil spokes/10mil gap not qualified for exposed pads, high-current paths or assembly.'),
 'PlaneConnect':('CONDITIONALLY_VALID','Negative-plane thermal settings are inactive as a useful power-plane constraint on a simple2-signal-layer stack; future stack/process decides applicability.'),
 'PlaneClearance':('CONDITIONALLY_VALID','20mil negative-plane antipad is not universal clearance or creepage; only applicable if corresponding planes exist.')}
actual=[]
ignore={'SELECTION','LAYER','LOCKED','POLYGONOUTLINE','USERROUTED','KEEPOUT','UNIONINDEX','RULEKIND','NETSCOPE','LAYERKIND','SCOPE1EXPRESSION','SCOPE2EXPRESSION','NAME','ENABLED','PRIORITY','COMMENT','UNIQUEID','DEFINEDBYLOGICALDOCUMENT'}
for r in b['extracted']['Rules6']:
    f=r['fields']
    status,reason=specific.get(f['NAME'],('CONDITIONALLY_VALID','Saved default/routing/test configuration; evaluate actual applicability and parameters for gateway topology/assembly. Presence is not native scope or process validation.'))
    params={k:v for k,v in f.items() if k not in ignore and not k.startswith(('MIDLAYER','MID LAYER'))}
    actual.append(dict(rule_name=f['NAME'],rule_type=f['RULEKIND'],scope_1=f['SCOPE1EXPRESSION'],scope_2=f['SCOPE2EXPRESSION'],
        priority=f['PRIORITY'],enabled=f['ENABLED'],connective_check=f['NETSCOPE'],layer_kind=f['LAYERKIND'],
        parameters=json.dumps(params,separators=(',',':')),classification=status,reason=reason,
        saved_batch_kind_selected=str(r['kind_ordinal']) in batch,saved_online_kind_selected=str(r['kind_ordinal']) in online,
        source=b['path']+'::Rules6/Data@'+str(r['offset']),native_query_evaluation='NOT_PERFORMED - blocked handler',
        approval_needed='YES for any later native write; D2-D8 for physical values' if status!='VALID' else 'Future implementation authorization D0'))
with (OUT/'actual_rules.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(actual[0]));w.writeheader();w.writerows(actual)
table=['| Rule / type | Saved scope1; scope2 / priority | Key parameters | Gateway reuse assessment | Exact record offset |',
       '|---|---|---|---|---|']
for r in actual:
    table.append('| '+ ' | '.join([r['rule_name']+' / '+r['rule_type'],r['scope_1']+'; '+r['scope_2']+' / '+r['priority'],r['parameters'],r['classification']+' - '+r['reason'],'B1 Rules6/Data@'+r['source'].split('@')[-1]])+' |')
(OUT/'actual_rules_table.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
report=DOC/'pcb_design_rules_audit.md'
if report.exists():
    text=report.read_text(encoding='utf-8')
    start='<!-- ACTUAL_RULES_START -->'
    end='<!-- ACTUAL_RULES_END -->'
    prefix,rest=text.split(start,1)
    _,suffix=rest.split(end,1)
    report.write_text(prefix+start+'\n\n'+'\n'.join(table)+'\n\n'+end+suffix,encoding='utf-8')
from collections import Counter
print('Existing saved rule classifications:',dict(Counter(r['classification'] for r in actual)))
