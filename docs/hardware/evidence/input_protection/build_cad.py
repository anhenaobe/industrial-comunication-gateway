"""Source-dimensioned input protection candidates. No binary CAD writes here."""
import json,shutil,hashlib
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path.cwd(); OUT=Path(__file__).parent
LIB=ROOT/'hardware/academic_rev1/libraries'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=OUT/'library_backup.json'
if not manifest.exists():
    backup=LIB/'backups'/('input_protection_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    backup.mkdir(parents=True)
    data=[]
    for n in ['Gateway_Academic.SchLib','Gateway_Academic.PcbLib','Gateway_Academic.LibPkg']:
        src=LIB/n; dst=backup/n;shutil.copy2(src,dst)
        data.append(dict(source=str(src),backup=str(dst),sha256=sha(src)))
    manifest.write_text(json.dumps(data,indent=2)+'\n')
footprints=[];symbols=[];assets=[]
def pad(n,x,y,w,h):
    return dict(designator=str(n),x=x,y=y,width=w,height=h,shape='rectangle',
                rotation=0,layer='Top Layer',hole_size=0,is_plated=False,
                solder_mask_expansion_mode='none',paste_mask_expansion_mode='none')
def body(w,h):
    # Mechanical body and pin-one marker are documentation, not a courtyard rule.
    pts=[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2),(-w/2,-h/2)]
    return [dict(x1=a,y1=b,x2=c,y2=d,width=.05,layer='Mechanical 1')
            for (a,b),(c,d) in zip(pts,pts[1:])]
def fp(name,pads,source,notes,w,h):
    footprints.append(dict(name=name,pads=pads,tracks=body(w,h),description=(source+'; '+notes)[:500]))
def sym(name,pins,footprint,manufacturer,source,pdf,status,notes,prefix='U'):
    half=(len(pins)+1)//2;ps=[]
    for i,(num,label,typ) in enumerate(pins):
        left=i<half; row=i if left else i-half
        ps.append(dict(designator=str(num),name=label,electrical_type=typ,
                       x=-80 if left else 80,y=20*(half-1-row),length=20,
                       orientation='left' if left else 'right',hidden=False))
    parameters={'Manufacturer':manufacturer,'Manufacturer Part Number':name,
                'Source':source,'Datasheet':pdf or 'https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1','CAD Status':'CAD_CANDIDATE' if footprint else 'CAD_BLOCKED',
                'Electrical Approval':status,'Limitations':notes}
    symbols.append(dict(name=name,designator=prefix+'?',description=(source+'; '+notes)[:500],
                        pins=ps,rectangles=[dict(x1=-80,y1=-10,x2=80,y2=20*half)],
                        footprints=[dict(name=footprint,is_current=True)] if footprint else [],
                        parameters=[dict(name=k,value=v,hidden=True,x=0,y=0) for k,v in parameters.items()]))
    assets.append(dict(mpn=name,symbol=name,footprint=footprint,manufacturer=manufacturer,
                       source=source,local_pdf=pdf,electrical_status=status,
                       cad_status='CAD_CANDIDATE' if footprint else 'CAD_BLOCKED',limitations=notes,
                       pin_map={str(n):{'function':label,'type':typ,'pad':str(n) if footprint else None} for n,label,typ in pins}))

source='Semtech TDS3011P Rev2.0 16-Jun-2021 pp5-7; p6 reference land pattern'
name='GW_TDS3011P_SEMTECH'
fp(name,[pad(1,-.5,-.725,.30,.65),pad(2,0,-.725,.30,.65),pad(3,.5,-.725,.30,.65),
         pad(4,.5,.725,.30,.65),pad(5,0,.725,.30,.65),pad(6,-.5,.725,.30,.65)],
   source,'Top view rotated to Fig3 p5: bottom1/2/3 GND, top6/5/4 IN. Pitch .5; innergap .8; extent2.1; rowcenters1.45. Mask/stencil DFM pending.',1.6,1.6)
sym('TDS3011P.C',[(i,'GND' if i<4 else 'IN','passive') for i in range(1,7)],name,'Semtech',source,
    'sources/input_protection/TDS3011P.pdf','PROPOSED_FOR_REUSE',
    'All six pins must connect. 30V working limit; source tolerance, hot leakage and transient coordination not approved. Manufacturer reference copper; mask/paste DFM pending.',prefix='D')

source='onsemi NIS3071/D Rev3 Apr2026 table1 p2; CASE510CM 98AON08122H IssueO p12'
name='GW_NIS3071_510CM_ONSEMI'
p=[]
for i,y in enumerate([1.575,.525,-.525,-1.575]):p.append(pad(i+1,-2.295,y,.71,.35))
for i,x in enumerate([-1.575,-.525,.525,1.575]):p.append(pad(i+5,x,-2.8,.52,.70))
for i,y in enumerate([-1.575,-.525,.525,1.575]):p.append(pad(i+9,2.295,y,.71,.35))
for i,x in enumerate([1.575,.525,-.525,-1.575]):p.append(pad(i+13,x,2.8,.52,.70))
p.append(pad('EP',0,0,2.85,4.75))
fp(name,p,source,'Top-view CCW1..16; side .71x.35; ends .52x.70; pitch1.05; extents5.30x6.30. EP2.85x4.75 is GND; EP is project identifier for unnumbered PAD. Stencil/vias/thermal design pending.',5,6)
pins=[(1,'OUT1','power'),(2,'IN1','power'),(3,'IN2','power'),(4,'OUT2','power'),
      (5,'FAULT_N','open_collector'),(6,'dvdt','passive'),(7,'ILIM','passive'),(8,'GND','power'),
      (9,'OUT4','power'),(10,'IN4','power'),(11,'IN3','power'),(12,'OUT3','power'),
      (13,'EN4','input'),(14,'EN3','input'),(15,'EN2','input'),(16,'EN1','input'),('EP','GND_PAD','power')]
sym('NIS3071MT4TWG',pins,name,'onsemi',source,'sources/input_protection/NIS3071-D.PDF','PROPOSED_FOR_REUSE',
    'MT4 Auto-Retry, one channel proposed. EP maps datasheet unnumbered PAD, not invented pin17. Unused IN2/3/4 and EN2/3/4 toGND; OUT2/3/4 unconnected. 43.2k is historical curve-based candidate. EP paste and thermal vias not assembly-qualified.')

source='Vishay88987 Rev24-Apr-2020 pp1,4; numbered anodes1/2, cathodeK; minimum mounting lands'
name='GW_SS3P6L_VISHAY_88987'
fp(name,[pad('K',0,0,4.80,4.72),pad(1,1.22,-3.805,1.40,1.27),pad(2,-1.22,-3.805,1.40,1.27)],
   source,'K large upper pad,1 lower right,2 lower left in package-view orientation. Small-pad gap1.04; overallheight6.80. OriginK center. Board thermal copper and stencil pending. Reject supplied VIS mapping.',4.6,6.1)
# Manufacturer specifies copper lands, but no body-to-land registration datum.
# Omit a guessed centered body outline on this asymmetric pattern.
footprints[-1]['tracks']=[]
sym('SS3P6L-M3/86A',[(1,'ANODE1','passive'),(2,'ANODE2','passive'),('K','CATHODE','passive')],name,
    'Vishay',source,'sources/SS3P6L_88987.pdf','PROPOSED_FOR_REUSE',
    'Exact suffix from existing source parameters. Manufacturer terminalK retained as padK; no inherited provider1/2/3 map. Both anodes connect input; cathode protected rail. Source/cable reverse envelope and hot loss pending.',prefix='D')

# Independently valid two-terminal symbol. Do not invent the missing land drawing.
sym('0451002.MRL',[(1,'END1','passive'),(2,'END2','passive')],None,'Littelfuse',
    'Official451/453 series Rev01-Dec-2025 pp1-4; electrical row002 and ordering',
    '', 'PENDING_USER_APPROVAL',
    '2A125VDC fast fuse candidate. End1/2 are project labels for nonpolar terminals. Official PDF download denied403; footprint blocked pending readable recommended pad-layout drawing. Supply fault, derating, inrush and coordination pending.',prefix='F')

# Altium stream names cannot contain slash; keep the exact MPN in parameters.
for s in symbols:
    if s['name']=='SS3P6L-M3/86A':s['name']='SS3P6L-M3_86A'
for a in assets:
    if a['mpn']=='SS3P6L-M3/86A':a['symbol']='SS3P6L-M3_86A'
for n,data in [('footprints_additions.json',footprints),('symbols_additions.json',symbols),('cad_assets.json',assets)]:
    (OUT/n).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'symbols':len(symbols),'footprints':len(footprints),'backup':json.loads(manifest.read_text())[0]['backup']}))
