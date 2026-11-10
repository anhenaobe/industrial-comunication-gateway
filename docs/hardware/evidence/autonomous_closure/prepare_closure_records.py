"""Reproducible, late BOM/CAD overlay. Does not write native CAD files."""
import csv,copy,json
from pathlib import Path
O=Path(__file__).parent;D=O.parent.parent
def save(name,obj): (O/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
rows={r['component_id']:r for r in csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig'))}
assets=json.loads((O/'cad_additions.json').read_text())
dec={'patches':{},'record_fields':{},'active_patches':{},'new_rows':[]}
def patch(id,**kw):dec['patches'].setdefault(id,{}).update(kw)
def record(id,approval='ENGINEERING_SELECTED_ACADEMIC_2026_11_08'):
 dec['record_fields'][id]=dict(design_approval=approval,validation_scope='SOURCE_REVIEW_AND_FILE_READBACK;NATIVE_CAPTURE_PENDING',test_status='NOT_ELECTRICALLY_TESTED')
def asset_for(mpn):return next(a for a in assets if a['mpn']==mpn)
def choose(id,mpn,val,pkg,qty=1,assembly='REQUIRED',rating='See manufacturer source'):
 patch(id,recommended_mpn=mpn,nominal_value=val,package=pkg,quantity=qty,assembly=assembly,rated_voltage_or_current=rating,electrical_status='DERIVED_PENDING_REVIEW',verification_status='CALCULATED',observations='Selected 2026-11-08 engineering closure; explicit wiring in construction guide. Native instances require local migration.',cad_route='PROJECT_LOCAL_VERIFIED')
 asset_for(mpn)['component_ids'].append(id);record(id)
for id,n in [('IN_J',2),('DO_JLOAD',2),('RS_J',3),('CAN_J',3),('DI_J',3)]:
 choose(id,f'TB002-500-0{n}BE',f'{n} poles;5mm pitch',f'TB002-500 {n}P TH',2 if id=='DO_JLOAD' else 1,rating='UL300V15A;IEC250V17.5A;academic circuit limits lower')
choose('MCU_JSWD','61300611121','6-position unkeyed custom SWD','6x1 2.54mm TH')
choose('MCU_JBOOT','61300211121','2-position BOOT recovery','2x1 2.54mm TH')
# No NRST button exists in the actual sheet: SW1 is BOOT recovery. Debugger
# reset/J3.4-to-J3.5 already provides reset access; do not make an unverified
# tactile package mandatory merely because an old placeholder row existed.
patch('MCU_SRESET',quantity=0,assembly='DNP',observations='Optional onboard reset button not selected. NRST is accessible at actual J3.4 and adjacentGND J3.5; debugger or a momentary external test contact provides reset. SW1 is BOOT recovery and should migrate locally to the verified2pinBOOT header,not be mistaken forNRST.')
record('MCU_SRESET','OPTIONAL_DNP_RESET_ACCESS_VIA_J3')
for id in ['RS_RT','CAN_RT']:
 choose(id,'CRCW1206120RFKEA','120 Ohm','1206',assembly='CONDITIONAL',rating='1%;0.25W at70C;200V or power-limited');patch(id,tolerance='1%',power_rating='0.25W',observations='Physical bus-end only; open-default2pinjumper in series. At5.174V differential the conservative DC dissipation screen is0.226W; normal differential voltage is lower. No bus-fault rating inferred.')
for id,function in [('RS_JTERM','RS485 end-termination jumper'),('CAN_JTERM','CAN end-termination jumper')]:
 dec['new_rows'].append(dict(clone_of='MCU_JBOOT',component_id=id,function=function,main_reference='Wurth61300211121 official p1 hole layout'))
 choose(id,'61300211121','2-pin termination enable,defaultOPEN','2x1 2.54mm TH',assembly='CONDITIONAL')
# New supply terminal keeps DO load current outside the electronics eFuse.
dec['new_rows'].append(dict(clone_of='DO_JLOAD',component_id='DO_JSUPPLY',function='External DO supply and common return',main_reference='Same Sky TB002-500 Rev1.04 p1-2'))
choose('DO_JSUPPLY','TB002-500-02BE','External24V and DO return','TB002-500 2P TH')
patch('DO_CVCCA3V3',quantity=0,assembly='DNP',observations='Former translator bypass; translator superseded. Existing native capacitor can be retained as extra3.3V local bypass after checking nets, but is not a mandatory DO part.')
choose('DO_RPDB','RC0603FR-072K49L','2.49 kOhm','0603',qty=2,rating='1%;0.1W;75V or power-limited') if any(a['mpn']=='RC0603FR-072K49L' for a in assets) else None
patch('DO_RPDB',recommended_mpn='RC0603FR-072K49L',nominal_value='2.49 kOhm',quantity=2,tolerance='1%',power_rating='0.1W',electrical_status='DERIVED_PENDING_REVIEW',verification_status='CALCULATED',observations='Each BSP IN to localSOURCE/GND; sets defaultOFF for new discrete5V driver.')
record('DO_RPDB')
for id,mpn,val,qty,function in [('DO_RBASE','RC0603FR-074K7L','4.7 kOhm',2,'MCU to NPN base'),('DO_RGS','RC0603FR-074K7L','4.7 kOhm',2,'PMOS gate-to-source defaultOFF'),('DO_RGATE','RC0603FR-07100RL','100 Ohm',2,'NPN collector to PMOS gate')]:
 dec['new_rows'].append(dict(clone_of='DO_RPDA',component_id=id,function=function,main_reference='Diodes MMBT3904/DMP2035U source-based driver calculation'))
 choose(id,mpn,val,'0603',qty=qty,rating='1%;0.1W;75V or power-limited');patch(id,tolerance='1%',power_rating='0.1W')
patch('DO_SUPPRESS',quantity=0,assembly='DNP',observations='No additional inductive clamp selected. Initial0.5A resistive-load bringup; verify actual repetitive inductive energy before using inductive loads.')
dec['active_patches']['ACTIVE_SN74LVC2T45DCTR']=dict(quantity=0,assembly='DNP',selection_status='SUPERSEDED',capture_status='NOT_POPULATED',electrical_status='PROVISIONAL',observations='Superseded for DO drive: loadedVOH not guaranteed>=4.5V. Historical symbol retained; replace locally with two NPN/PMOS input-driver channels. No global ECO.')
record('ACTIVE_SN74LVC2T45DCTR','SUPERSEDED_2026_11_08')
dec['active_patches']['ACTIVE_BSP75NTA']=dict(electrical_status='DERIVED_PENDING_REVIEW',verification_status='CALCULATED',capture_status='CONNECTION_SPEC_READY_NATIVE_IMPLEMENTATION_PENDING',selection_status='ENGINEERING_SELECTED',pin_pad_check='VERIFIED IN,D,S,S_TAB functional pad positions from Diodes DS33016 pp1,8',action='Implement source-backed discrete5V driver; verify IN-to-SOURCE>=4.5V and OFF during reset before loads',observations='BSP source/lands closed. 0.5A resistive prototype target, external24V load supply; electrical testing not yet performed.')
record('ACTIVE_BSP75NTA')
for mpn in ['MMBT3904-7-F','DMP2035U-7']:
 a=asset_for(mpn);id=a['asset_id'];dec['active_patches'][id]=dict(quantity=2,assembly='REQUIRED',electrical_status='DERIVED_PENDING_REVIEW',capture_status='CONNECTION_SPEC_READY_NATIVE_IMPLEMENTATION_PENDING',selection_status='ENGINEERING_SELECTED',observations='Selected discrete5V BSP input driver. Pin IDs are manufacturer functional terminal roles; physical top-view mapping verified. No24V load current in these transistors.');record(id)

# Reuse exact same-manufacturer mounting patterns, without redrawing compact glyphs.
before=json.loads((O/'symbols_before.json').read_text())['symbols'];updates=[]
all_assets=[]
for folder in ['library_preparation','electrical_closure','input_protection_freeze','tps26620','ethernet_75ohm','ethernet_1nf','bsp75n_closure']:
 for name in ['cad_assets.json','cad_additions.json']:
  p=O.parent/folder/name
  if p.exists():all_assets+=json.loads(p.read_text(encoding='utf-8'))
for s in before:
 mpn=next((p['value'] for p in s.get('parameters',[]) if p['name'] in ['Manufacturer Part Number','MPN']),'')
 target=('GW_RC0603_YAGEO_REFLOW' if mpn.startswith('RC0603FR-') else 'GW_0603_KEMET_NOMINAL' if mpn.startswith('C0603C') else 'GW_0805_KEMET_NOMINAL' if mpn.startswith('C0805C') else {'C5750X7R2A475K230KA':'GW_C5750_TDK_REFLOW','C3225X7R1C156M250AB':'GW_C3225_TDK_REFLOW','XAL4030-682MEC':'GW_XAL4030_COILCRAFT','XAL4040-103MEC':'GW_XAL4040_COILCRAFT','CL10A105KB8NNNC':'GW_SAMSUNG_CL10_1608_REFLOW','CL21A106KAYNNNE':'GW_SAMSUNG_CL21_2012_REFLOW'}.get(mpn))
 if not target or (s.get('footprints') and all(f['name']==target for f in s['footprints'])):continue
 new=copy.deepcopy(s);new['footprints']=[dict(name=target,is_current=True)]
 # Keep identities, compact graphics, electrical parameters and pin endpoints.
 for p in new.get('parameters',[]):
  if p['name'] in ['CAD_Status','CAD Status']:p['value']='CAD_VERIFIED_SOURCE_LAND;NATIVE_INSTANCE_ECO_PENDING'
  if p['name'] in ['CAD_Limitations','Limitations']:p['value']='Same-manufacturer series mounting geometry verified; prototype mask/paste choices recorded. Electrical application limits unchanged. Native instance links/ECO pending.'
 updates.append(new)
 for a in all_assets:
  if a['symbol']==s['name']:
   a=copy.deepcopy(a);a.update(footprint=target,cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',package_requirement=target,limitations='Exact-MPN/same-manufacturer mounting pattern verified;existing symbol graphics/pins/MPN unchanged. Native instance ECO and assembly review pending.')
   if mpn.startswith(('CL10A','CL21A')):
    a['source']='Samsung officialMLCC_2401 catalogp159 reflowranges;exactproductHTML L/W/Ttolerance:CL10+/-0.10,CL21+/-0.20mm. Midpointlands areexplicitprototypechoices.'
    a['limitations']='Manufacturerlandrangesverifiedforcorrectbodytolerancerow;selectedmidpointgeometry,mask+.05,paste1:1prototypechoices. X5R+85C andDCbias/applicationassumptionsunchanged. NativeinstanceECOpending.'
   assets.append(a)
 # The canonical10k and2.49k entries are used by DO; keep row assignment explicit.
for a in assets:
 if a['mpn']=='RC0603FR-072K49L' and 'DO_RPDB' not in a['component_ids']:a['component_ids'].append('DO_RPDB')

# Physical RNX A/B interface verified from both local TI drawings. No geometry edit.
a=copy.deepcopy(next(a for a in all_assets if a['asset_id']=='ACTIVE_LMR36015FBRNXR'))
a.update(cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',limitations='RNX0012A/B pin positions and manufacturer copper/mask/stencil readback verified2026-11-08. Both saved alternatives retained. Pin12SW;3musttieSW. CurrentA uses SMD1/2/10/11/12; B preferredNSMD perTI. Require assembler mask/paste capability and lot package verification.');assets.append(a)
dec['active_patches']['ACTIVE_LMR36015FBRNXR']=dict(electrical_status='ELECTRICAL_VERIFIED',capture_status='CONNECTION_SPEC_READY_NATIVE_REPAIRS_PENDING')
for id in ['ACTIVE_STM32H723VET6','TPD4E05U06DQAR']:
 a=copy.deepcopy(next(a for a in all_assets if a['asset_id']==id))
 note=('ST DS13313Rev5 Fig65 p218/PDF219:100pads,0.5pitch,0.3x1.2lands,16.7outer/14.3inner span;physicalCCW map verified. Mask+.05/paste1:1 prototype choices;nativeECO pending.' if id.startswith('ACTIVE_STM') else 'TI SLVSBO7O DQA0010A pp29-30:rounded landsR0.05 usingAltiumhalf-side50%/25%,NSMD+.05;3/8 paste windows0.565x0.36mm at0.10mm stencil. ExternalNC-pass-through continuity must be implemented natively.')
 a.update(cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',limitations=note);assets.append(a)
save('symbol_link_updates.json',updates);save('cad_assets.json',assets);save('bom_decisions.json',dec)
for review in json.loads((O/'geometry_reviews.json').read_text()):
 a=copy.deepcopy(next(a for a in all_assets if a['mpn']==review['mpn'] and a['symbol']==review['mpn']))
 a.update(cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',source=review['source'],limitations=review['limitations']);assets.append(a)
save('cad_assets.json',assets)
identity={}
verified=O/'symbols_verified.json'
if verified.exists():
 for s in json.loads(verified.read_text())['symbols']:
  p={v['name']:v['value'] for v in s.get('parameters',[])}
  mpn=p.get('Manufacturer Part Number',p.get('MPN',''))
  if mpn:identity[mpn]=p.get('Manufacturer','NOT_VERIFIED')
 save('component_identity.json',identity)
print('Prepared late overlay:',len(assets),'assets,',len(updates),'local symbol link updates,',len(dec['new_rows']),'new BOM rows')
