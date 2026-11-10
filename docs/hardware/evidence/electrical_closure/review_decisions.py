"""Reviewed electrical decisions and calculations, consumed by BOM regeneration."""
import json,math
from pathlib import Path
OUT=Path(__file__).parent
patches={}
def setrow(id,**kw): patches.setdefault(id,{}).update(kw)
def decision(id,source,note,state='CALCULATED',electrical='DERIVED_PENDING_REVIEW',**kw):
    setrow(id,electrical_value_source=source,observations=note,verification_status=state,
           electrical_status=electrical,**kw)

clock='FCLK Kyocera TNY1T-H1-DEX01-11 pp3-4,6; S1 table31; S3 sections7.6,8.3.10'
for id in ['MCU_YHSE','ETH_Y25']:
    decision(id,clock,'Selected independent 25MHz CMOS oscillator, one receiver each. VCC4=3V3; GND2=GND; EN1=3V3; OUT3 to PH0 or PHY XI9. No load capacitors. <=15pF total load and PHY phase-noise mask remain qualification gates.',state='PROVISIONAL',electrical='PROVISIONAL',
             quantity=1,assembly='REQUIRED',item_kind='AUXILIARY',nominal_value='25 MHz active CMOS',tolerance='total +/-30 ppm',
             rated_voltage_or_current='1.71..3.63 V supply; 3.3 V selected; load <=15 pF',
             package='2.0x1.6 mm 4-pad',recommended_mpn='KC2016Z25.0000C15XXK',
             function='Independent MCU HSE bypass clock' if id.startswith('MCU') else 'Independent PHY XI clock for RMII Leader')
for id in ['MCU_CHSE','MCU_RHSE','ETH_CXTAL','ETH_RXTAL']:
    decision(id,clock,'Not applicable to selected active CMOS oscillator; retain original requirement ID as DNP. No crystal load/drive network selected.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
decision('ETH_TMAG','FETH Pulse HX1188FNL revB sheets2-3; S4 sheet3/fig6-2',
         'Selected exact HX1188FNL. TD1/3 CT2; RD6/8 CT7; cableTX16/14 CT15; cableRX11/9 CT10; NC4/5/12/13. FNLT differs by tape packaging.',recommended_mpn='HX1188FNL',package='Pulse16 SMT 12.7x9.09 mm',electrical='ELECTRICAL_VERIFIED')
setrow('ETH_TMAG',item_kind='AUXILIARY')
decision('ETH_JRJ45','FETH Cinch CT710001 revB0 10-Jul-2023; S4 J17',
         'Confirmed SS-7188S-A-NF, separate shielded 8P8C. Pin1/2=TX pair,3/6=RX pair;4+5 and7+8 spare pair common-mode terminations. Shield S1/S2 to chassis. Stock risk does not revoke selection.',recommended_mpn='SS-7188S-A-NF',package='CT710001 B0 through-hole',electrical='ELECTRICAL_VERIFIED')
decision('ETH_CCT','S4 fig6-2 sheet3, C45/C46/C55/C56; S3 current-mode MDI',
         'Adopt complete HX1188 EVM termination variant: two parallel100nF at CT2 and two at CT7 to logic GND. No CT tie to3V3 and no extra49.9Ohm MDI terminations.',
         nominal_value='100 nF',tolerance='10%',rated_voltage_or_current='50 V; X7R',power_rating='N/A',
         recommended_mpn='C0603C104K5RACTU',package='0603',quantity=4,electrical='ELECTRICAL_VERIFIED')
decision('ETH_RBOB','S4 fig6-2 and table7-1 R43..46',
         'Four75Ohm EVM resistors: CT15/CT10 to common node feeding CBOB1; RJ45(4+5)/(7+8) each through75Ohm to second node feeding CBOB2. No DC short to logic ground.',
         recommended_mpn='CRCW080575R0FKEA',nominal_value='75 Ohm',tolerance='1%',power_rating='0.125 W',package='0805 resistor',quantity=4,electrical='ELECTRICAL_VERIFIED')
decision('ETH_CBOB','S4 fig6-2 and table7-1 C58/C59',
         'Two separate1nF/2kV EVM AC terminations to chassis. Component2kV rating is not safety certification; verify system insulation classification and exact land pattern before layout.',
         recommended_mpn='C1206C102KGRACAUT O'.replace(' ',''),nominal_value='1 nF',tolerance='10%',rated_voltage_or_current='2000 V; X7R; safety class unverified',package='1206',quantity=2,electrical='PROVISIONAL')
decision('ETH_DESD','S4 sheet3 U13; FESD TI SLVSBO7O table4-2 pp4,29-30',
         'Selected PHY-side TPD4E05U06: PHY TD+/TD- to1/2, RD+/RD- to4/5; grounds3/8 to logic GND. Optional NC pass-through10/9/7/6. Never bridge to cable-side or claim a cable surge rating.',
         state='PROVISIONAL',electrical='PROVISIONAL')
for id in ['ETH_CCHASSIS','ETH_RCHASSIS']:
    decision(id,'S4 C61/R51; S3 section9.4.1; schematic_readiness_gate.md E4',
             'Leave EVM logic-GND/chassis coupling unpopulated until PE/insulation policy is defined. Shield and cable terminations use chassis, not logic GND.',quantity=0,assembly='DNP',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
decision('ETH_RRMII','S3 tables8-6/8-7,8-9/8-10, fig8-13',
         'Freeze ENHANCED, RMII Leader, PHY address0; RX_D2/strap8=1 with2.49k pull-up; strap1 internal1, strap5 default0. Other default straps retained with no LEDs. GPIOs HiZ during POR sampling.',electrical='ELECTRICAL_VERIFIED')
for id in ['ETH_CEXT','ETH_RBIAS']:
    setrow(id,verification_status='CALCULATED',electrical_status='ELECTRICAL_VERIFIED')

for ch in [1,2]:
    decision(f'DI_RTHR{ch}','FDI Firstohm MM rev08-March-2023 pp75-78; S11 section8.2.1.2.1/table5.9/table8-1',
             'Selected MM2041k1%0.25W for NORMAL Type3 operation. At2.75mA and R+1%,P<=7.64mW. Non-P MM204 curve/overload limits do not establish500V line-FGND or1kV system surge. Reflow lands1.3x1.6 innergap1.6mm.',
             recommended_mpn='MM204F1K00TKRTR3K0',package='MELF0204 MM204',power_rating='0.25 W at70C, derated to0 at125C',
             rated_voltage_or_current='200 V maximum working; DC applied drop <3 V; pulse gate separate',tolerance='1%',electrical='DERIVED_PENDING_REVIEW')
    decision(f'DI_RSENSE{ch}','S11 equation1 and table5.9; Yageo local exact-value sheet',
             '562Ohm1%; current limit2.25mA typical; selected Type3. Conservative P at2.75mA and R+1%=4.29mW. SENSE-IN resistor, not across24V.',electrical='ELECTRICAL_VERIFIED')
    decision(f'DI_CIN{ch}','S11 figure8-2/table8-1/section8.4; local KEMET sheet',
             '10nF100V SENSE-to-field COM. TI Type3/10nF test setup lists500V line-FGND,1kV other surge modes; not a demonstrated gateway rating. No extra TVS populated.',electrical='ELECTRICAL_VERIFIED')
decision('DI_J','S11 figure8-9 common field ground; selected two-channel group-isolated input configuration',
         'IN1/IN2/FIELD_COM. FGND1 and FGND2 share FIELD_COM on field side only; GND1 remains separate. Group isolation selected, no channel-to-channel rating claimed. Exact connector drawing remains pending.',state='PROVISIONAL',electrical='PROVISIONAL')

for id in ['RS_RPULSE','RS_TVS']:
    decision(id,'S6 fig8-5/table8-1; FSM Bourns CDSOT23-SM712 pp1-3',
             'UNQUALIFIED optional THVD1400 reference network: TWO10Ohm resistors, one in EACH bus line. THVD1420 shares -7..+12V common-mode and +/-16V absmax, but SM712 positive clamp19/20/26V exceeds absmax. Do not transfer1kV claim. Retain conditional positions; selected115200baud circuit uses built-in device protection only.',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
decision('RS_RT','S6 fig8-1/section8.2; calculated3.412V squared/118.8Ohm=98mW',
         '120Ohm end termination only if physical bus end, jumper normally OPEN at intermediate node.0.25W minimum candidate; max fault/ambient rating still required. No external bias by default.',state='CALCULATED')
for id in ['RS_RDE','RS_RRE']:
    setrow(id,observations=('10k default: DE low, nRE high, MCU GPIOs HiZ at reset.115200baud8N1 half-duplex selected; exact FOJAN MPN remains unqualified, use documented Yageo alternative after CAD identity update.'))
decision('CAN_STBY','S8 table2.0 p11 and sections1.1/1.2',
         'Internal STBY pull-up75..175k toVIO selects standby while MCU isHiZ. TXD internal20..50k pull-up gives recessive. MCU drives STBY low only after stable supplies; no external pull populated.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
decision('CAN_TVS','S8 table2.0 absmax/ESD; S7 application schematic',
         'No external CAN TVS selected. Use manufacturer basic circuit. Built-in test ratings are component-level, not gateway IEC compliance.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
for id in ['CAN_CBUS','CAN_CMC']:
    decision(id,'S7 sections3.5-3.8; S8 fig1-6',
             'Selected basic CAN-FD transceiver connection; optional bus shunt caps/choke DNP. No unnecessary capacitive load at2Mbps.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
decision('CAN_RSPLIT','S7 section3.5/tableB-2; S8 basic bus application',
         'Retained optional split-termination alternative, NOT selected for simultaneous use. Selected one120Ohm bus-end termination row CAN_RT added separately. Intermediate-node default DNP.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
decision('CAN_CSPLIT','S7 section3.5',
         'DNP with unselected split network. Do not populate alongside selected conventional120Ohm termination.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
for id in ['DO_RPDA','DO_RPDB']:
    decision(id,'S9 table5.5; S10 p4 note8; schematic_readiness_gate.md DO1',
             '10k pull-down intent retained for reset OFF. Translator noOE, correct DIR=VCCA3V3. VOH at actual1.2mA+B pull-down load not guaranteed>=4.5V; full protection drive BLOCKED. Do not approve from nominal5V.',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
for id in ['MCU_RBOOT','RS_RDE','RS_RRE','DO_RPDA','DO_RPDB']:
    setrow(id,recommended_mpn='RC0603FR-0710KL',tolerance='1%',rated_voltage_or_current='75 V maximum; power-limited working voltage',power_rating='0.1 W at70C')
    if id in ['RS_RDE','RS_RRE']:
        setrow(id,observations='10k Yageo selected: DE low and nRE high at MCU reset;115200baud8N1 half-duplex. Exact local Yageo datasheet replaces unqualified FOJAN identity.',electrical_status='ELECTRICAL_VERIFIED',verification_status='CALCULATED')
setrow('MCU_RBOOT',observations='10k Yageo to GND, BOOT0 recovery access to3V3; AN5419 example adopted. Check option bytes during commissioning.',electrical_status='ELECTRICAL_VERIFIED',verification_status='CALCULATED')

for prefix in ['B3','B5']:
    decision(prefix+'_CIN','S5 section10.1 capacitance note,10.2.1.2.6 and11; TDK exact characterization missing',
             'C5750X7R2A475K230KA100V retained. CIN>=4.7uF EFFECTIVE required plus2x220nF HF; quantity cannot be closed from nominal4.7uF. Official curve retrieval403; no bias factor invented.',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
    decision(prefix+'_COUT','S5 table10-1 explicitly RATED CAPACITANCE; section10.1 effective-value note and10.2.1.2.5',
             'Retain3x15uF16V TDK per1MHz table RATED-capacitance example. This explicit table exception does not remove DC-bias/ESR/transient/stability checks. Exact bias/ESR evidence pending; not released.',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
    decision(prefix+'_CVCC','S5 section10.1 and10.2.1.2.8; existing Samsung P9 bias evidence',
             'BLOCKED application: internalVCC is5V and needs1uF/16V ceramic. Existing CL10A105KB8NNNC typical Ceff at5V is only0.656uF before tolerance/T/aging. Retain candidate identity/position, but do not approve single nominal1uF. A qualified replacement/bank and LDO capacitor compatibility are required.',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
    for suffix in ['RFBT','RFBB']:
        setrow(prefix+'_'+suffix,electrical_status='ELECTRICAL_VERIFIED',verification_status='CALCULATED')
    decision(prefix+'_L','S5 equations4-5; FL Coilcraft doc806-1 and806-4',
             'Retain exact Coilcraft6.8uH(B3)/10uH(B5). Nominal/load ripple and DCR calculations in electrical_calculations.json.25C Isat/Irms suffice for normal design load; hot/fault Isat and core loss still unqualified.',state='CALCULATED',electrical='DERIVED_PENDING_REVIEW')

decision('IN_REVERSE','FIN TDK-Lambda external DC-DC components figure5; Vishay88987 SS3P6L ratings',
         'Selected prototype topology: one series SS3P6L after input fuse, not redundant ORing. Exact packaging suffix/cooling and reverse transient envelope remain pending; no claim of IEC robustness.',
         recommended_mpn='SS3P6L-M3/86A',package='SMPC TO-277A',quantity=1,assembly='REQUIRED',state='PROVISIONAL',electrical='PROVISIONAL')
decision('IN_TVS','FIN Littelfuse SMBJ series electrical table SMBJ33A; S5 input max60V',
         'Candidate unidirectional SMBJ33A AFTER series reverse diode: cathodeVIN_PROT,anodeGND.33Vstandoff,53.3Vclamp@11.3A specified pulse. Only6.7V buck headroom before tolerances/parasitics/temperature; no sustained OV protection or DO36V fault guarantee. NOT released.',
         recommended_mpn='SMBJ33A',package='SMB DO-214AA',quantity=1,assembly='REQUIRED',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
decision('IN_FUSE','FIN TDK-Lambda figure5; current budget in electrical_calculations.json',
         'Single fuse ahead of reverse diode/clamp. Current/time-current/I2t/interrupt rating cannot be selected until DO load faults, supply limit, inrush and TVS coordination are defined. No guessed fuse MPN.',quantity=1,assembly='REQUIRED',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')
decision('IN_FILTER','S5 section11; FIN TDK-Lambda input filter guidance',
         'No additional LC stage selected; local mandated buck decoupling remains. Bulk/damping needs source/cable impedance. Avoid unreviewed high-Q input resonance.',quantity=0,assembly='DNP',electrical='ELECTRICAL_VERIFIED')
decision('IN_BULK','S5 section11; selected prototype front-end, fault coordination pending',
         'Bulk after protection, voltage rating must exceed actual clamp including overshoot;35V professor part is unsuitable. C/ESR/MPN pending source/cable and start-up analysis.',quantity='',assembly='REQUIRED',state='BLOCKED',electrical='ELECTRICAL_BLOCKED')

new_rows=[
 {'clone_of':'ETH_CVDDIO_10N','component_id':'MCU_COSC','subsystem':'MCU','function':'10nF bypass for MCU active oscillator','main_reference':'KC2016Z25.0000C15XXK','quantity':1,'electrical_value_source':clock,'observations':'Kyocera section8 requires10nF close toVCC4/GND2. No crystal load capacitors.','verification_status':'CALCULATED','electrical_status':'ELECTRICAL_VERIFIED'},
 {'clone_of':'ETH_CVDDIO_10N','component_id':'ETH_COSC','subsystem':'Ethernet','function':'10nF bypass for PHY active oscillator','main_reference':'KC2016Z25.0000C15XXK','quantity':1,'electrical_value_source':clock,'observations':'Kyocera section8 requires10nF close toVCC4/GND2.','verification_status':'CALCULATED','electrical_status':'ELECTRICAL_VERIFIED'},
 {'clone_of':'RS_RT','component_id':'CAN_RT','subsystem':'CAN','function':'Optional conventional bus-end120Ohm termination','main_reference':'ATA6561-GAQW','quantity':1,'assembly':'CONDITIONAL','recommended_mpn':'TBD','electrical_value_source':'S8 basic CAN bus120Ohm termination; endpoint assumption','observations':'Populate through jumper only at physical cable end; leave unpopulated at intermediate node. Does not set PCB differential impedance.','verification_status':'CALCULATED','electrical_status':'DERIVED_PENDING_REVIEW'},
]
result={'date':'2026-11-07','patches':patches,'new_rows':new_rows,
        'architecture':'oneRS485,oneCAN,twoDI,twoDO,twoindependentbucks,single18-30Vinput',
        'note':'Selected for capture is independent from electrical qualification, CAD qualification and industrial compliance.'}
(OUT/'bom_decisions.json').write_text(json.dumps(result,indent=2)+'\n')

# Calculations use datasheet values or explicitly labelled engineering allowances.
rails={
 '3V3':{'MCU_all_peripherals_550MHz_Tj105C_max_mA':430,'PHY_100BaseTX_leader_max_mA':70,
        'THVD1420_60mA_output_bound_plus1p8mA_quiescent_mA':61.8,'ISO1212_logic_max_mA':1.9,
        'ATA6561_VIO_max_mA':.5,'two_oscillators_allowance_mA':20,'misc_IO_debug_translator_allowance_mA':35},
 '5V':{'ATA6561_dominant_max_mA':70,'BSP_inputs_two_at5V_max_mA':2.4,
       'two10k_output_pulldowns_mA':1,'translator_switching_and_misc_allowance_mA':10}}
calculations={'method':'Manufacturer bounds plus labelled engineering allowances; not measured consumption. DO drain current excluded from buck rails.',
              'rails_mA':rails,'rail_totals_mA':{k:sum(v.values()) for k,v in rails.items()},'design_limits_mA':{'3V3':700,'5V':100},'regulator_rating_mA':1500,'bucks':{}}
for key,vout,load,L,dcr in [('B3',3.3,.7,6.8e-6,.0741),('B5',5,.1,10e-6,.0924)]:
    ripple=vout*(1-vout/30)/(L*.8*.85e6)
    irms=math.sqrt(load**2+ripple**2/12)
    rb=43200 if key=='B3' else 24900
    calculations['bucks'][key]={'L_H':L,'ripple_nominal_A':vout*(1-vout/30)/(L*1e6),'ripple_fmin_Lminus20_A':ripple,
      'normal_load_A':load,'peak_normal_A':load+ripple/2,'rms_normal_A':irms,'inductor_DCR_loss_25C_W':irms**2*dcr,
      'peak_at1p5A_A':1.5+ripple/2,'ton_at30V_fmax_ns':vout/30/1.15e6*1e9,
      'feedback_nominal_V':1+100000/rb,'feedback_min_V':.985*(1+99000/(rb*1.01)),
      'feedback_max_V':1.015*(1+101000/(rb*.99)),
      'thermal_note':'No efficiency/core-loss or effective RthetaJA measured; datasheet RthetaJA is not a board-temperature guarantee.'}
calculations['DI']={'typical_current_mA':2.25,'formula_VIH_typ_V':8.25+2.25,'formula_VIL_typ_V':7.1+2.25,
 'authoritative_table5p9_VIH_typ_max_V':[10.4,10.95],'authoritative_table5p9_VIL_min_typ_V':[8.7,9.2],
 'RTHR_max_continuous_W':(.00275)**2*1010,'RSENSE_max_continuous_W':(.00275)**2*562*1.01,
 'pulse_example_only':'500V actually across1k gives250W initially; compare the actual resistor waveform/energy, not the generator setting, with the MM204 curve. Not a declared survival test.'}
calculations['DO']={'cold_Pconduction_per_0p5A_W':.5**2*.675,'cold_deltaT_208CperW_C':.5**2*.675*208,
 'warning':'RDS increases with temperature; these cold calculations are not hot-current approval. DS33016 p5 gives520mA at85C minimum copper, only20mA above proposed0.5A, for its own stated conditions.',
 'VI_protection_min_V':4.5,'translator_guaranteed_VOH_at4p5V_32mA_V':3.8,'protection_drive_verified':False}
calculations['input']={'logic_buck_input_bound_at18V_eta_assumed0p75_A':(3.3*.7+5*.1)/(18*.75),
 'including_2x0p5A_DO_A':1+(3.3*.7+5*.1)/(18*.75),'eta_assumption':'0.75 is engineering budgeting only, not measured efficiency',
 'SMBJ33A_nominal_clamp_to_60V_headroom_V':60-53.3,'fault_coordination':'BLOCKED'}
(OUT/'electrical_calculations.json').write_text(json.dumps(calculations,indent=2)+'\n')
print('Reviewed BOM patches',len(patches),'additional rows',len(new_rows), 'rail totals mA',calculations['rail_totals_mA'])
