"""Structural checks for the documentation package; not an ERC or circuit test."""
import csv
import hashlib
import json
from pathlib import Path

root=Path.cwd()
hardware=root/'docs/hardware'
with (hardware/'passive_bom.csv').open(encoding='utf-8-sig',newline='') as f:
    bom=list(csv.DictReader(f))
with (hardware/'cad_library_mapping.csv').open(encoding='utf-8-sig',newline='') as f:
    mapping=list(csv.DictReader(f))
with (hardware/'library_inventory.csv').open(encoding='utf-8-sig',newline='') as f:
    inventory={r['referencia_cad']:r for r in csv.DictReader(f)}
closure_path=hardware/'evidence/electrical_closure/bom_decisions.json'
closure=json.loads(closure_path.read_text()) if closure_path.exists() else None
expected_bom=111+len(closure.get('new_rows',[])) if closure else 111
assert len(bom)==expected_bom and len(mapping)==expected_bom+8
active_mapping=[r for r in mapping if r['item_kind']=='ACTIVE']
passive_mapping=[r for r in mapping if r['item_kind']!='ACTIVE']
assert len(active_mapping)==8
assert len({r['component_id'] for r in active_mapping})==8
assert all(r['quantity']=='' for r in active_mapping)
assert len({r['component_id'] for r in bom})==len(bom)
assert [r['component_id'] for r in bom]==[r['component_id'] for r in passive_mapping]
states={'VERIFIED','CALCULATED','PROVISIONAL','MISSING','BLOCKED'}
cad_states={'CAD_VERIFIED','CAD_CANDIDATE','CAD_MISSING','CAD_BLOCKED'}
electrical_states={'ELECTRICAL_VERIFIED','DERIVED_PENDING_REVIEW','PROVISIONAL','ELECTRICAL_BLOCKED'}
for r,m in zip(bom,passive_mapping):
    assert r['verification_status'] in states
    assert r['electrical_status'] in electrical_states
    assert r['cad_status'] in cad_states
    assert r['symbol_status'] in cad_states and r['footprint_status'] in cad_states
    assert r['cad_status']==m['cad_status']
    assert r['electrical_status']==m['electrical_status']
    assert r['electrical_value_source']
    assert r['design_reference']=='UNASSIGNED'
    assert r['verification_status']!='VERIFIED'
    if r['quantity']:
        assert int(r['quantity'])>=0
    assert r['recommended_mpn']==m['recommended_mpn']
    assert r['symbol']==m['symbol'] and r['footprint']==m['footprint']
    if 'Professor_shared' in r['cad_origin']:
        assert (root/'hardware/academic_rev1/libraries/Professor_shared.SchLib').is_file()
        assert (root/'hardware/academic_rev1/libraries/Professor_shared.PcbLib').is_file()
        assert r['symbol'] in inventory
        assert r['footprint']==inventory[r['symbol']]['encapsulado_referencia_cad']
    if r['assembly']=='DNP':
        assert r['quantity']=='0'

# Preserve all original rows, quantities, MPNs and unapproved selections.
before=list(csv.DictReader((hardware/'evidence/library_preparation/passive_bom_before.csv').open(encoding='utf-8-sig')))
allowed={'symbol','footprint','cad_origin','cad_status','electrical_status'}
assert len(before)==111
for old,new in zip(before,bom):
    for key in old:
        closure_derived={'specification_key','electrical_status_original'} if closure else set()
        declared=set(closure['patches'].get(old['component_id'],{})) if closure else set()
        if key not in allowed|closure_derived|declared:
            assert old[key]==new[key],(old['component_id'],key)
    assert old['component_id']==new['component_id']
    if closure:
        for key,value in closure['patches'].get(old['component_id'],{}).items():
            # CAD fields and independent states are handled by the asset registry.
            if key not in {'electrical_status'}:
                assert new[key]==str(value),(old['component_id'],key,value,new[key])

counts=json.loads((hardware/'evidence/passive_selection_counts.json').read_text())
required=[r for r in bom if r['item_kind']=='PASSIVE' and r['assembly']=='REQUIRED']
assert sum(int(r['quantity']) for r in required if r['quantity'])==counts['required_known_units']==(78 if closure else 71)
assert sum(not r['quantity'] for r in required)==counts['required_unknown_quantity_groups']==(3 if closure else 4)
assert counts['teacher_candidate_required_units']+counts['external_required_known_units']==counts['required_known_units']

expected={
    'docs/industrial_gateway_requirements.md':'94cf02d2ffda0c162331bf360872836a6e84cea0d94c643ddbf0c56d39a1b4c6',
    'shared_lib (1).IntLib':'91594ede8aadf6449fff5b44b7443deafeb73cfaf0bc1eb1ff434d8ac1fb6159',
}
hashes={}
for name,digest in expected.items():
    hashes[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
    assert hashes[name]==digest
manifest=json.loads((root/'hardware/academic_rev1/libraries/library_manifest.json').read_text(encoding='utf-8-sig'))
for item in manifest:
    path=root/'hardware/academic_rev1/libraries'/item['file']
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual==item['sha256'],item['file']
    hashes[str(path.relative_to(root))]=actual

# Check new files explicitly: ordinary git diff omits untracked documentation.
files=[hardware/name for name in ['passive_component_selection.md','passive_bom.csv',
                                  'cad_library_mapping.csv','manufacturer_layout_guidelines.md']]
for file in files:
    text=file.read_text(encoding='utf-8-sig')
    assert '\ufffd' not in text
    assert all(line==line.rstrip() for line in text.splitlines()),file
    assert text.endswith('\n')
report=(hardware/'passive_component_selection.md').read_text(encoding='utf-8')
assert report.count('<!-- GENERATED_BOM_TABLES -->')==1
for sub in {r['subsystem'] for r in bom}:
    assert '### BOM '+sub in report
assert 'Mode los' not in report and 'mode los' not in report

result=dict(structural_checks='PASS', bom_groups=len(bom), mapping_groups=len(mapping),
            counts=counts, preserved_sha256=hashes,
            limitations=['See schematic_readiness_gate.md: IntLib compiled with six missing-model warnings; native placement/DFM pending' if closure else 'See library preparation report for source/disk CAD checks; native placement and compilation pending', 'No ERC/DRC',
                         'No electrical simulation or physical validation'])
(hardware/'evidence/passive_delivery_validation.json').write_text(
    json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
