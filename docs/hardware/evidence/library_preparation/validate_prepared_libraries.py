"""Validate saved official-reader snapshots and repository conservation.

This is structural/source-input roundtrip validation, not native placement,
manufacturer approval, ERC, electrical closure, or an IntLib compiler.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

OUT=Path(__file__).parent
ROOT=Path.cwd()
LIB=ROOT/'hardware/academic_rev1/libraries'
def read(name):
    return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
sch=read('destination_schlib_final.json')
pcb=read('destination_pcblib_final.json')
assert sch['status']==pcb['status']=='success'
assert not sch['has_more'] and not pcb['has_more']
symbols={s['name']:s for s in sch['symbols']}
footprints={f['name']:f for f in pcb['footprints']}
assert len(symbols)==37 and len(footprints)==15
expected_symbols=read('symbols_payload.json')
for want in expected_symbols:
    got=symbols[want['name']]
    assert {p['designator']:(p['name'],p['electrical_type']) for p in got['pins']}=={p['designator']:(p['name'],p['electrical_type']) for p in want['pins']},want['name']
    refs={f['name'] for f in got.get('footprints',[])}
    assert refs=={f['name'] for f in want.get('footprints',[])},want['name']
    assert refs<=footprints.keys(),want['name']
    actual_params={p['name']:p['value'] for p in got['parameters']}
    for p in want['parameters']:
        assert actual_params[p['name']]==p['value'],(want['name'],p['name'])
    if want['name'].startswith('GW_'):
        assert all('0603F104Z500CT' not in actual_params.get(k,'') for k in ['Manufacturer Part Number','Value','Comment'])
for want in read('footprints_payload.json'):
    got=footprints[want['name']]
    assert len(got['pads'])==len(want['pads'])
    assert len({p['designator'] for p in got['pads']})==len(got['pads'])
    pads={p['designator']:p for p in got['pads']}
    for p in want['pads']:
        actual=pads[p['designator']]
        for key in ['x','y','width','height','rotation']:
            assert abs(actual.get(key,0)-p.get(key,0))<.00002,(want['name'],p['designator'],key)
        assert actual.get('hole_size',0)==p.get('hole_size',0)
        assert actual['layer']==p['layer']
        if want['name'].startswith('GW_CAND_'):
            continue
        for key in ['solder_mask_expansion','paste_mask_expansion']:
            assert abs(actual.get(key,0)-p.get(key,0))<.00002,(want['name'],key)
            assert actual[key+'_mode']=='manual'
    assert len(got.get('fills',[]))==len(want.get('fills',[]))
    for actual,p in zip(got.get('fills',[]),want.get('fills',[])):
        assert actual['layer']=='Top Paste'
        for key in ['x1','x2','y1','y2']:
            assert abs(actual[key]-p[key])<.00002
assert not symbols['BSP75NTA'].get('footprints')
assert {p['designator'] for p in symbols['BSP75NTA']['pins']}=={'IN','D','S','S_TAB'}
assert {p['designator']:p['name'] for p in symbols['ISO1212DBQR']['pins']}['12']=='SUB2'
assert {p['designator']:p['name'] for p in symbols['ISO1212DBQR']['pins']}['13']=='SUB1'
assert {p['designator']:p['name'] for p in symbols['LMR36015FBRNXR']['pins']}['12']=='SW'

preserved={}
for item in read('source_hashes_before.json'):
    actual=hashlib.sha256(Path(item['Path']).read_bytes()).hexdigest()
    assert actual.upper()==item['Hash'].upper(),item['Path']
    preserved[item['Path']]=actual
bom=list(csv.DictReader((ROOT/'docs/hardware/passive_bom.csv').open(encoding='utf-8-sig')))
assets=read('cad_assets.json')
mandatory=[r for r in bom if r['item_kind']=='PASSIVE' and r['assembly']=='REQUIRED']
specs={r['specification_key']:r for r in mandatory}
assert len(specs)==26
package_requirements={r['package_requirement'] for r in mandatory if r['package_requirement_state']=='DEFINED'}
unresolved_requirements={r['package_requirement'] for r in mandatory if r['package_requirement_state']=='UNRESOLVED'}
active=[a for a in assets if a['item_kind']=='ACTIVE']
active_requirements={a['package_requirement'] for a in active}
all_requirements=package_requirements|active_requirements
covered_requirements={r['package_requirement'] for r in mandatory if r['footprint'] in footprints}|{a['package_requirement'] for a in active if a['footprint'] in footprints}
project=(ROOT/'hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb').read_text()
assert '.SchDoc' not in project and '.PcbDoc' not in project
assert 'DocumentPath=libraries\\Gateway_Academic.SchLib' in project
assert 'DocumentPath=libraries\\Gateway_Academic.PcbLib' in project
pkg=(LIB/'Gateway_Academic.LibPkg').read_text()
assert 'DocumentPath=Gateway_Academic.SchLib' in pkg and 'DocumentPath=Gateway_Academic.PcbLib' in pkg
assert not (LIB/'Gateway_Academic.IntLib').exists()
result=dict(status='PASS',symbol_count=len(symbols),footprint_count=len(footprints),
    active_specifications=8,active_candidate_pairs=7,active_unfinished=1,
    mandatory_passive_specifications=26,
    mandatory_symbol_candidates=sum(r['symbol'] in symbols for r in specs.values()),
    mandatory_footprint_candidates=sum(r['footprint'] in footprints for r in specs.values()),
    mandatory_package_requirements=len(package_requirements),
    unresolved_mandatory_requirement_groups=len(unresolved_requirements),
    active_package_requirements=len(active_requirements),
    mandatory_and_active_package_requirements=len(all_requirements),
    covered_package_requirements=len(covered_requirements),
    verified_package_requirements=0,conditional_passive_specifications=len({r['specification_key'] for r in bom if r['item_kind']=='PASSIVE' and r['assembly']=='CONDITIONAL'}),
    mandatory_package_requirement_inventory=sorted(package_requirements),
    asset_categories=dict(Counter(a['item_kind'] for a in assets)),
    preserved_sources=preserved,
    destination_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [LIB/'Gateway_Academic.SchLib',LIB/'Gateway_Academic.PcbLib',LIB/'Gateway_Academic.LibPkg']},
    native_close_reopen='PENDING',native_representative_placement='PENDING',
    compiler='NOT_RUN; native handler failure, then user requested computer released',
    intlib_exists=False,final_schematic_readiness='Conditional')
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'preserved_sources','destination_hashes','mandatory_package_requirement_inventory'}},indent=2))
