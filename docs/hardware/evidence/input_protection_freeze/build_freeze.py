"""Explicit manufacturer geometry, approved prototype values and generator overlay.
No binary CAD writes. Native files are written/read through Electronics AI.
"""
import json,shutil,hashlib,csv,copy,sys
from pathlib import Path
R=Path.cwd();O=Path(__file__).parent;L=R/'hardware/academic_rev1/libraries'
S=L/'sources/academic_freeze';S.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(O.parent));from symbol_style import style
docs={
 'fuse_manufacturer_drawing.pdf':'https://media.digikey.com/pdf/Data%20Sheets/Littelfuse%20PDFs/451_453SERIES.pdf',
 'TDK_exact.pdf':'https://datasheet.octopart.com/C5750X7R2A475K-TDK-datasheet-37185778.pdf',
 'YAGEO_mount.pdf':'https://sigma.octopart.com/138820526/technical_drawing/Yageo-AT0603FRE074K7L.pdf',
 'KEMET_family.pdf':'https://datasheet.lcsc.com/datasheet/pdf/da640179b8b977b6a47e045528de98bb.pdf?productCode=C21380065',
 'RC0603FR-0762KL.pdf':'https://yageogroup.com/download/specsheet/RC0603FR-0762KL',
 'RC0603FR-0715KL.pdf':'https://yageogroup.com/download/specsheet/RC0603FR-0715KL',
 'C0805C225K5RACTU.pdf':'https://yageogroup.com/download/specsheet/C0805C225K5RACTU',
 'C0603C680J5GACTU.pdf':'https://docs.rs-online.com/cdb0/0900766b816ffe5b.pdf'}
manifest=[]
for name,url in docs.items():
    p=O/name;assert p.read_bytes().startswith(b'%PDF-'),name
    dst=S/name;shutil.copy2(p,dst)
    manifest.append(dict(local=str(dst.relative_to(R)),url=url,sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),
                         provenance='Manufacturer-authored document; retrieval host recorded, not a third-party CAD model.'))
(O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def unwrap(p):
    d=json.loads(p.read_text());return d.get('structuredContent') or json.loads(d['content'][0]['text'])
fps=[];syms=[];assets=[]
def pad(n,x,y,w,h,mask=.025):return dict(designator=str(n),x=x,y=y,width=w,height=h,shape='rectangle',
    layer='Top Layer',hole_size=0,is_plated=False,rotation=0,
    solder_mask_expansion_mode='manual',solder_mask_expansion=mask,
    paste_mask_expansion_mode='manual',paste_mask_expansion=0)
def foot(n,p,src,note):
    fps.append(dict(name=n,pads=p,description=(src+'; '+note)[:500]));return n
def symbol(mpn,pins,fp,source,manufacturer,value,ids,kind='AUXILIARY',cad='CAD_VERIFIED',note=''):
    half=(len(pins)+1)//2;ps=[]
    for i,(n,label,typ) in enumerate(pins):
        left=i<half;row=i if left else i-half
        ps.append(dict(designator=str(n),name=label,electrical_type=typ,x=-70 if left else 70,
            y=20*(half-1-row),length=20,orientation='left' if left else 'right',hidden=False))
    params={'Manufacturer':manufacturer,'Manufacturer Part Number':mpn,'Value':value,'Source':source,
            'Design Approval':'PROTOTYPE_APPROVED','Electrical Test':'NOT_TESTED','CAD Status':cad,'Limitations':note}
    syms.append(dict(name=mpn,designator=('R?' if 'RC0603' in mpn else 'D?' if mpn.startswith('TDS') else 'C?'),
        description=(source+'; '+value+'; '+note)[:500],pins=ps,rectangles=[dict(x1=-70,y1=-10,x2=70,y2=20*half)],
        footprints=[dict(name=fp,is_current=True)],parameters=[dict(name=k,value=v or 'None',hidden=True,x=0,y=0) for k,v in params.items()]))
    if mpn.startswith('RC0603'):style(syms[-1],'resistor')
    elif mpn.startswith(('C5750','C0805','C0603','C3225')):style(syms[-1],'capacitor')
    asset(mpn,mpn,fp,source,ids,kind,cad,note)
def asset(mpn,sym,fp,source,ids,kind='AUXILIARY',cad='CAD_VERIFIED',note=''):
    assets.append(dict(asset_id=('ACTIVE_'+mpn if kind=='ACTIVE' else mpn),item_kind=kind,component_ids=ids,
        mpn=mpn,symbol=sym,footprint=fp,source=source,cad_status=cad,symbol_status=cad,footprint_status=cad,
        limitations=note or 'Pin/pad identity and explicit source dimensions checked. Prototype process choice; not electrically tested.',
        package_requirement=fp))
two=[(1,'1','passive'),(2,'2','passive')]

src='Semtech TDS3311P Rev2.4 pp2,7-9; official product portal confirms33V orderTDS3311P.C'
ft=foot('GW_TDS3311P_SEMTECH',[pad(1,-.5,-.725,.3,.65),pad(2,0,-.725,.3,.65),pad(3,.5,-.725,.3,.65),
    pad(4,.5,.725,.3,.65),pad(5,0,.725,.3,.65),pad(6,-.5,.725,.3,.65)],src,
    'Manufacturer reference lands; all1/2/3GND and4/5/6IN. Mask+.025 and1:1paste are prototype process choices.')
symbol('TDS3311P.C',[(n,'GND' if n<=3 else 'IN','passive') for n in range(1,7)],ft,src,'Semtech','33V working;42Vmax specified35A pulse',['IN_TVS'])

src='Littelfuse451/453 manufacturer recommended pad layout; saved historical p371; current2025p4 identical dimension list'
# Resolve the rounded drawing dimensions: (6.86-2.95)/2=1.955, rounding1.96.
ft=foot('GW_0451_LITTELFUSE',[pad(1,-2.4525,0,1.955,3.15),pad(2,2.4525,0,1.955,3.15)],src,
    'Nonpolar project1/2; pad1.955x3.15 rounds1.96; centers4.905; outside6.86,inside2.95. No holder.')
asset('0451002.MRL','0451002.MRL',ft,src,['IN_FUSE'])

src='Yageo Mounting13-Feb-2018 V10 p4 Fig4/Table1; exact62k/15k manufacturer spec sheets'
ft=foot('GW_RC0603_YAGEO_REFLOW',[pad(1,-.85,0,.9,.8),pad(2,.85,0,.9,.8)],src,
    'A2.6 overall,B.8 innergap,C.9 padwidth,D.8 padheight; no generic0603 default.')
symbol('RC0603FR-0762KL',two,ft,src,'Yageo','62.0kOhm1%0.1W75V',['IN_RLIM'],'PASSIVE')
symbol('RC0603FR-0715KL',two,ft,src,'Yageo','15.0kOhm1%0.1W75V',['IN_RFAULT'],'PASSIVE')

src='TDK C5750X7R2A475K230KA exact2014web-derived PDF p1 lands,p2 DCbias; current official product page same PA/PB/PC'
ft=foot('GW_C5750_TDK_REFLOW',[pad(1,-2.85,0,1.3,5.0),pad(2,2.85,0,1.3,5.0)],src,
    'Selected PA4.40 gap/PB1.30 length/PC5.00 height within manufacturer4.1-4.8/1.2-1.4/4-5 ranges.')
symbol('C5750X7R2A475K230KA',two,ft,src,'TDK','4.7uF10%100VX7R',['B3_CIN','B5_CIN','IN_BULK'],'PASSIVE')

src='KEMET exact0805 spec body/termination dimensions; KEMET C1027 p12 Table3 nominal2012 reflow lands transferred to mechanically matching commercial0805'
ft=foot('GW_0805_KEMET_NOMINAL',[pad(1,-.9,0,1.15,1.45),pad(2,.9,0,1.15,1.45)],src,
    'Nominal C=.90,Y=1.15,X=1.45. Mechanical reuse from KEMET table; no COTS electrical qualification claimed; same2012case checked.')
symbol('C0805C224K1RACTU',two,ft,src,'KEMET','220nF10%100VX7R',['B3_CHF','B5_CHF','IN_HF'],'PASSIVE')
symbol('C0805C225K5RACTU',two,ft,src,'KEMET','2.2uF10%50VX7R',['B3_CVCC','B5_CVCC'],'PASSIVE',
    note='VCC5V local bypass;2.2uF prototype selection replaces known insufficient1uF part. Assumed>=60% bias retention; verify stableVCC at bring-up.')
src='KEMET C0603C680J5GACTU exact manufacturer spec; shared1608 body; KEMET C1027Table3p12 nominal1608 lands'
ft=foot('GW_0603_KEMET_NOMINAL',[pad(1,-.8,0,.95,1),pad(2,.8,0,.95,1)],src,
    'Nominal C=.80,Y=.95,X=1.00; manufacturer land geometry reused for same0603 body. Timing option DNP.')
symbol('C0603C680J5GACTU',two,ft,src,'KEMET','68pF5%50VC0G',['IN_CDVDT'],'PASSIVE',note='DNP in frozen BOM; dvdt open. Fit only if startup review/measurement requires slower ramp.')

src='TDK official C3225X7R1C156M250AB product page lands PA2.0-2.4 PB1.0-1.2 PC1.9-2.5; TI table10-1 rated45uF example'
ft=foot('GW_C3225_TDK_REFLOW',[pad(1,-1.65,0,1.1,2.5),pad(2,1.65,0,1.1,2.5)],src,
    'Selected PA2.20 gap/PB1.10 padlength/PC2.50 height, no generic1210 default; 16V output only.')
symbol('C3225X7R1C156M250AB',two,ft,src,'TDK','15uF20%16VX7R',['B3_COUT','B5_COUT'],'PASSIVE',note='3 per buck:45uF rated per TI1MHz example. Prototype load-step/ripple confirmation pending; do not connect to24V input.')

# Preserve the exact manufacturer land pattern as an alternate. This additional
# version changes only the ground land height, explicitly for the1oz green process.
nf=copy.deepcopy(unwrap(O/'original_GW_NIS3071_510CM_ONSEMI.json')['component'])
nf['name']='GW_NIS3071_510CM_PROTO';nf.pop('guid',None);nf.pop('primitive_order',None)
for p in nf['pads']:
    for k in ['raw_tail','guid','identity_guid','identity_guid_b','unique_id']:p.pop(k,None)
    p['solder_mask_expansion_mode']='manual';p['solder_mask_expansion']=.025
    p['paste_mask_expansion_mode']='manual';p['paste_mask_expansion']=0
    if p['designator']=='EP':p['height']=4.58;p['paste_mask_expansion']=-2.0
nf['fills']=[dict(layer='Top Paste',x1=x-.55,y1=y-.9,x2=x+.55,y2=y+.9) for x in [-.65,.65] for y in [-1.,1.]]
nf['description']='NIS3071 CASE510CM reference perimeter pads. Prototype DFM variant: groundEP2.85x4.58 instead4.75; coppergap.160,maskbridge.110 with+.025mask. Four1.10x1.80paste windows60.7%. Max bodyEP4.65 overhangs land.035 each end;98.5% overlap. Engineering choice, not manufacturer-exact land.'
fps.append(nf)
asset('NIS3071MT4TWG','NIS3071MT4TWG',nf['name'],'onsemi Apr2026 table1/CASE510CM; explicit prototypeDFM variant',['ACTIVE_NIS3071MT4TWG'],'ACTIVE',
    note='Pins1..16 plusEP ground unchanged. EP height reduced to4.58 for.16 clearance; original exact pattern retained alternate. Native compile and functional test pending.')
asset('SS3P6L-M3/86A','SS3P6L-M3_86A','GW_SS3P6L_VISHAY_88987','Vishay88987pp1,4; corrected1/2anodes andKcathode',['IN_REVERSE','IN_SOUT'],note='Approved series part. IN_SOUT footprint is DNP; same part not guaranteed to clampOUT above-.3V at all fault currents.')

for n,v in [('footprints.json',fps),('symbols.json',syms),('cad_assets.json',assets)]:
    (O/n).write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'new_symbols':len(syms),'new_footprints':len(fps),'assets':len(assets)}))
