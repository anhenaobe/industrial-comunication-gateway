"""Latest reviewed application proposal, applied after the approved NIS freeze.
No schematic/PCB generation. Component selection and setting approval separate.
"""
import json,math,csv,hashlib
from pathlib import Path
O=Path(__file__).parent;R=Path.cwd();L=R/'hardware/academic_rev1/libraries'
src='TI SLVSDT4F Table6-1/Table7.5, Eq2/5/6/7, Fig10-1; input_protection_reference section10'
patches={};new=[];records={};assets=[]
def record(id,approval='PROPOSED_APPLICATION_VALUES'):
    records[id]=dict(design_approval=approval,validation_scope='SUPERVISED_LAB_24V_18_30V_TARGET; CALCULATED_NOT_TESTED',test_status='NOT_ELECTRICALLY_TESTED')
def patch(id,mpn,value,notes,quantity=1):
    patches[id]=dict(recommended_mpn=mpn,nominal_value=value,main_reference='TPS26620DRCR',quantity=quantity,
       assembly='REQUIRED' if quantity else 'DNP',verification_status='CALCULATED',electrical_status='DERIVED_PENDING_REVIEW',
       electrical_value_source=src,observations=notes,cad_route='PROJECT_LOCAL_VERIFIED')
    record(id)
patch('IN_RLIM','RC0603FR-0713K3L','13.3 kOhm',
      'Pin7 ILIM to EF_RTN pin5; Eq5 6.636/13.3=0.49895A. Table7.5 0.47/0.50/0.52A at13.3k test condition. Supersedes NIS62k, not buck FB resistors.')
patches['IN_RLIM'].update(tolerance='1%',rated_voltage_or_current='75 V',power_rating='0.1 W',package='0603')
patch('IN_CDVDT','C0603C103K1RACTU','10 nF',
      'Pin8 dVdT to EF_RTN. Eq2 ramp4.92ms at24V; not NIS68pF option. 21.648uF COUT plus0.217A budget gives~0.322A typ startup estimate.')
patches['IN_CDVDT'].update(tolerance='10%',rated_voltage_or_current='100 V; X7R',package='0603',power_rating='N/A')
patch('IN_RFAULT','RC0603FR-0715KL','15.0 kOhm',
      'DNP historical pull-up option. TPS pin9 FLT left NC in simple capture configuration; no fault line populated.',0)
for id in ['IN_BULK','IN_HF']:
    patches[id]=dict(main_reference='TPS26620DRCR',function='TPS26620 local input bypass' if id=='IN_BULK' else 'TPS26620 input high-frequency bypass',observations='Retained input bypass: VIN_CLAMP/pin1 to GND_PWR/pin6, NOT EF_RTN; TI section9.3.8 explicit IN-to-GND recommendation. Local short return.')
for id in ['DO_CVCCA3V3','DO_CVCCB5']:
    patches[id]=dict(main_reference='SN74LVC2T45DCTR candidate drive; not electrically approved')
for id,mpn,value,fun in [('IN_UV_TOP','RC0603FR-07768KL','768 kOhm','IN to UVLO divider top'),
 ('IN_UV_MID','RC0603FR-0733K2L','33.2 kOhm','UVLO to OVP divider middle'),
 ('IN_UV_BOTTOM','RC0603FR-0730K1L','30.1 kOhm','OVP to EF_RTN divider bottom')]:
    patch(id,mpn,value,fun+'; nominal UV rising15.759V / OV rising33.141V, local IN-to-RTN reference. Proposed academic thresholds.')
    patches[id].update(function=fun,tolerance='1%',rated_voltage_or_current='75 V',power_rating='0.1 W',package='0603')
    new.append(dict(clone_of='ETH_RBIAS',component_id=id,subsystem='Entrada',**patches.pop(id)))
for mpn,ids in [('RC0603FR-0713K3L',['IN_RLIM']),('RC0603FR-07768KL',['IN_UV_TOP']),
 ('RC0603FR-0733K2L',['IN_UV_MID']),('RC0603FR-0730K1L',['IN_UV_BOTTOM']),('C0603C103K1RACTU',['IN_CDVDT'])]:
    fp='GW_RC0603_YAGEO_REFLOW' if mpn.startswith('RC') else 'GW_0603_KEMET_NOMINAL'
    assets.append(dict(asset_id=mpn,item_kind='PASSIVE',component_ids=ids,mpn=mpn,symbol=mpn,footprint=fp,
       source=src,cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',
       limitations='Exact manufacturer spec and existing source-bound lands; saved readback. Application settings proposed, hardware not tested.',package_requirement=fp))
fp='GW_DRC0010J_TI_TPS2662'
assets.append(dict(asset_id='ACTIVE_TPS26620DRCR',item_kind='ACTIVE',component_ids=[],mpn='TPS26620DRCR',symbol='TPS26620DRCR',footprint=fp,
 source=src,cad_status='CAD_CANDIDATE',symbol_status='CAD_VERIFIED',footprint_status='CAD_CANDIDATE',
 limitations='Numbered pins1-10/EP11 verified; RTN != GND. Manufacturer geometry saved; four EP copper regions require native custom-pad11 conversion and net inheritance verification before PCB use.',package_requirement=fp))
record('ACTIVE_TPS26620DRCR','APPROVED_COMPONENT_SELECTION');record('ACTIVE_NIS3071MT4TWG','SUPERSEDED')
active={
 'ACTIVE_NIS3071MT4TWG':dict(quantity=0,assembly='DNP',selection_status='SUPERSEDED',capture_status='HISTORICAL_ONLY',
     electrical_status='PROVISIONAL',verification_status='SUPERSEDED',observations='Superseded by TPS26620DRCR; retained native historical resource and CAD mapping. No placement in academic circuit.'),
 'ACTIVE_TPS26620DRCR':dict(quantity=1,assembly='REQUIRED',selection_status='APPROVED_COMPONENT_SELECTION',
     capture_status='SYMBOL_READY_FOOTPRINT_NATIVE_CHECK_PENDING',electrical_status='DERIVED_PENDING_REVIEW',verification_status='CALCULATED',
     pin_pad_check='VERIFIED numbered1-10/EP11; extension net inheritance UNVERIFIED',
     dimensional_check='TI DRC0010J dimensions saved; native custom-pad and corner review pending',
     action='Finish native thermal-pad11 conversion/net check before PCB use')}
(O/'bom_decisions.json').write_text(json.dumps(dict(date='2026-11-07',patches=patches,new_rows=new,record_fields=records,active_patches=active),indent=2)+'\n')
(O/'cad_assets.json').write_text(json.dumps(assets,indent=2)+'\n')
# Reviewable formulas and simple independent tolerance bounds (resistor1%).
r1,r2,r3=768.,33.2,30.1
uv=lambda a,b,c,v:v*(a+b+c)/(b+c)
ov=lambda a,b,c,v:v*(a+b+c)/c
cmax=4*(4.7+.22)*1.1*1e-6
calc=dict(ilim_A=6.636/13.3,ilim_with_R1pct_A=[6.636/(13.3*1.01),6.636/(13.3*.99)],
 ilim_datasheet_A=[.47,.5,.52],ilim_screen_low_A=.47/1.01,
 uv_rise_V=uv(r1,r2,r3,1.2),uv_fall_typ_V=uv(r1,r2,r3,1.1),ov_rise_V=ov(r1,r2,r3,1.2),ov_fall_typ_V=ov(r1,r2,r3,1.12),
 uv_rise_bounds_V=[uv(r1*.99,r2*1.01,r3*1.01,1.18),uv(r1*1.01,r2*.99,r3*.99,1.23)],
 ov_rise_bounds_V=[ov(r1*.99,r2*.99,r3*1.01,1.18),ov(r1*1.01,r2*1.01,r3*.99,1.23)],
 COUT_nom_uF=4*(4.7+.22),COUT_max_uF=cmax*1e6,
 default_24V_charge_A=cmax*24/.000660,
 ramps_ms={str(v):20500*v*10e-9*1000 for v in [18,24,30]},
 typ_charge_A=cmax*1.98e-6*24.6/10e-9,
 fast_charge_A=cmax*2.33e-6*25.2/9e-9,
 start_bound_A=.217+cmax*2.33e-6*25.2/9e-9,
 load_W=3.3*.7+5*.1,
 power_typ_W=.217**2*.478+30*.000343,
 power_screen_W=.217**2*.8+30*.000482,
 assumptions=['0.217A conservative nominal load allowance; not a constant-power startup guarantee',
 '3V3/5V load allocation2.81W, buckeff75%, SS3drop0.6V; TPS RON0.8ohm andIQ0.482mA screening give~0.218A at18V',
 'No DO drain current through main electronics input; no extra24V bulk beyond two input banks',
 'Threshold bounds omit leakage; at18V string21.65uA >>20x combined0.2uA max pin leakage',
 'OV/UV thresholds local to IN/RTN after diode; source cutoff shifted by diode drop',
 'Table7.5 1.20V thresholds supersede application prose1.19V for calculation'])
calc['start_bound_A']=.218+cmax*2.33e-6*25.2/9e-9
(O/'calculations.json').write_text(json.dumps(calc,indent=2)+'\n')
manifest=[]
for p in (L/'sources/tps26620').glob('*.pdf'):
    assert p.read_bytes().startswith(b'%PDF-')
    manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
       url='https://www.ti.com/lit/ds/symlink/tps2662.pdf' if p.stem=='tps2662' else 'https://yageogroup.com/download/specsheet/'+p.stem))
(O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(calc,indent=2))
