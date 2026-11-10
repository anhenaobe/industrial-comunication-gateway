"""Source-backed CAD input, in mm for footprints and mils for native symbols.

No binary CAD synthesis. This file emits reviewed input for Electronics AI.
Run from the repository root. Datasheets are existing local files; no network.
"""
import csv
import json
from pathlib import Path

OUT = Path(__file__).parent
ROOT = Path('hardware/academic_rev1/libraries')
models = []


def active(mpn, names, types, source, footprint, manufacturer, notes=''):
    pins = []
    half = (len(names)+1)//2
    for i, (name, typ) in enumerate(zip(names, types)):
        left = i < half
        row = i if left else len(names)-1-i
        pins.append(dict(designator=str(i+1), name=name, electrical_type=typ,
                         x=-1000 if left else 1000, y=(half-1-row)*100,
                         length=200, rotation=0 if left else 180))
    model = dict(mpn=mpn, symbol=mpn, pins=pins, source=source,
                 footprint=footprint, manufacturer=manufacturer, notes=notes,
                 rectangle=dict(x1=-800,y1=-100,x2=800,y2=half*100))
    models.append(model)
    return model


mcu = list(csv.DictReader(open('hardware/academic_rev1/mcu_pin_reference.csv', encoding='utf-8-sig')))
names = [r['pin_name'] for r in mcu]
types = ['power' if n.startswith(('VDD','VSS','VBAT','VREF','VCAP')) else
         'input' if n in ('BOOT0','PH0-OSC_IN') else
         'output' if n=='PH1-OSC_OUT' else 'bidirectional' for n in names]
active('STM32H723VET6',names,types,'DS13313 Rev5 fig5, table7 pp57-71, fig65 p218 (PDF p219)',
       'GW_LQFP100_ST_1L','STMicroelectronics','GPIOs use bidirectional ERC type; oscillator pins have dedicated types. VCAP power pins are LDO outputs, never connect to VDD.')
active('DP83826IRHBR',
       ['ModeSelect','CEXT','VDDA3V3','RD_M','RD_P','TD_M','TD_P','XO','XI/50MHzIn','RBIAS','MDIO','MDC','RX_D3','RX_D2','RX_D1','RX_D0','VDDIO','RX_DV/CRS_DV','RX_CLK/50MHz_RMII','RX_ER','PWRDN/INT','TX_CLK','TX_EN','TX_D0','TX_D1','TX_D2','TX_D3','COL/LED2/TX_ER/GPIO','CRS/LED3','LED0','CLKOUT/LED1','RST_N','GND_EP'],
       ['input','passive','power','bidirectional','bidirectional','bidirectional','bidirectional','output','input','passive','bidirectional','input','bidirectional','bidirectional','bidirectional','bidirectional','power','bidirectional','bidirectional','bidirectional','bidirectional','bidirectional','input','input','input','input','input','bidirectional','bidirectional','bidirectional','bidirectional','input','power'],
       'SNLS647I table5-1 pp5-6; exposed pad p7; RHB0032M 4223725/A PDF pp111-113',
       'GW_RHB0032M_TI','Texas Instruments','Multi-function strap pins conservatively bidirectional. Mode not frozen. EP33 must be soldered to ground; thermal vias are board-level optional, filled/plugged/tented if under paste.')
active('LMR36015FBRNXR',['PGND','VIN','NC','BOOT','VCC','AGND','FB','PG','EN','VIN','PGND','SW'],
       ['power','power','passive','power','power','power','input','open_collector','input','power','power','power'],
       'SNVSB49D p4; RNX0012A 4222858/A PDF pp44-46 and RNX0012B 4223969/C pp47-49',
       'GW_RNX0012A_TI','Texas Instruments','CAD_CANDIDATE: confirm delivered RNX revision A/B. NC3 is externally connected to SW per TI. RNX12 is SW, not a ground exposed pad. Two footprint variants retained.')
active('THVD1420DR',['R','/RE','DE','D','GND','A','B','VCC'],
       ['output','input','input','input','power','bidirectional','bidirectional','power'],
       'SLLSF78B table4-1 p3; D0008A 4214825/C PDF pp30-32','GW_SOIC8_1P27_5P4','Texas Instruments')
active('ATA6561-GAQW',['TXD','GND','VCC','RXD','VIO','CANL','CANH','STBY'],
       ['input','power','power','output','power','bidirectional','bidirectional','input'],
       'DS20005991B pin table p3; C04-2057-OA RevE p19','GW_SOIC8_1P27_5P4','Microchip')
active('ISO1212DBQR',['GND1','VCC1','EN','OUT1','OUT2','NC','NC','GND1','FGND2','IN2','SENSE2','SUB2','SUB1','FGND1','IN1','SENSE1'],
       ['power','power','input','output','output','passive','passive','power','power','input','input','passive','passive','power','input','input'],
       'SLLSEY7G table4-2 p4; DBQ0016A 4214846/A PDF pp44-46','GW_DBQ0016A_TI','Texas Instruments',
       'SUB12 and SUB13 must remain separate floating nets. TI recommends an individual 2x2mm floating copper island for each; these board-level islands are NOT encoded in this package footprint. Never join to either FGND, GND1 or each other. NC6/7 unconnected.')
active('SN74LVC2T45DCTR',['VCCA','A1','A2','GND','DIR','B2','B1','VCCB'],
       ['power','bidirectional','bidirectional','power','input','bidirectional','bidirectional','power'],
       'SCES516N table4-1 p2; DCT0008A 4220784/D PDF pp28-30','GW_DCT0008A_TI','Texas Instruments','Electrical candidate only; no OE pin. VOH at BSP75N input load remains open.')
# Manufacturer shows positional roles, but no terminal numbers. Do not invent
# conventional SOT223 numbering. A role-labelled symbol is independently useful
# for inspection, deliberately has NO footprint, and remains CAD_BLOCKED.
bsp=active('BSP75NTA',['IN','D','S','S_TAB'],['input','passive','power','power'],
           'Diodes DS33016 Rev7-2 pp1,8; terminal numbering absent','', 'Diodes Incorporated',
           'CAD_BLOCKED: terminal identifiers are role names, not manufacturer numbers. Tab=Source, isolated from Drain. Need exact numbered Type DN drawing/model before any placement or footprint binding.')
for p in bsp['pins']:
    p['designator']=p['name']


def pad(n,x,y,w,h,mask=.05,paste=0,shape='roundrect'):
    return dict(designator=str(n),x=x,y=y,width=w,height=h,shape=shape,
                corner_radius=round(min(.05/(min(w,h)/2)*100,100),4) if shape=='roundrect' else 0,
                layer='Top Layer',hole_size=0,rotation=0,
                solder_mask_expansion=mask,solder_mask_expansion_mode='manual',
                paste_mask_expansion=paste,paste_mask_expansion_mode='manual')


footprints=[]
def fp(name,pads,source,body,notes='',paste_windows=None):
    footprints.append(dict(name=name,pads=pads,source=source,body=body,notes=notes,paste_windows=paste_windows or []))

# ST figure65: outside span16.7, inside span14.3, pad1.2x.3, pitch.5.
p=[]
for i in range(25):
    p += [pad(i+1,-6+i*.5,-7.75,.3,1.2),pad(i+26,7.75,-6+i*.5,1.2,.3),
          pad(i+51,6-i*.5,7.75,.3,1.2),pad(i+76,-7.75,6-i*.5,1.2,.3)]
fp('GW_LQFP100_ST_1L',p,models[0]['source'],[14,14],
   'Copper matches ST fig65; mask +0.05mm and 1:1 paste are explicit engineering choices, assembly/fab review pending, not manufacturer-qualified mask/stencil.')
p=[]
for i in range(8):
    p += [pad(i+1,-2.4,1.75-i*.5,.6,.25),pad(i+9,-1.75+i*.5,-2.4,.25,.6),
          pad(i+17,2.4,-1.75+i*.5,.6,.25),pad(i+25,1.75-i*.5,2.4,.25,.6)]
p.append(pad(33,0,0,2.1,2.1,paste=-1.05,shape='rectangle'))
fp('GW_RHB0032M_TI',p,models[1]['source'],[5,5],
   'EP33 paste suppressed; four .94mm square paste windows at +/- .57mm (TI 80% example). No automatic thermal-via drill holes.',
   [dict(x=x,y=y,width=.94,height=.94) for x in [-.57,.57] for y in [-.57,.57]])
for rev in ['A','B']:
    p=[]
    for n,y in [(1,1.125),(2,.475),(3,-.175),(4,-.675),(11,1.125),(10,.475),(9,-.175),(8,-.675)]:
        mask=-.05 if rev=='A' and n in (1,2,10,11) else .05 if rev=='A' else .07
        # A's green SMD openings are the dimensioned .6x.25 lands.
        # Copper extends .05mm beyond each opening edge (4222858/A).
        smd=rev=='A' and n in (1,2,10,11)
        land=pad(n,-.9 if n<=4 else .9,y,.7 if smd else .6,.35 if smd else .25,mask=mask)
        if smd:
            land['corner_radius']=57
        p.append(land)
    p += [pad(n,x,-1.4,.25,.6,mask=.05 if rev=='A' else .07) for n,x in [(5,-.5),(6,0),(7,.5)]]
    land=pad(12,0,.7875,.35 if rev=='A' else .25,1.925 if rev=='A' else 1.825,mask=-.05 if rev=='A' else .07,paste=-1,shape='roundrect')
    if rev=='A':
        land['corner_radius']=57
    p.append(land)
    fp('GW_RNX0012'+rev+'_TI',p,models[2]['source'],[2,3],
       'Confirm actual RNX revision before use. Pin12 SW: no ground tab. Paste12 suppressed, two .25x.812mm windows at y=.2815,1.2935 per drawing; 0.125mm stencil.',
       [dict(x=0,y=y,width=.25,height=.812) for y in [.2815,1.2935]])
def dual(name,n,pitch,span,w,h,source,body,mask):
    p=[]
    for i in range(n//2):
        p += [pad(i+1,-span/2,((n//2-1)/2-i)*pitch,w,h,mask=mask),
              pad(n-i,span/2,((n//2-1)/2-i)*pitch,w,h,mask=mask)]
    fp(name,p,source,body)
dual('GW_SOIC8_1P27_5P4',8,1.27,5.4,1.55,.6,models[3]['source']+'; '+models[4]['source'],[3.9,4.9],.07)
dual('GW_DBQ0016A_TI',16,.635,5.4,1.6002,.4064,models[5]['source'],[3.9,4.9],.0508)
dual('GW_DCT0008A_TI',8,.65,3.8,1.1,.4,models[6]['source'],[2.95,2.8],.07)

payload=dict(active_models=models,footprints=footprints)
(OUT/'model_inputs.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(active=len(models),footprints=len(footprints),pins=sum(len(m['pins']) for m in models))))
