"""Approved prototype overlay; retains all existing component IDs and other circuits."""
import json,csv
from pathlib import Path
O=Path(__file__).parent
base={r['component_id']:r for r in csv.DictReader((O/'before_passive_bom.csv').open(encoding='utf-8-sig'))}
patches={};new=[];records={}
def row(id,mpn,value,tol,rating,package,qty,notes,kind='PASSIVE',assembly='REQUIRED',power='N/A',func=None):
    r=dict(recommended_mpn=mpn,nominal_value=value,tolerance=tol,rated_voltage_or_current=rating,
        package=package,quantity=qty,observations=notes,assembly=assembly,item_kind=kind,power_rating=power,
        electrical_value_source='Approved academic freeze; input_protection_reference section10; manufacturer evidence/input_protection_freeze',
        verification_status='VERIFIED',electrical_status='ELECTRICAL_VERIFIED',cad_route='PROJECT_LOCAL_VERIFIED')
    if func:r['function']=func
    if id in base:patches[id]=r
    else:new.append(dict(clone_of='ETH_RBIAS',component_id=id,subsystem='Entrada',main_reference='NIS3071MT4TWG',**r))
    records[id]=dict(design_approval='PROTOTYPE_APPROVED',validation_scope='SUPERVISED_LAB_24V_18_30V_TARGET',test_status='NOT_ELECTRICALLY_TESTED')

row('IN_FUSE','0451002.MRL','2 A','Manufacturer fuse characteristic','125 VDC','Littelfuse451 SMD',1,
    'User-approved2A backup fuse. Lab current limit1.0A for normal nominal24V startup; no industrial coordination claim. Manufacturer land pattern saved.',kind='AUXILIARY',func='Upstream physical fuse F1')
row('IN_REVERSE','SS3P6L-M3/86A','3 A Schottky','N/A','60 V reverse','SMPC TO-277A',1,
    'User-approved series diode. Both anodes1/2 toVIN_FUSED,largeK toVIN_CLAMP. Power off/discharge before changing polarity.',kind='AUXILIARY')
row('IN_TVS','TDS3311P.C','33 V working','Manufacturer table','42 V maximum specified35A pulse','DFN6 1.6x1.6',1,
    'User-approved replacement for TDS3011P and unreleasedSMBJ33A draft. Pins4/5/6VIN_CLAMP;1/2/3GND. Not continuousOV protection.',kind='AUXILIARY')
row('IN_RLIM','RC0603FR-0762KL','62.0 kOhm','1%','75 V','0603',1,
    'User-approved RLIM to pin7/GND. Figure7 typicalITH~1A,ICB~2A,not exact guarantees. Historical43.2k superseded ONLY as eFuse setting; buck3V3 feedback43.2k retained.',power='0.1 W',func='eFuse current-setting resistor')
row('IN_RFAULT','RC0603FR-0715KL','15.0 kOhm','1%','75 V','0603',1,
    'Optional MCU status implemented:FAULT5 pull-up to3V3,~0.22mA. Fault activeLOW,notPGOOD. No startup dependency.',power='0.1 W',func='FAULT pull-up')
row('IN_BULK','C5750X7R2A475K230KA','4.7 uF','10%','100 V X7R','2220',1,
    'Practical local NIS input bypass,afterD_REV,beforeIN1. No large electrolytic or addedLC filter. Not downstream startup capacitance.',func='NIS local input bypass')
row('IN_HF','C0805C224K1RACTU','220 nF','10%','100 V X7R','0805',1,
    'Parallel HF bypass at NIS IN1/GND close to pins; reuses buck HF MPN.',func='NIS input high-frequency bypass')
row('IN_CDVDT','C0603C680J5GACTU','68 pF option; OPEN by default','5%','50 V C0G','0603',0,
    'DNP;pin6 open for default startup. Reserved68pF footprint permits slower ramp if bring-up observes retries. No jumper-to-ground.',assembly='DNP',func='Optional eFuse slew capacitor')
row('IN_SOUT','SS3P6L-M3/86A','DNP negative-output clamp option','N/A','60 V reverse','SMPC TO-277A',0,
    'DNP footprint only:anodes1/2GND,K24V_ELEC. No inductive electronics load/long harness assumed. This part is NOT guaranteed-.3V clamp; review before population.',kind='AUXILIARY',assembly='DNP',func='Reserved output-clamp footprint')
for n in ['B3','B5']:
    row(n+'_CIN','C5750X7R2A475K230KA','4.7 uF','10%','100 V X7R','2220',2,
        'Two per regulator. ExactTDK bias graph~3.6uF per part at30V;~6.48uF bank after10% allowance. Prototype confirmation by ripple/startup; no industrial characterization gate.')
    row(n+'_CHF','C0805C224K1RACTU','220 nF','10%','100 V X7R','0805',2,
        'Preserve one220nF at each VIN/PGND pair;exactKemet0805 body and manufacturer nominal lands checked.')
    row(n+'_CVCC','C0805C225K5RACTU','2.2 uF','10%','50 V X7R','0805',1,
        'Replaces prior1uF/50VX5R with known0.656uF effective at5V. Prototype assumption>=60% retention gives>=1.188uF. Verify VCC startup and steady ripple; no externalVCC load exceptPG pull-up.')
    row(n+'_COUT','C3225X7R1C156M250AB','15 uF','20%','16 V X7R','1210',3,
        'Preserves TI1MHz table10-1 RATED45uF example. Output only,never24V rail. Bias/stability confirmed during academic load-step test; manufacturerdimensioned footprint now available.')
records['ACTIVE_NIS3071MT4TWG']=dict(design_approval='PROTOTYPE_APPROVED',validation_scope='SUPERVISED_LAB_24V_18_30V_TARGET',test_status='NOT_ELECTRICALLY_TESTED')
records['ACTIVE_LMR36015FBRNXR']=dict(records['ACTIVE_NIS3071MT4TWG'])
active={id:dict(electrical_status='ELECTRICAL_VERIFIED',verification_status='VERIFIED',selection_status='PROTOTYPE_APPROVED',capture_status='READY_FOR_MANUAL_CAPTURE') for id in ['ACTIVE_NIS3071MT4TWG','ACTIVE_LMR36015FBRNXR']}
doc=dict(date='2026-11-07',scope='USER_APPROVED_ACADEMIC_PROTOTYPE; not tested/certified',patches=patches,new_rows=new,record_fields=records,active_patches=active)
(O/'bom_decisions.json').write_text(json.dumps(doc,indent=2)+'\n')
print(len(patches),'updated IDs;',len(new),'new IDs')
