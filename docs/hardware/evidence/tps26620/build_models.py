"""Source-bound authoring inputs; binary CAD IO is exclusively Electronics AI.
TI SLVSDT4F Table6-1, DRC0010J drawings4218878/B, board/stencil examples.
"""
import json,copy,sys,shutil,hashlib
from pathlib import Path
O=Path(__file__).parent;R=Path.cwd();L=R/'hardware/academic_rev1/libraries'
sys.path.insert(0,str(O.parent));from symbol_style import style
before=json.loads((O/'symbols_before.json').read_text(encoding='utf-8'))['symbols']
updates=[]
for old in before:
    n=old['name'];kind=None
    if n=='SS3P6L-M3_86A':kind='schottky'
    elif old.get('rectangles') and len(old.get('pins',[]))==2:
        if n.startswith(('RC0603','MM204')):kind='resistor'
        elif n.startswith(('C5750','C0805','C0603','C3225')):kind='capacitor'
        elif n.startswith('XAL'):kind='inductor'
        elif n=='0451002.MRL':kind='fuse'
    if kind:updates.append(style(copy.deepcopy(old),kind))
nis=copy.deepcopy(next(s for s in before if s['name']=='NIS3071MT4TWG'))
for p in nis['parameters']:
    if p['name'] in ['Design Approval','Electrical Approval']:
        p['value']='SUPERSEDED_BY_TPS26620DRCR';p.pop('raw_params',None)
nis['parameters'].append(dict(name='Revision Use',value='HISTORICAL_RESOURCE_ONLY; no Academic Rev1 placement',hidden=True,x=0,y=0))
updates.append(nis)
src='TI TPS2662 SLVSDT4F Dec2021 Table6-1 p4; DRC0010J4218878/B board p44/stencil p45'
fp='GW_DRC0010J_TI_TPS2662'
pins=[]
for num,name,typ,x,y,orient in [(1,'IN','power',-90,40,'left'),(2,'UVLO','input',-90,20,'left'),
 (3,'OVP','input',-90,0,'left'),(4,'SHDN_N','input',-90,-20,'left'),(10,'OUT','power',90,40,'right'),
 (9,'FLT_N','open_collector',90,20,'right'),(8,'dVdT','bidirectional',90,0,'right'),
 (7,'ILIM','bidirectional',90,-20,'right'),(5,'RTN','power',-60,-60,'down'),
 (11,'RTN_EP','power',-20,-60,'down'),(6,'GND','power',60,-60,'down')]:
    pins.append(dict(designator=str(num),name=name,electrical_type=typ,x=x,y=y,orientation=orient,length=20,
                     hidden=False,show_name=True,show_designator=True))
params={'Manufacturer':'Texas Instruments','Manufacturer Part Number':'TPS26620DRCR',
 'Datasheet':'https://www.ti.com/lit/ds/symlink/tps2662.pdf','Local Datasheet':'sources/tps26620/tps2662.pdf',
 'Source':src,'CAD Status':'CAD_CANDIDATE','Design Approval':'APPROVED_COMPONENT_SELECTION',
 'Electrical Test':'NOT_TESTED','Critical Connection':'Pin5 and EP11 to EF_RTN, NEVER directly to system GND pin6',
 'Fault Response':'TPS26620 latch-off, adjustable overvoltage cutoff; not TPS26621 auto-retry'}
syms=[dict(name='TPS26620DRCR',designator='U?',description='Single-channel60V eFuse; TPS26620 latch-off; RTN != system GND; DRC10+EP11',
 pins=pins,rectangles=[dict(x1=-90,y1=-60,x2=90,y2=60)],footprints=[dict(name=fp,is_current=True)],
 parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in params.items()])]
def two(mpn,value,foot,kind,manufacturer,source):
    s=dict(name=mpn,designator='R?' if kind=='resistor' else 'C?',description=value+'; '+source,
      pins=[dict(designator=str(i),name=str(i),electrical_type='passive',x=0,y=0) for i in [1,2]],
      footprints=[dict(name=foot,is_current=True)],parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in {
       'Manufacturer':manufacturer,'Manufacturer Part Number':mpn,'Value':value,'Source':source,
       'Datasheet':('https://yageogroup.com/download/specsheet/'+mpn if kind=='resistor' else 'sources/DI_CIN_C0603C103K1RACTU.pdf'),
       'Design Approval':'PROPOSED_APPLICATION_VALUE','CAD Status':'CAD_VERIFIED','Electrical Test':'NOT_TESTED'}.items()])
    syms.append(style(s,kind))
for mpn,v in [('RC0603FR-0713K3L','13.3kOhm1%0.1W75V'),('RC0603FR-07768KL','768kOhm1%0.1W75V'),
              ('RC0603FR-0733K2L','33.2kOhm1%0.1W75V'),('RC0603FR-0730K1L','30.1kOhm1%0.1W75V')]:
    two(mpn,v,'GW_RC0603_YAGEO_REFLOW','resistor','Yageo','Exact Yageo spec; manufacturer Mounting2018p4Fig4/Table1')
two('C0603C103K1RACTU','10nF10%100VX7R','GW_0603_KEMET_NOMINAL','capacitor','KEMET',
    'Exact KEMET DI_CIN spec; KEMET C1027Table3 nominal1608 mechanically compatible reference lands')
def pad(n,x,y,w,h,r=0):
    return dict(designator=str(n),x=x,y=y,width=w,height=h,shape='rounded_rectangle',corner_radius_percent=r,
       layer='Top Layer',hole_size=0,is_plated=False,solder_mask_expansion_mode='manual',solder_mask_expansion=.05,
       paste_mask_expansion_mode='manual',paste_mask_expansion=0 if n!=11 else -1.)
pads=[pad(n,-1.4,1-(n-1)*.5,.6,.24,21) for n in range(1,6)]
pads +=[pad(n,1.4,-1+(n-6)*.5,.6,.24,21) for n in range(6,11)]
pads +=[pad(11,0,0,1.65,2.4,3)]+[pad(11,x,y,.25,.5,20) for x in [-.25,.25] for y in [-1.45,1.45]]
# Retain exact manufacturer geometry. The backend refuses repeated11 pads.
# Copper regions reproduce the tongues; native conversion to a custom pad11
# and ECO net inheritance remain REQUIRED before PCB use. No fictitious terminals.
extension_regions=[dict(layer='Top Layer',kind='copper',name='EP11_EXTENSION_REQUIRES_NATIVE_CUSTOM_PAD',
 vertices=[dict(x=x+dx,y=y+dy) for dx,dy in [(-.125,-.25),(.125,-.25),(.125,.25),(-.125,.25)]])
 for x in [-.25,.25] for y in [-1.45,1.45]]
pads=pads[:11]
fills=[dict(layer='Top Paste',x1=-.75,x2=.75,y1=y-.53,y2=y+.53) for y in [-.63,.63]]
fills +=[dict(layer='Top Paste',x1=x-.125,x2=x+.125,y1=y-.17,y2=y+.17) for x in [-.25,.25] for y in [-1.53,1.53]]
fills +=[dict(layer='Top Solder',x1=x-.175,x2=x+.175,y1=y-.3,y2=y+.3) for x in [-.25,.25] for y in [-1.45,1.45]]
foot=dict(name=fp,description=src+'; CAD_CANDIDATE: EP11 extensions require native custom-pad conversion/net inheritance; RTN only',pads=pads,fills=fills,regions=extension_regions,
 tracks=[dict(x1=-1.5,y1=y,x2=1.5,y2=y,width=.1,layer='Mechanical 1') for y in [-1.5,1.5]])
for name,data in [('symbols.json',syms),('footprints.json',[foot]),('updates.json',updates)]:
    (O/name).write_text(json.dumps(data,indent=2)+'\n')
S=L/'sources/tps26620';S.mkdir(exist_ok=True)
pdf=O.parent/'input_protection_freeze/tps2662.pdf';shutil.copy2(pdf,S/'tps2662.pdf')
print(json.dumps(dict(new_symbols=len(syms),new_footprints=1,modified=[s['name'] for s in updates])))
