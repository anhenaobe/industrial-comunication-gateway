import json,hashlib,csv,re,subprocess
from pathlib import Path
from urllib.parse import unquote
O=Path(__file__).parent;D=O.parent.parent
load=lambda n:json.loads((O/n).read_text(encoding='utf-8'))
s=load('symbol_after.json')['component'];f=load('footprint_after.json')['component']
assert s['name']=='C1206C102KGRACAUTO' and s['footprints'][0]['name']==f['name']=='GW_C1206_KEMET_C1076_DENSITY_B'
assert [(p['designator'],p['electrical_type'],p['hidden']) for p in s['pins']]==[('1','passive',False),('2','passive',False)]
assert len(s.get('lines',[]))==2 and not s.get('rectangles')
for p,x in zip(f['pads'],[-1.5,1.5]):
 assert abs(p['x']-x)<2e-6 and p['y']==0
 assert abs(p['width']-1.15)<2e-6 and abs(p['height']-1.8)<2e-6
 assert p['shape']=='rectangle' and p['layer']=='Top Layer' and p.get('hole_size',0)==0
 assert p['solder_mask_expansion_mode']=='manual' and abs(p['solder_mask_expansion']-.05)<2e-6
 assert p['paste_mask_expansion_mode']=='manual' and p.get('paste_mask_expansion',0)==0
assert len(f['pads'])==2 and len(f['tracks'])==4
for n in ['validate_sch.json','validate_pcb.json']:
 v=load(n);assert v['error_count']==0 and v['warning_count']==0
for i,c in [(0,65),(1,36)]:
 d=load('diff_'+str(i)+'.json');assert d['summary']['unchanged_count']==c and not d['modified'] and not d['removed'] and len(d['added'])==1
def rows(path):return {r['component_id']:r for r in csv.DictReader(path.open(encoding='utf-8-sig'))}
old=rows(O/'before_passive_bom.csv');now=rows(D/'passive_bom.csv');assert old.keys()==now.keys()
for id,r in old.items():
 for key in r:
  if id!='ETH_CBOB':assert r[key]==now[id][key],(id,key)
 for key in ['recommended_mpn','quantity','assembly','nominal_value','tolerance','electrical_status']:assert r[key]==now[id][key],(id,key)
for name in ['passive_bom.csv','final_bom.csv','cad_library_mapping.csv']:
 r=rows(D/name)['ETH_CBOB'];assert r['quantity']=='2' and r['recommended_mpn']==s['name'] and r['symbol']==s['name'] and r['footprint']==f['name'] and r['lcsc_code']=='C600002' and r['cad_status']=='CAD_VERIFIED'
 assert Path(r['local_datasheet']).exists()
hashes=load('hashes_before.json');changed=[p for p,h in hashes.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
libs=[p for p in changed if Path(p).suffix.lower() in ['.schlib','.pcblib','.intlib','.libpkg']]
assert {Path(p).name for p in libs}=={'Gateway_Academic.SchLib','Gateway_Academic.PcbLib'},libs
external=[p for p in changed if p not in libs]
for p in external:assert Path(p).suffix.lower() in ['.schdoc','.prjpcb','.pcbdoc']
guide=(D/'schematic_construction_guide.md').read_text(encoding='utf-8')
oldguide=(D/'evidence/construction_sync/before_schematic_construction_guide.md').read_text(encoding='utf-8')
def table(t):return t.split('## 6.')[1].split('### D. Connection checklist')[1].split('### E.')[0]
assert table(guide)==table(oldguide)
links=0
for name in ['schematic_construction_guide.md','ethernet_1nf_library_closure.md']:
 for target in re.findall(r'\]\(([^)]+)\)',(D/name).read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  assert (D/unquote(target.split('#')[0]).strip('<>')).exists(),target;links+=1
for a in load('source_manifest.json'):assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
diff=subprocess.run(['git','diff','--check'],capture_output=True,text=True);assert diff.returncode==0
status=subprocess.run(['git','status','--short'],capture_output=True,text=True)
result=dict(passed=True,symbol=s['name'],footprint=f['name'],BOM_quantity=2,library_counts=[66,37],previous_objects_unchanged=[65,36],
 native_compilation='NOT_RUN; stale IntLib',native_design_writes_issued=False,other_library_hashes_preserved=True,
 external_native_changes_observed=external,unrelated_BOM_rows_preserved=True,electrical_approval_unchanged=True,termination_topology_preserved=True,
 local_links_checked=links,git_diff_check=0,git_status=status.stdout)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='git_status'},indent=2))
