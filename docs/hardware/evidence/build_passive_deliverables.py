"""Rebuild the two CSVs and per-subsystem BOM tables from reviewed decisions.

No CAD binary parsing, model creation, or electrical validation is performed here.
REQUIRED means part of the documented candidate circuit, not approved for purchase.
"""
import csv
import json
from collections import Counter
from pathlib import Path

OUT = Path('docs/hardware')
LIB = 'hardware/academic_rev1/libraries/'
inventory = {r['referencia_cad']: r for r in csv.DictReader(
    (OUT / 'library_inventory.csv').open(encoding='utf-8-sig'))}
rows = []


def add(id, sub, function, parent, value='TBD', tolerance='TBD', rating='TBD',
        power='N/A', package='TBD', mpn='TBD', source='', notes='', qty=1,
        assembly='REQUIRED', state='PROVISIONAL', teacher='', kind='PASSIVE',
        electrical='PROVISIONAL', external_symbol='', external_footprint=''):
    symbol, footprint, origin = 'MISSING', 'MISSING', 'MISSING'
    route = 'EXTERNAL_REQUIRED'
    if teacher:
        candidate = inventory[teacher]
        symbol = teacher
        footprint = candidate['encapsulado_referencia_cad']
        origin = LIB + 'Professor_shared.SchLib + Professor_shared.PcbLib'
        route = 'TEACHER_EXACT_CANDIDATE' if mpn == candidate['mpn'] else 'TEACHER_GENERIC_CANDIDATE'
        notes += ' Modelo candidato existente; sin cotejo visual de pads/pines en Altium.'
    elif external_symbol:
        symbol, footprint = external_symbol, external_footprint
        origin = LIB + external_symbol + '.SchLib / .PcbLib'
        route = 'EXTERNAL_PRESENT_CANDIDATE'
    row = dict(component_id=id, subsystem=sub, function=function, main_reference=parent,
               nominal_value=value, tolerance=tolerance, rated_voltage_or_current=rating,
               power_rating=power, package=package, recommended_mpn=mpn,
               symbol=symbol, footprint=footprint, cad_origin=origin,
               electrical_value_source=source, verification_status=state,
               observations=notes.strip(), quantity='' if qty is None else qty,
               assembly=assembly, item_kind=kind, electrical_status=electrical,
               cad_status='BLOCKED' if symbol != 'MISSING' else 'MISSING',
               cad_route=route, design_reference='UNASSIGNED',
               specification_key='|'.join([value,tolerance,rating,power,package,mpn]))
    rows.append(row)


CAP = 'Cap_0.1uF_0603_50V'
CAP8 = 'Cap_10uF_0805_25V_'
RES = 'Res_10k_0603_1/10W'
C100 = dict(value='100 nF', tolerance='10%', rating='50 V; X7R; -55..125 C',
            package='0603', mpn='C0603C104K5RACTU', teacher=CAP,
            notes='Ficha KEMET local p1. Adaptar parametros; no usar el Y5V 0603F104Z500CT como equivalente.')
C1 = dict(value='1 uF', tolerance='10%', rating='50 V; X5R; -55..85 C',
          package='0603', mpn='CL10A105KB8NNNC', teacher='Cap_1uF_0603_50V',
          notes='Samsung ficha oficial; Ceff/ESR pendientes por aplicacion. Limite X5R 85 C: no homologado para ambiente superior.')
C10N = dict(value='10 nF', tolerance='10%', rating='100 V; X7R; -55..125 C',
            package='0603', mpn='C0603C103K1RACTU', teacher=CAP,
            notes='Ficha KEMET local DI_CIN p1; no confundir con externo CL10B103KA8WPNC 25 V.')
R10K = dict(value='10 kOhm', tolerance='5%', rating='>= 3.3 V; tension de trabajo por verificar',
            power='0.1 W', package='0603', mpn='FRC0603J103TS', teacher=RES,
            notes='Ratings transcritos del CAD; falta ficha FOJAN. Alternativa RC0603FR-0710KL con ficha oficial local, mismo footprint candidato.')

# MCU: actual LQFP100, LDO, no battery, external reference tied to VDDA.
for suffix,pin in enumerate([11,27,50,75,100],1):
    add(f'MCU_CVDD{suffix}','MCU',f'Desacoplo VDD pin {pin}','STM32H723VET6',
        source='S1 fig5/tabla7; S2 tabla2 p7',**C100)
add('MCU_CBULK','MCU','Reserva VDD','STM32H723VET6',value='4.7 uF',tolerance='10%',
    rating='16 V; X7R',package='0805',mpn='C0805C475K4RACTU',teacher=CAP8,
    source='S2 tabla2 p7; P3 ficha KEMET p1',notes='Ceff a 3.3 V pendiente; no sustituir por 10 uF solo por disponibilidad.')
for rail,pin in [('VDDA',21),('VBAT',6),('VREF',20)]:
    add('MCU_C'+rail+'1','MCU',f'{rail} pin {pin}; reserva','STM32H723VET6',source='S1 fig5; S2 tabla2 pp7-8',**C1)
    add('MCU_C'+rail+'2','MCU',f'{rail} pin {pin}; HF','STM32H723VET6',source='S1 fig5; S2 tabla2 pp7-8',**C100)
for n,pin in enumerate([48,73],1):
    add(f'MCU_CVCAP{n}','MCU',f'Salida LDO VCAP pin {pin}','STM32H723VET6',value='2.2 uF',
        tolerance='10% candidato; ST permite 20%',rating='10 V; X7R; ESR <100 mOhm',package='0603',
        mpn='C0603C225K8RACTU',teacher=CAP,source='S1 tabla14 p92; P2 ficha KEMET p1',
        notes='Falta ESR y capacitancia bajo VCORE/temperatura/envejecimiento. No conectar 3.3 V ni carga externa a VCAP.')
add('MCU_CNRST','MCU','NRST pin14 a GND','STM32H723VET6',source='S1 fig18 p135 (0.1 uF)',**C100)
add('MCU_RBOOT','MCU','BOOT0 pin94 a GND','STM32H723VET6',source='S2 seccion5.2 fig19 p30: 10 kOhm ejemplo tipico',**R10K)
add('MCU_YHSE','MCU','Referencia precisa HSE si HSI no satisface FDCAN','STM32H723VET6',
    source='S1 seccion6.3 osciladores; S2 seccion3; ST AN2867',qty=None,assembly='TBD',state='BLOCKED',
    notes='Frecuencia/MPN/CL/ESR/drive y margen de arranque no cerrados. HSI permite minimo MCU; no valida temporizacion CAN-FD.')
add('MCU_CHSE','MCU','Capacitores de carga HSE','STM32H723VET6',
    source='S2 seccion3; ST AN2867',qty=None,assembly='TBD',state='BLOCKED',
    notes='Solo si se adopta cristal: CL=(C1*C2)/(C1+C2)+Cstray. No fijar 22/33 pF sin CL/parasiticos.')
add('MCU_RHSE','MCU','Limitacion drive oscilador HSE si necesaria','STM32H723VET6',
    source='ST AN2867; S1 osciladores',qty=None,assembly='TBD',state='BLOCKED',notes='Solo tras cristal y drive level; no es resistencia obligatoria universal.')
add('MCU_LSE','MCU','Red LSE RTC','STM32H723VET6',qty=0,assembly='DNP',state='PROVISIONAL',
    source='S2 seccion3',notes='Sin requisito RTC preciso en alcance reducido; no incorporar cristal ni dos cargas por defecto.')
for id,fun,value,teacher in [('MCU_JSWD','SWD','6 posiciones','H_Male_6x1_TH_100mil'),('MCU_SRESET','Pulsador reset','SPST-NO','Sw_PUSH_4.5x4.5x5.0xmm'),('MCU_JBOOT','Recuperacion BOOT','2 posiciones','H_Male_2x1_TH_100mil')]:
    add(id,'MCU',fun,'STM32H723VET6',value=value,teacher=teacher,kind='AUXILIARY',
        source='S2 seccion6; propuesta pinout pendiente',state='BLOCKED',notes='Pinout, MPN y orientacion pendientes. No alimentar VDD desde VTref; SWD PA13/PA14 y NRST.')

# PHY: two supply banks, current datasheet; EVM is a reference, not copied wholesale.
for rail in ['VDDA3V3','VDDIO']:
    add(f'ETH_C{rail}_HF','Ethernet',rail+' HF','DP83826IRHBR',source='S3 fig9-6 p99',**C100)
    add(f'ETH_C{rail}_10N','Ethernet',rail+' HF','DP83826IRHBR',source='S3 fig9-6 p99',**C10N)
    add(f'ETH_C{rail}_1U','Ethernet',rail+' reserva','DP83826IRHBR',source='S3 fig9-6 p99',**C1)
    add(f'ETH_C{rail}_10U','Ethernet',rail+' reserva','DP83826IRHBR',value='10 uF',tolerance='10%',rating='25 V; X5R; -55..85 C',
        package='0805',mpn='CL21A106KAYNNNE',teacher=CAP8,source='S3 fig9-6 p99; Samsung ficha oficial',
        notes='Ceff a 3.3 V y temperatura pendientes. No usar para entrada 30 V.')
add('ETH_CEXT','Ethernet','CEXT pin2 a GND','DP83826IRHBR',value='2 nF',tolerance='5% seleccion',rating='50 V; C0G',
    package='0603',mpn='C0603C202J5GACTU',teacher=CAP,source='S3 tabla5-1 p5; P4 ficha KEMET p1',
    notes='Conflicto EVM C57=100 nF; prevalece requisito actual 2 nF, no copiar C57.')
add('ETH_RBIAS','Ethernet','RBIAS pin10 a GND','DP83826IRHBR',value='6.49 kOhm',tolerance='1%',rating='75 V max; limite sqrt(P*R)',
    power='0.1 W @70 C',package='0603',mpn='RC0603FR-076K49L',teacher=RES,source='S3 tabla5-1; P5 ficha Yageo p1',
    notes='P<3.3^2/6490=1.68 mW; actualizacion de valor/MPN sobre simbolo generico pendiente.')
add('ETH_RRMII','Ethernet','RX_D2 strap8 pull-up a VDDIO','DP83826IRHBR',value='2.49 kOhm',tolerance='1%',rating='75 V max; limite sqrt(P*R)',
    power='0.1 W @70 C',package='0603',mpn='RC0603FR-072K49L',teacher=RES,source='S3 tablas8-6/8-7 fig8-13 pp48-49',
    notes='Candidato ENHANCED/RMII leader: ModeSelect NC, strap1=1 default, strap8=1, strap5=0 default. Ver tabla del informe; sin LEDs de straps.')
add('ETH_Y25','Ethernet','Cristal PHY 25 MHz','DP83826IRHBR',value='25 MHz',tolerance='TOTAL <=50 ppm',rating='CL 15..40 pF; ESR <=50 Ohm',
    source='S3 tabla9-2 p97; EVM XTAL1 tabla7-1',state='BLOCKED',
    notes='EVM ECS-250-12-33Q-JES-TR (CL12 pF) no demuestra tabla9-2 actual. Seleccion exacta y drive pendientes; no hay cristal docente.')
add('ETH_CXTAL','Ethernet','Cargas del cristal PHY','DP83826IRHBR',value='TBD segun CL y Cstray',tolerance='C0G <=5%',
    rating='>= VDDIO',package='0603 candidato',teacher='Cap_33pF_0603_50V',source='S3 fig9-4; tabla9-2; EVM C43/C44=22 pF',
    qty=2,state='BLOCKED',notes='33 pF docente solo candidato mecanico; no valor aprobado. Cargas EVM 22 pF no universales.')
add('ETH_RXTAL','Ethernet','R1 de oscilador si requerido','DP83826IRHBR',source='S3 fig9-4; recomendaciones fabricante cristal',qty=None,assembly='TBD',state='BLOCKED')
add('ETH_FB','Ethernet','Ferritas de alimentacion opcionales','DP83826IRHBR',value='60 Ohm @100 MHz candidato',tolerance='25%',rating='2 A; DCR 100 mOhm segun CAD',
    package='0603',mpn='HCB1608KF-600T20',teacher='FB_60_0603_2A',source='S3 fig9-6: opcional',qty=0,assembly='DNP',
    notes='No exigir filtro adicional sin EMC; verificar curva de impedancia y resonancia con banco local si se monta.')
add('ETH_TMAG','Ethernet','Magnetics aislados','DP83826IRHBR',value='1:1; 350 uH candidato',tolerance='Relacion +/-2%',rating='HPOT >=1500 Vrms; limites tabla9-1',
    package='12.7x9.09 mm segun EVM',mpn='HX1188FNLT',source='S3 tabla9-1; S4 T2 y BOM p28',state='BLOCKED',
    notes='Candidato oficial EVM; falta ficha exacta Pulse/pinout/land pattern. No confundir inductor de buck.')
add('ETH_CCT','Ethernet','Derivacion center taps lado PHY','DP83826IRHBR',value='2 nF',tolerance='TBD',rating='TBD',
    source='S3 fig9-2 p95',qty=2,state='BLOCKED',notes='No copiar 4x100 nF EVM sin revisar red HX1188; coordenar con magnetics y jack.')
add('ETH_RBOB','Ethernet','Terminacion lado cable','DP83826IRHBR',value='75 Ohm',tolerance='1% objetivo',power='>=0.125 W candidato EVM',
    package='TBD',source='S3 fig9-2: dos; S4 R43..46: cuatro',qty=None,state='BLOCKED',
    notes='Cantidad depende de pares usados/no usados y circuito interno RJ45; no sumar ambas redes.')
add('ETH_CBOB','Ethernet','Acoplo terminacion a chasis','DP83826IRHBR',value='TBD',rating='Aislamiento por definir; EVM 2 kV',
    source='S3 fig9-2 10 nF; S4 C58/C59=1 nF/2 kV',qty=None,state='BLOCKED',notes='Topologias diferentes: resolver al seleccionar jack/magnetics.')
add('ETH_CCHASSIS','Ethernet','Acoplo chasis/GND','DP83826IRHBR',value='4.7 nF candidato EVM',rating='2 kV candidato; seguridad por revisar',
    package='1812 EVM; >=1206 segun S3',mpn='1812GC472KAT1A',source='S3 seccion9.2.5.3; S4 C61 BOM p22',assembly='CONDITIONAL',state='BLOCKED',
    notes='MPN AVX transcrito EVM; ficha dimensional/seguridad pendiente. No usar0603 de50V. Aprobar politica PE/chasis.')
add('ETH_RCHASSIS','Ethernet','Descarga chasis/GND','DP83826IRHBR',value='1 MOhm candidato EVM',rating='TBD aislamiento',
    source='S4 R51 fig6-2',assembly='CONDITIONAL',state='BLOCKED',notes='No aprobar puente resistivo de aislamiento sin politica de chasis.')
add('ETH_JRJ45','Ethernet','Jack RJ45 blindado separado de magnetics','DP83826IRHBR',value='8P8C shielded',mpn='SS-7188S-A-NF candidato EVM',
    source='S4 J17 BOM p25; S3 tabla9-1',state='BLOCKED',kind='AUXILIARY',notes='Cotejar circuito interno, pinout, blindaje, HPOT y footprint con ficha del MPN; no coincidencia geometrica solamente.')
add('ETH_DESD','Ethernet','Proteccion cuatro lineas MDI','DP83826IRHBR',value='4 canales baja C',package='DQA USON10',mpn='TPD4E05U06DQAR',
    source='S4 U13 fig6-2 y BOM p29',state='BLOCKED',kind='AUXILIARY',notes='Ficha TI, capacitancia, clamp y retorno pendientes; no sustituir por USBLC6 por footprint.')
add('ETH_RESET','Ethernet','Reset temporizado desde MCU','DP83826IRHBR',qty=0,assembly='DNP',source='S3 reset timing seccion7; pines RST_N',
    notes='Sin RC arbitrario. Usar GPIO/supervisor tras definir secuencia y tiempos de strap; no compartir a ciegas NRST MCU.')
add('ETH_RMDIO','Ethernet','Pull-up MDIO adicional','DP83826IRHBR',qty=0,assembly='DNP',source='S3 tabla5-1: PU interno',
    notes='No duplicar por defecto. Dimensionar solo tras verificar subida a MDC real, capacitancia y pull-up interno.')

# Both bucks use the proposed FB variant; their BOM is not the AR simulation BOM.
for sub,prefix,v,load,L,mpn,rfbb in [('Buck3V3','B3',3.3,0.7,'6.8 uH','XAL4030-682MEC','43.2'),('Buck5V','B5',5,0.1,'10 uH','XAL4040-103MEC','24.9')]:
    parent='LMR36015FBRNXR (propuesto)'
    add(prefix+'_L',sub,'Inductor buck',parent,value=L,tolerance='20%',rating='Isat25C '+('3.6 A; Irms20C 3.0 A' if v==3.3 else '3.0 A; Irms20C 2.2 A'),
        package='XAL4030' if v==3.3 else 'XAL4040',mpn=mpn,source='S5 tabla10-1; ecuaciones4-5; P6 tabla806-1',state='CALCULATED',electrical='CALCULATED',
        notes='DCRmax25C '+('74.1' if v==3.3 else '92.4')+' mOhm. Isat es caida30% tipica; falta derating caliente/curva L(I)/perdidas nucleo y CAD. No usar inductor docente sin Isat verificable.')
    add(prefix+'_CIN',sub,'Banco ceramico entrada',parent,value='4.7 uF por unidad; Ceff total >=4.7 uF objetivo conservador',tolerance='10%',rating='100 V; X7R',
        package='2220',mpn='C5750X7R2A475K230KA',source='S5 seccion10.2.1.2.6; P7 TDK ficha oficial',qty=None,state='BLOCKED',
        notes='No fijar cantidad hasta curva bias a30 V+tolerancia+temperatura. 4.7 nominal no garantiza 4.7 efectivo. Carga RMS objetivo >= '+str(load/2)+' A banco; 2220 no presente profesor.')
    add(prefix+'_CHF',sub,'Bypass de cada par VIN-PGND',parent,value='220 nF',tolerance='10%',rating='100 V; X7R',package='0805',
        mpn='C0805C224K1RACTU',teacher=CAP8,qty=2,source='S5 seccion10.2.1.2.6 p23; ficha KEMET local p1',
        notes='Uno por par VIN-PGND en lados opuestos; falta Ceff y cotejo dimensiones pads.')
    add(prefix+'_COUT',sub,'Banco salida',parent,value='15 uF por unidad; 45 uF nominal banco',tolerance='20%',rating='16 V; X7R',package='1210',
        mpn='C3225X7R1C156M250AB',qty=3,source='S5 tabla10-1: 3x15 uF nominal; P8 TDK ficha oficial',state='BLOCKED',
        notes='Ceff a '+str(v)+' V, ESR, escalon de carga y Bode pendientes. No atribuir 45 uF efectivos ni ESR3.04mOhm del modelo AR. Sin footprint1210 docente.')
    add(prefix+'_CBOOT',sub,'BOOT a SW',parent,source='S5 seccion10.2.1.2.7:100nF >=16V',**C100)
    add(prefix+'_CVCC',sub,'VCC interno a GND',parent,source='S5 seccion10.2.1.2.8:1uF >=16V',**C1)
    rows[-1]['verification_status']='BLOCKED'
    rows[-1]['observations']+=' Curva Samsung:0.656uF tip a5V antes tolerancia/temperatura; no demuestra1uF efectivo. Cerrar MPN/banco equivalente antes liberar.'
    for label,val,part in [('RFBT','100','RC0603FR-07100KL'),('RFBB',rfbb,'RC0603FR-07'+rfbb.replace('.','K')+'L')]:
        add(prefix+'_'+label,sub,'Divisor feedback '+label,parent,value=val+' kOhm',tolerance='1%',rating='75 V max; limite sqrt(P*R)',
            power='0.1 W @70 C',package='0603',mpn=part,teacher=RES,source='S5 tabla10-1 y ecuacion3; ficha Yageo local p1',state='CALCULATED',electrical='CALCULATED',
            notes='Vout nominal calculado '+('3.31481' if v==3.3 else '5.01606')+' V; ver esquinas de tolerancia. Cambiar parametros en copia docente.')
    add(prefix+'_CFF',sub,'Feed-forward sobre RFBT',parent,value='20 pF',tolerance='5%',rating='50 V; C0G',package='0603',mpn='C0603C200J5GACTU',teacher=CAP,
        assembly='CONDITIONAL',source='S5 tabla10-1 y seccion10.2.1.2.9; ficha KEMET p1',notes='Valor guia fabricante; validar lazo. Con RFBT100k no obligatorio universal; reservar DNP hasta respuesta/Bode.')
    add(prefix+'_RENP',sub,'UVLO externo/PG si se utilizan',parent,qty=0,assembly='DNP',source='S5 pines; ecuacion10; seccion10.2.1.2.8',
        notes='EN a VIN, PG sin uso: cero resistencias. Si se exige UVLO18 V o PG, dimensionar redes por ecuacion10 y cargas; no contar pull-up inexistente.')
    add(prefix+'_CDAMP',sub,'Bulk amortiguador de cableado si se requiere',parent,qty=None,assembly='CONDITIONAL',source='S5 seccion11 y10.2.1.2.6',state='BLOCKED',
        notes='C/ESR dependen impedancia fuente/cable y front-end. Electrolitico docente35 V no aprobado frente transitorios.')

# Front end deliberately remains a closure queue, not a recreated old architecture.
for id,fun in [('IN_FUSE','Fusible o proteccion electronica'),('IN_REVERSE','Bloqueo polaridad inversa'),('IN_TVS','Supresion sobretension/transitorios'),('IN_BULK','Reserva y amortiguacion entrada'),('IN_FILTER','Filtro EMC si necesario')]:
    add(id,'Entrada',fun,'Entrada unica 18..30 V (propuesta pendiente)',qty=None,state='BLOCKED',assembly='TBD',
        kind='PASSIVE' if id in ['IN_FUSE','IN_BULK','IN_FILTER'] else 'AUXILIARY',
        source='S5 seccion11; requisitos usuario; no circuito simplificado aprobado',
        notes='Definir fuente, corriente cargas DO, inrush, sobrevoltaje continuo, surge/norma y retorno. No heredar LTC4414/DMP6023LSS/NIS3071 ni sus pasivos.')
add('IN_J','Entrada','Conector entrada','18..30 VDC',value='2 polos + politica PE',rating='>=30 V continuo mas transitorios; corriente TBD',
    kind='AUXILIARY',state='BLOCKED',teacher='Con_2x1_TH_5mm',mpn='JL126-50002G01',source='Alcance usuario; inventario borneras docente',notes='Priorizar bornera docente tras MPN/tension/corriente/taladros, no jack ambiguo2.0/2.1 mm.')

# RS485 1 channel. Endpoint termination conditional, no external fail-safe bias by default.
add('RS_CVCC','RS485','VCC 3.3 V','THVD1420DR propuesto',source='S6 seccion9 p19',**C100)
add('RS_RT','RS485','Terminacion en extremo de cable','THVD1420DR',value='120 Ohm si Z0=120 Ohm',tolerance='1%',rating='>=3.3 V continuo; falla de bus aparte',power='>=0.25 W objetivo a70 C',
    package='1206 candidato; no0603 0.1W',mpn='TBD',assembly='CONDITIONAL',state='CALCULATED',electrical='CALCULATED',
    source='S6 seccion8.2 fig8-1; calculo P=Vdiff^2/R',notes='3.3^2/118.8=91.7mW antes tolerancia rail y derating. Docente120Ohm/0.1W no tiene margen termico demostrado. Solo dos extremos de bus.')
add('RS_RDE','RS485','DE a GND durante arranque','THVD1420DR',source='S6 seccion10.1 item6:1..10k; fig8-5:10k',**R10K)
add('RS_RRE','RS485','nRE a VCC durante arranque','THVD1420DR',source='S6 seccion10.1 item6:1..10k; fig8-5:10k',**R10K)
add('RS_RPULSE','RS485','Limitacion residual en A/B si surge1kV','THVD1420DR',value='10 Ohm',tolerance='5%',rating='Pulse-proof segun ficha exacta',power='Pulsos por verificar',package='0603',
    mpn='CRCW0603010RJNEAHP',teacher=RES,qty=2,assembly='CONDITIONAL',state='BLOCKED',source='S6 fig8-5 tabla8-1 p19',
    notes='Referencia usa THVD1400 a5 V. No valida THVD1420/3.3V/12Mbps: verificar VOD tras20Ohm, residuales clamp, pulsos y timing.')
add('RS_TVS','RS485','Proteccion A/B','THVD1420DR',value='Asimetrica -7/+12 V candidata',package='SOT23',mpn='CDSOT23-SM712',assembly='CONDITIONAL',state='BLOCKED',kind='AUXILIARY',
    source='S6 tabla8-1 p19',notes='No TVS aislado si clamp excede bus +/-16 V absoluto; red resistiva requerida y verificacion residual. Capacitancia y velocidad pendientes.')
add('RS_BIAS','RS485','Bias externo','THVD1420DR',qty=0,assembly='DNP',source='S6 seccion7.4 tabla7-2 fail-safe',notes='Open/short/idle fail-safe integrado; no duplicar polarizacion. Revisar otros nodos si el sistema la exige.')
add('RS_J','RS485','Bornera A/B/COM','THVD1420DR',value='3 polos',kind='AUXILIARY',state='BLOCKED',teacher='Con_3x1_TH_5mm',mpn='MX126-5.0-03P-GN01-Cu-S-A',source='S6 red half-duplex; inventario docente',notes='Ratings, corrientes de falla, pinout y referencia comun pendientes; no asumir aislamiento galvanico.')

# CAN split termination follows the official Microchip EV kit, not timing test Fig2-1.
for rail in ['VCC5','VIO3V3']:
    add('CAN_C'+rail,'CAN','Desacoplo '+rail,'ATA6561-GAQW propuesto',source='S7 tablaB-2 C3/C5; figA-1',**C100)
add('CAN_RSPLIT','CAN','Dos mitades terminacion extremo','ATA6561-GAQW',value='62 Ohm',tolerance='<=1%; matching <1% deseable',rating='Bus CAN; falla DC por verificar',power='0.5 W por resistor segun EVM',package='1206',
    qty=2,assembly='CONDITIONAL',state='BLOCKED',source='S7 seccion3.5 pp17-18 y tablaB-2 p32',notes='124Ohm diferencial; no usar120Ohm docente en paralelo ni fijar60Ohm total por nodo. MPN0.5W1206 pendiente.')
add('CAN_CSPLIT','CAN','Punto medio a GND','ATA6561-GAQW',value='4.7 nF',tolerance='TBD',rating='50 V; X7R candidato',package='0805',assembly='CONDITIONAL',state='MISSING',
    source='S7 seccion3.5 rango4.7..47nF; tablaB-2 C1',notes='Valor por defecto EVM; no son15pF/CL de circuito de timing.')
add('CAN_CBULK','CAN','Reserva VCC opcional','ATA6561-GAQW',value='47 uF',tolerance='TBD',rating='10 V minimo EVM',package='1210 candidato',assembly='CONDITIONAL',state='MISSING',
    source='S7 tablaB-2 C2',notes='No obligatoria universal si buck y distribucion aportan reserva; comprobar caida/transitorios antes poblar.')
add('CAN_CBUS','CAN','Capacitancias EMC simetricas opcionales','ATA6561-GAQW',value='100 pF aprox',tolerance='Matching lo menor posible',rating='TBD bus',qty=2,assembly='CONDITIONAL',state='BLOCKED',
    source='S7 seccion3.5 p18',notes='Validar CAN-FD5Mbps y carga total de bus antes de agregar; no copiar automaticamente.')
add('CAN_CMC','CAN','Choke modo comun opcional','ATA6561-GAQW',value='TBD segun EMC',qty=0,assembly='DNP',source='S7 seccion3.5:opcional',notes='No adoptar automaticamente B82799 sin validar timing CAN-FD.')
add('CAN_STBY','CAN','Pull-up STBY externo','ATA6561-GAQW',qty=0,assembly='DNP',source='S8 tabla electrica modo control; S7 seccion3.8',notes='Pull-up interno75..175k aVIO, standby con GPIO HiZ. Controlar por GPIO; no fijar PD que habilite bus al boot.')
add('CAN_TVS','CAN','TVS CAN externo segun inmunidad','ATA6561-GAQW',qty=None,assembly='TBD',kind='AUXILIARY',state='BLOCKED',source='S8 absmax bus; S7 seccion3.5',notes='No especificacion EMC/cable/falla a24V cerrada. Seleccion y capacitancia pendientes; proteccion interna no prueba sistema.')
add('CAN_J','CAN','Bornera CANH/CANL/COM','ATA6561-GAQW',value='3 polos',state='BLOCKED',kind='AUXILIARY',teacher='Con_3x1_TH_5mm',mpn='MX126-5.0-03P-GN01-Cu-S-A',source='S7 circuito tipico',notes='Ratings/pinout, reglas de bus y opcion de terminacion pendientes.')

# Low-side DO + translator; resistor sizing explicitly our calculation.
for rail in ['VCCA3V3','VCCB5']:
    add('DO_C'+rail,'DO','Desacoplo '+rail,'SN74LVC2T45DCUR propuesto',source='S9 seccion8.3 (0.01/0.022uF por VCC multiple; 0.1uF aceptable paralelo)',**C100)
for port in ['A','B']:
    add('DO_RPD'+port,'DO','Pulldown '+port+'1/'+port+'2 arranque','SN74LVC2T45/BSP75N',qty=2,state='CALCULATED',electrical='CALCULATED',
        source='S9 seccion7.3 Ioff/I/O HiZ; S10 VIN(TH)>=1V; calculo propio seccionDO',**R10K)
add('DO_RSER','DO','Resistencias serie control','BSP75N',qty=0,assembly='DNP',source='S10 IINmax1.2mA @5V; S9 VOH',notes='No agregar resistencia arbitraria que reduzca VIN bajo4.5V para protecciones. Revisar VOH con carga1.2mA+pulldown.')
add('DO_SUPPRESS','DO','Supresion carga inductiva externa','BSP75NTA',qty=None,assembly='TBD',state='BLOCKED',kind='AUXILIARY',
    source='S10 tablas clamp/avalancha/termica pp3-6',notes='Faltan L/ciclo/temperatura/tiempo desmagnetizacion; no declarar550mJ universal ni elegir diodo solo por corriente500mA.')
add('DO_JLOAD','DO','Bornes Vcampo/DRAIN por carga','BSP75NTA',value='2 polos por canal',rating='>=30 V y0.5 A/canal mas fallas',qty=2,kind='AUXILIARY',state='BLOCKED',
    teacher='Con_2x1_TH_5mm',mpn='JL126-50002G01',source='S10 low-side; requisitos alcance',notes='Priorizar bornera docente; source/tab a retorno campo; no terminal high-side. Retornos1A fuera GND analogico.')

# 1 ISO1212, two inputs. Type3 is a documented candidate, not implied by “24V”.
for ch in [1,2]:
    add(f'DI_RSENSE{ch}','DI',f'SENSE{ch} a IN{ch}','ISO1212DBQR propuesto',value='562 Ohm',tolerance='1%',rating='75 V max; limite sqrt(P*R)',power='0.1 W @70 C',
        package='0603',mpn='RC0603FR-07562RL',teacher=RES,source='S11 seccion8.2.1.2.1 ecuacion1; ficha Yageo local',state='CALCULATED',electrical='CALCULATED',
        notes='Ityp2.25mA; P conservadora a2.75mA=4.30mW. No es resistor de24V completos; corriente de campo separada deVCC1.')
    add(f'DI_RTHR{ch}','DI',f'Serie entrada{ch}24V Type3','ISO1212DBQR',value='1 kOhm',tolerance='1% objetivo',rating='Surge/pulsos por verificar',power='>=0.25 W MELF pulse rated',
        package='MELF segun fabricante',source='S11 seccion8.2.1.2.1 ecuaciones2-4; tabla8-1 Type3',state='MISSING',
        notes='TI exige0.25W MELF si limita surge. No sustituir por FOJAN1k0603/0.1W. Type3 pendiente adopcion; Type1 usaria2.5k.')
    add(f'DI_CIN{ch}','DI',f'SENSE{ch} a FGND{ch}','ISO1212DBQR',source='S11 tabla8-1 y seccion8.4; 10nF >=50V; ficha KEMET local',**C10N)
add('DI_CVCC','DI','VCC1 a GND1 logico','ISO1212DBQR',source='S11 seccion8.3',**C100)
add('DI_CPE','DI','Acoplo FGND a PE opcional','ISO1212DBQR',value='500 pF candidato',rating='2 kV; seguridad por definir',assembly='CONDITIONAL',state='BLOCKED',
    source='S11 fig8-2',notes='No puente aGND1; solo si existePE/arquitectura aislamiento aprobada. No copiar automaticamente.')
add('DI_TVS','DI','TVS adicional entrada si EMC requiere','ISO1212DBQR',qty=0,assembly='DNP',kind='AUXILIARY',source='S11 seccion8.2.1.2.5 tabla8-1',
    notes='Red TI tiene robustez condicionada aMELF/CIN/layout; no agregarTVS28V sin revisar ubicacion trasRTHR, umbral y clamp.')
add('DI_J','DI','Bornera IN1/IN2/COM campo','ISO1212DBQR',value='3 polos si COM comun',kind='AUXILIARY',state='BLOCKED',teacher='Con_3x1_TH_5mm',mpn='MX126-5.0-03P-GN01-Cu-S-A',source='S11 fig8-2',
    notes='Aislamiento de grupo o por canal pendiente. SUB1/SUB2 NC; FGND noGND1. EN definido aVCC1 si salidas permanentes, sin resistor necesario.')

# Independent CAD evidence is maintained by library preparation. Regeneration
# must preserve project-local bindings and must never imply electrical approval.
closure_path=OUT/'evidence/electrical_closure/bom_decisions.json'
closure=json.loads(closure_path.read_text(encoding='utf-8')) if closure_path.exists() else {}
if closure:
    import copy
    existing={r['component_id']:r for r in rows}
    for extra in closure.get('new_rows',[]):
        cloned=copy.deepcopy(existing[extra['clone_of']])
        cloned.update({k:v for k,v in extra.items() if k!='clone_of'})
        rows.append(cloned)
    for r in rows:
        r.update(closure.get('patches',{}).get(r['component_id'],{}))
        r['specification_key']='|'.join(str(r[k]) for k in ['nominal_value','tolerance','rated_voltage_or_current','power_rating','package','recommended_mpn'])
freeze_dir=OUT/'evidence/input_protection_freeze'
freeze_path=freeze_dir/'bom_decisions.json'
freeze=json.loads(freeze_path.read_text(encoding='utf-8')) if freeze_path.exists() else {}
tps_dir=OUT/'evidence/tps26620'
tps_path=tps_dir/'bom_decisions.json'
if tps_path.exists():
    latest=json.loads(tps_path.read_text(encoding='utf-8'))
    for key in ['patches','record_fields','active_patches']:
        for component_id,changes in latest.get(key,{}).items():
            freeze.setdefault(key,{}).setdefault(component_id,{}).update(changes)
    freeze.setdefault('new_rows',[]).extend(latest.get('new_rows',[]))
eth_dir=OUT/'evidence/ethernet_75ohm'
if (eth_dir/'bom_decisions.json').exists():
    latest=json.loads((eth_dir/'bom_decisions.json').read_text(encoding='utf-8'))
    for key in ['patches','record_fields','active_patches']:
        for component_id,changes in latest.get(key,{}).items():
            freeze.setdefault(key,{}).setdefault(component_id,{}).update(changes)
cap_dir=OUT/'evidence/ethernet_1nf'
if (cap_dir/'bom_decisions.json').exists():
    latest=json.loads((cap_dir/'bom_decisions.json').read_text(encoding='utf-8'))
    for key in ['patches','record_fields','active_patches']:
        for component_id,changes in latest.get(key,{}).items():
            freeze.setdefault(key,{}).setdefault(component_id,{}).update(changes)
do_dir=OUT/'evidence/bsp75n_closure'
if (do_dir/'bom_decisions.json').exists():
    latest=json.loads((do_dir/'bom_decisions.json').read_text(encoding='utf-8'))
    for key in ['patches','record_fields','active_patches']:
        for component_id,changes in latest.get(key,{}).items():
            freeze.setdefault(key,{}).setdefault(component_id,{}).update(changes)
mission_dir=OUT/'evidence/autonomous_closure'
if (mission_dir/'bom_decisions.json').exists():
    latest=json.loads((mission_dir/'bom_decisions.json').read_text(encoding='utf-8'))
    for key in ['patches','record_fields','active_patches']:
        for component_id,changes in latest.get(key,{}).items():
            freeze.setdefault(key,{}).setdefault(component_id,{}).update(changes)
    freeze.setdefault('new_rows',[]).extend(latest.get('new_rows',[]))
if freeze:
    import copy
    existing={r['component_id']:r for r in rows}
    for extra in freeze.get('new_rows',[]):
        cloned=copy.deepcopy(existing[extra['clone_of']])
        cloned.update({k:v for k,v in extra.items() if k!='clone_of'})
        rows.append(cloned)
    for r in rows:
        r.update(freeze.get('patches',{}).get(r['component_id'],{}))
        r['specification_key']='|'.join(str(r[k]) for k in ['nominal_value','tolerance','rated_voltage_or_current','power_rating','package','recommended_mpn'])
asset_file=OUT/'evidence/library_preparation/cad_assets.json'
assets=json.loads(asset_file.read_text(encoding='utf-8')) if asset_file.exists() else []
closure_assets=OUT/'evidence/electrical_closure/cad_additions.json'
if closure_assets.exists():
    assets+=json.loads(closure_assets.read_text(encoding='utf-8'))
if (freeze_dir/'cad_assets.json').exists():
    assets+=json.loads((freeze_dir/'cad_assets.json').read_text(encoding='utf-8'))
if (tps_dir/'cad_assets.json').exists():
    assets+=json.loads((tps_dir/'cad_assets.json').read_text(encoding='utf-8'))
if (eth_dir/'cad_assets.json').exists():
    assets+=json.loads((eth_dir/'cad_assets.json').read_text(encoding='utf-8'))
if (cap_dir/'cad_assets.json').exists():
    assets+=json.loads((cap_dir/'cad_assets.json').read_text(encoding='utf-8'))
if (do_dir/'cad_assets.json').exists():
    for revised in json.loads((do_dir/'cad_assets.json').read_text(encoding='utf-8')):
        indexes=[i for i,a in enumerate(assets) if a['asset_id']==revised['asset_id']]
        assert len(indexes)==1,'DO override must replace exactly one existing stable asset'
        assets[indexes[0]]=revised
if (mission_dir/'cad_assets.json').exists():
    for revised in json.loads((mission_dir/'cad_assets.json').read_text(encoding='utf-8')):
        indexes=[i for i,a in enumerate(assets) if a['asset_id']==revised['asset_id']]
        assert len(indexes)<=1,'Duplicate asset identity'
        if indexes: assets[indexes[0]]=revised
        else: assets.append(revised)
by_id={id:a for a in assets if a['item_kind']!='ACTIVE' for id in a['component_ids']}
for r in rows:
    old_electrical=r['electrical_status']
    r['electrical_status_original']=old_electrical
    r['electrical_status']=(old_electrical if old_electrical in {'ELECTRICAL_VERIFIED','DERIVED_PENDING_REVIEW','ELECTRICAL_BLOCKED'} else
                            'ELECTRICAL_BLOCKED' if r['verification_status'] in {'BLOCKED','MISSING'}
                            else 'DERIVED_PENDING_REVIEW' if old_electrical=='CALCULATED'
                            else 'ELECTRICAL_VERIFIED' if old_electrical=='VERIFIED' else 'PROVISIONAL')
    a=by_id.get(r['component_id'])
    if a and a['mpn']!=r['recommended_mpn']:
        a=None # Never retain the identity of a replaced MPN.
    if not a and r['recommended_mpn']!='TBD':
        a=next((x for x in assets if x['item_kind']!='ACTIVE' and x['mpn']==r['recommended_mpn']),None)
    r['symbol_status']='CAD_MISSING'
    r['footprint_status']='CAD_MISSING'
    r['cad_limitations']='Exact model/manufacturer drawing or selection is unresolved.'
    r['package_requirement']=r['package'] if r['package']!='TBD' else 'UNRESOLVED:'+r['component_id']
    r['package_requirement_state']='DEFINED' if r['recommended_mpn']!='TBD' and r['component_id'] not in {'ETH_TMAG','ETH_JRJ45','ETH_CCHASSIS'} else 'UNRESOLVED'
    if a:
        for key in ['symbol','footprint','cad_status','symbol_status','footprint_status','package_requirement']:
            r[key]=a[key]
        r['cad_origin']=LIB+'Gateway_Academic.SchLib + Gateway_Academic.PcbLib'
        r['cad_limitations']=a['limitations']
        if a['footprint']!='MISSING': r['package_requirement_state']='DEFINED'
    else:
        # An inherited generic value (e.g. 33pF for an unselected crystal)
        # is not a prepared academic CAD selection.
        r['symbol']=r['footprint']=r['cad_origin']='MISSING'
        r['cad_status']='CAD_BLOCKED' if r['verification_status']=='BLOCKED' or r['recommended_mpn']=='TBD' else 'CAD_MISSING'
        r['symbol_status']=r['footprint_status']=r['cad_status']
    r['selection_status']='DNP' if r['assembly']=='DNP' else 'SELECTED_FOR_CAPTURE' if r['recommended_mpn']!='TBD' else 'UNSELECTED'
    r['capture_status']='NOT_POPULATED' if r['assembly']=='DNP' else 'BLOCKED' if r['electrical_status']=='ELECTRICAL_BLOCKED' else 'CONDITIONAL_CAPTURE'
    r['availability_category']='UNKNOWN - no verified JLC Basic/Preferred classification'
    r['stock_status']='UNKNOWN - not an inventory reservation'
    r['sourcing_observed_at']='2026-11-07' if closure else ''
    for key in ['lcsc_code','datasheet_url','local_datasheet']:
        r[key]=a.get(key,'') if a else ''
    if a:
        for key in ['availability_category','stock_status']:
            if key in a:r[key]=a[key]
    if r['recommended_mpn']=='MM204F1K00TKRTR3K0':
        r['availability_category']='JLC Extended; C233005; public JSON-LD'
        r['stock_status']='Public page reports out_of_stock; quantity unavailable; recheck assembly stock'
    for key in ['design_approval','validation_scope','test_status']:
        r[key]=freeze.get('record_fields',{}).get(r['component_id'],{}).get(key,'NOT_REVIEWED_IN_FREEZE')
    if r['design_approval']=='PROTOTYPE_APPROVED':
        r['selection_status']='PROTOTYPE_APPROVED' if r['assembly']!='DNP' else 'APPROVED_DNP_OPTION'
        r['capture_status']='READY_FOR_MANUAL_CAPTURE' if r['assembly']!='DNP' else 'NOT_POPULATED'

identity_path=mission_dir/'component_identity.json'
manufacturer_by_mpn=json.loads(identity_path.read_text(encoding='utf-8')) if identity_path.exists() else {}
for r in rows:
    r['manufacturer']=manufacturer_by_mpn.get(r['recommended_mpn'],'NOT_SELECTED' if r['recommended_mpn']=='TBD' else 'NOT_VERIFIED')
assert len({r['component_id'] for r in rows}) == len(rows)
fields = list(rows[0])
with (OUT/'passive_bom.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
mapping=[]
for r in rows:
    mapping.append(dict(component_id=r['component_id'], recommended_mpn=r['recommended_mpn'],
                        symbol=r['symbol'], footprint=r['footprint'], cad_origin=r['cad_origin'],
                        selection_route=r['cad_route'], verification_status=r['cad_status'],
                        pin_pad_check='VERIFIED source-numbered pins and persisted pad readback' if r['cad_status']=='CAD_VERIFIED' else 'PENDING; verify actual symbol pins against footprint pads in Altium',
                        dimensional_check='VERIFIED cited manufacturer dimensions / documented prototype DFM variant' if r['cad_status']=='CAD_VERIFIED' else 'PENDING; compare pad dimensions/masks/pitch with exact manufacturer drawing',
                        source=r['electrical_value_source'],
                        action='Use saved exact project-local model; manufacturing-output review remains' if r['cad_status']=='CAD_VERIFIED' else 'Reuse existing model only after qualification; clone parameters for different MPN/value' if r['symbol']!='MISSING' else 'Acquire manufacturer/verified CAD; create only after checking generic alternatives',
                        observations=r['observations'],cad_status=r['cad_status'],
                        electrical_status=r['electrical_status'],item_kind=r['item_kind'],
                        symbol_status=r['symbol_status'],footprint_status=r['footprint_status'],
                        specification_key=r['specification_key'],package_requirement=r['package_requirement'],
                        quantity=r['quantity'],cad_limitations=r['cad_limitations'],package_requirement_state=r['package_requirement_state'],
                        selection_status=r['selection_status'],capture_status=r['capture_status'],availability_category=r['availability_category'],stock_status=r['stock_status'],
                        design_approval=r['design_approval'],validation_scope=r['validation_scope'],test_status=r['test_status'],
                        lcsc_code=r['lcsc_code'],datasheet_url=r['datasheet_url'],local_datasheet=r['local_datasheet']))
for a in assets:
    if a['item_kind']!='ACTIVE':
        continue
    mapping.append(dict(component_id=a['asset_id'],recommended_mpn=a['mpn'],symbol=a['symbol'],
        footprint=a['footprint'],cad_origin=LIB+'Gateway_Academic.SchLib + Gateway_Academic.PcbLib',
        selection_route='PROJECT_LOCAL_AUTHORED',verification_status=a['cad_status'],
        pin_pad_check='See library_preparation_report and saved destination readback; BSP role pins are unfinished.',
        dimensional_check='Source-backed package data; native placement/assembly review pending.',
        source=a['source'],action='Resolve recorded limitations before final schematic use.',
        observations=a['limitations'],cad_status=a['cad_status'],electrical_status='ELECTRICAL_BLOCKED' if a['mpn'] in {'BSP75NTA','SN74LVC2T45DCTR'} else 'PROVISIONAL',
        item_kind='ACTIVE',symbol_status=a['symbol_status'],footprint_status=a['footprint_status'],
        specification_key=a['mpn'],package_requirement=a['package_requirement'],quantity='',cad_limitations=a['limitations'],package_requirement_state='DEFINED',
        selection_status='SELECTED_FOR_CAPTURE',capture_status='BLOCKED' if a['mpn']=='BSP75NTA' else 'CONDITIONAL_CAPTURE',
        availability_category='UNKNOWN',stock_status='UNKNOWN'))
for m in mapping:
    if m['cad_status']=='CAD_VERIFIED':
        m['pin_pad_check']='VERIFIED manufacturer pin functions and saved destination pad readback'
        m['dimensional_check']='VERIFIED cited dimensions and explicit prototype-process geometry; see input protection reference'
    for key in ['design_approval','validation_scope','test_status']:
        m.setdefault(key,freeze.get('record_fields',{}).get(m['component_id'],{}).get(key,'NOT_REVIEWED_IN_FREEZE'))
    if m['component_id'] in freeze.get('active_patches',{}):
        m.update({k:v for k,v in freeze['active_patches'][m['component_id']].items() if k in m})
    if m['item_kind']=='ACTIVE':
        m['verification_status']=m['cad_status'] # Mapping status is CAD,not BOM/electrical status.
        m['quantity']='' # Mapping describes specifications; only final_bom has placement quantities.
    m['manufacturer']=manufacturer_by_mpn.get(m['recommended_mpn'],'NOT_SELECTED' if m['recommended_mpn']=='TBD' else 'NOT_VERIFIED')
with (OUT/'cad_library_mapping.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(mapping[0]));w.writeheader();w.writerows(mapping)

# Procurement view includes actual active quantities, independently from the
# specification-only active CAD mapping rows (which retain blank quantities).
if closure:
    final_rows=[dict(r) for r in rows]
    for a in assets:
        if a['item_kind']!='ACTIVE': continue
        r={key:'' for key in fields}
        r.update(component_id=a['asset_id'],subsystem='Active devices',function='Fixed architecture active specification',main_reference=a['mpn'],
                 recommended_mpn=a['mpn'],quantity=2 if a['mpn'] in {'BSP75NTA','LMR36015FBRNXR'} else 1,
                 assembly='REQUIRED',item_kind='ACTIVE',symbol=a['symbol'],footprint=a['footprint'],
                 cad_status=a['cad_status'],symbol_status=a['symbol_status'],footprint_status=a['footprint_status'],
                 electrical_status='ELECTRICAL_BLOCKED' if a['mpn'] in {'BSP75NTA','SN74LVC2T45DCTR'} else 'PROVISIONAL',
                 verification_status='BLOCKED' if a['mpn'] in {'BSP75NTA','SN74LVC2T45DCTR'} else 'PROVISIONAL',
                 electrical_value_source=a['source'],observations=a['limitations'],package=a['package_requirement'],design_reference='UNASSIGNED',
                 cad_origin=LIB+'Gateway_Academic.SchLib + Gateway_Academic.PcbLib',selection_status='SELECTED_FOR_CAPTURE',
                 availability_category='UNKNOWN',stock_status='UNKNOWN',sourcing_observed_at='2026-11-07')
        r.update({k:v for k,v in freeze.get('active_patches',{}).get(r['component_id'],{}).items() if k in r})
        for key in ['design_approval','validation_scope','test_status']:
            r[key]=freeze.get('record_fields',{}).get(r['component_id'],{}).get(key,'NOT_REVIEWED_IN_FREEZE')
        r['manufacturer']=manufacturer_by_mpn.get(r['recommended_mpn'],'NOT_VERIFIED')
        final_rows.append(r)
    with (OUT/'final_bom.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(final_rows)

passives=[r for r in rows if r['item_kind']=='PASSIVE']
required=[r for r in passives if r['assembly']=='REQUIRED']
conditional=[r for r in passives if r['assembly']=='CONDITIONAL']
stats=dict(bom_groups=len(rows),passive_groups=len(passives),
           required_known_units=sum(r['quantity'] for r in required if isinstance(r['quantity'],int)),
           required_unknown_quantity_groups=sum(r['quantity']=='' for r in required),
           conditional_known_units=sum(r['quantity'] for r in conditional if isinstance(r['quantity'],int)),
           required_distinct_specifications=len({r['specification_key'] for r in required}),
           required_distinct_concrete_mpns=len({r['recommended_mpn'] for r in required if r['recommended_mpn']!='TBD'}),
           teacher_candidate_required_units=sum(r['quantity'] for r in required if isinstance(r['quantity'],int) and r['cad_route'].startswith('TEACHER')),
           external_required_known_units=sum(r['quantity'] for r in required if isinstance(r['quantity'],int) and r['cad_route']=='EXTERNAL_REQUIRED'),
           fully_verified_units=0, fully_verified_teacher_units=0, fully_verified_external_units=0,
           statuses=dict(Counter(r['verification_status'] for r in rows)))
(OUT/'evidence/passive_selection_counts.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')

cols=fields[:16]+['quantity','assembly','electrical_status','cad_status']
labels=['ID','Subsistema','Funcion','Referencia principal (fabricante)','Valor nominal','Tolerancia','Tension/corriente nominal','Potencia','Encapsulado','MPN recomendado/candidato','Simbolo candidato','Footprint candidato','Origen CAD','Fuente valor electrico','Estado global','Observaciones','Cantidad','Montaje','Estado electrico','Estado CAD']
tables=[]
for sub in dict.fromkeys(r['subsystem'] for r in rows):
    tables += ['\n### BOM '+sub+'\n','| '+' | '.join(labels)+' |','|'+'|'.join(['---']*len(cols))+'|']
    for r in rows:
        if r['subsystem']==sub:
            tables.append('| '+' | '.join(str(r[c]).replace('|','/').replace('\n',' ') or 'TBD' for c in cols)+' |')
report = OUT/'passive_component_selection.md'
marker = '<!-- GENERATED_BOM_TABLES -->'
if report.exists():
    introduction = report.read_text(encoding='utf-8').split(marker)[0]
    report.write_text(introduction + marker + '\n' + '\n'.join(tables) + '\n',encoding='utf-8')
print(json.dumps(stats,indent=2))
