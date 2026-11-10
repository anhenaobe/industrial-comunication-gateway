"""Validate saved CAD evidence, selected BOM changes and preserved engineering files."""
import csv,hashlib,json,subprocess
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path.cwd();DOC=ROOT/'docs/hardware';OUT=Path(__file__).parent
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def data(result):
    assert not result.get('isError'),result
    return result.get('structuredContent') or json.loads(result['content'][0]['text'])
before=read('hashes_before.json')
allowed={str(ROOT/'hardware/academic_rev1/libraries'/n) for n in
         ['Gateway_Academic.SchLib','Gateway_Academic.PcbLib','Project Outputs for Gateway_Academic/Gateway_Academic.IntLib']}
after={p:sha(p) for p in before}
changed={p:dict(before=before[p],after=after[p]) for p in before if before[p]!=after[p]}
assert set(changed)<=allowed,changed
assert len(changed)==3,changed

diff=read('final_library_diffs.json')
for ext,added,unchanged in [('SchLib',9,37),('PcbLib',8,15)]:
    s=data(diff[ext])['summary']
    assert s['added_count']==added and s['unchanged_count']==unchanged
    assert s['modified_count']==s['removed_count']==0
for r in read('final_library_validation.json'):
    assert r['status']=='fulfilled'
    d=data(r['value']);assert d['error_count']==d['warning_count']==0

components={}
for r in read('saved_component_readback.json'):
    assert r['result']['status']=='fulfilled'
    d=data(r['result']['value']);components[(r['extension'],r['name'])]=d['component']
mm=read('final_native_results.json')['MMreadback']
for i,r in enumerate(mm):
    assert r['status']=='fulfilled'
    d=data(r['value']);components[('SchLib' if i==0 else 'PcbLib',d['component_name'])]=d['component']
last=read('final_compilation.json')
r=data(last['R10Kreadback']);components[('SchLib',r['component_name'])]=r['component']
for ext,filename,primitive in [('SchLib','symbols_additions.json','pins'),('PcbLib','footprints_additions.json','pads')]:
    for expected in read(filename):
        actual=components[(ext,expected['name'])]
        e={p['designator']:p for p in expected[primitive]};a={p['designator']:p for p in actual[primitive]}
        assert e.keys()==a.keys(),expected['name']
        for num,p in e.items():
            for key in ['x','y','width','height','hole_size','length']:
                if key in p:assert abs(p[key]-a[num].get(key,0))<.00002,(expected['name'],num,key)
            for key in ['name','electrical_type','orientation','layer','is_plated']:
                if key in p:assert p[key]==a[num][key],(expected['name'],num,key)
        if ext=='SchLib':
            assert [(x['name'],x['is_current']) for x in expected['footprints']]==[(x['name'],x['is_current']) for x in actual['footprints']]
            pars={x['name']:x['value'] for x in actual['parameters']}
            assert pars['Manufacturer Part Number']==expected['name']

compiled=read('compiled_source_extraction.json')
assert sha(compiled['intlib'])==compiled['sha256']
assert all(x['matches_current_source_bytes'] and sha(x['path'])==x['sha256'] for x in compiled['embedded'])
inventory=read('compiled_inventory.json')
sch=data(inventory['SchLib']);pcb=data(inventory['PcbLib'])
assert sch['total_count']==46 and pcb['total_count']==23
unlinked=[x['name'] for x in sch['components'] if x['footprint_count']==0]
assert len(unlinked)==6
messages=data(last['messages'])
assert messages['count']==6 and all(x['severity']=='Warning' and x['message']=='Missing Component Models' and not x['suppressed'] for x in messages['messages'])
assert data(last['detach'])['engine_release_confirmed']

with (DOC/'passive_bom.csv').open(encoding='utf-8-sig',newline='') as f:bom=list(csv.DictReader(f))
with (DOC/'cad_library_mapping.csv').open(encoding='utf-8-sig',newline='') as f:mapping=list(csv.DictReader(f))
with (DOC/'final_bom.csv').open(encoding='utf-8-sig',newline='') as f:final=list(csv.DictReader(f))
assert len(bom)==114 and len(mapping)==122 and len(final)==122
assert len({r['component_id'] for r in final})==122
active=[r for r in final if r['item_kind']=='ACTIVE']
assert len(active)==8 and sum(int(r['quantity']) for r in active)==10
assert all(r['quantity']=='' for r in mapping if r['item_kind']=='ACTIVE')
byid={r['component_id']:r for r in bom}
assert byid['ETH_JRJ45']['recommended_mpn']=='SS-7188S-A-NF'
assert byid['ETH_TMAG']['recommended_mpn']=='HX1188FNL'
assert byid['ETH_CCT']['quantity']=='4' and byid['ETH_RBOB']['quantity']=='4' and byid['ETH_CBOB']['quantity']=='2'
assert all(byid[x]['quantity']=='0' and byid[x]['assembly']=='DNP' for x in ['MCU_CHSE','MCU_RHSE','ETH_CXTAL','ETH_RXTAL','CAN_TVS','CAN_CMC','CAN_CBUS','CAN_RSPLIT','CAN_CSPLIT'])
assert all(byid[x]['recommended_mpn']=='RC0603FR-0710KL' and byid[x]['symbol']=='RC0603FR-0710KL' for x in ['MCU_RBOOT','RS_RDE','RS_RRE','DO_RPDA','DO_RPDB'])
assert all(byid[x]['quantity']=='' and byid[x]['electrical_status']=='ELECTRICAL_BLOCKED' for x in ['B3_CIN','B5_CIN','IN_BULK'])
assert byid['DI_RTHR1']['recommended_mpn']==byid['DI_RTHR2']['recommended_mpn']=='MM204F1K00TKRTR3K0'
assert all(byid[x]['item_kind']=='AUXILIARY' for x in ['MCU_YHSE','ETH_Y25','ETH_TMAG'])

paths=[DOC/n for n in ['passive_bom.csv','cad_library_mapping.csv','final_bom.csv','passive_component_selection.md']]
stable={str(p):sha(p) for p in paths}
regen=subprocess.run(['C:/dev/tools/python/python.exe',str(DOC/'evidence/build_passive_deliverables.py')],cwd=ROOT,capture_output=True,text=True)
assert regen.returncode==0,regen.stderr
assert stable=={str(p):sha(p) for p in paths},'Regeneration changed reviewed artifacts'
for p in paths+[DOC/'schematic_readiness_gate.md',DOC/'manufacturer_layout_guidelines.md']:
    text=p.read_text(encoding='utf-8-sig');assert '\ufffd' not in text
    assert all(line==line.rstrip() for line in text.splitlines()),p
    assert text.endswith('\n')
check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
assert check.returncode==0,check.stdout+check.stderr
status=subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True,check=True)
(OUT/'git_status_after.txt').write_text(status.stdout,encoding='utf-8')
result=dict(status='PASS',checked_at_utc=datetime.now(timezone.utc).isoformat(),
    protected_files=len(before),unchanged_protected_files=len(before)-len(changed),intended_changed_native_files=changed,
    revA_academic_sheet_board_and_firmware_preserved=True,original_library_objects_unchanged=True,
    authored_symbol_readbacks=9,authored_footprint_readbacks=8,geometry_tolerance_mm=.00002,
    compiled_source_byte_identity=True,compiled_symbol_count=46,compiled_footprint_count=23,
    compiler_warnings=messages['messages'],unlinked_retained_symbols=unlinked,
    bom_rows=114,mapping_rows=122,final_bom_rows=122,active_specifications=8,active_units=10,
    generator_idempotent=True,git_diff_check_exit_code=check.returncode,git_diff_check_output=check.stdout+check.stderr,
    native_engine_released=True,limitations=['No full schematic, ERC/DRC, routed board, thermal/loop test or industrial compliance test',
      'BSP numbered map and loaded protection drive blocked; buck effective-capacitance and input fault coordination blocked',
      'Source-backed CAD candidates still require mask/stencil, courtyard/height and fabrication qualification'])
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['intended_changed_native_files','compiler_warnings','git_diff_check_output']},indent=2))
