"""Vishay20035 Rev18-Jun-2018 p9 exact reflow lands; no binary CAD IO."""
import json,shutil,sys,hashlib
from pathlib import Path
O=Path(__file__).parent;L=Path('hardware/academic_rev1/libraries');S=L/'sources/ethernet_75ohm';S.mkdir(exist_ok=True)
manifest=[]
for n in ['C4275','C844859']:
 p=Path('C:/Users/justa/Downloads')/(n+'.pdf');dst=S/p.name;shutil.copy2(p,dst)
 manifest.append(dict(path=dst.as_posix(),original=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
sys.path.insert(0,str(O.parent));from symbol_style import style
mpn='CRCW080575R0FKEA';fp='GW_CRCW0805_VISHAY_20035_REFLOW'
params={'Manufacturer':'Vishay','Manufacturer Part Number':mpn,'Value':'75 Ohm','Tolerance':'1%',
 'Power Rating':'0.125 W at70C; derating applies','Package':'0805 /2012','TCR':'100 ppm/K',
 'Datasheet':'https://www.vishay.com/docs/20035/dcrcwe3.pdf','Local Datasheet':'sources/ethernet_75ohm/C844859.pdf',
 'Source':'Vishay20035 Rev18-Jun-2018 p3 ordering, p9 body/reflow lands; JLC C844859 exact identity observed2026-11-07',
 'LCSC Part Number':'C844859','CAD Status':'CAD_VERIFIED','Design Approval':'RETAINED_ORIGINAL_SELECTION',
 'Electrical Test':'NOT_TESTED','Terminal Mapping':'Nonpolar resistor: project pin1=left pad1,pin2=right pad2',
 'Assembly':'JLC Extended observed; quantity unknown; verify before ordering'}
s=dict(name=mpn,designator='R?',description='75Ohm1%0.125W0805 Vishay D/CRCW e3; Ethernet cable termination; not C-suffix commodity variant',
 pins=[dict(designator=str(i),name=str(i),electrical_type='passive',x=0,y=0) for i in [1,2]],
 footprints=[dict(name=fp,is_current=True)],parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in params.items()])
style(s,'resistor')
pads=[dict(designator=str(i),x=x,y=0,width=.95,height=1.45,shape='rectangle',layer='Top Layer',hole_size=0,is_plated=False,
 solder_mask_expansion=.05,solder_mask_expansion_mode='manual',paste_mask_expansion=0,paste_mask_expansion_mode='manual') for i,x in [(1,-.975),(2,.975)]]
tracks=[dict(x1=a,y1=b,x2=c,y2=d,width=.05,layer='Mechanical 1') for a,b,c,d in [(-1,-.625,1,-.625),(1,-.625,1,.625),(1,.625,-1,.625),(-1,.625,-1,-.625)]]
f=dict(name=fp,description='Vishay20035p9 reflow0805 G1.00 Y0.95 X1.45 Z2.90mm; centers1.95mm; body2.0x1.25mm. Mask+.05/paste1:1 prototype process choices.',pads=pads,tracks=tracks)
(O/'symbols.json').write_text(json.dumps([s],indent=2)+'\n');(O/'footprints.json').write_text(json.dumps([f],indent=2)+'\n')
print('Authored one exact75Ohm symbol and one Vishay reflow footprint.')
