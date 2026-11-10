"""Read-only extraction of current Altium-generated IntLib compressed sources.

The IntLib and project libraries are never rewritten. Extracted bytes are checked
by the official Electronics AI library reader separately.
"""
import hashlib,json,sys,zlib
from pathlib import Path
sys.path.insert(0,'C:/dev/tmp/gateway-audit-python')
import olefile
ROOT=Path.cwd()
LIB=ROOT/'hardware/academic_rev1/libraries'
OUT=Path(__file__).parent
compiled=LIB/'Project Outputs for Gateway_Academic/Gateway_Academic.IntLib'
dest=LIB/'validation/closure_20261107/decoded_final'
dest.mkdir(parents=True,exist_ok=True)
reader=olefile.OleFileIO(compiled)
result={'intlib':str(compiled),'sha256':hashlib.sha256(compiled.read_bytes()).hexdigest(),'embedded':[]}
for stream,ext in [('SchLib/0.schlib','SchLib'),('PCBLib/0.pcblib','PcbLib')]:
    raw=reader.openstream(stream.split('/')).read()
    assert raw[0]==2 and raw[1:3]==b'\x78\x9c'
    data=zlib.decompress(raw[1:])
    assert data[:8]==bytes.fromhex('d0cf11e0a1b11ae1')
    path=dest/('Gateway_Academic.'+ext);path.write_bytes(data)
    result['embedded'].append({'stream':stream,'path':str(path),'bytes':len(data),
        'sha256':hashlib.sha256(data).hexdigest(),'matches_current_source_bytes':data==(LIB/path.name).read_bytes()})
raw=reader.openstream('LibCrossRef.Txt').read()
cross=zlib.decompress(raw[1:])
(OUT/'compiled_cross_reference.txt').write_bytes(cross)
result['cross_reference_bytes']=len(cross)
(OUT/'compiled_source_extraction.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
