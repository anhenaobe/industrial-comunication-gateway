"""Author only evidence-bound project-local models; no schematic or PCB writes."""
import json,copy,hashlib
from pathlib import Path
O=Path(__file__).parent;L=Path('hardware/academic_rev1/libraries')
symbols={x['name']:x for x in json.loads((O/'symbols_before.json').read_text())['symbols']}
footprints={x['name']:x for x in json.loads((O/'footprints_before.json').read_text())['footprints']}
new_symbols=[];new_footprints=[];assets=[]
def pin(id,name,x,y,orientation,kind='passive',length=20):return dict(designator=id,name=name,x=x,y=y,length=length,orientation=orientation,electrical_type=kind,show_name=True,show_designator=False)
def line(a,b,c,d):return dict(x1=a,y1=b,x2=c,y2=d,line_width=1,color=128)
def pad(id,x,y,w,h,drill=0):return dict(designator=id,x=x,y=y,width=w,height=h,shape='round' if drill else 'rectangle',layer='MultiLayer' if drill else 'Top Layer',hole_size=drill,is_plated=bool(drill),solder_mask_expansion=.1 if drill else .05,solder_mask_expansion_mode='manual',paste_mask_expansion=-10 if drill else 0,paste_mask_expansion_mode='manual')
def outline(x1,y1,x2,y2,layer='Mechanical 1'):return [dict(x1=a,y1=b,x2=c,y2=d,width=.05,layer=layer) for a,b,c,d in [(x1,y1,x2,y1),(x2,y1,x2,y2),(x2,y2,x1,y2),(x1,y2,x1,y1)]]
def parameters(mfr,mpn,source,desc,extra=None):
 values={'Manufacturer':mfr,'Manufacturer Part Number':mpn,'Value':desc,'Source':source,'CAD Status':'CAD_VERIFIED_GEOMETRY;NATIVE_PLACEMENT_PENDING','Electrical Status':'DERIVED_PENDING_REVIEW',**(extra or {})}
 return [dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in values.items()]
def asset(mpn,symbol,fp,source,kind='AUXILIARY',ids=None,status='CAD_VERIFIED'):
 assets.append(dict(asset_id='CLOSURE_'+mpn,item_kind=kind,component_ids=ids or [],mpn=mpn,symbol=symbol,footprint=fp,source=source,cad_status=status,symbol_status='CAD_VERIFIED',footprint_status=status,package_requirement=fp,limitations='Manufacturer geometry/functional terminal positions verified; native placement/transfer not performed. Process expansions are stated prototype choices.'))

# Both Diodes datasheets explicitly identify top-view terminal functions rather
# than numeric identifiers: retain those functions as the actual Altium pin/pad IDs.
for mpn,npn,roles,src in [('MMBT3904-7-F',True,['B','E','C'],'Diodes DS30036 Rev27-2 March2025 p1 top view/order, p3 electrical, p6 suggested lands'),('DMP2035U-7',False,['G','S','D'],'Diodes DS31830 Rev11-2 June2025 p1 top view/order,p2 electrical,p6 suggested lands')]:
 fp='GW_'+('MMBT3904_BEC' if npn else 'DMP2035U_GSD')+'_DIODES'
 new_footprints.append(dict(name=fp,description=src+'; lower-left B/G,lower-right E/S,upper C/D; functional IDs intentional. C2.0 X.8 X1=1.35 Y.9 Y1=2.9mm; mask+.05,paste1:1.',pads=[pad(roles[0],-.95,-1,.8,.9),pad(roles[1],.95,-1,.8,.9),pad(roles[2],0,1,.8,.9)],tracks=outline(-1.5,-.7,1.5,.7)))
 if npn:
  pins=[pin('B','B',-20,0,'left','input'),pin('E','E',20,-20,'right'),pin('C','C',20,20,'right')]
  lines=[line(-20,0,-5,0),line(-5,-15,-5,15),line(-5,8,20,20),line(-5,-8,20,-20),line(12,-13,18,-19),line(18,-19,11,-19),line(18,-19,16,-12)]
 else:
  pins=[pin('G','G',-20,0,'left','input'),pin('S','S',20,20,'right'),pin('D','D',20,-20,'right')]
  lines=[line(-20,0,-10,0),line(-10,-14,-10,14),line(0,-15,0,-7),line(0,-4,0,4),line(0,7,0,15),line(0,15,12,15),line(12,15,12,20),line(12,20,20,20),line(0,-15,12,-15),line(12,-15,12,-20),line(12,-20,20,-20),line(0,0,10,0),line(0,0,5,3),line(0,0,5,-3),line(10,0,12,20)]
 new_symbols.append(dict(name=mpn,description=src+'; conventional '+('NPN' if npn else 'PMOS')+' symbol; used in5V BSP input driver,NOT24V load path',designator='Q?',designator_x=-20,designator_y=40,pins=pins,lines=lines,parameters=parameters('Diodes Incorporated',mpn,src,'NPN 40V200mA' if npn else 'PMOS20V;VGS±10V',{'Datasheet':'sources/autonomous_closure/'+('MMBT3904.pdf' if npn else 'DMP2035U.pdf'),'Terminal Mapping':'Top view tab/lead above C/D; lower-left B/G; lower-right E/S; manufacturer functional IDs, no guessed numbers'}),footprints=[dict(name=fp,is_current=True)]))
 asset(mpn,mpn,fp,src,kind='ACTIVE')

# Explicit Same Sky series order-code construction and manufacturer p2 hole layout.
for n in [2,3]:
 mpn=f'TB002-500-0{n}BE';fp=f'GW_TB002_500_{n}P_SAMESKY';span=5*(n-1);src='Same Sky TB002-500 Rev1.04 09/12/2024 p1 order key,p2 PCB layout'
 ps=[pad(str(i+1),5*i,0,2.2,2.2,1.3) for i in range(n)];ps[0]['shape']='rectangle'
 new_footprints.append(dict(name=fp,description=src+';5mm pitch,1.30mm drilled holes;2.20mm copper diameter prototype annular-ring choice;wire-entryfront=-Y;project assigns1left+Xsequence.',pads=ps,tracks=outline(-2.5,-3.5,span+2.5,4.1)))
 new_symbols.append(dict(name=mpn,description=src+'; project contact1left in PCBtopview with wire entry facing-Y;not manufacturer polarity',designator='J?',designator_x=-30,designator_y=20*n,pins=[pin(str(i+1),str(i+1),-30,(n-1-i)*20,'left') for i in range(n)],rectangles=[dict(x1=-30,y1=-10,x2=20,y2=20*n-10)],parameters=parameters('Same Sky (formerly CUI Devices)',mpn,src,f'{n}-pole5mm terminal block',{'Datasheet':'sources/autonomous_closure/tb002-500.pdf','Physical Mapping':'Project-defined1left then+X in PCBtopview; wire-entryfront-Y. Confirm wire polarity against silk before bringup.'}),footprints=[dict(name=fp,is_current=True)]))
 asset(mpn,mpn,fp,src)

# Manufacturer recommended hole pattern, not a guessed connector helper default.
for n in [2,6]:
 mpn=f'61300{n}11121';fp=f'GW_WRPHD_{n}X1_254_WURTH';span=2.54*(n-1);src=f'Wurth {mpn} official datasheet p1 dimensions/recommended hole pattern;1.10mm holes2.54pitch'
 ps=[pad(str(i+1),2.54*i,0,1.8,1.8,1.1) for i in range(n)];ps[0]['shape']='rectangle'
 new_footprints.append(dict(name=fp,description=src+';copper1.8mm diameter/mask+.1 prototype process selection;pin1markedend,sequence+X.',pads=ps,tracks=outline(-1.27,-1.27,span+1.27,1.27)))
 new_symbols.append(dict(name=mpn,description=src+';project orientationpin1lefttopview,sequence+X',designator='J?',designator_x=-30,designator_y=n*20,pins=[pin(str(i+1),str(i+1),-30,(n-1-i)*20,'left') for i in range(n)],rectangles=[dict(x1=-30,y1=-10,x2=20,y2=20*n-10)],parameters=parameters('Wurth Elektronik',mpn,src,f'{n}x1 2.54mm straight male header',{'Datasheet URL':f'https://www.we-online.com/components/products/datasheet/{mpn}.pdf'}),footprints=[dict(name=fp,is_current=True)]))
 asset(mpn,mpn,fp,src)

# Reuse only already-verified same-manufacturer RC0603 mounting geometry; clone
# the compact zigzag graphics and refresh all identity/rating parameters.
base=symbols['RC0603FR-0710KL']
for mpn,val in [('RC0603FR-074K7L','4.7 kOhm'),('RC0603FR-07100RL','100 Ohm')]:
 s=copy.deepcopy(base);s['name']=mpn;s['description']=mpn+';1%0.1W75V0603; manufacturer RCseries ordering;Yageo mounting13Feb2018V10p4'
 s['parameters']=parameters('Yageo',mpn,'Yageo RC0603 series order coding; Mounting13Feb2018V10 p4 Fig4/Table1',val,{'Tolerance':'1%','Voltage Rating':'75V or sqrt(P*R),whichever lower','Power Rating':'0.1W at70C','Package':'0603','Electrical Status':'DERIVED_PENDING_REVIEW;ORDER_CODE_FAMILY_SUPPORTED;EXACT_NOMINAL_SHEET_PENDING'})
 s['footprints']=[dict(name='GW_RC0603_YAGEO_REFLOW',is_current=True)];s.pop('primitive_order',None)
 # New component must receive new unique graphics/model identities on authoring.
 for k in ['header_params','designator_unique_id']:s.pop(k,None)
 for k in ['lines','polylines','rectangles','pins']:
  for p in s.get(k,[]):p.pop('raw_params',None);p.pop('unique_id',None)
 new_symbols.append(s);asset(mpn,mpn,'GW_RC0603_YAGEO_REFLOW','Yageo same-series RC0603 manufacturer land pattern; electrical order code nominal sheet pending')

# One optional bus-end termination model, shared by CAN and RS485. Manufacturer
# Vishay20035 p9 REFLOW1206: G1.50,Y1.05,X1.80,Z3.60mm; body3.2x1.6.
mpn='CRCW1206120RFKEA';fp='GW_CRCW1206_VISHAY_20035_REFLOW'
s=copy.deepcopy(symbols['CRCW080575R0FKEA']);s['name']=mpn;s['description']='Vishay D/CRCW e3 family20035;120ohm1%0.25W1206; optional bus-end termination,open-default jumper.'
s['parameters']=parameters('Vishay',mpn,'Vishay20035 family ordering/power;18Jun2018p9 REFLOW1206 lands','120 Ohm',{'Tolerance':'1%','Power Rating':'0.25W at70C','Package':'1206','Datasheet':'sources/ethernet_75ohm/C844859.pdf','Electrical Status':'DERIVED_PENDING_REVIEW;END_NODE_ONLY;STOCK_UNVERIFIED'})
s['footprints']=[dict(name=fp,is_current=True)];s.pop('primitive_order',None)
for k in ['header_params','designator_unique_id']:s.pop(k,None)
for k in ['lines','polylines','rectangles','pins']:
 for v in s.get(k,[]):v.pop('raw_params',None);v.pop('unique_id',None)
new_symbols.append(s)
new_footprints.append(dict(name=fp,description='Vishay20035p9 REFLOW1206 G1.50 Y1.05 X1.80 Z3.60mm;centres2.55mm;body3.2x1.6mm. Mask+.05/paste1:1 prototype process.',pads=[pad('1',-1.275,0,1.05,1.8),pad('2',1.275,0,1.05,1.8)],tracks=outline(-1.6,-.8,1.6,.8)))
asset(mpn,mpn,fp,'Vishay20035p9 family1206 reflow;120R1% order code;0.25W at70C;stock notverified')

# Samsung exact retained product HTML establishes the correct tolerance row:
# CL10A105KB8NNNC1608+/-0.10;CL21A106KAYNNNE2012+/-0.20.
# ManufacturerMLCC_2401p159 gives ranges;explicitmidpoints are prototypechoices.
for name,gap,pw,ph,Lb,Wb,row in [('GW_SAMSUNG_CL10_1608_REFLOW',.68,.76,.85,1.6,.8,'1608+/-0.10:a.63-.73,b.71-.81,c.80-.90'),('GW_SAMSUNG_CL21_2012_REFLOW',.88,.96,1.40,2.0,1.25,'2012+/-0.20:a.83-.93,b.91-1.01,c1.35-1.45')]:
 x=(gap+pw)/2
 new_footprints.append(dict(name=name,description='SamsungMLCC_2401Jan2024p159reflow;'+row+'mm;selectedmidpointswithinranges. Pin1/2nonpolarprojectconvention;mask+.05,paste1:1.',pads=[pad('1',-x,0,pw,ph),pad('2',x,0,pw,ph)],tracks=outline(-Lb/2,-Wb/2,Lb/2,Wb/2)))

# Backend refuses duplicate pad IDs. Use explicit aliases and REQUIRE native
# one-to-many mapping of symbol11 to every alias. Do not bind this candidate
# with the default one-to-one map. It is not a fabrication-ready replacement.
t=copy.deepcopy(footprints['GW_DRC0010J_TI_TPS2662']);t['name']='GW_DRC0010J_TI_TPS2662_EP11';t['description']='TI SLVSDT4F DRC0010J pp43-45; exact copper union central11+segment aliases11A/B/C/D. REQUIRED one-to-many model mapping: symbol11=>pads11,11A,11B,11C,11D all EF_RTN. CANDIDATE_MAPPING_PENDING; do not use default1:1.';t.pop('regions',None)
for p in t['pads']:
 p.pop('raw_tail',None);p['corner_radius_percent']=6 if p['designator']=='11' else 42
for suffix,(x,y) in zip('ABCD',[(x,y) for x in [-.25,.25] for y in [-1.445,1.445]]):
 p=pad('11'+suffix,x,y,.25,.51);p.update(shape='rounded_rectangle',corner_radius_percent=40,paste_mask_expansion=-1);t['pads'].append(p)
t['fills']=[x for x in t.get('fills',[]) if x['layer']=='Top Paste']
new_footprints.append(t)

(O/'new_symbols.json').write_text(json.dumps(new_symbols,indent=2)+'\n');(O/'new_footprints.json').write_text(json.dumps(new_footprints,indent=2)+'\n');(O/'cad_additions.json').write_text(json.dumps(assets,indent=2)+'\n')
print('Authored',len(new_symbols),'symbols and',len(new_footprints),'footprints; no native documents written')
