import json,csv,collections,os,re
from pathlib import Path
O=Path(__file__).parent;D=O.parents[1];root=Path.cwd()
def j(n):return json.loads((O/n).read_text())
lib={x['name']:x for x in j('library.json')['symbols']};meta=j('placed_metadata.json');selected=list(csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig')));mapping=list(csv.DictReader((D/'cad_library_mapping.csv').open(encoding='utf-8-sig')))
group=collections.defaultdict(list);sel=collections.defaultdict(list)
for x in meta:group[x['parameters'].get('Manufacturer Part Number') or 'UNRESOLVED:'+x['lib_ref']].append(x)
unresolved=[]
for x in selected:
 if x['assembly']!='REQUIRED':continue
 mp=x['recommended_mpn']
 if mp and mp not in ('TBD','MISSING') and not mp.startswith('TBD'):sel[mp].append(x)
 else:unresolved.append(x)
pdfs=list(Path('hardware/academic_rev1/libraries/sources').rglob('*.pdf'))+list(Path('C:/dev/7mo/design/Datasheets_industrial_gateway').glob('*.pdf'))
aliases={'STM32H723VET6':'DS_stm32h723zg.pdf','DP83826IRHBR':'dp83826i.pdf','ISO1212DBQR':'iso1212.pdf','LMR36015FBRNXR':'lmr36015.pdf','TPS26620DRCR':'tps2662.pdf','THVD1420DR':'thvd1400.pdf','ATA6561-GAQW':'20005991B.pdf','SN74LVC2T45DCTR':'sn74lvc2t45.pdf','BSP75NTA':'BSP75N.pdf','SS3P6L-M3/86A':'SS3P6L_88987.pdf','TDS3011P.C':'TDS3011P.pdf','0451002.MRL':'fuse_manufacturer_drawing.pdf','HX1188FNL':'HX1188FNL.pdf','SS-7188S-A-NF':'SS-7188S-A-NF_drawing.pdf','KC2016Z25.0000C15XXK':'KC2016Z25.0000C15XXK_e.pdf','TPD4E05U06DQAR':'tpd4e05u06.pdf','XAL4030-682MEC':'xal4000.pdf','XAL4040-103MEC':'xal4000.pdf','MM204F1K00TKRTR3K0':'Firstohm_MM.pdf','C5750X7R2A475K230KA':'TDK_exact.pdf','CRCW080575R0FKEA':'C844859.pdf','C1206C102KGRACAUTO':'C600002.pdf'}
exact_verified={'BSP75NTA','CRCW080575R0FKEA','C1206C102KGRACAUTO'}
rows=[]
for mp in sorted(set(group)|set(sel)):
 actual=group[mp];targets=sel[mp];p=actual[0]['parameters'] if actual else {};
 if not actual and targets:
  source=lib.get(targets[0]['symbol'],{});p={v['name']:v.get('value','') for v in source.get('parameters',[])}
 m=[x for x in mapping if x['recommended_mpn']==mp]
 want=mp+'.pdf';paths=[x for x in pdfs if x.name.lower()==want.lower()]
 if not paths and mp in aliases:paths=[x for x in pdfs if x.name.lower()==aliases[mp].lower()]
 if not paths:
  for t in targets:
   q=Path(t.get('local_datasheet',''))
   if q.is_file() and q.suffix.lower()=='.pdf':paths=[q];break
 path=paths[0] if paths else None
 rev={'BSP75NTA':'DS33016 Rev7-2 Jan2024','TPS26620DRCR':'SLVSDT4F Dec2021','LMR36015FBRNXR':'SNVSB49D','DP83826IRHBR':'SNLS647I Aug2025','ISO1212DBQR':'SLLSEY7G','STM32H723VET6':'DS13313; Table7/8 exactLQFP100','HX1188FNL':'RevB 05/30/14 sheet2','SS-7188S-A-NF':'CT710001 RevB0'}.get(mp,'NOT_EXTRACTED')
 models=sorted({v for x in actual for v in x['models']});targetfp=sorted({x['footprint'] for x in m if x['footprint'] not in ('','MISSING')})
 qty=sum(int(x['quantity']) for x in targets if x['quantity'].isdigit())
 r=dict(manufacturer=p.get('Manufacturer','NOT_RECONCILED'),mpn=mp,actual_sheets=';'.join(sorted({x['sheet'] for x in actual})),actual_qty=len(actual),designators=';'.join(x['parameters']['Designator'] for x in actual),documented_required_qty=qty,required_bom_ids=';'.join(x['component_id'] for x in targets),local_pdf=os.path.relpath(path,D).replace('\\','/') if path else '',revision=rev,exact_part_package_coverage='VERIFIED_RECENT_REPORT' if mp in exact_verified else ('LOCATED_NOT_EXACT_ORDERING_REVERIFIED' if path else 'MISSING_LOCAL'),pin_numbering='FUNCTIONAL_POSITIONS_VERIFIED' if mp=='BSP75NTA' else ('NONPOLAR_TWO_TERMINAL' if actual and all(len(x['pins'])==2 for x in actual) else 'PARTIAL_OR_NOT_RECHECKED'),mechanical='RECENT_VERIFIED_REPORT' if mp in exact_verified else 'NOT_RECHECKED',manufacturer_land_pattern='RECENT_VERIFIED_REPORT' if mp in exact_verified else 'NOT_RECHECKED',placed_footprint=';'.join(models),project_library_candidate=';'.join(targetfp),footprint_verification=';'.join(sorted({x['cad_status'] for x in m})) or 'NOT_IN_MAPPING',missing_information='No claim of full package qualification; missing instance links differ from missing source resources')
 if len(actual)!=qty:r['missing_information']+='; actual/required quantity differs (not automatic excess: DNP/spec dedup or wrong MPN possible)'
 if not path:r['missing_information']+='; exact manufacturer PDF needed'
 rows.append(r)
with (D/'datasheet_inventory_rev1.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def table(head,rs):return '| '+' | '.join(head)+' |\n|'+'|'.join(['---']*len(head))+'|\n'+''.join('| '+' | '.join(str(x).replace('|','/') for x in r)+' |\n' for r in rs)
s='''# Academic Rev.1 — manufacturer datasheet inventory

Inventory from the actual native project, independently checked against saved component records. No parts were replaced during this audit. **44 distinct placed MPNs/identities,106 components**; union below also includes concrete required BOM MPNs not yet placed. Required quantities are summed BOM positions, not evidence of approval or physical population. Unselected conditional and DNP positions are excluded from required totals. No variant exists: physical DNP settings remain unresolved.

This is a retrieval/verification input for the next task, not a claim that every datasheet or footprint is verified. A located family PDF does not prove ordering code, pins or manufacturer land pattern; NOT_RECHECKED and LOCATED_NOT_EXACT_ORDERING_REVERIFIED are deliberate. Full per-MPN columns, including mechanical/land-pattern/pin coverage, are in [structured CSV](datasheet_inventory_rev1.csv). Manufacturer for absent parts remains NOT_RECONCILED rather than guessed. Source CAD_VERIFIED status is recorded provenance, not a fresh footprint measurement in this audit.

'''
s+=table(['Manufacturer / MPN','Actual qty / designators / sheets','BOM required qty','Local manufacturer document / revision','Placed footprint / source candidate','Evidence / missing information'],[(r['manufacturer']+' / '+r['mpn'],str(r['actual_qty'])+' / '+r['designators']+' / '+r['actual_sheets'],r['documented_required_qty'],('[PDF](<'+r['local_pdf']+'>)' if r['local_pdf'] else 'MISSING')+' / '+r['revision'],(r['placed_footprint'] or 'INSTANCE MISSING')+' / '+r['project_library_candidate'],r['exact_part_package_coverage']+'; '+r['footprint_verification']+'; '+r['missing_information']) for r in rows])
s+='\n## Required physical positions without exact MPN\n\n'+table(['BOM ID','Function','Quantity','Recorded identity'],[(r['component_id'],r['function'],r['quantity'],r['recommended_mpn']) for r in unresolved])
s+='\n## Retrieval and footprint work next\n\nObtain exact absent manufacturer PDFs (notably TDS3311P.C and unselected connector/header/button identities), reconcile superseded placed parts and quantity deficits, verify ordering suffix/package, then inspect manufacturer lands and correct instance links. TPS custom thermal pad and source candidate packages need dedicated verification. No new footprints were generated. Existing exact resistor/capacitor datasheets may be nominal specification sheets without recommended lands; do not assume otherwise.\n'
(D/'datasheet_inventory_rev1.md').write_text(s,encoding='utf-8')
assert all((D/r['local_pdf']).exists() for r in rows if r['local_pdf'])
print('Inventory entries',len(rows),'placed',len(group),'all PDF links exist')
