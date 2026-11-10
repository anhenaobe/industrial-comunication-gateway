"""Verify saved evidence, pin/pad correspondence, links and protected source hashes."""
import hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path.cwd();OUT=Path(__file__).parent
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def data(r):
    assert r['status']=='fulfilled',r
    v=r['value']; assert not v.get('isError'),v
    return v.get('structuredContent') or json.loads(v['content'][0]['text'])
r=[data(x) for x in read('final_readback_validation.json')]
symbols=read('symbols_additions.json'); footprints=read('footprints_additions.json');assets=read('cad_assets.json')
for i,s in enumerate(symbols):
    got=r[i]['component']; assert got['name']==s['name']
    fields=('designator','name','electrical_type','x','y','length','orientation','hidden')
    assert [{k:p.get(k) for k in fields} for p in got['pins']]==[{k:p.get(k) for k in fields} for p in s['pins']],s['name']
    assert [f['name'] for f in got.get('footprints',[])]==[f['name'] for f in s.get('footprints',[])],s['name']
    expected={p['name']:p['value'] for p in s['parameters']}
    actual={p['name']:p['value'] for p in got.get('parameters',[])}
    # Altium omits empty optional parameter values; no missing path is implied.
    assert all(actual.get(k,'')==v for k,v in expected.items()),s['name']
for i,f in enumerate(footprints):
    got=r[i+4]['component'];assert got['name']==f['name']
    actual={p['designator']:p for p in got['pads']}
    assert set(actual)=={p['designator'] for p in f['pads']}
    for p in f['pads']:
        a=actual[p['designator']]
        for k in ('x','y','width','height','rotation','hole_size'):
            assert abs(a.get(k,0)-p.get(k,0))<.0001,(f['name'],p['designator'],k,a.get(k),p.get(k))
        for k in ('shape','layer','is_plated','paste_mask_expansion_mode','solder_mask_expansion_mode'):
            assert a.get(k)==p.get(k),(f['name'],p['designator'],k)
    assert len(got.get('tracks',[]))==len(f.get('tracks',[])),f['name']
for a in assets:
    if a['footprint']:
        f=next(f for f in footprints if f['name']==a['footprint'])
        assert set(a['pin_map'])=={p['designator'] for p in f['pads']}
assert r[7]['status']==r[8]['status']=='valid'
assert r[7]['error_count']==r[8]['error_count']==0
assert r[7]['warning_count']==r[8]['warning_count']==0
assert [r[7]['component_count'],r[8]['component_count']]==[50,26]
for i,expected in [(9,4),(10,3)]:
    assert r[i]['removed']==r[i]['modified']==[]
    assert len(r[i]['added'])==expected

changes=[]; protected=[]
for p,h in read('hashes_before.json').items():
    assert Path(p).exists(),p
    if sha(p)!=h:changes.append(p)
    else:protected.append(p)
assert {Path(p).name for p in changes}=={'Gateway_Academic.SchLib','Gateway_Academic.PcbLib'},changes
for b in read('library_backup.json'):
    assert sha(b['backup'])==b['sha256'],b
for name in ['passive_bom.csv','cad_library_mapping.csv','schematic_readiness_gate.md']:
    assert sha(OUT/('before_'+name))==sha(ROOT/'docs/hardware'/name),name

pdfs=[]
for e in read('datasheet_manifest.json'):
    assert sha(e['original'])==sha(ROOT/e['local'])==e['sha256']
    assert (ROOT/e['local']).read_bytes().startswith(b'%PDF-')
    pdfs.append(e['local'])
doc=ROOT/'docs/hardware/input_protection_reference.md'
links=[]
for target in re.findall(r'\]\(([^\n]+?)\)',doc.read_text(encoding='utf-8')):
    if target.startswith(('https:','http:','#')):continue
    assert not target.startswith(('/', 'C:')),target
    local=doc.parent/unquote(urlsplit(target).path.strip('<>'))
    assert local.exists(),(target,str(local))
    links.append(target)
for p in [doc,OUT/'build_cad.py',OUT/'prepare_sources.py',OUT/'verify_preparation.py',OUT/'verification_scope.md']:
    assert all(line.rstrip()==line for line in p.read_text(encoding='utf-8').splitlines()),p

gitcheck=subprocess.run(['git','diff','--check'],capture_output=True,text=True)
assert gitcheck.returncode==0,gitcheck.stdout+gitcheck.stderr
status=subprocess.run(['git','status','--short'],capture_output=True,text=True,check=True)
(OUT/'git_status_final.txt').write_text(status.stdout,encoding='utf-8')
intlibs=[p for p in protected if Path(p).suffix.lower()=='.intlib' and 'Gateway_Academic' in p]
release=dict(source_symbol_count=50,source_footprint_count=26,
    added_symbols=[s['name'] for s in symbols],added_footprints=[f['name'] for f in footprints],
    cad_status='CAD_CANDIDATE',electrical_status='PROPOSED_FOR_REUSE',
    fuse_status='PENDING_USER_APPROVAL; symbol only; footprint CAD_BLOCKED',
    native_compile='NOT_ATTEMPTED: user forbids another automation session',
    integrated_library_status='STALE: existing compiled inventory46 symbols23 footprints, additions absent',
    unchanged_intlib_sha256={p:sha(p) for p in intlibs})
(OUT/'library_release_status.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8')
result=dict(status='PASS',symbols_read_back=4,footprints_read_back=3,
    numbered_contacts_checked=sum(len(s['pins']) for s in symbols),
    pads_checked=sum(len(f['pads']) for f in footprints),
    existing_symbols_unchanged=46,existing_footprints_unchanged=23,
    native_sources_protected=len(protected),native_files_modified=changes,
    schematic_or_pcb_changes=[],original_pdfs_unchanged=len(pdfs),
    report_local_links_checked=len(links),local_pdf_links=sum('.pdf' in x.lower() for x in links),
    git_diff_check='PASS',bom_and_mapping_unchanged=True,
    source_hashes_after={p:sha(p) for p in list(read('hashes_before.json'))})
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='source_hashes_after'},indent=2))
