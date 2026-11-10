"""Read-only OLE inspection of two explicitly bounded reference PCB files.

No Altium API writes, file rewrite, DRC, rule import or stackup change.
Requires the existing local olefile package; run from repository root.
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0,'C:/dev/tmp/gateway-audit-python')
import olefile

OUT=Path(__file__).parent
ROOT=Path.cwd()
BASE=Path('C:/dev/7mo/design/electronic-design-dc-dc/buck_boost_design')
BOARDS=[BASE/'PCB1.PcbDoc',BASE/'Altium/PCB1.PcbDoc']

def records(data,kind_prefix=False):
    result=[]
    offset=0
    while offset<len(data):
        start=offset
        kind=None
        if kind_prefix:
            kind=struct.unpack_from('<H',data,offset)[0]
            offset+=2
        length=struct.unpack_from('<I',data,offset)[0]
        offset+=4
        assert 0<length<=len(data)-offset,(start,length,len(data))
        raw=data[offset:offset+length]
        offset+=length
        assert raw.endswith(b'\x00'),(start,raw[-12:])
        text=raw[:-1].decode('cp1252')
        fields={}
        for segment in text.split('|'):
            if '=' in segment:
                k,v=segment.split('=',1)
                fields[k]=v
        result.append(dict(offset=start,length=length,kind_ordinal=kind,fields=fields,raw_text=text))
    assert offset==len(data)
    return result

boards=[]
hashes={}
for i,path in enumerate(BOARDS):
    hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
    with olefile.OleFileIO(path,write_mode=False) as ole:
        inventory=[dict(stream='/'.join(s),size=ole.get_size(s)) for s in ole.listdir()]
        counts={s[0]:struct.unpack('<I',ole.openstream(s).read())[0] for s in ole.listdir() if s[-1]=='Header' and ole.get_size(s)==4}
        extracted={}
        for name in ['Rules6','Classes6','Nets6','Board6','Components6','DifferentialPairs6','Design Rule Checker Options6']:
            data=ole.openstream(name+'/Data').read()
            extracted[name]=records(data,kind_prefix=name=='Rules6') if data else []
            if name in counts and name!='Design Rule Checker Options6':
                assert len(extracted[name])==counts[name],(name,counts[name],len(extracted[name]))
        for name in ['ConstraintManager','SignalClasses','LayerKindMapping','BoardRegions','WaivedViolations']:
            data=ole.openstream(name+'/Data').read()
            extracted[name]=dict(bytes=len(data),ascii_fragments=[m.decode('cp1252') for m in re.findall(rb'[ -~]{5,}',data)],hex_prefix=data[:100].hex())
        boards.append(dict(path=str(path),sha256=hashes[str(path)],streams=inventory,counts=counts,extracted=extracted))

academic=ROOT/'hardware/academic_rev1'
protected=[p for p in academic.rglob('*') if p.is_file() and p.suffix.lower() in {'.prjpcb','.pcbdoc','.schdoc','.schlib','.pcblib','.libpkg','.intlib','.rul'}]
protected += [BASE/'PCB_Project_1.PrjPcb',BASE/'Altium/PCB_Project_1.PrjPcb',*BOARDS]
for p in protected:
    hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/'native_files_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
(OUT/'saved_board_records.json').write_text(json.dumps(boards,indent=2)+'\n')
print('Boards byte-identical:',boards[0]['sha256']==boards[1]['sha256'])
for r in boards[0]['extracted']['Rules6']:
    print(json.dumps({'offset':r['offset'],'kind':r['kind_ordinal'],**r['fields']}))
print('CLASSES',json.dumps([r['fields'] for r in boards[0]['extracted']['Classes6']]))
print('NETS',json.dumps([r['fields'] for r in boards[0]['extracted']['Nets6']]))
print('COUNTS',json.dumps(boards[0]['counts']))
print('STACK',json.dumps({k:v for k,v in boards[0]['extracted']['Board6'][0]['fields'].items() if any(s in k.upper() for s in ['STACK','DIELECTRIC','COPPER','THICK','LAYER'])}))
