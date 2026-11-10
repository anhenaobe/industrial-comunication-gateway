import json,csv,hashlib,re,subprocess
from pathlib import Path
from urllib.parse import unquote
O=Path(__file__).parent;D=O.parent.parent
load=lambda n:json.loads((O/n).read_text(encoding='utf-8'))
s=load('symbol_after.json')['component'];f=load('footprint_after.json')['component']
assert s['name']=='CRCW080575R0FKEA'
assert [(p['designator'],p['name'],p['electrical_type'],p['hidden']) for p in s['pins']]==[('1','1','passive',False),('2','2','passive',False)]
assert s['footprints'][0]['name']==f['name']=='GW_CRCW0805_VISHAY_20035_REFLOW'
assert len(s['rectangles'])==1 and s['rectangles'][0]['x2']-s['rectangles'][0]['x1']==30
assert len(f['pads'])==2
for p,x in zip(f['pads'],[-.975,.975]):
 assert abs(p['x']-x)<2e-6 and abs(p['y'])<2e-6
 assert abs(p['width']-.95)<2e-6 and abs(p['height']-1.45)<2e-6
 assert p['shape']=='rectangle' and p['layer']=='Top Layer' and p.get('hole_size',0)==0
 assert abs(p['solder_mask_expansion']-.05)<2e-6 and p['solder_mask_expansion_mode']=='manual'
 assert p.get('paste_mask_expansion',0)==0 and p['paste_mask_expansion_mode']=='manual'
for i,count in [(0,64),(1,35)]:
 d=load('diff_'+str(i)+'.json');assert d['summary']['unchanged_count']==count and not d['modified'] and not d['removed'] and len(d['added'])==1
for n in ['validate_sch.json','validate_pcb.json']:
 v=load(n);assert v['error_count']==0 and v['warning_count']==0
hashes=load('hashes_before.json');changed=[p for p,h in hashes.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
library_changes=[p for p in changed if Path(p).suffix.lower() in ['.schlib','.pcblib']]
assert {Path(p).name for p in library_changes}=={'Gateway_Academic.SchLib','Gateway_Academic.PcbLib'}
external_changes=[p for p in changed if p not in library_changes]
assert set(external_changes)<={'hardware\\academic_rev1\\Ethernet.SchDoc','hardware\\academic_rev1\\MCU.SchDoc','hardware\\academic_rev1\\Power.SchDoc','hardware\\academic_rev1\\Industrial_Gateway_Academic.PrjPcb'},external_changes
def rows(p):return {r['component_id']:r for r in csv.DictReader(p.open(encoding='utf-8-sig'))}
old=rows(O/'before_passive_bom.csv');now=rows(D/'passive_bom.csv');assert old.keys()==now.keys()
for id,r in old.items():
 for key in r:
  if id!='ETH_RBOB':assert r[key]==now[id][key],(id,key)
 for key in ['recommended_mpn','quantity','assembly','nominal_value','tolerance']:
  assert r[key]==now[id][key],(id,key)
for file in ['passive_bom.csv','final_bom.csv','cad_library_mapping.csv']:
 r=rows(D/file)['ETH_RBOB'];assert r['quantity']=='4' and r['recommended_mpn']==s['name'] and r['symbol']==s['name'] and r['footprint']==f['name']
 assert r['lcsc_code']=='C844859' and r['cad_status']=='CAD_VERIFIED' and Path(r['local_datasheet']).exists()
for a in load('source_manifest.json'):assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
guide=(D/'schematic_construction_guide.md').read_text(encoding='utf-8')
before=(D/'evidence/construction_sync/before_schematic_construction_guide.md').read_text(encoding='utf-8')
def pins(t):return t.split('## 6.')[1].split('### D. Connection checklist')[1].split('### E.')[0]
assert pins(guide)==pins(before),'Ethernet connection topology changed'
links=0
for name in ['schematic_construction_guide.md','ethernet_75ohm_library_closure.md']:
 for target in re.findall(r'\]\(([^)]+)\)',(D/name).read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  assert (D/unquote(target.split('#')[0]).strip('<>')).exists(),target
  links+=1
diff=subprocess.run(['git','diff','--check'],capture_output=True,text=True);assert diff.returncode==0
status=subprocess.run(['git','status','--short'],capture_output=True,text=True)
result=dict(passed=True,source_inventory=[65,36],existing_objects_unchanged=[64,35],validation_errors=0,validation_warnings=0,
 resistor_positions=4,retained_mpn=s['name'],lcsc_code='C844859',native_compilation='NOT_RUN; existing IntLib stale',
 library_files_changed=library_changes,external_native_changes_observed=external_changes,
 schematic_or_project_write_operations_issued=False,professor_and_other_library_hashes_preserved=True,
 unrelated_BOM_rows_preserved=True,topology_preserved=True,local_links_checked=links,git_diff_check=0,git_status=status.stdout)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='git_status'},indent=2))
