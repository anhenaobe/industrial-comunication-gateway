"""Focused documentation checks; no native operations or industrial qualification."""
import csv,re,json,hashlib,io,subprocess
from pathlib import Path
from urllib.parse import unquote
O=Path(__file__).parent;D=O.parent.parent;R=Path.cwd()
old=(O/'before_schematic_construction_guide.md').read_text(encoding='utf-8')
new=(D/'schematic_construction_guide.md').read_text(encoding='utf-8')
def section(text,n):return re.search(r'^## '+str(n)+r'\..*?(?=^## \d+\.|\Z)',text,re.M|re.S)[0]
def pinrows(text):
 d=text.split('### D. Connection checklist')[1].split('### E.')[0]
 return [l for l in d.splitlines() if l.startswith('|')]
assert pinrows(section(old,4))==pinrows(section(new,4)),'MCU pins/reservations changed'
for n in [5,6,7,8,9,10]:assert pinrows(section(old,n))==pinrows(section(new,n)),'Interface pin rows changed '+str(n)
for n in [2,3]:
 assert pinrows(section(old,n).replace('VIN_PROT','24V_ELEC'))==pinrows(section(new,n))
required=['0.49895A','15.759V','14.446V','33.142V','30.932V','EF_RTN','TPS26620DRCR','SS3P6L-M3_86A','VCORE_CAP','48, 73 VCAP','PH1','4.92','latch-off']
for v in required:assert v in new,v
bom={r['component_id']:r for r in csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig'))}
mapping={r['component_id']:r for r in csv.DictReader((D/'cad_library_mapping.csv').open(encoding='utf-8-sig'))}
rows=0
for line in new.splitlines():
 if not line.startswith('| '):continue
 cells=[v.strip() for v in line.split('|')[1:-1]];id=cells[0].split(' / ')[0]
 if id not in bom:continue
 r=bom[id];m=mapping[id];assert cells[1].split(';')[0].strip()==r['recommended_mpn'],id
 q=cells[0].split(' / ')[1];assert q==(str(1) if id=='ACTIVE_LMR36015FBRNXR' else r['quantity'] or 'TBD'),id
 assert cells[3]=='`'+m['symbol']+'` / `'+m['footprint']+'`',id
 rows+=1
protected=json.loads((O/'protected_hashes_before.json').read_text())
changed=[]
for name,sha in protected.items():
 p=Path(name)
 if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:changed.append(name)
assert set(changed)=={'docs\\hardware\\passive_bom.csv','docs\\hardware\\final_bom.csv'},changed
# Reconstruct the two pre-task CSV bytes; only approved descriptive metadata differs.
for name in changed:
 p=Path(name)
 with p.open(encoding='utf-8-sig',newline='') as f:rdr=csv.DictReader(f);fields=rdr.fieldnames;rs=list(rdr)
 for r in rs:
  if r['component_id']=='IN_BULK':r['function']='NIS local input bypass'
  if r['component_id']=='IN_HF':r['function']='NIS input high-frequency bypass'
  if r['component_id'] in ['DO_CVCCA3V3','DO_CVCCB5']:r['main_reference']='SN74LVC2T45DCUR propuesto'
 out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rs)
 assert hashlib.sha256(out.getvalue().encode('utf-8-sig')).hexdigest()==protected[name],name
links=[]
for target in re.findall(r'\]\(([^)]+)\)',new):
 if '://' in target or target.startswith('#'):continue
 path=unquote(target.split('#')[0]).strip('<>')
 if path:assert (D/path).exists(),target;links.append(path)
for n in range(1,11):
 s=section(new,n)
 for letter in 'ABCDEFG':assert '### '+letter+'.' in s,(n,letter)
assert hashlib.sha256(Path('C:/Users/justa/Downloads/tps2662.pdf').read_bytes()).hexdigest()==hashlib.sha256(Path('hardware/academic_rev1/libraries/sources/tps26620/tps2662.pdf').read_bytes()).hexdigest()
diff=subprocess.run(['git','diff','--check'],capture_output=True,text=True);assert diff.returncode==0,diff.stdout
status=subprocess.run(['git','status','--short'],capture_output=True,text=True)
result=dict(passed=True,BOM_rows_checked=rows,local_links_checked=len(links),MCU_and_interface_pin_tables_preserved=True,
 buck_pin_change_only='VIN_PROT renamed24V_ELEC in documentation',native_and_firmware_hashes_unchanged=True,
 BOM_changes_only='IN bypass descriptions and DO bypass parent metadata; no IDs/MPNs/values/quantities changed',
 downloads_datasheet_matches_project_copy=True,native_compile_ERC_DRC='NOT_RUN',git_diff_check=diff.returncode,git_status=status.stdout)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='git_status'},indent=2))
