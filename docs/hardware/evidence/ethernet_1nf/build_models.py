import json,sys,shutil,hashlib
from pathlib import Path
O=Path(__file__).parent;L=Path('hardware/academic_rev1/libraries');S=L/'sources/ethernet_1nf';S.mkdir(exist_ok=True)
src=Path('C:/Users/justa/Downloads/C600002.pdf');dst=S/src.name;shutil.copy2(src,dst)
(O/'source_manifest.json').write_text(json.dumps([dict(path=dst.as_posix(),original=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest())],indent=2)+'\n')
sys.path.insert(0,str(O.parent));from symbol_style import style
n='C1206C102KGRACAUTO';fp='GW_C1206_KEMET_C1076_DENSITY_B'
source='KEMET C1076_X7R_HV_AUTO_SMD9/10/2019 pp1-2 ordering/rating,p4 body,p10 Table3 densityB1206; C600002 exact catalog identity'
params={'Manufacturer':'KEMET','Manufacturer Part Number':n,'Value':'1 nF','Tolerance':'10%','Voltage Rating':'2000 VDC',
 'Dielectric':'X7R','Package':'1206 /3216','Datasheet':'sources/ethernet_1nf/C600002.pdf','Source':source,
 'LCSC Part Number':'C600002','CAD Status':'CAD_VERIFIED','Electrical Approval':'PROVISIONAL_APPLICATION; not safety-Y certified',
 'Electrical Test':'NOT_TESTED','Terminal Mapping':'Nonpolar, project1-left/2-right; symbol1->pad1,2->pad2',
 'Assembly':'JLC Extended observed2026-11-07; quantity unknown; no stock reservation'}
s=dict(name=n,designator='C?',description='KEMET1nF10%2kVDCX7R1206; Ethernet chassis AC return; no safety-Y or surge claim',
 pins=[dict(designator=str(i),name=str(i),electrical_type='passive',x=0,y=0) for i in [1,2]],
 footprints=[dict(name=fp,is_current=True)],parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in params.items()]);style(s,'capacitor')
pads=[dict(designator=str(i),x=x,y=0,width=1.15,height=1.8,shape='rectangle',layer='Top Layer',hole_size=0,is_plated=False,
 solder_mask_expansion=.05,solder_mask_expansion_mode='manual',paste_mask_expansion=0,paste_mask_expansion_mode='manual') for i,x in [(1,-1.5),(2,1.5)]]
tracks=[dict(x1=a,y1=b,x2=c,y2=d,width=.05,layer='Mechanical 1') for a,b,c,d in [(-1.6,-.8,1.6,-.8),(1.6,-.8,1.6,.8),(1.6,.8,-1.6,.8),(-1.6,.8,-1.6,-.8)]]
f=dict(name=fp,description='KEMET C1076p10 Table3 DensityB1206:C1.50,Y1.15,X1.80mm; centers3.00; gap1.85; body3.2x1.6mm. Mask+.05/paste1:1 process choices, not safety insulation geometry.',pads=pads,tracks=tracks)
for name,data in [('symbols.json',[s]),('footprints.json',[f])]: (O/name).write_text(json.dumps(data,indent=2)+'\n')
asset=dict(asset_id=n,item_kind='PASSIVE',component_ids=['ETH_CBOB'],mpn=n,symbol=n,footprint=fp,source=source,cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',package_requirement=fp,
 limitations='Manufacturer densityB reflow geometry; mask+.05/paste1:1 explicit process choices. 2kVDC is not safety-Y certification. No hardware, industrial surge or insulation compliance claim.',
 lcsc_code='C600002',datasheet_url='https://yageogroup.com/download/specsheet/C1206C102KGRACAUTO',local_datasheet=dst.as_posix(),
 availability_category='JLC Extended; C600002; public JSON-LD observed2026-11-07',stock_status='Catalog reports in_stock; quantity unknown; recheck assembly stock')
(O/'cad_assets.json').write_text(json.dumps([asset],indent=2)+'\n')
(O/'bom_decisions.json').write_text(json.dumps(dict(patches={'ETH_CBOB':dict(cad_route='PROJECT_LOCAL_VERIFIED',electrical_value_source=source,
 observations='Two1nF2kVDC capacitors: nodeA->CHASSIS and separately nodeB->CHASSIS. C600002 exact MPN confirmed; not Y safety certified; no topology change.')}),indent=2)+'\n')
print('Prepared one exact capacitor symbol, footprint and CAD binding; quantities/MPN unchanged.')
