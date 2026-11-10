"""Publish current closure notices and selected/native component reconciliation.
No native-CAD writes. Rerunnable without duplicating notices or inventory rows.
"""
import csv,json,re,os,hashlib,collections
from pathlib import Path
O=Path(__file__).parent;D=O.parent.parent;ROOT=Path.cwd();L=ROOT/'hardware/academic_rev1/libraries'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def writecsv(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
bom=list(csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig')))
mapping=list(csv.DictReader((D/'cad_library_mapping.csv').open(encoding='utf-8-sig')))
native=load(O/'metadata_before.json');req=collections.Counter();opt=collections.Counter();placed=collections.defaultdict(list)
for r in bom:
 q=int(r['quantity'] or 0)
 if r['assembly']=='REQUIRED':req[r['recommended_mpn']]+=q
 if r['assembly']=='CONDITIONAL':opt[r['recommended_mpn']]+=q
for c in native:
 mpn=c['parameters'].get('Manufacturer Part Number','NOT_RECORDED');placed[mpn].append(c)
reconcile=[]
for mpn in sorted(set(req)|set(opt)|set(placed)):
 if mpn=='TBD' and not placed.get(mpn):continue
 reconcile.append(dict(mpn=mpn,target_required_qty=req[mpn],conditional_reserved_qty=opt[mpn],native_qty=len(placed[mpn]),native_designators=';'.join(x['designator'] for x in placed[mpn]),native_sheets=';'.join(sorted({x['sheet'] for x in placed[mpn]})),difference_required_minus_native=req[mpn]-len(placed[mpn]),note='TargetBOMversusnativebaseline;quantitycomparisondoesnotinferconnectivityorapproveequivalents'))
writecsv(O/'bom_native_reconciliation.csv',reconcile)
nativebom={c['designator']:c for c in load(O/'native_bom_before.json')['components']}
models=[]
overrides={'C7':'C5750X7R2A475K230KA','C16':'C5750X7R2A475K230KA','C12':'C0805C225K5RACTU','C21':'C0805C225K5RACTU','J3':'61300611121','SW1':'61300211121'}
for c in native:
 id=c['designator'];mpn=c['parameters'].get('Manufacturer Part Number','NOT_RECORDED');expected=overrides.get(id,mpn)
 selected=next((m for m in mapping if m['recommended_mpn']==expected),{})
 old=nativebom[id].get('footprint','');target=selected.get('footprint','NOT_SELECTED')
 status='MODEL_NAME_MATCH_ONLY' if old==target else 'LOCAL_MODEL_LINK_MIGRATION' if target!='NOT_SELECTED' else 'NATIVE_ONLY_IDENTITY_REVIEW'
 if id in overrides:status='LOCAL_EXACT_COMPONENT_MIGRATION'
 if id in ['R6','R9','C11','C20','U9']:status='SELECTED_DNP_OR_SUPERSEDED;SEE_GUIDE'
 models.append(dict(sheet=c['sheet'],designator=id,native_mpn=mpn,target_mpn=expected,native_symbol=c['symbol'],native_footprint=old,target_symbol=selected.get('symbol',''),target_footprint=target,action=status,note='Modelnamesdonotproveelectricalconnection/applicationvalidity;seecriticalfindings. Noautomaticglobalupdate.'))
writecsv(O/'native_model_reconciliation.csv',models)

sources=L/'sources';pdfs=list(sources.rglob('*.pdf'));ds=ROOT.parent/'Datasheets_industrial_gateway'
manual={'STM32H723VET6':ds/'DS_stm32h723zg.pdf','DP83826IRHBR':ds/'dp83826i.pdf','LMR36015FBRNXR':ds/'lmr36015.pdf','THVD1420DR':ds/'thvd1400.pdf','ATA6561-GAQW':ds/'20005991B.pdf','ISO1212DBQR':ds/'iso1212.pdf','BSP75NTA':sources/'bsp75n_closure/BSP75N.pdf','TPS26620DRCR':sources/'tps26620/tps2662.pdf','SS3P6L-M3/86A':sources/'SS3P6L_88987.pdf','0451002.MRL':sources/'academic_freeze/fuse_manufacturer_drawing.pdf','C5750X7R2A475K230KA':sources/'academic_freeze/TDK_exact.pdf','TB002-500-02BE':sources/'autonomous_closure/tb002-500.pdf','TB002-500-03BE':sources/'autonomous_closure/tb002-500.pdf','CRCW080575R0FKEA':sources/'ethernet_75ohm/C844859.pdf','CRCW1206120RFKEA':sources/'ethernet_75ohm/C844859.pdf','MM204F1K00TKRTR3K0':sources/'electrical_closure/Firstohm_MM.pdf','CL10A105KB8NNNC':sources/'autonomous_closure/Samsung_MLCC_2401.pdf','CL21A106KAYNNNE':sources/'autonomous_closure/Samsung_MLCC_2401.pdf'}
for mpn in ['61300211121','61300611121']:manual[mpn]=None
inventory=[]
for mpn in sorted(m for m in set(req)|set(opt)|set(placed) if m!='TBD'):
 selected=[r for r in bom if r['recommended_mpn']==mpn and r['assembly']in['REQUIRED','CONDITIONAL']]
 model=next((r for r in mapping if r['recommended_mpn']==mpn),{})
 matches=[p for p in pdfs if mpn.lower() in p.name.lower() and p.read_bytes().startswith(b'%PDF')]
 if mpn in manual:matches=([manual[mpn]] if manual[mpn] and manual[mpn].exists() else [])
 rels=sorted({Path(os.path.relpath(p,D)).as_posix() for p in matches})
 family=mpn.startswith(('RC0603','CRCW','CL10','CL21','TB002'))
 coverage=('FAMILY_OR_ORDER_CODE;exactnominalPDFnotasserted' if family else 'SOURCE_REGISTER_COVERS_SELECTED_PART;seeprovenance') if rels else 'NO_LOCAL_EXACT_PDF_IDENTIFIED;sourceweb/HTMLmaycover'
 pin=('NONPOLAR_PROJECT_1_TO_1_2_TO_2' if any(r['item_kind']=='PASSIVE' for r in selected) else 'FUNCTIONAL_ALPHABETIC_IDS_AND_DOCUMENTED_PHYSICAL_POSITIONS' if mpn in ['BSP75NTA','MMBT3904-7-F','DMP2035U-7'] else 'MANUFACTURER_NUMBERED_OR_PROJECT_CONNECTOR_ASSIGNMENT;seeconstructiontable')
 inventory.append(dict(manufacturer=next((r.get('manufacturer','') for r in selected),'NATIVE_ONLY'),mpn=mpn,target_required_qty=req[mpn],conditional_reserved_qty=opt[mpn],native_qty=len(placed[mpn]),native_designators=';'.join(x['designator'] for x in placed[mpn]),sheets=';'.join(sorted({x['sheet'] for x in placed[mpn]})),local_pdf_links=';'.join(rels),coverage=coverage,revision_or_reference=model.get('source','NOT_RECHECKED;native-onlymismatch'),pin_mapping_evidence=pin,mechanical_and_lands='SOURCE_GEOMETRY_VERIFIED' if model.get('cad_status')=='CAD_VERIFIED' else 'PENDING_OR_HISTORICAL',footprint=model.get('footprint',''),cad_status=model.get('cad_status','NOT_SELECTED'),notes=model.get('cad_limitations','Native-onlycomponent;comparetargetBOM')))
writecsv(D/'datasheet_inventory_closure.csv',inventory)
md=['# Current selected/native datasheet inventory —2026-11-08','', 'Generated from the current targetBOM/CADmapping and the actual108-component native baseline. Required andconditional counts are distinct. Native-only mismatches are retained. Family PDFs do not automatically prove every ordering suffix;revision/source locators are in theCSV. Every local link below was checked.','', '[Complete structured inventory](datasheet_inventory_closure.csv). Manufacturergeometry verification is separate from nativeinstanceECO,ERC andmanufacturing release.','', '| MPN | Required / conditional / native | Local manufacturerPDF | Source CAD |','|---|---|---|---|']
for r in inventory:
 links='; '.join(f'[PDF{j+1}]({p.replace(" ","%20")})' for j,p in enumerate(r['local_pdf_links'].split(';')) if p)
 md.append(f"| {r['mpn']} | {r['target_required_qty']} / {r['conditional_reserved_qty']} / {r['native_qty']} | {links or 'No localPDF identified;see source register'} | {r['cad_status']} |")
(D/'datasheet_inventory_closure.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

tag='AUTONOMOUS_CLOSURE_20261108'
notice=f'''<!-- {tag}_START -->
> **Current2026-11-08 baseline:** use [schematic_construction_guide.md](schematic_construction_guide.md) and [electrical_closure_rev1.md](electrical_closure_rev1.md). Source libraries now contain76symbols/48footprints;file validation0errors,4intentionalTPS-subpad warnings.98of99mandatoryBOM rows have sourceCAD geometry verified;TPS thermal-pad net transfer remains candidate. Native corrections,ERC andIntLib compilation remain pending after bridge loss. Earlier counts/holds below are historical snapshots,not current release approval.
<!-- {tag}_END -->
'''
for name in ['schematic_readiness_gate.md','input_protection_reference.md','symbol_library_verification.md','altium_library_preparation_report.md','bsp75n_physical_closure.md','schematic_audit_rev1.md','datasheet_inventory_rev1.md']:
 p=D/name
 if not p.exists():continue
 t=p.read_text(encoding='utf-8');t=re.sub(r'<!-- '+tag+r'_START -->.*?<!-- '+tag+r'_END -->\n?', '',t,flags=re.S)
 head,_,body=t.partition('\n');t=head+'\n\n'+notice+'\n'+body.lstrip('\n');p.write_text(t,encoding='utf-8')
for name in ['passive_component_selection.md','manufacturer_layout_guidelines.md']:
 p=D/name;t=p.read_text(encoding='utf-8');t=re.sub(r'<!-- '+tag+r'_START -->.*?<!-- '+tag+r'_END -->\n?', '',t,flags=re.S)
 head,_,body=t.partition('\n');t=head+'\n\n'+notice+'\n'+body.lstrip('\n');p.write_text(t,encoding='utf-8')

lay=D/'manufacturer_layout_guidelines.md';t=lay.read_text(encoding='utf-8');mark='## Current closure layout additions —2026-11-08'
t=t.split(mark)[0].rstrip()+'''\n\n'''+mark+'''

- TPS EP isEF_RTN,notGND. New compound candidate requires one-to-many symbol11mapping to11/11A/B/C/D orone nativecustompad;do not transfer it with1:1mapping. Thermalvias must stay onEF_RTN anduse agreedassembler treatment.
- Altium roundedrectangle percentage is ofhalf the shorter side. TI R0.05 corresponds toDQA50% for0.20mm leadlands,25% for0.40mm GNDlands;TPSlead42% givesR0.0504,central6% givesR0.0495,fingers40% givesR0.05. [Official Altium pad API definition](https://www.altium.com/documentation/altium-dxp-developer/pcb-api-design-objects-interfaces-reference). Initial incorrect percentage interpretation was corrected before finalreadback.
- RNX A/B share electricalpositions;pin12/NC3areSW. Keep bothVIN/PGND/HF loops compact,FBquiet andseparate switch nodes. Match the saved A/B copper/mask/stencil to the delivered package.
- ISO SUB12/13 eachget an independentfloating2x2mm copperisland;never join toFGND/GND/eachother. DI fieldresistors arefieldsideonly;fix actualR21/R22beforelayout.
- BSP lower-leftIN,lower-centreD,lower-rightS,upperSOURCE TAB. Route loadreturn separately fromquietlogic into the same systemGND;do not route it throughEF_RTN/FIELD_COM. Manufacturerthermal area relates toDRAINcopper;source-tab packages fromothermanufacturers are not substitutes.
- NPN/PMOSdriver transistors carry only5Vlogicinput current. Keep4.7kG-S and2.49kIN-S pull-down connections local;externalDOpositive must remain outside24V_ELEC. See guide10for the chosen circuit.
- Samsung MLCC_2401p159:CL10 +/-0.10mm row selects a=.68,b=.76,c=.85mm;CL21 +/-0.20mm row a=.88,b=.96,c=1.40mm. These are documented midpoints inside manufacturer ranges,not universal0603/0805 defaults. Mask+.05/paste1:1 are prototypechoices. Exact body tolerances come from the retained SamsungproductHTML.
- The connector andtransformerbody outlines/3D/courtyards are not universally implemented;manualplacement must use manufacturerbody envelopes andboardedge/access drawings,not onlypadhulls. Wurth/SameSkynewTH paste disabled. Inspect remainingTH/stencil outputs beforefabrication.
- CurrentJLCPCB1oz greenmask capability covers the chosenTHannuli and~0.10mm maskbridges. Publicgeneric minimumSMTland is0.25x0.25mm;obtain specificDFM acceptance forTI DQA0.20mm/TPS0.24mm leadlands beforemanufacturing. Do not enlarge verifiedlands blindly. [Official capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). This does not define orapprove a PCBstack.
'''
lay.write_text(t,encoding='utf-8')
conv=L/'SYMBOL_CONVENTIONS.md';t=conv.read_text(encoding='utf-8');mark='##2026-11-08 closure additions'
t=t.split(mark)[0].rstrip()+'\n\n'+mark+'''

Keep the existing compactANSIzigzag resistors andtwo-plate capacitors with8-unit(80mil) pins. The closure changed model/verification metadata,not their graphics orconnectionpoints. New MMBT3904/DMP2035U use conventionalNPN/PMOS symbols. Functional AltiumIDs B/E/C andG/S/D deliberately match the exact manufacturerTOP-view positions;do not replace them with inferredgeneric numericpins. BSP remains the protected-deviceblock withIN/D/S/S_TAB. TDS/eFuse/otherIC blocks remain functionalblocks. No schematicinstance auto-update was performed.
'''
conv.write_text(t,encoding='utf-8')

wp=O/'WORKING_PLAN.md';t=wp.read_text(encoding='utf-8');start='<!-- FINAL_STATE -->'
t=t.split(start)[0].rstrip()+'\n\n'+start+'''
Final decisions supersede the early research alternatives above. SelectedDOdriver:DiodesMMBT3904-7-F+DMP2035U-7,2each;4.7kbase/4.7kG-S/100ohmgate/2.49kBSPdown,existing10kGPIOdown. NoNexperiaalternativewasadopted. Sourceinventory76/48.20legacy passive/model links and13other existing verification-metadata updates;all67originalpinarrayspreserved. New9symbols/10feet. DQA/TPSradii corrected toAltiumhalf-side convention. AllmandatorysourcegeometryexceptTPSnetmapping closed;Samsungcatalogp159closesbothremainingMLCCfoottypes. NativePowergeometryrepairpendingfreshcompile;othernativefunctionalrecordsintact;projectsave regeneratedIDs/referencecache. NoPCB/professor/firmwarewrites. See finalreport/verification artifacts. No more CADwrites should occur withoutnewreadback.
'''
wp.write_text(t,encoding='utf-8')
print('Reconciled',len(reconcile),'MPNs;wrote',len(inventory),'inventory rows and current notices')
