"""Manufacturer functional-position mapping. No equivalent-vendor numbering."""
import json,hashlib,shutil,copy
from pathlib import Path
O=Path(__file__).parent;L=Path('hardware/academic_rev1/libraries');S=L/'sources/bsp75n_closure';S.mkdir(exist_ok=True)
source=Path('C:/dev/7mo/design/Datasheets_industrial_gateway/BSP75N.pdf');dst=S/source.name;shutil.copy2(source,dst)
(O/'source_manifest.json').write_text(json.dumps(dict(path=dst.as_posix(),original=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),manufacturer_url='https://www.diodes.com/assets/Datasheets/BSP75N.pdf'),indent=2)+'\n')
old=json.loads((O/'original_0.json').read_text(encoding='utf-8'))['component'];s=copy.deepcopy(old)
fp='GW_BSP75N_SOT223_DN_DIODES';src='Diodes DS33016 Rev7-2 Jan2024 p1 Top View Pin Out, p8 Suggested Pad Layout; functional pad identifiers preserve original symbol pins'
s['description']='BSP75NTA smart low-side switch; physical terminal positions and Diodes land pattern verified; IN,D,S,S_TAB identifiers; driver VOH acceptance remains pending.'
values={'Source':src,'CAD Status':'CAD_VERIFIED','Limitations':'Physical mapping verified from Diodes top view: with tab above, left IN, middle D, right S; tab S_TAB=Source. No manufacturer numeric pin IDs asserted. Loaded driver VOH and startup OFF not yet verified.',
 'Electrical Approval':'ELECTRICAL_BLOCKED_DRIVER_VOLTAGE_PENDING','Datasheet':'sources/bsp75n_closure/BSP75N.pdf'}
for p in s['parameters']:
 if p['name'] in values:p['value']=values.pop(p['name']);p.pop('raw_params',None)
s['parameters'] += [dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in values.items()]
s['parameters'] += [dict(name='Physical Mapping',value='IN left lower;D center lower;S right lower;S_TAB upper tab;Top View',hidden=True,x=0,y=0)]
s['footprints']=[dict(name=fp,is_current=True)]
# Primitive ordering must include newly added parameters, while retaining all
# existing pins, graphic records and identity fields.
s.pop('primitive_order',None)
def pad(n,x,y,w,h):return dict(designator=n,x=x,y=y,width=w,height=h,shape='rectangle',layer='Top Layer',hole_size=0,is_plated=False,
 solder_mask_expansion=.05,solder_mask_expansion_mode='manual',paste_mask_expansion=0,paste_mask_expansion_mode='manual')
f=dict(name=fp,description=src+'; C2.30 C1=6.40 X1.20 X1=3.30 Y1.60 Y1=1.60 Y2=8.00mm; mask+.05/paste1:1 explicit prototype process.',
 pads=[pad('IN',-2.3,-3.2,1.2,1.6),pad('D',0,-3.2,1.2,1.6),pad('S',2.3,-3.2,1.2,1.6),pad('S_TAB',0,3.2,3.3,1.6)],
 tracks=[dict(x1=a,y1=b,x2=c,y2=d,width=.05,layer='Mechanical 1') for a,b,c,d in [(-3.25,-1.75,3.25,-1.75),(3.25,-1.75,3.25,1.75),(3.25,1.75,-3.25,1.75),(-3.25,1.75,-3.25,-1.75)]])
(O/'symbol_update.json').write_text(json.dumps(s,indent=2)+'\n');(O/'footprints.json').write_text(json.dumps([f],indent=2)+'\n')
asset=dict(asset_id='ACTIVE_BSP75NTA',item_kind='ACTIVE',component_ids=[],mpn='BSP75NTA',symbol='BSP75NTA',footprint=fp,source=src,cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',package_requirement=fp,
 limitations='Physical positions/Diodes lands verified using IN,D,S,S_TAB pad IDs; no guessed numbers. Driver>=4.5V for overtemperature protection and reset-OFF still need prototype acceptance. No automatic electrical approval.')
(O/'cad_assets.json').write_text(json.dumps([asset],indent=2)+'\n')
dec=dict(active_patches={'ACTIVE_BSP75NTA':dict(electrical_status='ELECTRICAL_BLOCKED',capture_status='PHYSICAL_WIRING_READY_DRIVER_ACCEPTANCE_PENDING',selection_status='SELECTED_FOR_CAPTURE',
 pin_pad_check='VERIFIED Diodes functional terminals to physical pad positions; alphabetic identifiers retained',dimensional_check='VERIFIED DS33016p8 exact suggested land pattern',action='Use saved BSP footprint; verify loaded drive and reset-OFF before energizing DO loads')},
 record_fields={'ACTIVE_BSP75NTA':dict(design_approval='SELECTED_DEVICE;DRIVE_NOT_APPROVED',validation_scope='ACADEMIC_PROTOTYPE_PHYSICAL_MAPPING_CLOSED',test_status='NOT_ELECTRICALLY_TESTED')})
(O/'bom_decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
calc=dict(V5_tolerance_min=4.86249,V5_tolerance_max=5.17365,IIN_at5V_max_A=.0012,RPDB_min_ohm=9900,load_screen_A=.0012+5.17365/9900,
 droop_budget_V=4.86249-4.5,equivalent_source_R_budget_ohm=(4.86249-4.5)/(.0012+5.17365/9900),
 limitations='1.2mA manufacturer limit at5V only, not all-voltage proof. R_budget is engineering target, not guaranteed SN74 output resistance. Source/return drop further reduces margin.')
(O/'calculations.json').write_text(json.dumps(calc,indent=2)+'\n')
print('BSP physical mapping uses retained IN,D,S,S_TAB pin identities; footprint authored from Diodesp8.')
