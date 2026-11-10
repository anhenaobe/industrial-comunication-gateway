"""Explicit, manufacturer-dimensioned inputs for the official library writer.

Does not write binary CAD. No generic package helper dimensions are used.
Mask/paste settings on new SMD lands follow board rules until DFM approval.
"""
import json
from pathlib import Path
OUT=Path(__file__).parent
footprints=[];symbols=[];assets=[]
def pad(n,x,y,w,h,**kw):
    return dict(designator=str(n),x=x,y=y,width=w,height=h,shape='rectangle',
                layer='Top Layer',**kw)
def footprint(name,pads,source,notes):
    footprints.append(dict(name=name,description=(source+'; '+notes)[:500],pads=pads))
def symbol(name,pins,fp,source,manufacturer,ids,notes='',prefix='U'):
    # Pin identities come from each cited pin table, never the arrangement.
    n=len(pins);half=(n+1)//2
    ps=[]
    for i,(num,label,typ) in enumerate(pins):
        left=i<half;row=i if left else i-half
        ps.append(dict(designator=str(num),name=label,electrical_type=typ,
                       x=-60 if left else 60,y=20*(half-1-row),length=20,
                       orientation='left' if left else 'right'))
    symbols.append(dict(name=name,designator=prefix+'?',description=(source+'; '+notes)[:500],
                        pins=ps,rectangles=[dict(x1=-60,y1=-10,x2=60,y2=20*half)],
                        footprints=[dict(name=fp,is_current=True)] if fp else [],
                        parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in {
                            'Manufacturer':manufacturer,'Manufacturer Part Number':name,
                            'Source':source,'CAD Status':'CAD_CANDIDATE',
                            'Limitations':notes or 'Manufacturer geometry readback; native placement/DFM pending.'}.items()]))
    assets.append(dict(asset_id=name,item_kind='AUXILIARY',component_ids=ids,mpn=name,
                       symbol=name,footprint=fp or 'MISSING',source=source,
                       cad_status='CAD_CANDIDATE' if fp else 'CAD_BLOCKED',
                       symbol_status='CAD_CANDIDATE',footprint_status='CAD_CANDIDATE' if fp else 'CAD_MISSING',
                       limitations=notes or 'Exact drawing geometry; native placement, mask/paste and assembly qualification pending.',
                       package_requirement=fp or 'UNRESOLVED:'+name))

source='Kyocera TNY1T-H1-DEX01-11 17-Jul-2026 pp4,6 table2 fig4'
footprint('GW_KC2016Z_KYOCERA',[pad(1,-.9,-.6,.6,.8),pad(2,.9,-.6,.6,.8),
                                 pad(3,.9,.6,.6,.8),pad(4,-.9,.6,.6,.8)],source,
          'Top view derived by mirroring numbered bottom view; 1=STANDBY,2=GND,3=OUT,4=VCC; no crystal load pads.')
symbol('KC2016Z25.0000C15XXK',[(1,'STANDBY','input'),(2,'GND','power'),(3,'OUT_25MHz','output'),(4,'VCC','power')],
       'GW_KC2016Z_KYOCERA',source,'Kyocera',['MCU_YHSE','ETH_Y25'],
       'Two independent oscillators proposed; 10nF per supply. Tie1 to3V3. Load<=15pF and PHY phase-noise qualification pending.',prefix='Y')

source='Pulse HX1188FNL revB 30-May-2014 sheets2-3 PS-2005.002-D'
# Inch dimensions govern. Copper extent .400 outside, .270 inside.
p=[]
for i in range(8):
    x=(i-3.5)*1.27
    p.extend([pad(i+1,x,-(.400+.270)*25.4/4,.030*25.4,(.400-.270)*25.4/2),
              pad(16-i,x,(.400+.270)*25.4/4,.030*25.4,(.400-.270)*25.4/2)])
footprint('GW_HX1188FNL_PULSE',p,source,'16 lands; 1.27mm pitch, .762x1.651mm; row centers +/-4.2545mm. No metal-under-transformer keepout encoded: board gate.')
roles=['TD+','TCT','TD-','NC','NC','RD+','RCT','RD-','RX-','CMT_RX','RX+','NC','NC','TX-','CMT_TX','TX+']
symbol('HX1188FNL',[(i+1,n,'passive') for i,n in enumerate(roles)],'GW_HX1188FNL_PULSE',source,'Pulse Electronics',['ETH_TMAG'],
       'Use exact winding map; NC4,5,12,13 remain unconnected. FNLT is packaging variant; selected MPN FNL.',prefix='T')

source='Coilcraft document806-4 revised02/25/26 Recommended Land Pattern'
for name,height,ids in [('XAL4030-682MEC',3.1,['B3_L']),('XAL4040-103MEC',4.1,['B5_L'])]:
    fp='GW_'+name.split('-')[0]+'_COILCRAFT'
    # .093in pad center spacing, .038in pad width, .134in height.
    footprint(fp,[pad(1,-.093*25.4/2,0,.038*25.4,.134*25.4),
                  pad(2,.093*25.4/2,0,.038*25.4,.134*25.4)],source,
              'Terminals assigned project1/2 for nonpolar winding; place high dv/dt at stripe/terminal1. Height '+str(height)+'mm. Mask/paste DFM pending.')
    symbol(name,[(1,'1','passive'),(2,'2','passive')],fp,source,'Coilcraft',ids,
           'Nonpolar winding; pin1=marked high-dv/dt end by project convention. Full load/hot Isat and loss qualification pending.',prefix='L')

source='Bourns CDSOT23-SM712 saved2026-11-07 pp1-2 pin diagram and Recommended Footprint'
# Rotated 180deg versus the land sketch to match the top-view pin diagram.
footprint('GW_SM712_BOURNS',[pad(1,-.95,-1,.85,.85),pad(2,.95,-1,.85,.85),pad(3,0,1,.85,.85)],source,
          'Pins1/2 bus;3 reference. +/-7/12V asymmetric clamp. Not a generic SOT23 substitution.')
symbol('CDSOT23-SM712',[(1,'BUS_A','passive'),(2,'BUS_B','passive'),(3,'GND_REF','passive')],
       'GW_SM712_BOURNS',source,'Bourns',['RS_TVS'],
       'CAD mapping supported; no transferred 1kV surge rating for THVD1420. Populate only after protection qualification.',prefix='D')

source='TI SLVSBO7O table4-2 p4; DQA0010A 4220328/A board/stencil pp29-30'
p=[]
for i in range(5):
    p.extend([pad(i+1,-.835/2,1-i*.5,.565,.4 if i==2 else .2),
              pad(10-i,.835/2,1-i*.5,.565,.4 if i==2 else .2)])
footprint('GW_DQA0010A_TI',p,source,'0.5mm pitch; pad3/8 .565x.4; others .565x.2; rectangular candidate replaces R.05 corners, pending stencil/DFM review.')
names=['D1+','D1-','GND','D2+','D2-','NC','NC','GND','NC','NC']
symbol('TPD4E05U06DQAR',[(i+1,n,'power' if n=='GND' else 'passive') for i,n in enumerate(names)],
       'GW_DQA0010A_TI',source,'Texas Instruments',['ETH_DESD'],
       'PHY-side only, per DP83826EVM sheet3. GND3/8 to logic GND. NC6/7/9/10 may be pass-through pads; preserve isolation.',prefix='D')

source='Cinch/Stewart CT710001 revB0 10-Jul-2023 component-side recommended hole layout'
p=[]
for n in range(1,9):
    # pin1 is .050in from the mounting-post datum, pin2 .100in.
    x=n*1.27
    p.append(dict(designator=str(n),x=x,y=6.35 if n%2 else 8.89,width=1.5,height=1.5,
                  hole_size=.889,layer='Multi-Layer',shape='round',is_plated=True))
for name,x in [('S1',-2.032),('S2',13.462)]:
    p.append(dict(designator=name,x=x,y=3.048,width=2.3,height=2.3,hole_size=1.5748,
                  layer='Multi-Layer',shape='round',is_plated=True))
for name,x in [('MP1',0),('MP2',11.43)]:
    p.append(dict(designator=name,x=x,y=0,width=3.2,height=3.2,hole_size=3.2,
                  layer='Multi-Layer',shape='round',is_plated=False))
footprint('GW_SS7188SANF_STEWART',p,source,
          'Holes/positions from drawing; signal1..8=.89drill, shield1.57, mounts3.2NPTH. Copper lands1.5/2.3 are ENGINEERING CANDIDATES; fab annular ring/finished holes/body edge pending.')
symbol('SS-7188S-A-NF',[(i,str(i),'passive') for i in range(1,9)]+[('S1','SHIELD1','passive'),('S2','SHIELD2','passive')],
       'GW_SS7188SANF_STEWART',source,'Cinch / Stewart',['ETH_JRJ45'],
       'Numbered contacts per component-side drawing. S1/S2 are project labels for unnumbered shield tabs; MP1/2 are non-electrical mounting holes. Candidate copper lands; sourcing risk separate.',prefix='J')

source='Firstohm MM rev08-March-2023 printedpp75-78; p78 reflow pad table MM16/MM204'
footprint('GW_MM204_FIRSTOHM',[pad(1,-1.45,0,1.3,1.6),pad(2,1.45,0,1.3,1.6)],source,
          'Reflow minimum lands1.3x1.6, inner spacing1.6mm; nonpolar numbering project1/2. Pulse qualification separate.')
symbol('MM204F1K00TKRTR3K0',[(1,'1','passive'),(2,'2','passive')],'GW_MM204_FIRSTOHM',source,'Firstohm',
       ['DI_RTHR1','DI_RTHR2'],'1kOhm1%,0.25W@70C; normal Type3 operation supported. 500V/1kV system surge withstand NOT established.',prefix='R')

symbol('RC0603FR-0710KL',[(1,'1','passive'),(2,'2','passive')],'GW_CAND_0603_res',
       'Existing exact Yageo RC0603FR-0710KL sheet p1; AN5419 boot example; TI SLLSF78B section10.1',
       'Yageo',['MCU_RBOOT','RS_RDE','RS_RRE','DO_RPDA','DO_RPDB'],
       '10kOhm1%0.1W@70C; replaces unqualified FOJAN identity. Shared professor lands remain CAD_CANDIDATE, not qualified manufacturer lands.',prefix='R')

(OUT/'footprints_additions.json').write_text(json.dumps(footprints,indent=2)+'\n')
(OUT/'symbols_additions.json').write_text(json.dumps(symbols,indent=2)+'\n')
(OUT/'cad_additions.json').write_text(json.dumps(assets,indent=2)+'\n')
print(len(footprints),'new footprint candidates;',len(symbols),'symbol candidates')
