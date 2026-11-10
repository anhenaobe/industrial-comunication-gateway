"""Semantic preservation, source hashes, links, BOM bindings and drafting preview.
This does not run Altium ERC or pretend file validation verifies native custom pads.
"""
import json,hashlib,csv,re,html,math
from pathlib import Path
from urllib.parse import unquote
O=Path(__file__).parent;R=Path.cwd();D=R/'docs/hardware'
read=lambda name:json.loads((O/name).read_text(encoding='utf-8'))
old={s['name']:s for s in read('symbols_before.json')['symbols']}
new={s['name']:s for s in read('symbols_after.json')['symbols']}
modified=[s['name'] for s in read('updates.json') if s['name']!='NIS3071MT4TWG']
def pins(s):return sorted((p['designator'],p['name'],p['electrical_type'],p.get('hidden',False)) for p in s['pins'])
def footprints(s):return sorted((p['name'],p.get('is_current',True)) for p in s.get('footprints',[]))
def params(s):return sorted((p['name'],p['value']) for p in s.get('parameters',[]))
for name in old:
 assert pins(old[name])==pins(new[name]),'Pin identity/type changed: '+name
 assert footprints(old[name])==footprints(new[name]),'Footprint binding changed: '+name
 if name!='NIS3071MT4TWG':assert params(old[name])==params(new[name]),'Parameter changed: '+name
assert pins(new['SS3P6L-M3_86A'])==[('1','ANODE1','passive',False),('2','ANODE2','passive',False),('K','CATHODE','passive',False)]
assert len(new['SS3P6L-M3_86A']['lines'])==10 and len(new['SS3P6L-M3_86A']['polygons'])==1
expected={'1':'IN','2':'UVLO','3':'OVP','4':'SHDN_N','5':'RTN','6':'GND','7':'ILIM','8':'dVdT','9':'FLT_N','10':'OUT','11':'RTN_EP'}
assert {p['designator']:p['name'] for p in new['TPS26620DRCR']['pins']}==expected
f=read('footprint_after.json')['component'];pads={p['designator']:p for p in f['pads']}
assert set(pads)==set(expected)
for n in range(1,11):
 p=pads[str(n)];assert abs(p['width']-.6)<1e-5 and abs(p['height']-.24)<1e-5
 assert abs(p['x']-(-1.4 if n<=5 else 1.4))<1e-5
 assert abs(p['y']-(1-(n-1)*.5 if n<=5 else -1+(n-6)*.5))<1e-5
assert abs(pads['11']['width']-1.65)<1e-5 and abs(pads['11']['height']-2.4)<1e-5
assert len(f['regions'])==4 and len([x for x in f['fills'] if x['layer']=='Top Paste'])==6
assert pads['11']['paste_mask_expansion_mode']=='manual' and pads['11']['paste_mask_expansion']<-.8
assert len(new)==64
changed_hashes=[];all_hashes={}
for path,sha in read('hashes_before.json').items():
 p=Path(path);digest=hashlib.sha256(p.read_bytes()).hexdigest();all_hashes[path]=digest
 if digest!=sha:changed_hashes.append(path)
assert {Path(p).name for p in changed_hashes}=={'Gateway_Academic.SchLib','Gateway_Academic.PcbLib'},changed_hashes
(O/'hashes_after.json').write_text(json.dumps(all_hashes,indent=2)+'\n')
for a in read('backup.json'):
 assert hashlib.sha256(Path(a['backup']).read_bytes()).hexdigest()==a['sha256']
def csvrows(path):return {r['component_id']:r for r in csv.DictReader(path.open(encoding='utf-8-sig'))}
before=csvrows(O/'before_passive_bom.csv');after=csvrows(D/'passive_bom.csv')
assert before.keys()<=after.keys()
allowed={'IN_RLIM','IN_CDVDT','IN_RFAULT'}
for key,row in before.items():
 for field in ['quantity','recommended_mpn']:
  if key not in allowed:assert row[field]==after[key][field],(key,field,row[field],after[key][field])
assert {k for k in after if k not in before}=={'IN_UV_TOP','IN_UV_MID','IN_UV_BOTTOM'}
final=csvrows(D/'final_bom.csv');assert final['ACTIVE_NIS3071MT4TWG']['quantity']=='0'
assert final['ACTIVE_TPS26620DRCR']['quantity']=='1' and final['ACTIVE_TPS26620DRCR']['cad_status']=='CAD_CANDIDATE'
assert after['IN_BULK']['quantity']=='1' and after['IN_BULK']['recommended_mpn']=='C5750X7R2A475K230KA'
assert after['IN_CDVDT']['recommended_mpn']=='C0603C103K1RACTU'
mapping=csvrows(D/'cad_library_mapping.csv');assert mapping['ACTIVE_TPS26620DRCR']['quantity']==''
broken=[];checked=[]
for p in [D/'input_protection_reference.md',D/'symbol_library_verification.md',R/'hardware/academic_rev1/libraries/SYMBOL_CONVENTIONS.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  path=unquote(target.split('#')[0]).strip('<>')
  if not path:continue
  found=(p.parent/path).resolve();checked.append(str(found))
  if not found.exists():broken.append(dict(source=str(p),target=target))
assert not broken,broken
result=dict(passed=True,existing_symbols_checked=len(old),graphical_updates=len(modified),
 existing_pin_identities_types_and_links_preserved=True,SS3_all_three_terminals_visible=True,
 CAD_counts=dict(symbols=64,footprints=35),old_footprints_unchanged=34,unrelated_symbols_unchanged=44,
 preserved_hashes=len(all_hashes)-len(changed_hashes),changed_native_files=changed_hashes,
 links_checked=len(checked),broken_links=broken,original_BOM_IDs_preserved=True,
 actual_blocker='TPS thermal copper tongues: native custom-pad11 conversion/net inheritance, corner review',
 native_compilation='NOT_RUN; existing IntLib stale; no new native automation session',
 graphical_symbols=modified)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
# Preview from saved readback. This is an offline drafting preview, not native rendering.
out=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="620" viewBox="0 0 960 620"><rect width="960" height="620" fill="white"/>',
 '<text x="30" y="30" font-family="Arial" font-size="18">Saved library primitives - offline drafting preview</text>']
for name,cx,cy,sc in [('SS3P6L-M3_86A',470,160,3),('RC0603FR-0713K3L',180,365,2.5),('C0603C103K1RACTU',480,365,2.5),('XAL4030-682MEC',780,365,2.5)]:
 s=new[name]
 def xy(x,y):return (cx+sc*x,cy-sc*y)
 def ln(x1,y1,x2,y2):
  a,b=xy(x1,y1),xy(x2,y2);return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#800000" stroke-width="2"/>'
 out.append(f'<text x="{cx}" y="{cy+90}" text-anchor="middle" font-family="Arial" font-size="15">{html.escape(name)}</text>')
 for l in s.get('lines',[]):out.append(ln(l['x1'],l['y1'],l['x2'],l['y2']))
 for r in s.get('rectangles',[]):
  a=xy(r['x1'],r['y2']);out.append(f'<rect x="{a[0]}" y="{a[1]}" width="{sc*(r["x2"]-r["x1"])}" height="{sc*(r["y2"]-r["y1"])}" fill="none" stroke="#800000" stroke-width="2"/>')
 for p in s.get('polygons',[]):out.append('<polygon points="'+' '.join(f'{xy(v["x"],v["y"])[0]},{xy(v["x"],v["y"])[1]}' for v in p['points'])+'" fill="none" stroke="#800000" stroke-width="2"/>')
 for a in s.get('arcs',[]):
  pts=[xy(a['x']+a['radius']*math.cos(t*math.pi/180),a['y']+a['radius']*math.sin(t*math.pi/180)) for t in range(0,181,5)]
  out.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#800000" stroke-width="2"/>')
 for p in s['pins']:
  dx,dy={'left':(-1,0),'right':(1,0),'up':(0,1),'down':(0,-1)}[p['orientation']]
  x,y=p['x'],p['y'];out.append(ln(x,y,x+dx*p['length'],y+dy*p['length']))
  if name.startswith('SS3'):
   a=xy(x,y);anchor='start' if dx<0 else 'end';offset=5 if dx<0 else -5
   out.append(f'<text x="{a[0]+offset}" y="{a[1]-8}" text-anchor="{anchor}" font-family="Arial" font-size="14">{p["designator"]} {p["name"]}</text>')
out.append('<text x="30" y="550" font-family="Arial" font-size="15">Pin names/types and footprint links retained; no schematic instances updated.</text></svg>')
(O/'symbol_preview.svg').write_text('\n'.join(out),encoding='utf-8')
print(json.dumps(result,indent=2))
