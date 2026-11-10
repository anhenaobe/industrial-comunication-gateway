"""Read-only CFB stream extraction for independently checking saved SchDoc records."""
import struct,re,json
from pathlib import Path
def stream(path,name):
 b=path.read_bytes();ss=1<<struct.unpack_from('<H',b,30)[0];ms=1<<struct.unpack_from('<H',b,32)[0]
 def sec(i):return b[(i+1)*ss:(i+2)*ss]
 dif=list(struct.unpack_from('<109I',b,76));di,n=struct.unpack_from('<II',b,68)
 for _ in range(n):
  vals=struct.unpack('<'+'I'*(ss//4),sec(di));dif+=vals[:-1];di=vals[-1]
 fat=[]
 for i in dif:
  if i<0xfffffffa:fat+=struct.unpack('<'+'I'*(ss//4),sec(i))
 def chain(i,table,read):
  out=bytearray();seen=set()
  while i<0xfffffffa:
   assert i not in seen;seen.add(i);out+=read(i);i=table[i]
  return bytes(out)
 directory=chain(struct.unpack_from('<I',b,48)[0],fat,sec);entries={}
 for i in range(0,len(directory),128):
  r=directory[i:i+128];ln=struct.unpack_from('<H',r,64)[0]
  if ln:entries[r[:ln-2].decode('utf-16le')]=(struct.unpack_from('<I',r,116)[0],struct.unpack_from('<Q',r,120)[0])
 start,size=entries[name]
 if size>=4096:return chain(start,fat,sec)[:size]
 mf=chain(struct.unpack_from('<I',b,60)[0],fat,sec);mt=struct.unpack('<'+'I'*(len(mf)//4),mf)
 root=chain(entries['Root Entry'][0],fat,sec)
 return chain(start,mt,lambda i:root[i*ms:(i+1)*ms])[:size]
def read(path):
 data=stream(path,'FileHeader');out=[];i=0
 while i+4<=len(data):
  n=struct.unpack_from('<I',data,i)[0]&0xffffff;i+=4
  if not n:break
  r=data[i:i+n];i+=n
  text=r.rstrip(b'\x00').decode('latin1')
  out.append(dict((k.upper(),v) for k,v in (s.split('=',1) for s in text.split('|') if '=' in s)))
 return out
if __name__=='__main__':
 rows=[dict(file=str(f),records=read(f)) for f in Path('hardware/academic_rev1').glob('*.SchDoc')]
 Path(__file__).with_name('disk_records.json').write_text(json.dumps(rows,indent=2))
 for x in rows:print(x['file'],len(x['records']))
