"""Preserve task baselines and obtain only small, exact manufacturer documents.

No dependencies, libraries or packages are installed/downloaded. Existing source
documents are never overwritten. Run once from the repository root.
"""
import csv
import hashlib
import importlib.util
import json
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).parent
SRC = ROOT/'hardware/academic_rev1/libraries/sources/electrical_closure'
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)
baseline = OUT/'baseline'
baseline.mkdir(exist_ok=True)
for name in ['passive_bom.csv','cad_library_mapping.csv','passive_component_selection.md','manufacturer_layout_guidelines.md']:
    dst=baseline/name
    if not dst.exists(): shutil.copy2(ROOT/'docs/hardware'/name,dst)
protected={}
for folder in ([] if (OUT/'hashes_before.json').exists() else [ROOT/'hardware',ROOT/'firmware']):
    for p in folder.rglob('*'):
        if p.is_file() and (folder.name=='firmware' or p.suffix.lower() in ['.schlib','.pcblib','.intlib','.prjpcb','.libpkg','.schdoc','.pcbdoc']):
            protected[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [ROOT/'shared_lib (1).IntLib', ROOT/'docs/industrial_gateway_requirements.md']:
    protected[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
if not (OUT/'hashes_before.json').exists():
    (OUT/'hashes_before.json').write_text(json.dumps(protected,indent=2)+'\n')
docs={
 'KC2016Z25.0000C15XXK_e.pdf':'https://ele.kyocera.com/assets/products/crystal-device/specification/KC2016Z25.0000C15XXK_e.pdf',
 'HX1188FNL.pdf':'https://productfinder.pulseeng.com/doc_type/WEB301/doc_num/HX1188FNL/doc_part/HX1188FNL.pdf',
 'SS-7188S-A-NF_drawing.pdf':'https://www.cinch.com/media/drawings/products/ethernet-usb/dr-stw-ss-7188s-a-nf-ss-7188s-a-nf-50.pdf',
 'CDSOT23-SM712.pdf':'https://www.bourns.com/pdfs/CDSOT23-SM712.pdf',
 'xal4000.pdf':'https://www.coilcraft.com/getmedia/6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf',
 'C5750X7R2A475K230KA_characteristics.pdf':'https://product.tdk.com/info/en/documents/chara_sheet/c5750x7r2a475k230ka.pdf',
 'C3225X7R1C156M250AB_characteristics.pdf':'https://product.tdk.com/info/en/documents/chara_sheet/c3225x7r1c156m250ab.pdf',
 'tpd4e05u06.pdf':'https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf',
}
def fetch(item):
    name,url=item
    result={'filename':name,'url':url,'destination':str(SRC/name),'observed_at_utc':datetime.now(timezone.utc).isoformat()}
    try:
        p=SRC/name
        if p.exists(): data=p.read_bytes();result['status']='existing'
        else:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=22) as response: data=response.read(4_000_001)
            assert data.startswith(b'%PDF') and len(data)<=4_000_000,'Not a small PDF'
            p.write_bytes(data);result['status']='saved'
        result.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e: result.update(status='BLOCKED',error=str(e))
    return result
results=list(ThreadPoolExecutor(max_workers=4).map(fetch,docs.items()))
(OUT/'manufacturer_documents.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
print('Existing PDF modules:',{name:bool(importlib.util.find_spec(name)) for name in ['fitz','pypdf','pdfplumber']})
