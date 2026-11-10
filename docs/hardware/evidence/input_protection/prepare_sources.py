"""Preserve native inputs and reuse local manufacturer PDFs; no network/install."""
import hashlib,json,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path.cwd();OUT=Path(__file__).parent
SRC=ROOT/'hardware/academic_rev1/libraries/sources/input_protection'
ORIGINAL=Path('C:/dev/7mo/design/Datasheets_industrial_gateway')
OUT.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if not (OUT/'hashes_before.json').exists():
    paths=[p for p in (ROOT/'hardware').rglob('*') if p.is_file() and p.suffix.lower() in {'.schlib','.pcblib','.intlib','.libpkg','.prjpcb','.schdoc','.pcbdoc'}]
    paths += [ROOT/'shared_lib (1).IntLib',ROOT/'docs/industrial_gateway_requirements.md']
    (OUT/'hashes_before.json').write_text(json.dumps({str(p):sha(p) for p in paths},indent=2)+'\n')
    for name in ['passive_bom.csv','cad_library_mapping.csv','schematic_readiness_gate.md']:
        shutil.copy2(ROOT/'docs/hardware'/name,OUT/('before_'+name))
files={'TDS3011P.pdf':'https://www.semtech.com/products/circuit-protection/surgeswitch/tds3011p',
       'NIS3071-D.PDF':'https://www.onsemi.com/pdf/datasheet/nis3071-d.pdf',
       '4414fc.pdf':'https://www.analog.com/media/en/technical-documentation/data-sheets/4414fc.pdf',
       'DMP6023LSS.pdf':'https://www.diodes.com/datasheet/download/DMP6023LSS.pdf',
       'lmr36015.pdf':'https://www.ti.com/lit/ds/symlink/lmr36015.pdf'}
entries=[]
existing=list((ROOT/'hardware/academic_rev1/libraries/sources').rglob('*.pdf'))
for name,url in files.items():
    source=ORIGINAL/name
    h=sha(source)
    duplicate=next((p for p in existing if sha(p)==h),None)
    target=duplicate or SRC/name
    if not target.exists():shutil.copy2(source,target)
    entries.append(dict(filename=name,original=str(source),local=str(target.relative_to(ROOT)),sha256=h,official_url=url,reused_existing_project_pdf=duplicate is not None))
(OUT/'datasheet_manifest.json').write_text(json.dumps(entries,indent=2)+'\n')
sys.path.insert(0,'C:/dev/tools/pdf-review-deps')
import pymupdf
for e in entries:
    doc=pymupdf.open(ROOT/e['local'])
    (OUT/(e['filename']+'.txt')).write_text('\n'.join('=== PDF PAGE '+str(i+1)+' ===\n'+page.get_text(sort=True) for i,page in enumerate(doc)),encoding='utf-8')
    selected={'TDS3011P.pdf':[0,1,3,4,5],'NIS3071-D.PDF':[0,1,2,5,6,9,10,11,12],'DMP6023LSS.pdf':[0,6]}.get(e['filename'],[])
    for i in selected:
        if i<len(doc):doc[i].get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(str(OUT/(e['filename']+'-p'+str(i+1)+'.png')))
    print(e['filename'],len(doc),'pages',e['local'])
