"""Source-backed pin/role reservation; documentation only, not schematic emission."""
import csv,json
from pathlib import Path
ROOT=Path.cwd();OUT=Path(__file__).parent
pins={r['pin_name']:r['physical_pin'] for r in csv.DictReader((ROOT/'hardware/academic_rev1/mcu_pin_reference.csv').open(encoding='utf-8-sig'))}
rows=[]
def bind(role,mpn,pin,name,net,source,status='ACCEPTED_FOR_CAPTURE',note=''):
    rows.append(dict(component_role=role,mpn=mpn,pin=str(pin),pin_name=name,net_role=net,
                     source=source,status=status,notes=note))
for pin in [11,27,50,75,100]:bind('MCU','STM32H723VET6',pin,'VDD','3V3','S1 fig5/table7')
for pin in [10,26,49,74,99]:bind('MCU','STM32H723VET6',pin,'VSS','GND','S1 fig5/table7')
for name,pin,net in [('VDDA',21,'3V3_ANALOG'),('VSSA',19,'GND'),('VREF+',20,'3V3_ANALOG'),('VBAT',6,'3V3'),('VCAP',48,'VCORE_CAP'),('VCAP',73,'VCORE_CAP'),('BOOT0',94,'BOOT0'),('NRST',14,'NRST')]:
    bind('MCU','STM32H723VET6',pin,name,net,'S1 fig5/table7/table14; S2 table2/fig19',note='VCORE_CAP is internal LDO output, never3V3;2.2uF at each VCAP' if name=='VCAP' else '')
assigned={'PH0':'MCU_HSE25','PH1':'NC_HSE_BYPASS','PA13':'SWDIO','PA14':'SWCLK',
          'PA1':'RMII_REF50','PA2':'MDIO','PC1':'MDC','PA7':'RMII_CRS_DV','PC4':'RMII_RXD0','PC5':'RMII_RXD1','PB11':'RMII_TX_EN','PB12':'RMII_TXD0','PB13':'RMII_TXD1',
          'PD8':'RS485_TXD','PD9':'RS485_RXD','PD10':'RS485_DE','PD11':'RS485_nRE',
          'PD0':'CAN_RXD','PD1':'CAN_TXD','PE7':'CAN_STBY','PE2':'DO1_LOGIC','PE3':'DO2_LOGIC','PE4':'DI1_LOGIC','PE5':'DI2_LOGIC','PE6':'PHY_nRESET'}
for name,net in assigned.items():
    bind('MCU','STM32H723VET6',pins[name],name,net,'S1 table7 LQFP100; selected GPIO reservations',
         'BLOCKED' if net.startswith('DO') else 'CONDITIONAL_CAPTURE' if '25' in net else 'ACCEPTED_FOR_CAPTURE',
         'Pin reservation only; AF selection and reset-state firmware must be reviewed. USART3 PD8/9; FDCAN1 PD0/1; Ethernet AF pins.')
assert len({r['pin'] for r in rows if r['component_role']=='MCU'})==len([r for r in rows if r['component_role']=='MCU'])
for role,net in [('OSC_MCU','MCU_HSE25'),('OSC_PHY','PHY_XI25')]:
    for pin,name,node in [(1,'STANDBY','3V3'),(2,'GND','GND'),(3,'OUT',net),(4,'VCC','3V3')]:
        bind(role,'KC2016Z25.0000C15XXK',pin,name,node,'FCLK table2 pp4,6','CONDITIONAL_CAPTURE','10nF VCC-GND; <=15pF output load and PHY phase noise pending')
for pin,name,net in [(3,'VDDA3V3','3V3'),(17,'VDDIO','3V3'),(33,'GND_EP','GND'),(2,'CEXT','CEXT_2nF'),(10,'RBIAS','RBIAS_6K49'),(8,'XO','NC_XO'),(9,'XI','PHY_XI25'),
                     (7,'TD_P','MDI_TXP'),(6,'TD_M','MDI_TXN'),(5,'RD_P','MDI_RXP'),(4,'RD_M','MDI_RXN'),
                     (11,'MDIO','MDIO'),(12,'MDC','MDC'),(19,'RX_CLK','RMII_REF50'),(18,'CRS_DV','RMII_CRS_DV'),(16,'RX_D0','RMII_RXD0'),(15,'RX_D1','RMII_RXD1'),
                     (23,'TX_EN','RMII_TX_EN'),(24,'TX_D0','RMII_TXD0'),(25,'TX_D1','RMII_TXD1'),(32,'RST_N','PHY_nRESET')]:
    bind('PHY','DP83826IRHBR',pin,name,net,'S3 table5-1, section8.3.10; straps defined separately')
for pin,name,net in [(1,'TD+','MDI_TXP'),(3,'TD-','MDI_TXN'),(6,'RD+','MDI_RXP'),(8,'RD-','MDI_RXN'),(2,'TCT','PHY_TX_CT'),(7,'RCT','PHY_RX_CT'),
                     (16,'TX+','CABLE_TXP'),(14,'TX-','CABLE_TXN'),(11,'RX+','CABLE_RXP'),(9,'RX-','CABLE_RXN'),(15,'CMT_TX','CABLE_TX_CT'),(10,'CMT_RX','CABLE_RX_CT')]:
    bind('MAGNETICS','HX1188FNL',pin,name,net,'FETH Pulse revB sheet2; S4 sheet3')
for role,mpn,ps in [
 ('RS485','THVD1420DR',[(1,'R','RS485_RXD'),(2,'nRE','RS485_nRE'),(3,'DE','RS485_DE'),(4,'D','RS485_TXD'),(5,'GND','GND'),(6,'A','RS485_A'),(7,'B','RS485_B'),(8,'VCC','3V3')]),
 ('CAN','ATA6561-GAQW',[(1,'TXD','CAN_TXD'),(2,'GND','GND'),(3,'VCC','5V'),(4,'RXD','CAN_RXD'),(5,'VIO','3V3'),(6,'CANL','CANL'),(7,'CANH','CANH'),(8,'STBY','CAN_STBY')]),
 ('DI','ISO1212DBQR',[(1,'GND1','GND'),(2,'VCC1','3V3'),(3,'EN','3V3'),(4,'OUT1','DI1_LOGIC'),(5,'OUT2','DI2_LOGIC'),(6,'NC','NC6'),(7,'NC','NC7'),(8,'GND1','GND'),(9,'FGND2','FIELD_COM'),(10,'IN2','DI2_IN'),(11,'SENSE2','DI2_SENSE'),(12,'SUB2','FLOAT_SUB2'),(13,'SUB1','FLOAT_SUB1'),(14,'FGND1','FIELD_COM'),(15,'IN1','DI1_IN'),(16,'SENSE1','DI1_SENSE')])]:
    for pin,name,net in ps:bind(role,mpn,pin,name,net,'S6 pin table / S8 pin table / S11 table4-2 respectively')
for role,rail in [('BUCK3V3','3V3'),('BUCK5V','5V')]:
    for pin,name,net in [(1,'PGND','GND'),(2,'VIN','VIN_PROT'),(3,'NC',role+'_SW'),(4,'BOOT',role+'_BOOT'),(5,'VCC',role+'_VCC_INTERNAL'),(6,'AGND','GND'),(7,'FB',role+'_FB'),(8,'PG','NC_'+role+'_PG'),(9,'EN','VIN_PROT'),(10,'VIN','VIN_PROT'),(11,'PGND','GND'),(12,'SW',role+'_SW')]:
        bind(role,'LMR36015FBRNXR',pin,name,net,'S5 pin table/figure10-1; NC3 joins SW12',
             'CONDITIONAL_CAPTURE','CIN/COUT and input coordination unresolved; output rail '+rail+' after correct inductor')
for pin,name,net in [(1,'D1+','MDI_TXP'),(2,'D1-','MDI_TXN'),(3,'GND','GND'),(4,'D2+','MDI_RXP'),(5,'D2-','MDI_RXN'),(6,'NC','MDI_RXN'),(7,'NC','MDI_RXP'),(8,'GND','GND'),(9,'NC','MDI_TXN'),(10,'NC','MDI_TXP')]:
    bind('ETH_ESD','TPD4E05U06DQAR',pin,name,net,'FESD table4-2; S4 U13 sheet3','CONDITIONAL_CAPTURE',
         'NC pads are not internally series-connected. EVM pass-through needs continuous external copper joining the same-net pads.')
for pin,name,net in [(1,'VCCA','3V3'),(2,'A1','DO1_LOGIC'),(3,'A2','DO2_LOGIC'),(4,'GND','GND'),(5,'DIR','3V3'),(6,'B2','DO2_DRIVE'),(7,'B1','DO1_DRIVE'),(8,'VCCB','5V')]:
    bind('DO_TRANSLATOR','SN74LVC2T45DCTR',pin,name,net,'S9 pin table; DIR=VCCA','BLOCKED','Intended direction only; loaded >=4.5V BSP protection drive is NOT verified')
with (OUT/'capture_pin_bindings.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Documented pin-role bindings:',len(rows))
