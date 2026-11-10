"""Inspect only native project/PCB history archives in the located workspace."""
import hashlib
import io
import json
import struct
import sys
import zipfile
from pathlib import Path
sys.path.insert(0,'C:/dev/tmp/gateway-audit-python')
import olefile

OUT=Path(__file__).parent
inventory=json.loads((OUT/'reference_archive_inventory.json').read_text())
result=[]
for raw in inventory['nearby_native_history_files']:
    p=Path(raw)
    if not zipfile.is_zipfile(p):
        continue
    item=dict(archive=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),members=[])
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            member=dict(name=name)
            if name.lower().endswith('.pcbdoc'):
                data=z.read(name)
                with olefile.OleFileIO(io.BytesIO(data),write_mode=False) as o:
                    rules=o.openstream('Rules6/Data').read()
                    offset=0
                    rr=[]
                    while offset<len(rules):
                        pos=offset
                        kind,length=struct.unpack_from('<HI',rules,offset)
                        offset+=6
                        text=rules[offset:offset+length].rstrip(b'\x00').decode('cp1252')
                        offset+=length
                        rr.append(dict(offset=pos,kind_ordinal=kind,fields=dict(v.split('=',1) for v in text.split('|') if '=' in v)))
                    assert offset==len(rules)
                    member.update(sha256=hashlib.sha256(data).hexdigest(),rules=rr)
            elif name.lower().endswith('.prjpcb'):
                text=z.read(name).decode('utf-8-sig',errors='replace')
                member['document_paths']=[line for line in text.splitlines() if line.startswith('DocumentPath=')]
            item['members'].append(member)
    result.append(item)
(OUT/'reference_history_records.json').write_text(json.dumps(result,indent=2)+'\n')
boards=[(r['archive'],m) for r in result for m in r['members'] if 'rules' in m]
print('History archives:',len(result),'PCB members:',len(boards))
unique={}
for archive,m in boards:
    summary=[dict(name=r['fields'].get('NAME'),kind=r['fields'].get('RULEKIND'),scope1=r['fields'].get('SCOPE1EXPRESSION'),scope2=r['fields'].get('SCOPE2EXPRESSION'),priority=r['fields'].get('PRIORITY'),**{k:v for k,v in r['fields'].items() if k in ['GAP','MINLIMIT','MAXLIMIT','PREFEREDWIDTH','MINSOLDERMASKWIDTH','OBJECTCLEARANCES']}) for r in m['rules'] if r['fields'].get('RULEKIND') in ['Clearance','Width','MinimumSolderMaskSliver']]
    key=json.dumps(summary,sort_keys=True)
    unique.setdefault(key,dict(source=archive+'!'+m['name'],rules=summary,copies=0))['copies']+=1
print(json.dumps(list(unique.values()),indent=2))
