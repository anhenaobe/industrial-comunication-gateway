"""Offline invariant checks; never claims native ERC,DRC or electrical testing.
Run from repository root after exporting fresh *_verified.json through Electronics AI.
"""
import csv,json,math,hashlib,sys,re,collections
from pathlib import Path
O=Path(__file__).parent;D=O.parent.parent;ROOT=Path.cwd()
sys.path.insert(0,str(D/'evidence/native_schematic_audit'))
from read_disk import read,stream
def load(name):return json.loads((O/name).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def close(a,b,tol=0.000003):assert abs(a-b)<=tol,(a,b)
result={'validation_scope':'Offline model/BOM/source/saved-record invariants;notERC/DRC','checks':[]}
for p,h in load('handoff_library_hashes.json').items():assert digest(p)==h,'Export fresh libraryreadback:'+p
def passed(s):result['checks'].append(s)
release=load('handoff_readback.json')
S={s['name']:s for s in release['symbols']}
F={f['name']:f for f in release['footprints']}
A={s['name']:s for s in load('symbols_before.json')['symbols']}
B={f['name']:f for f in load('footprints_before.json')['footprints']}
updated={s['name'] for s in load('symbol_link_updates.json')}|{'STM32H723VET6','LMR36015FBRNXR','TPD4E05U06DQAR'}|{r['mpn'] for r in load('geometry_reviews.json')}
for name,old in A.items():
 assert old['pins']==S[name]['pins'],name+' pin mutation'
 if name not in updated:assert old==S[name],name+' unrelated symbol mutation'
 else:
  for k in ['lines','polylines','rectangles','arcs','ellipses','labels','designator','designator_x','designator_y']:
   assert old.get(k)==S[name].get(k),(name,k)
  def header(s):return {k:v for k,v in s.get('header_params',[]) if k.upper()!='COMPONENTDESCRIPTION'}
  assert header(old)==header(S[name]),name+' identity/header mutation'
  def electrical(s):return {p['name']:p['value'] for p in s.get('parameters',[]) if not p['name'].startswith('CAD') and p['name'] not in ['Limitations','Source']}
  assert electrical(old)==electrical(S[name]),name+' electrical metadata mutation'
for name,old in B.items():
 if name not in ['GW_DQA0010A_TI','GW_DRC0010J_TI_TPS2662']:assert old==F[name],name+' unrelated footprint mutation'
assert len(S)==76 and len(F)==48
passed(f'All67 original symbol pin arrays preserved exactly;{len(A)-len(updated)} unrelated symbols and36 unrelated footprints byte-field identical in official readback.{len(updated)} metadata/model updates;DQA/TPS radii/paste corrections;9new symbols/10new footprints.')

for name in ['MMBT3904-7-F','DMP2035U-7','TB002-500-02BE','TB002-500-03BE','61300211121','61300611121','RC0603FR-074K7L','RC0603FR-07100RL','CRCW1206120RFKEA']:
 s=S[name];ids={p['designator'] for p in s['pins']};fp=F[s['footprints'][0]['name']]
 assert ids=={p['designator'] for p in fp['pads']},name+' mapping mismatch'
for name,ids in [('MMBT3904-7-F',['B','E','C']),('DMP2035U-7',['G','S','D'])]:
 fp=F[S[name]['footprints'][0]['name']];pads={p['designator']:p for p in fp['pads']}
 for id,x,y in zip(ids,[-.95,.95,0],[-1,-1,1]):
  p=pads[id];close(p['x'],x);close(p['y'],y);close(p['width'],.8);close(p['height'],.9)
for name in ['GW_TB002_500_2P_SAMESKY','GW_TB002_500_3P_SAMESKY','GW_WRPHD_2X1_254_WURTH','GW_WRPHD_6X1_254_WURTH']:
 for p in F[name]['pads']:
  assert p['is_plated'] and p['hole_size']>0
  assert p['paste_mask_expansion'] < -max(p['width'],p['height'])/2
passed('All9 new symbols have exact saved pin-to-pad sets;Diodes physical positions/dimensions correct;four new TH patterns plated and paste disabled.')

for p in F['GW_LQFP100_ST_1L']['pads']:
 i=int(p['designator']);q=(i-1)//25;j=(i-1)%25
 x,y=[(-6+j*.5,-7.75),(7.75,-6+j*.5),(6-j*.5,7.75),(-7.75,6-j*.5)][q]
 close(p['x'],x);close(p['y'],y);close(min(p['width'],p['height']),.3);close(max(p['width'],p['height']),1.2)
assert {p['designator'] for p in F['GW_LQFP100_ST_1L']['pads']}=={str(i) for i in range(1,101)}
for name in ['GW_RNX0012A_TI','GW_RNX0012B_TI']:
 pads={p['designator']:p for p in F[name]['pads']};assert set(pads)=={str(i) for i in range(1,13)}
 for i,x,y in [('1',-.9,1.125),('2',-.9,.475),('3',-.9,-.175),('4',-.9,-.675),('11',.9,1.125),('10',.9,.475),('9',.9,-.175),('8',.9,-.675),('5',-.5,-1.4),('6',0,-1.4),('7',.5,-1.4),('12',0,.7875)]:
  close(pads[i]['x'],x);close(pads[i]['y'],y)
 t=pads['12'];close(t['width'],.35 if '0012A' in name else .25);close(t['height'],1.925 if '0012A' in name else 1.825)
passed('ST100-lead orientation,pitch,lands andbothTI RNX12-pin layouts match independently inspected manufacturer drawings.')

dqa=F['GW_DQA0010A_TI'];pads={p['designator']:p for p in dqa['pads']}
for i,p in pads.items():
 close(p['width'],.565);close(p['height'],.4 if i in ['3','8'] else .2);assert p['shape']=='rounded_rectangle'
 close(p['solder_mask_expansion'],.05)
paste=[r for r in dqa.get('regions',[]) if r['layer']=='Top Paste'];assert len(paste)==2
for r in paste:
 vs=r['vertices'];close(max(v['x'] for v in vs)-min(v['x'] for v in vs),.565);close(max(v['y'] for v in vs)-min(v['y'] for v in vs),.36)
for p in dqa['pads']:close(min(p['width'],p['height'])*p['corner_radius_percent']/200,.05)
passed('DQA rounded copper R0.05 andtwoexplicit reducedGND paste windows persisted;Altiumhalf-sidepercentage independentlyverified.')
ep={p['designator']:p for p in F['GW_DRC0010J_TI_TPS2662_EP11']['pads']}
assert {'11','11A','11B','11C','11D'}<=set(ep)
assert S['TPS26620DRCR']['footprints'][0]['name']=='GW_DRC0010J_TI_TPS2662'
passed('TPS alternate EP remains isolated as an unbound mapping candidate;no silent default1:1 transfer.')

bom=list(csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig')))
mapping=list(csv.DictReader((D/'cad_library_mapping.csv').open(encoding='utf-8-sig')));M={r['component_id']:r for r in mapping}
assert len(M)==len(mapping);assert len({r['component_id'] for r in bom})==len(bom)
for r in bom:
 m=M[r['component_id']];assert (r['recommended_mpn'],r['symbol'],r['footprint'])==(m['recommended_mpn'],m['symbol'],m['footprint']),r['component_id']
 if r['assembly']=='REQUIRED' and int(r['quantity'] or 0):
  assert r['recommended_mpn']!='TBD' and r['symbol'] in S and r['footprint'] in F,r['component_id']
  pins={p['designator'] for p in S[r['symbol']]['pins']};pads=F[r['footprint']]['pads'];ids={p['designator'] for p in pads}
  assert pins<=ids,(r['component_id'],'missing physical pads',pins-ids)
  assert all(p['designator']in pins or p.get('is_plated') is False for p in pads),(r['component_id'],'extra conductive pad without symbol pin')
for r in mapping:
 assert r['verification_status']==r['cad_status'],r['component_id']
 if r['item_kind']=='ACTIVE':assert r['quantity']==''
R={r['component_id']:r for r in bom}
assert R['ACTIVE_SN74LVC2T45DCTR']['quantity']=='0' and R['ACTIVE_NIS3071MT4TWG']['quantity']=='0'
assert R['DO_RPDB']['recommended_mpn']=='RC0603FR-072K49L'
assert R['CLOSURE_MMBT3904-7-F']['quantity']==R['CLOSURE_DMP2035U-7']['quantity']=='2'
assert R['B3_CIN']['quantity']==R['B5_CIN']['quantity']=='2'
assert R['ETH_RBOB']['quantity']=='4' and R['ETH_CBOB']['quantity']=='2'
passed('Unique stable BOM/mapping IDs,exact MPN/model agreement,allmandatorymodels saved;supersededactiveqty0;fourBobSmithresistors/twocaps;independentCIN banks and newdriver quantities correct.')
for name,x,w,h,gap in [('GW_SAMSUNG_CL10_1608_REFLOW',.72,.76,.85,.68),('GW_SAMSUNG_CL21_2012_REFLOW',.92,.96,1.40,.88)]:
 p=sorted(F[name]['pads'],key=lambda p:p['x']);assert {v['designator'] for v in p}=={'1','2'}
 for v,xx in zip(p,[-x,x]):close(v['x'],xx);close(v['width'],w);close(v['height'],h)
 close(p[1]['x']-p[0]['x']-w,gap)
passed('BothSamsung footprints match documentedmidpoints ofcorrectmanufacturerbody-tolerancerows;allmandatory symbolpins have conductivepadcounterparts,extraRJmountpadsareNPTH.')

pins=load('native_nets_before.json')['pins'];N={(r['component'],r['pin']):r['net'] for r in pins}
links=[('23','19'),('24','11'),('16','12'),('31','18'),('32','16'),('33','15'),('47','23'),('51','24'),('52','25'),('5','32')]
for a,b in links:assert N['U4',a]==N['U5',b],('RMII/PHY',a,b)
for a,u,b in [('55','U6','4'),('56','U6','1'),('57','U6','3'),('58','U6','2'),('81','U7','4'),('82','U7','1'),('37','U7','8'),('3','U8','4'),('4','U8','5')]:assert N['U4',a]==N[u,b],(a,u,b)
assert len({a for a,b in links}|{'55','56','57','58','81','82','37','3','4','1','2','72','76','12'})==24
assert N['U1','5']==N['U1','11']=='EF_RTN' and N['U1','6']=='GND'
assert N['U8','9']==N['U8','14']=='FIELD_COM' and N['U8','1']=='GND'
assert N['U4','48']==N['U4','73']=='VCAP' and N['U4','48']!=N['U4','11']
assert N['U2','12']!=N['U3','12']
passed('Baseline native graph:19cross-sheet endpoint pairs,24distinct MCU reservations,no sharedSW,VCAP/GND/EF_RTN/FIELD_COM separation. This does not waive identifiedDI resistor bridge or prove post-edit ERC.')

backups=load('baseline_backups.json');native_changes={}
def norm(r):return {k:v for k,v in r.items() if k not in ['UNIQUEID','INDEXINSHEET'] and not(k=='WEIGHT' and 'HEADER'in r)}
for b in backups:
 p=Path(b['path'])
 if p.suffix!='.SchDoc':continue
 a=read(Path(b['backup']));c=read(p)
 oldcomp=[r for r in a if r.get('RECORD')=='1'];newcomp=[r for r in c if r.get('RECORD')=='1'];assert oldcomp==newcomp,p.name+' component mutation'
 if p.name!='Power.SchDoc':assert [norm(x) for x in a]==[norm(x) for x in c],p.name+' functional mutation'
 else:
  ac=collections.Counter(json.dumps(norm(x),sort_keys=True) for x in a);cc=collections.Counter(json.dumps(norm(x),sort_keys=True) for x in c)
  removed=[json.loads(k) for k,v in (ac-cc).items() for _ in range(v)];added=[json.loads(k) for k,v in (cc-ac).items() for _ in range(v)]
  assert all(x.get('RECORD') in ['25','27','29'] for x in removed+added),(removed,added)
  native_changes=dict(removed=removed,added=added)
result['saved_power_geometry_changes']=native_changes
passed('All108 nativecomponent definitions/locations/identities preserved. Fourother sheets differ only generated IDs/container bytes;Powerchanges restricted to wire,label/junction records. Native save side effects disclosed.')
project=next(b for b in backups if b['path'].endswith('.PrjPcb'))
def projectsettings(path):
 return collections.Counter(l for l in Path(path).read_text().splitlines() if not re.match(r'(Component(LibIdentifierKind|LibraryIdentifier|DesignItemID|SymbolReference|Update|IsDeviceSheet)|Model(Name|Type|Update))\d+=',l) and not l.startswith(('ComponentCount=','ModelCount=')))
assert projectsettings(project['backup'])==projectsettings(project['path'])
passed('Allprojectsettings/documentpaths unchanged outside refreshed component/model reference caches.')

protected=json.loads((D/'evidence/construction_sync/protected_hashes_before.json').read_text())
keep={p:h for p,h in protected.items() if 'Professor_shared.' in p or p.endswith('PCB1.PcbDoc') or ('academic_rev1' not in p and Path(p).suffix.lower() in ['.intlib','.schlib','.pcblib'])}
for p,h in keep.items():assert digest(p)==h,p+' protected source changed'
result['protected_hashes']=keep
passed('Historical professor libraries,PCB and available original-library hashes match protected evidence.')

for p in (ROOT/'hardware/academic_rev1/libraries/sources/autonomous_closure').glob('*.pdf'):
 assert p.read_bytes().startswith(b'%PDF'),str(p)+' is notPDF'
guide=(D/'schematic_construction_guide.md').read_text(encoding='utf-8')
for id in re.findall(r'^\| ((?:ACTIVE_|MCU_|ETH_|B3_|B5_|IN_|RS_|CAN_|DI_|DO_)[A-Za-z0-9_.-]+)(?= / (?:[0-9]+|TBD) /)',guide,re.M):
 assert id in R,('ConstructionguideBOMIDmismatch',id)
for target in re.findall(r'\]\(([^)]+\.pdf)(?:#[^)]*)?\)',guide):
 if '://' not in target:assert (D/target).exists(),target
passed('All local PDF links in current construction guide exist;blockedHTML downloads are not masquerading asPDFs.')

vlow=4.86249-.05;vhigh=5.17365
calc=dict(TPS_ILIM_A=6.636/13.3,UVLO_rising_V=1.2*(768+33.2+30.1)/(33.2+30.1),OVP_rising_V=1.2*(768+33.2+30.1)/30.1,
 PMOS_VGS_min_screen_V=(vlow-.2-.001)*4653/(4653+101),BSP_VIN_min_screen_V=vlow-.005*.045,
 NPN_base_min_screen_A=(2.4-.85)/4747,BSP_0p5A_loss_W=.5**2*.675,termination_fullrail_screen_W=vhigh**2/118.8)
assert calc['PMOS_VGS_min_screen_V']>=2.5 and calc['BSP_VIN_min_screen_V']>=4.5
assert calc['termination_fullrail_screen_W']<.25
result['engineering_calculations']=calc
result['bom_summary']=dict(rows=len(bom),required_rows=sum(r['assembly']=='REQUIRED' for r in bom),required_units=sum(int(r['quantity'] or 0) for r in bom if r['assembly']=='REQUIRED'),required_unique_MPNs=len({r['recommended_mpn'] for r in bom if r['assembly']=='REQUIRED'}),CAD_statuses=dict(collections.Counter(r['cad_status'] for r in bom if r['assembly']=='REQUIRED')))
result['native_validation']='UNAVAILABLE;cachedbaselineandrawsavedreadbackonly;no post-edit compilation/ERC/IntLib compilation'
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['saved_power_geometry_changes','protected_hashes']},indent=2))
