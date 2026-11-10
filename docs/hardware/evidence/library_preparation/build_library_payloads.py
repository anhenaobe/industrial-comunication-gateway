"""Prepare official file-library API payloads; does not write binary libraries.

Native lib_add_pins failed on CurrentPartID. Reuse the saved official-reader
snapshot for glyphs, replace inherited identities, and emit explicit primitives.
"""
import copy
import csv
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).parent
LIB='hardware/academic_rev1/libraries/'
inputs=json.loads((OUT/'model_inputs.json').read_text())
sources=json.loads((OUT/'source_models_readback.json').read_text())
bom=list(csv.DictReader((OUT/'passive_bom_before.csv').open(encoding='utf-8-sig')))


def clean(value):
    if isinstance(value,dict):
        return {k:clean(v) for k,v in value.items() if k not in {
            'raw_params','header_params','unique_id','designator_unique_id',
            'primitive_order','guid','identity_guid','identity_guid_b',
            'source_library_name','target_file_name','all_pin_count',
            'extra_streams','stream_name'}}
    if isinstance(value,list):
        return [clean(v) for v in value]
    return value


def params(values):
    return [dict(name=k,value=str(v).replace('|','/'),hidden=True,x=0,y=0)
            for k,v in values.items()]


symbols=[]
assets=[]
for i,m in enumerate(inputs['active_models']):
    blocked=m['mpn']=='BSP75NTA'
    pins=[]
    for p in m['pins']:
        left=p['x']<0
        pins.append(dict(designator=p['designator'],name=p['name'],
                         electrical_type=p['electrical_type'],
                         x=-80 if left else 80,y=p['y']//10,length=20,
                         orientation='left' if left else 'right'))
    refs=[dict(name=m['footprint'],is_current=True)] if m['footprint'] else []
    if m['mpn']=='LMR36015FBRNXR':
        refs.append(dict(name='GW_RNX0012B_TI',is_current=False))
    status='CAD_BLOCKED' if blocked else 'CAD_CANDIDATE'
    s=dict(name=m['symbol'],description=(m['mpn']+'; '+status+'; '+m['notes'])[:256],
           designator='U?',designator_x=-80,designator_y=m['rectangle']['y2']/10+10,
           pins=pins,rectangles=[{k:v/10 for k,v in m['rectangle'].items()}],
           footprints=refs,parameters=params({
               'Manufacturer':m['manufacturer'],'Manufacturer Part Number':m['mpn'],
               'Value':m['mpn'],'Comment':m['mpn'],'CAD_Status':status,
               'Electrical_Status':'PROVISIONAL','CAD_Source':m['source'],
               'CAD_Limitations':m['notes'] or 'Circuit not electrically released.'}))
    symbols.append(s)
    assets.append(dict(asset_id='ACTIVE_'+m['mpn'].replace('-','_'),item_kind='ACTIVE',
                       component_ids=['ACTIVE_'+m['mpn'].replace('-','_')],mpn=m['mpn'],
                       symbol=s['name'],footprint=m['footprint'] or 'MISSING',
                       source=m['source'],cad_status=status,
                       symbol_status='CAD_BLOCKED' if blocked else 'CAD_CANDIDATE',
                       footprint_status='CAD_BLOCKED' if blocked else 'CAD_CANDIDATE',
                       limitations=m['notes'],package_requirement=m['footprint'] or 'BSP75NTA_SOT223_DN_NUMBERING_BLOCKED'))

# Exact specification keys, NOT quantities, define reusable symbols.
groups={}
for r in bom:
    groups.setdefault(r['specification_key'],[]).append(r)
reused_footprints=set()
for key,rr in groups.items():
    r=rr[0]
    mpn=r['recommended_mpn']
    glyph=r['symbol']
    footprint=r['footprint']
    kind=r['item_kind']
    # No guessed clock/magnetics/protection substitution.
    if any(x['component_id'] in {'ETH_Y25','ETH_CXTAL','ETH_TMAG','ETH_CCHASSIS','ETH_JRJ45','ETH_DESD','RS_TVS'} for x in rr):
        continue
    if mpn=='TBD' and kind!='AUXILIARY':
        continue
    if glyph=='MISSING' and kind=='PASSIVE':
        if mpn.startswith('XAL'):
            glyph='Inductor_10uH_4A_7.2*6.6mm'
        elif mpn.startswith(('C5750','C3225')):
            glyph='Cap_0.1uF_0603_50V'
        else:
            continue
        footprint='MISSING'
    if glyph not in sources:
        continue
    digest=hashlib.sha256(key.encode()).hexdigest()[:8]
    name=('GW_'+(mpn if mpn!='TBD' else glyph)+'_'+digest).replace('/','_').replace('*','x')
    s=clean(copy.deepcopy(sources[glyph]))
    s['name']=name
    s['description']=(mpn+'; '+r['nominal_value']+'; '+r['rated_voltage_or_current']+'; CAD_CANDIDATE')[:256]
    prefix='R' if glyph.startswith('Res_') else 'C' if glyph.startswith('Cap_') else 'L' if glyph.startswith('Inductor_') else 'FB' if glyph.startswith('FB_') else 'SW' if glyph.startswith('Sw_') else 'J'
    s['designator']=prefix+'?'
    if mpn.startswith(('C0603','C0805')):
        manufacturer='KEMET'
    elif mpn.startswith('CL'):
        manufacturer='Samsung Electro-Mechanics'
    elif mpn.startswith('RC'):
        manufacturer='Yageo'
    elif mpn.startswith('FRC'):
        manufacturer='FOJAN'
    elif mpn.startswith('CRCW'):
        manufacturer='Vishay'
    elif mpn.startswith('XAL'):
        manufacturer='Coilcraft'
    elif mpn.startswith(('C5750','C3225')):
        manufacturer='TDK'
    else:
        manufacturer='UNVERIFIED; see original candidate BOM'
    limitation='Glyph pins/types inspected; exact manufacturer land-pattern/mask/paste qualification pending.'
    if footprint=='MISSING':
        limitation='Symbol only. Exact manufacturer land pattern absent locally; footprint blocked. Ratings copied from provisional BOM, not newly approved.'
    if footprint=='CON_2x1_TH_5MM':
        limitation='Professor pads have Y offset 0.127mm: pin1 y=.254, pin2 y=.127. Exact JL126 drawing required; footprint retained as explicitly unverified candidate.'
    if footprint=='Sw_PUSH_4.5x4.5x5mm':
        limitation='Footprint unfinished: paired pads 1/1 and 2/2 in professor source are rejected by official writer duplicate-designator validation. Exact switch MPN/terminal-pairing drawing and native copy verification required. No pad renumbering invented.'
        footprint='MISSING'
    s['parameters']=params({'Manufacturer':manufacturer,'Manufacturer Part Number':mpn,
        'Value':r['nominal_value'],'Comment':r['nominal_value'],'Tolerance':r['tolerance'],
        'Rating':r['rated_voltage_or_current'],'Power Rating':r['power_rating'],
        'Package':r['package'],'CAD_Status':'CAD_CANDIDATE' if footprint!='MISSING' else 'CAD_BLOCKED',
        'Electrical_Status':'PROVISIONAL','CAD_Source':'Professor_shared.SchLib glyph '+glyph,
        'CAD_Limitations':limitation,'Electrical_Notes':r['observations']})
    s['footprints']=[] if footprint=='MISSING' else [dict(name='GW_CAND_'+footprint,is_current=True)]
    symbols.append(s)
    if footprint!='MISSING':
        reused_footprints.add(footprint)
    assets.append(dict(asset_id='SPEC_'+digest,item_kind=kind,component_ids=[x['component_id'] for x in rr],
        mpn=mpn,specification_key=key,symbol=name,
        footprint='MISSING' if footprint=='MISSING' else 'GW_CAND_'+footprint,
        source='Professor_shared.SchLib:'+glyph+'; '+r['electrical_value_source'],
        cad_status='CAD_CANDIDATE' if footprint!='MISSING' else 'CAD_BLOCKED',
        symbol_status='CAD_CANDIDATE',footprint_status='CAD_CANDIDATE' if footprint!='MISSING' else 'CAD_BLOCKED',
        limitations=limitation,package_requirement='GW_CAND_'+footprint if footprint!='MISSING' else r['package']))

footprints=[]
for f in inputs['footprints']:
    pads=[]
    for p in f['pads']:
        p=copy.deepcopy(p)
        if p['shape']=='roundrect':
            p['shape']='rounded_rectangle'
            p['corner_radius_percent']=round(p.pop('corner_radius'))
        else:
            p.pop('corner_radius',None)
        pads.append(p)
    w,h=f['body']
    # Body projection on mechanical layer; no ambiguous copper outline.
    pts=[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
    tracks=[dict(x1=a[0],y1=a[1],x2=b[0],y2=b[1],width=.1,layer='Mechanical 1') for a,b in zip(pts,pts[1:]+pts[:1])]
    # Mark pad1 outside copper in silkscreen. Datum follows explicit pad1.
    p1=next(p for p in pads if p['designator']=='1')
    tracks.append(dict(x1=p1['x']-.2,y1=p1['y']+p1['height']/2+.3,
                       x2=p1['x']+.2,y2=p1['y']+p1['height']/2+.3,width=.1,layer='Top Overlay'))
    fills=[dict(x1=p['x']-p['width']/2,y1=p['y']-p['height']/2,
                x2=p['x']+p['width']/2,y2=p['y']+p['height']/2,layer='Top Paste') for p in f['paste_windows']]
    footprints.append(dict(name=f['name'],description=(f['source']+'; '+f['notes'])[:255],
                           pads=pads,tracks=tracks,fills=fills))
for name in sorted(reused_footprints):
    f=copy.deepcopy(sources[name])
    f['name']='GW_CAND_'+name
    f['description']='CAD_CANDIDATE; professor geometry inspected; exact MPN land/mask/paste unqualified. '+f.get('description','')
    footprints.append(f)

for name,value in [('symbols_payload.json',symbols),('footprints_payload.json',footprints),('cad_assets.json',assets)]:
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(symbols=len(symbols),footprints=len(footprints),active=8,assets=len(assets))))
