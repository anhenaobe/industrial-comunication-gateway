# Preparación de Rev. A para esquemático y PCB — 7 y 8 de noviembre de 2026

Auditoría: 2026-11-05. Rama: `main`, seguimiento `origin/main`.
**Propuesta para revisión humana. Se conserva STM32H723VET6; no se autoriza aquí
ninguna modificación del maestro, esquemático, PCB o firmware.**

## 1. Dictamen y disponibilidad de tiempo

**No es razonable comprometer la arquitectura completa actual terminada este fin
de semana.** Hay cálculos aprovechables, pero no un circuito completo ni librerías
principales homologadas. El trabajo restante estimado para A es **45–65 horas
efectivas**, incluyendo correcciones. B, manteniendo H723, Ethernet, un RS-485 y
las dos DO, requiere **30–46 h**; C, ruta mínima sin DO y sin rail de 5 V, **25–37 h**.
Son estimaciones de una persona familiarizada con Altium y electrónica, no garantías.

Se dispone de 2 h el jueves 5 y 4 h el viernes 6. Como no se definió la duración
de las jornadas intensivas, se supone **10–12 h efectivas por día** sábado y domingo:
**26–30 h totales**. Tiempo frente al computador, pausas y horas efectivas no son
equivalentes. Con jornadas de 8 h efectivas, el presupuesto baja a 22 h.
Las horas de esta auditoría no se contabilizan como horas de diseño ya realizadas
en los bloques pendientes ni como agotamiento automático de las seis horas indicadas.

B es la propuesta preferente por conservar las dos DO y buena parte del trabajo
existente, pero supera el presupuesto en gran parte del intervalo. C es una
contingencia marginalmente posible en el extremo favorable; también conserva
los bloqueos de MCU, Ethernet y alimentación. **Hoy ninguno está listo para pasar
directamente a layout.** No se recomienda migrar a ESP32-C3 ni Ethernet SPI.
La recomendación anterior de `simplified_gateway_feasibility.md` queda como
antecedente de otra restricción; la decisión provisional de esta sesión prevalece.

## 2. Evidencia inspeccionada y límites

### Fuentes locales

| ID | Ruta y contenido | Qué demuestra / qué no demuestra |
|---|---|---|
| M | `docs/industrial_gateway_requirements.md`, §§2–9 | Arquitectura, selección, cálculos condicionados y presupuesto; no netlist completa |
| P | `docs/proof_of_concept.md`, `firmware/poc/README.md`, fuentes y `platformio.ini` | PoC NUCLEO-F429ZI y Zephyr 4.3.0; no pinout ni alimentación de PCB H723VE |
| W | `docs/sources/webench/` | Dos BOM parciales y seis tablas de operación; no BOM consolidada de Rev. A |
| T9 | `Simulations/WBDesign9_TINA-TI/ExportFiles/Simulation/webench_design_18216184_9.tsc` | Título interno: `LMR36015ARNXR 18V-30V to 3.30V @ 1A` |
| T10 | `Simulations/WBDesign10_TINA-TI/ExportFiles/Simulation/webench_design_18216184_10.tsc` | Título interno: `LMR36015ARNXR 18V-30V to 5.00V @ 1A` |
| L | `shared_lib (1).IntLib`, `docs/hardware/library_inventory.{md,csv}`, `evidence/shared_lib_metadata.json` | 70 componentes seleccionables y 37 footprints; no integrados principales de Rev. A |
| D | `C:/dev/7mo/design/Datasheets_industrial_gateway/` | Datasheets de los doce tipos de componente; detalle abajo |
| R | `converter_pcb_layout_appli-e (1).pdf` | ROHM, *PCB Layout Techniques of Buck Converter*, No. 60AN066E Rev.003, octubre 2017; guía general, no layout LMR36015 validado |
| V | `C:/dev/7mo/design/PCB_Project/` y `electronic-design-dc-dc/` | Otros trabajos CAD y bibliotecas; no esquemático de este gateway demostrado |

El maestro real es `docs/industrial_gateway_requirements.md`; no existe el nombre
alternativo `industrial_linux_gateway_requirements.md`. El Power Budget consolidado
está en §8 de M; no se encontró una hoja de cálculo vigente que cierre sus incógnitas.

Se inspeccionaron también archivos sin seguimiento. El estado inicial tenía
modificaciones previas de `.gitignore`, `CMakeLists.txt`, `README.md` y `prj.conf`
en `firmware/poc/`, más `.vscode/`, `platformio.ini`, `zephyr/`, los informes de
hardware, la IntLib y el PDF de ROHM sin seguimiento. Se conservaron.
No se encontró SchDoc, PcbDoc, PrjPcb ni archivo de asignación de pines `.ioc`
del gateway en el árbol local inspeccionado, incluidos archivos ocultos salvo `.git`
y salidas de compilación excluidas. No se encontró ERC, DRC ni paquete de fabricación.

Las bibliotecas vecinas se leyeron por su directorio OLE: `PCB_Project/lib/Schlib2.SchLib`
contiene seis símbolos de pasivos/conectores/CP2102N; `electronic-design-dc-dc/entregable/Schlib1.SchLib`
contiene veinte entradas, incluyendo TPS61175PWP y LMZ10505TZX-ADJNOPB, no los IC
de Rev. A. Los SchDoc/PcbDoc de buck-boost no se contabilizan como diseño del gateway.
Pueden aportar pasivos específicos tras cotejo, no equivalencia eléctrica automática.
`D/revision_posterior/` contiene alternativas como SP3485, NCV8402 y DMP6023LE;
no son sustituciones aprobadas ni recursos CAD por estar sus PDF presentes.

### Datos que sí se pueden reutilizar

- Dominio 3.3 V, dominio 5 V y campo 24 V definidos; topologías funcionales de M.
- DO low-side, 500 mA por canal, BSP75N controlado a 5 V mediante traductor,
  dirección A→B y DIR conectado a VCCA.
- OR-ing: orientación drain a entrada/source a bus, CTL bajo y sensado Kelvin;
  referencias de pérdida de PFET de 33 mΩ y eFuse de 92 mΩ a las condiciones citadas.
- eFuse: un canal, variante MT4 Auto-Retry, `R_LIM = 43.2 kΩ`; ITH ≈1.4 A e
  ICB ≈2.8 A son estimaciones de gráfica, no cotas garantizadas.
- Bucks: familia LMR36015 cerrada; FB/1 MHz sigue siendo **MPN propuesto**.
  Guías iniciales de pasivos en M §6.7, sin BOM FB homologada.
- Consumos presupuestados 3.3 V: 534.303 mA; 5 V: 72.403 mA. Capacidades de diseño
  respectivas: 0.7 A y 0.1 A. La referencia MCU de 360 mA es condicionada, no consumo
  medido del firmware ni máximo universal. Las cargas DO no pertenecen al rail de control.

M mantiene pérdidas de conversión L3/L5, temperatura y balance de entrada sin
cerrar. No se puede deducir el margen real del eFuse tomando únicamente 1.18 A
de una referencia anterior. Estos cálculos ahorran rehacer el planteamiento, pero
no eliminan el trabajo de selección, conexión y verificación de pasivos.

### WEBENCH y TINA: diferencia entre archivo y resultado

`LMR66420_WEBENCH_BOM.csv` y sus tablas de 3.3 V pertenecen a un convertidor
histórico distinto. `LMR36015_WEBENCH_BOM.csv` usa **ARNXR**, 5 V y resultados
de operación a 0.1 A; no FB. Su inductor de 22 µH y sus capacitores no se trasladan
automáticamente a 1 MHz. La entrada de esa BOM declara 4.7 µF nominales pero
solo 310 nF efectivos, y bypass de 47 nF: comprobar de nuevo el desacoplamiento.
Los precios históricos exportados tampoco son cotizaciones actuales.

T9 y T10 contienen `LMR36015ARNXR` y títulos a 1 A. Su identificación se obtuvo
de las cadenas y del modelo interno; **no se reconstruyó toda la conectividad
binaria ni se abrió/simuló TINA en esta auditoría**. Los README de exportación
explican cómo simular, no certifican que se haya hecho. No se encontraron nuevas
curvas/resultados FB de arranque, transitorios, pérdidas o estabilidad. Por ello:

- Hay un antecedente AR para ambos voltajes, más amplio que las dos BOM WEBENCH.
- No hay prueba de que T9 corresponda a 0.7 A, T10 a 0.1 A o a las cargas reales.
- Ninguno valida el MPN FB propuesto. Conservar AR para ahorrar una simulación
  sería una decisión técnica nueva, con pasivos y carga ligera por revisar.

## 3. Estado real de los subsistemas

Definiciones: **Diseñado** = conexiones y valores justificados para el bloque;
**Parcial** = algunas decisiones/cálculos, con conexiones o verificaciones faltantes;
**Seleccionado** = integrado/topología elegidos, sin circuito suficiente;
**Pendiente** = no hay diseño suficiente. Ningún subsistema completo califica
como Diseñado con la evidencia actual; sí hay porciones calculadas reutilizables.

| Subsistema | Estado | Evidencia | Pendiente que impide considerarlo cerrado |
|---|---|---|---|
| MCU H723 y alimentación mínima | Seleccionado | M §3, D13 | Todos los pines de alimentación, VCAP, reset, BOOT, reloj y desacoplos |
| Asignación de pines y multiplexación | Pendiente | Sin `.ioc`/tabla propia; D13 tablas 7–8 | Tabla física LQFP100 y conflictos, reservas SWD/HSE y controles |
| Ethernet RMII/PHY | Seleccionado | M §4.1, D1 | Modo BASIC/ENHANCED, straps, reloj, magnetics/RJ45, protección, BOM y conexiones |
| Dos RS-485 | Seleccionado | M §4.2, D2; 50 mA asignados por IC | MPN de encapsulado, controles, terminación/bias/protección y conectores |
| CAN-FD | Seleccionado | M §4.3, D3 | MPN, standby seguro, terminación, desacoplos, TVS y pinout |
| Cuatro DI ISO1212 | Parcial | M §5.1/8.3, D4 | Valores de umbral/filtro/protección; separar condiciones del budget de diseño IEC |
| Dos DO y traductor | Parcial | M §§5.2–5.3/8.3, D5/D11 | Pull-downs, estado al arrancar/perder rails, carga inductiva, térmica, conectores |
| Dos ramas OR-ing | Parcial | M §6.2, D6/D7 | Sufijo LTC, protección coordinada, desacoplo y estados de pines sin uso |
| Protección TDS de entrada | Parcial | M §6.3, D8 | Margen de clamp, escenario de surge/OV continua y retorno/energía |
| eFuse | Parcial | M §§6.4–6.5, D9 | dvdt, Cin/Cout, EN, FAULT, peor caso ITH, arranque y layout térmico |
| Buck 3.3 V | Parcial | M §§6.6–6.7/8, W/T9/D12 | BOM FB, estabilidad, pérdidas, arranque/carga real y picos |
| Buck 5 V | Parcial | M §§6.6–6.7/8, W/T10/D12 | Lo anterior, especialmente carga ligera y eventual eliminación de CAN |
| SWD/consola/test points | Pendiente | PoC usa ST-LINK de Nucleo; headers genéricos L | Conector/pinout, VTref/GND/NRST y alimentación externa sin retorno indebido |
| Reglas mecánicas y PCB | Pendiente | R es solo guía general | Fabricante, stackup, dimensiones, montaje, impedancias y clearances |

## 4. Variantes, datasheets y circuitos de referencia

Los nombres de familia del maestro no bastan para congelar la BOM. Hay **19
dispositivos principales, doce tipos**, con dos reguladores que tienen BOM de
pasivos distintas. Las opciones de pedido siguientes son identificadas, no selecciones
automáticas. Todas requieren confirmar compra, revisión y encapsulado antes de CAD.
Las rutas D1–D13 se resuelven respecto a D de §2.

| Componente / cantidad | Variante documentada y encapsulado | Datasheet local y referencia de circuito | Cierre faltante / complejidad |
|---|---|---|---|
| STM32H723VET6 ×1 | Exacto, LQFP100, 14×14 mm, pitch 0.5 mm; VE tiene 512 KB Flash | D13 `DS_stm32h723zg.pdf`, DS13313 Rev.5; fig.5, tablas 7–8/14, figs.64–65; AN5419 §2 y circuito LDO | Alimentación/reloj/pines; alta, afecta toda la PCB |
| DP83826I ×1 | Familia; `DP83826IRHBR` identificado, RHB VQFN32 5×5 mm con pad expuesto | D1 `dp83826i.pdf`, SNLS647I; §8.4 straps, §9.2/figs.9-2,9-4,9-6; DP83826EVM como referencia | Cierre Ethernet completo; alta |
| THVD1420 ×2 | Familia; `THVD1420DR` SOIC8 o `THVD1420DRLR` DRL8; no intercambiables en PCB | D2 `thvd1400.pdf`, SLLSF78B; §8 aplicación, §9 alimentación, pinout p.3 | Preferir evaluar SOIC por montaje; terminación/protección/controles; baja-media por canal |
| ATA6561 ×1 | Familia; `ATA6561-GAQW` SOIC8 o `-GBQW` VDFN8; variantes industriales `-N` por confirmar | D3 `20005991B.pdf`, DS20005991B; aplicación §3, identificación p.25 | No sustituir por ATA6560: pin VIO/función difiere; media |
| ISO1212 ×2 | Familia; `ISO1212DBQR` SSOP16 identificado; no asumir equivalencia con sufijos S | D4 `iso1212.pdf`, SLLSEY7G; §8.2.1, figs.8-2/8-9/8-10, tabla 8-1 | Cuatro redes de campo, aislamiento y EMC; media-alta |
| BSP75N ×2 | Diodes DS33016; `BSP75NTA` o `BSP75NTC`, SOT223 tipo DN; embalaje distinto | D5 `BSP75N.pdf`, Rev.7-2; pinout/circuito interno, ratings p.3–4 y land pattern | No copiar otro fabricante BSP75N por nombre; baja-media |
| SN74LVC2T45 ×1 | Familia; DCU VSSOP8 o DCT SSOP8; YZP BGA no aconsejable para este plazo | D11 `sn74lvc2t45.pdf`, SCES516N; tabla 7-1 y fig.8-1 | Sufijo de pedido, pull-downs/secuencias; baja-media |
| LMR36015 ×2 | `LMR36015FBRNXR` propuesto: RNX VQFN-HR12, 2×3 mm, FPWM 1 MHz; AR es 400 kHz auto/PFM | D12 `lmr36015.pdf`, SNVSB49D; §§9.4.2,10.2, tabla 10-1 y ejemplo FB tabla 10-5 | Dos cálculos/BOM/validaciones diferentes; alta |
| NIS3071MT4TWG ×1 | Exacto, MT4 Auto-Retry, WQFN16 5×6 mm CASE 510CM con pad GND | D9 `NIS3071-D.PDF`, Rev.3; tabla 1, circuito/aplicación y fig.5 MT3/MT4 | No confundir MT3 latch, MTW4 ni NIV; media-alta |
| LTC4414 ×2 | Familia; `LTC4414EMS8#PBF` / `IMS8#PBF` y variantes reel; MSOP8 | D6 `4414fc.pdf`, Rev.C; fig.4 p.10 y aplicación de OR-ing | Grado térmico y pedido sin cerrar; margen de tensión no resuelto; alta por protección |
| DMP6023LSS-13 ×2 | Exacto, SO-8 convencional, sin pad inferior; no LE/SPS | D7 `DMP6023LSS.pdf`, DS37198 Rev.2-2; pinout, ratings y land pattern | Gate/source/drain y cobre térmico; baja-media |
| TDS3011P ×2 | Familia; código `TDS3011P.C`, DFN6 1.6×1.6 mm | D8 `TDS3011P.pdf`, Rev.2.0; tablas, conexión y land pattern | No es TVS SMA; múltiples pads/corriente de surge; media-alta |

AN5419 se consultó en la [fuente oficial ST, Rev.3 enero 2026](https://www.st.com/resource/en/application_note/an5419-getting-started-with-stm32h723733-stm32h725735-and-stm32h730-value-line-hardware-development-stmicroelectronics.pdf).
No estaba entre los PDF locales originales; la consulta web funcionó y el intento
de descarga local agotó el tiempo. No se marca como archivo local disponible.
El nombre `DS_stm32h723zg.pdf` no implica un ZG obligatorio: el documento cubre
xE/G; debe usarse la columna **LQFP100**, no LQFP144 de Nucleo.

## 5. Lista de pasivos y conexiones que falta cerrar

Es una lista de cierre del diseño actual, **no una BOM liberada**. `Definido`
significa valor/decisión existente en M; `guía` significa punto de partida del
fabricante aún por seleccionar; `TBD` significa que no hay valor aprobado.
Cantidades «por pin» o «por canal» requieren el pinout/topología final para
convertirse en cantidades de compra. No se fuerza un MPN ni una cantidad total
ficticia antes de ese cierre.

### MCU: alimentación, reloj, arranque y depuración

| Elemento | Lista y valor inicial verificable | Pendiente |
|---|---|---|
| VDD | Guía AN5419: 100 nF cerámico por VDD y 4.7 µF de reserva local | Contar pines LQFP100, seleccionar MPN/capacidad efectiva y ubicar por grupo |
| VDDA/VSSA | Guía: 1 µF + 100 nF; ferrita opcional, no obligatoria por defecto | Definir conexión a 3.3 V, filtro si procede y retorno; alimentar aunque no se usen ADC |
| VCAP | D13 tabla 14: dos 2.2 µF, ±20 %, ESR <100 mΩ para LDO; LQFP100 tiene VCAP en 48 y 73 | MPN y conexión según modo elegido; no llevar 3.3 V a VCAP ni cargarlo externamente |
| VBAT | Conexión a VDD si no hay batería; guía de desacoplo en AN5419 | Política sin batería y desacoplo real; no dejar flotante |
| VREF+ | Desacoplo/conexión según D13 y AN5419; referencia externa o VDDA, sin habilitar VREFBUF en conflicto | Valor/puente/filtro y número de pines específicos del encapsulado |
| USB y pines de alimentación especiales | Revisar columna física: VDD33USB/VDD50USB no existen en todos los encapsulados | No inventar pines ni dejar alimentaciones presentes sin tratamiento cuando USB no se use |
| HSE | Cristal/osc. y red de carga/serie: TBD; HSI posible solo tras cerrar precisión/PLL | Frecuencia, tolerancia, CL/ESR, arranque, capacitores con parásitos; no copiar reloj ST-LINK de Nucleo |
| LSE | Cristal 32.768 kHz y dos capacitores solo si RTC lo requiere | Proponer diferir LSE/RTC externo, no poblar red innecesaria |
| Reset | Capacitor NRST y pulsador/puente según AN5419; pull-up externo si justificado | Valores y descarga/tiempos; conexión al debug |
| BOOT0 | Resistencia a nivel de arranque seguro y acceso de recuperación, valores TBD | Interacción con option bytes y modo de carga; estado sin jumpers |
| SWD | Conector con SWDIO/SWCLK/NRST/VTref/GND; resistencias serie opcionales TBD | MPN, orientación, pin 1, tensión y prevención de alimentación inversa |
| Indicadores/test | Resistencias LED calculadas; test points 3.3/5/24/GND/reset | Selección, corriente y ubicaciones; indicadores extra son diferibles |

Para este H723, AN5419 distingue dispositivos con SMPS interno: **no copiar las
redes VLXSMPS/inductor de un H725/H735 al H723**. La propuesta de mínimo hardware
es VDD externo a 3.3 V con LDO interno, sujeta a confirmar configuración de arranque.
El esquema mínimo de la nota no sustituye el conteo físico ni la tabla de pines.

### Ethernet DP83826I

| Elemento | Lista a cerrar | Evidencia / restricción |
|---|---|---|
| RBIAS | 1 × 6.49 kΩ ±1 % a GND | D1 tabla de pines, pin 10; falta MPN/potencia/colocación |
| Desacoplo | Red por VDDA3V3 y VDDIO: guía 10 µF, 1 µF, 100 nF y 10 nF; ferritas opcionales | D1 fig.9-6: confirmar cantidades por alimentación/pin visualmente; no aprobar solo por texto extraído |
| Clock | Cristal 25 MHz con dos CL y resistencia si corresponde, o fuente CMOS compatible; leader produce referencia RMII apropiada, follower necesita 50 MHz | D1 §§8 y9.2.4: una sola fuente coherente, precisión/jitter y dirección por cerrar |
| Straps | Resistencias PU/PD de modo, dirección PHY, autonegociación, LED/clock y funciones BASIC/ENHANCED | D1 §8.4; defaults incluyen MII en determinados modos: sin straps no se supone RMII |
| MDIO/MDC | Pull-up MDIO si necesario; serie/terminación RMII solo según análisis | D1 documenta pull-up interno MDIO; no duplicar automáticamente ni colocar 49.9 Ω de otro PHY |
| Reset/interrupt/LED | Pulls/capacitor/reset, resistencias LED y conexiones sin uso | Tiempos de reset y strap sampling; evitar que LED/carga cambie el strap |
| Magnetics | Transformador 1:1 adecuado, center taps y red recomendada | D1 fig.9-2/tabla9-1; no adoptar la configuración transformerless fig.9-3 para RJ45 industrial |
| RJ45/chasis | MPN TBD; pinout del jack/magnetics, blindaje, red de terminación y capacitores de aislamiento | No hay conector seleccionado compatible; revisar circuito interno y tensión de aislamiento |
| Protección MDI | TVS/ESD de capacitancia y ratings compatibles, ubicación y retorno | No asumir que USBLC6 o TVS genérico 24 V sirven para pares Ethernet |

No hay BOM Ethernet cerrada. El [DP83826EVM oficial](https://www.ti.com/tool/DP83826EVM)
es fuente de referencia por adquirir/revisar en detalle, no prueba de equivalencia
de cualquier jack. El layout requiere MDI 100 Ω diferencial y RMII conforme al
datasheet, plano de retorno, tratamiento separado de chasis y aislamiento de magnetics.

### RS-485, CAN y E/S industriales

| Bloque / cantidad A | Pasivos y soporte pendientes | Qué ya existe / decisión técnica necesaria |
|---|---|---|
| THVD1420 ×2 | Desacoplo local por IC; 120 Ω por extremo terminador si corresponde; jumpers/puentes; pulls DE y /RE; bias externo solo si se justifica; TVS y elementos serie de protección; bornera y referencia de bus | D2 especifica fail-safe integrado, no implica inmunidad a surge de placa; no imponer bias innecesario. Calcular resistencia equivalente con dos terminaciones y potencia. Fijar TX inactivo al reset |
| ATA6561 ×1 | Desacoplo VCC 5 V y VIO 3.3 V; reserva local; terminación 120 Ω o split 2×60 Ω más C, una opción justificada; TVS CAN; choke opcional; pulls STBY/TXD; conector | D3 incluye aplicación y modos; integrar VIO, no confundir con ATA6560. Definir extremo de bus y estado recesivo/standby seguro |
| ISO1212 ×2 / 4 DI | Por canal: RSENSE, RTHR, CIN, protección y conector/FGND. Por IC: bypass VCC1; EN con nivel definido. Capacitancia a PE solo según estrategia de aislamiento | M usa RSENSE 562 Ω ±1 % y RTHR=0 como condición del budget, **no cierre de umbrales/EMC**. D4 tabla8-1 muestra redes diferentes: por ejemplo Type3 con 1 kΩ/10 nF o330 nF según ensayo. Elegir tipo, umbrales y respuesta antes de copiar valores |
| BSP75N ×2 | Pull-down de entrada/estado OFF, posible resistencia serie calculada, conector de carga, cobre térmico y protección energética de carga si necesaria | M fija 24 V/0.5 A y pérdidas ≈169 mW/canal a condiciones citadas; verificar Tj, energía inductiva y ciclo repetitivo; active clamp no garantiza cualquier inductancia |
| SN74LVC2T45 ×1 | Dos bypass locales (uno por rail), pulls de entradas A y evaluación de pulls B para pérdida de alimentación; resistencias serie si necesarias | M fija VCCA=3.3, VCCB=5 y DIR=VCCA. D11 §8.2.2 indica **no tiene pin OE**; no planificar un enable inexistente. Verificar capacidad source/sink, VIH/VIL y caída por resistencia bajo Icontrol máxima |

En DI verificar tolerancia/potencia continua y pulsada de RTHR, máxima tensión por
resistencia, ratings de CIN, distancia de aislamiento y relación FGND–GND–PE.
No unir tierras aisladas para facilitar routing. La selección Type1/2/3 y el
objetivo de ensayo cambian los pasivos; no se declara cumplimiento IEC por usar ISO1212.

En DO, 5 V de control debe seguir garantizando el nivel necesario en condiciones
de tolerancia/arranque. Los pulls deben mantener OFF con MCU sin configurar,
ambos rails subiendo en distinto orden y programador conectado. Una resistencia
serie grande puede reducir la entrada por debajo de la tensión necesaria para
las protecciones: comprobarla, no copiar una resistencia de gate de MOSFET común.

### Alimentación: lista por rama y por convertidor

| Red | Elementos que deben figurar o tener omisión justificada | Estado |
|---|---|---|
| Conector de entrada | Bornera/jack con rating, protección de polaridad, corriente/fusible si procede, cableado y retorno | TBD. Una sola entrada no elimina necesidad de seguridad eléctrica |
| TDS3011P por entrada | Conexión shunt completa, pads correctos y retorno corto; coordinación de protección/cable/fuente | Dispositivo elegido; no hay componente serie implícito ni protección de sobretensión continua |
| LTC4414 + DMP por entrada | PFET, desacoplo/reserva apropiados; CTL bajo definido; STAT pull-up si se usa; tratamiento NC; gate/sense y Kelvin | Topología y pérdidas justificadas; valores/MPN restantes y margen sin cerrar. No añadir zener/gate resistor por costumbre sin comprobar control |
| eFuse | R_LIM 43.2 kΩ E96; C_dvdt; Cin/Cout/reserva; FAULT pull-up si se usa; EN definido; TVS/Schottky si análisis de transitorios la exige | Solo R_LIM fijada. D9 tabla1 da 15 kΩ como referencia para FAULT. Elegir C_dvdt con carga/capacitancia y corriente de arranque; no inventar C_DVDD de otra variante |
| Canales eFuse sin uso | INx y ENx a GND y OUTx sin carga, según M/D9 | Conexiones definidas, falta incorporarlas al símbolo/netlist y conectar pad GND |
| Filtro de entrada | LC/pi y damping solo si justificados | 20–50 kHz en M es orientación conceptual, no valores L/C aprobados ni cumplimiento EMC |

| Pasivo de cada LMR36015FB | 3.3 V, diseño 0.7 A | 5 V, diseño 0.1 A | Cierre obligatorio |
|---|---|---|---|
| L | Guía tabla10-1: 6.8 µH | Guía: 10 µH | MPN, tolerancia, Isat, Irms, DCR, pérdida núcleo/cobre y protección de corriente |
| Cin | Guía ≥4.7 µF más bypass 220 nF en cada par VIN/PGND | Igual función; cálculo propio | Rating frente a máximo/transitorio, capacidad efectiva y corriente RMS. Tabla10-1 orienta 4.7 µF +2×220 nF por IC |
| Cout | Guía 3×15 µF, mínimo tabulado2×15 µF | Igual guía, no implica mismo MPN | Capacidad efectiva, ESR, estabilidad/transitorio, ripple y corriente de carga/descarga |
| RFBT/RFBB | Guía100 kΩ/43.2 kΩ | Guía100 kΩ/24.9 kΩ | Tolerancias, VREF y error DC; no confundir RFBB43.2 kΩ con R_LIM del eFuse |
| CFF | Guía20 pF | Guía20 pF | Verificar lazo; no añadir/omitir sin revisar §10.2.1.2.9 |
| Cboot |100 nF, al menos16 V, BOOT–SW | Igual | MPN cerámico, ubicación y rating; no copiar10 V de W |
| Cvcc |1 µF/16 V, VCC–GND | Igual | VCC es bias interno, no rail externo5 V |
| EN | Conexión a VIN permitida o divisor UVLO dimensionado | Igual decisión | No flotante; cerrar umbrales y secuencia |
| PG | Pull-up si usado, guía10–100 kΩ; tratamiento si no usado | Igual | Dominio correcto, no aplicar24 V a entrada MCU |
| Soft-start/SW/NC/tierras | Según pines y funciones exactas D12 | Igual | No añadir SS externo donde no hay pin; AGND/PGND y SW–NC según datasheet |

Puntos de cálculo que faltan para ambos bucks:

1. ΔIL por VIN/VOUT/f y tolerancia de L; Ipeak y RMS en todo el rango. Para el
   criterio de rizado, D12 indica usar la capacidad de 1.5 A del IC, no reducir
   sin más el inductor porque el rail de 5 V consuma pocos mA.
2. Capacidad efectiva bajo bias/temperatura/tolerancia, ESR y corriente RMS de
   capacitores. Rating nominal por encima del pico real, no solamente de 24 V;
   el ejemplo D12 usa capacitores de entrada100 V, cuya necesidad debe contrastarse
   con la protección y derating elegidos, no asumir50 V o35 V suficientes.
3. Carga ligera, apagado parcial y arranque: FB fuerza corriente inversa; no
   garantiza pérdidas bajas. Con CAN diferido, el rail de 5 V puede caer a pocos
   mA de control DO, por lo que se debe volver a evaluar, no usar72.403 mA de A.
4. Pruebas/cálculos a VIN18/24/30 V, carga nominal, capacidad de diseño y escalones;
   min ON/OFF y f extremo. La comprobación de tiempos de M es útil pero no basta.
5. Eficiencia/pérdidas/Tj propias de IC y pasivos, sin aplicar pérdidas totales
   del convertidor a θJA del IC. Actualizar balance eFuse con estos resultados.

## 6. Pinout: viabilidad física preliminar, no asignación final

No existe pinout completo aprobado. D13 tablas7–8 muestra una ruta RMII posible
en LQFP100; esto permite conservar el MCU y evita una migración injustificada.

| Señal para cotejo | Puerto de H723 disponible | Conflicto que debe reservarse |
|---|---|---|
| RMII REF_CLK / MDIO / MDC | PA1 / PA2 / PC1 | PA1 también USART2_DE, PA2 USART2_TX; no reservar USART2 sin revisión |
| RMII CRS_DV, RXD0, RXD1 | PA7 / PC4 / PC5 | GPIO/ADC/SPI alternativos; validar AF y número físico |
| RMII TX_EN, TXD0, TXD1 | PB11 / PB12 / PB13 | PB11 USART3_RX; PB12/13 FDCAN2_RX/TX, no pueden usarse simultáneamente |
| SWD | PA13/PA14, NRST | No reutilizar como E/S; reservar consola/debug y BOOT0 |
| HSE | PH0/PH1 | Red de reloj/recuperación y alimentación del MCU por cerrar |

El F429ZI de la PoC tiene otros puertos expuestos: **no copiar PG11/PG13/PG14 de
una Nucleo a este LQFP100**. USART3 en PD8/PD9 es una posibilidad a revisar, no
una asignación aprobada. Cerrar dos UART/DE, FDCAN si A, cuatro DI y dos DO,
reset/IRQ PHY, PG/FAULT si se usan y consola. La tabla definitiva necesita
puerto, AF, pin físico, dirección, rail, estado reset y función alternativa excluida.

## 7. CAD: disponible, localizado y verificado son estados distintos

No se encontró recurso CAD local de ninguno de los doce tipos principales.
Las páginas oficiales de varios fabricantes ofrecen acceso a proveedores CAD,
pero eso **no equivale a disponer de un SchLib/PcbLib homologado**.

Estados de la matriz: `L` = recurso localizado localmente, sin homologar;
`F` = fuente/portal encontrado; `P` = solo pinout/dibujo mecánico disponible como
base para preparar CAD. Ninguna fila tiene símbolo y footprint **verificados**.
Las estimaciones son horas-persona de circuito+preparación CAD antes de esquemático,
sin sumar placement/routing. Las copias de un mismo IC reutilizan la homologación.

| Componente | Símbolo | Footprint | Pasivos cerrados | Estado | Tiempo pendiente | Bloqueador |
|---|---|---|---|---|---:|---|
| STM32H723VET6 | F, no local/verificado | F/P LQFP100; no verificado | No | Seleccionado |3–4.5 h | Alimentación y cotejo100 pines |
| DP83826IRHBR, opción por ratificar | F, vista previa exacta | F, vista previa RHB32 | No | Seleccionado |4–6 h | Reloj/straps/jack y pad expuesto |
|2×THVD1420, paquete por cerrar | F TI | F TI, D oDRL | No | Seleccionado |1–2 h | MPN/bus/protección |
| ATA6561, paquete por cerrar | P/fuente de fabricante | P SOIC/VDFN | No | Seleccionado |1–2 h | Sufijo/control/terminación |
|2×ISO1212, paquete por cerrar | F TI | F TI DBQ16 | No | Parcial |2–3.5 h | Cuatro redes DI/aislamiento |
|2×BSP75NTA/TC por ratificar | P Diodes | P SOT223 tipoDN | No | Parcial |1–1.5 h | Pinout/estado seguro/térmica |
| SN74LVC2T45, paquete por cerrar | F TI | F TI DCU/DCT | No | Parcial |0.5–1 h | No OE; secuencia3.3/5 V |
| LMR36015FB3.3 V | F TI | F TI RNX12 | No | Parcial |2.5–4 h | BOM/validación específica |
| LMR36015FB5 V | Reutiliza símbolo anterior | Reutiliza footprint anterior | No | Parcial |1.5–3 h adicionales | Carga ligera y BOM propia |
| NIS3071MT4TWG | P, fuente onsemi | P CASE510CM, no verificado | Solo R_LIM | Parcial |1.5–2.5 h | dvdt/arranque/límites/pad |
|2×LTC4414, sufijo por cerrar | F ADI | F MSOP8 | No | Parcial |1–2 h | MPN/margen; protección se estima aparte |
|2×DMP6023LSS-13 | P Diodes | P SO8 | No red completa | Parcial |0.5–1 h | Orientación y múltiples S/D |
|2×TDS3011P.C por ratificar | P Semtech | P DFN6 específico | No coordinación | Parcial |1–2 h | Clamp/retorno/pads |
| RJ45/magnetics/reloj/ESD | P, MPN TBD | P, MPN TBD | No | Pendiente |2–4 h | Bloque Ethernet incompleto |
| Pasivos/borneras/headers L | L | L, no verificados para BOM nueva | No | Parcial |1–2 h por lote inicial | Ratings, MPN y dimensiones |

Estos intervalos se solapan en revisión de interfaces y se distribuyen en las
filas de selección/símbolos/footprints de §10; **no sumarlos de nuevo al total**.
No incluyen una iteración mayor de rediseño del front-end si las protecciones
no pueden coordinarse con los componentes elegidos.

### Fuentes CAD confiables consultadas

- [ST STM32H723VE, CAD Resources](https://www.st.com/en/microcontrollers-microprocessors/stm32h723ve.html):
  página oficial y sección CAD; no se obtuvo archivo exacto verificable. La
  [lista regional ST](https://www.stmcu.jp/design/hwdevelop/cad/92261/) también
  identifica H723VE. No confundir modelos VE con ZG.
- [TI DP83826I](https://www.ti.com/product/DP83826I),
  [THVD1420](https://www.ti.com/product/THVD1420),
  [ISO1212](https://www.ti.com/product/ISO1212),
  [SN74LVC2T45](https://www.ti.com/product/SN74LVC2T45) y
  [LMR36015](https://www.ti.com/product/LMR36015): enlaces oficiales a Ultra Librarian
  por encapsulado. El portal de DP83826I resolvió la referencia exacta
  `DP83826IRHBR`, mostró vistas de símbolo/footprint RHB32 y opciones Altium
  script/native; esto es una localización concreta, no un modelo homologado.
- [ADI LTC4414](https://www.analog.com/en/products/ltc4414.html): modelos de pedido
  y enlaces Ultra Librarian/SamacSys oficiales por MSOP8.
- [Diodes BSP75N](https://www.diodes.com/part/view/BSP75N) y
  [DMP6023LSS](https://www.diodes.com/part/view/DMP6023LSS): dibujos y datasheets;
  no se confirmó descarga CAD exacta en las páginas inspeccionadas.
- [Microchip ATA6561](https://www.microchip.com/en-us/product/ata6561),
  [onsemi NIS3071/D](https://www.onsemi.com/download/data-sheet/pdf/nis3071-d.pdf)
  y [Semtech TDS3011P](https://www.semtech.com/products/circuit-protection/surgeswitch/tds3011p):
  referencias de pinout/package; no se obtuvo modelo Altium verificado.

Se recuperó la página HTML del portal CAD de TI a una carpeta temporal de auditoría.
No se descargó ni importó un modelo de componente nuevo: el flujo de Ultra Librarian
incluye registro/condiciones y exportación que no se completaron en esta sesión.
No se da por hecho acceso autenticado ni se atribuye un fallo de consulta web a
inexistencia del modelo. Las fuentes están identificadas para su adquisición
autorizada y revisión; no es necesario esperar un proveedor si se puede preparar
un recurso trazable desde el dibujo exacto dentro del tiempo estimado.

Procedimiento para convertir `F/P` en «verificado»:

1. Congelar MPN/encapsulado y revisión del datasheet; guardar origen/hash del CAD
   descargado aparte de la librería docente. No ejecutar scripts de importación sin revisarlos.
2. Cotejar **todos** los pines del símbolo, alimentación oculta, partes múltiples,
   NC y pad expuesto. Verificar nombres, números, direcciones y pin types para ERC.
3. Cotejar numeración/orientación del footprint, dimensiones mínima/máxima,
   pitch, filas, taladros, máscara y pasta con el land pattern del fabricante.
   RNX HotRod, RHB, CASE510CM y DFN6 TDS son prioritarios; un QFN genérico no basta.
4. Revisar pin1 y vista superior/inferior, múltiples drain/source del SO8 y
   SOT223; después un registro de revisión con MPN, recurso y verificador.

Los footprints SO8/SOT223 presentes en L pueden ayudar geométricamente, pero
no se declara que correspondan a BSP75N/DMP sin cotejo. Tampoco el capacitor
100 nF Y5V de L es sustituto automático de los X7R/X5R especificados.

## 8. Riesgos P0/P1/P2 y condiciones de salida

P0 bloquea liberar el circuito afectado o avanzar directamente a PCB; P1 es
trabajo obligatorio antes de esquemático/layout según la columna; P2 puede
diferirse sin omitir conexiones esenciales. Una decisión de aceptar riesgo no
constituye validación eléctrica ni transforma un P0 técnico en un circuito seguro.

| Prioridad | Riesgo y evidencia | Para cerrarlo / momento |
|---|---|---|
| P0 | TDS máximo40 V coincide con absoluto40 V de LTC4414; M§6.3 lo conserva como trade-off aceptado | Mantener registro del trade-off; definir surge/fuente y coordinar protección con margen incluyendo L·di/dt. No garantizar inmunidad industrial actual. Si no hay solución demostrada, no liberar esa entrada |
| P0 | Ethernet sin magnetics/jack/reloj/straps completos, M/D1 | BOM y circuito de referencia cotejados, pinout de jack y modos de clock antes de esquemático definitivo |
| P0 | Alimentación mínima H723 sin cierre, D13/AN5419 | VDD/VDDA/VBAT/VCAP/reset/BOOT/reloj y tratamiento de todos los pines antes de ERC |
| P0 | Ningún IC principal con CAD local homologado | Cotejo pin/pad/dimensiones de recursos críticos antes de transferir a PCB |
| P0 | Bucks FB sin pasivos ni respuesta verificados; W/T son AR u otro IC | Congelar cada BOM, cierre de corriente/ripple/estabilidad/arranque y evaluación térmica; no copiar resultados AR |
| P1 | Pinmux sin tabla; PB11 RX USART3 y PB12/13 FDCAN2 comparten RMII | Tabla física y controles/defaults antes de asignar nets |
| P1 | ITH por gráfica y margen eFuse sin pérdidas L3/L5; C_dvdt TBD | Peor caso de carga/arranque a18 V, tolerancias, protección y respuesta Auto-Retry antes de cerrar alimentación |
| P1 | DO pueden activarse al reset/secuenciar rails; traductor sin OE | Pulls, corriente de control, tensión mínima y estado seguro antes de esquemático |
| P1 | DI:562 Ω/0 Ω del budget no define umbral y EMC | RTHR/CIN/protección/aislamiento por tipo y objetivo, antes de esquemático si se conservan |
| P1 | Fuente24 V, rail5 V y3.3 V pueden retroalimentarse por IO/debug o retornos | Revisar secuencias, Ioff, clamps, niveles y cargas; no asumir aislamiento de toda la placa porque las DI lo tengan |
| P1 | Capas/reglas/fabricante desconocidos | Stackup confirmado, impedancia y retorno Ethernet, corriente/clearance/ensamble antes de placement/routing |
| P1 | CAD pequeño y montaje: RNX2×3 mm, TDS1.6 mm, pads térmicos | Capacidad real de stencil/reflow/fabricante; reglas de pasta/vías y montaje antes de fabricar |
| P1 | Referencias/pasivos sin disponibilidad física/comercial probada | MPN y acceso real para no liberar BOM impracticable; CAD no acredita existencias |
| P2 | Diagramas decorativos, 3D no requerido para interferencias críticas, LEDs extra, diagnóstico avanzado | Diferir; conservar documentación mínima de programación, ensamblaje y fabricación |

**Capas:** cuatro capas es la hipótesis de estimación para facilitar plano GND
continuo y routing H723/RMII. No es una ley de mínimo universal. Dos capas exige
demostrar retorno, impedancia, espacio y térmica; no se adopta como ahorro seguro.
Anchura/separación mínima, vías, anillos, cobre, stackup, taladros y clearances
deben venir del fabricante. No fijar reglas numéricas inventadas. Routing MDI,
clock/RMII y loops buck deben priorizarse, con retornos de surge/carga controlados.

## 9. Escenarios, ahorro y conservación de DO

| Aspecto | A: Rev. A completa | B: simplificación conservadora propuesta | C: contingencia mínima |
|---|---|---|---|
| MCU/Ethernet | H723VET6 + DP83826I/RMII | Idénticos | Idénticos |
| RS-485 |2×THVD1420 |1×THVD1420 |1×THVD1420 |
| CAN-FD | ATA6561 | Diferido | Diferido |
| DI |4 mediante2×ISO1212 | Diferidas | Diferidas |
| DO |2×BSP75N + traductor | **Se conservan ambas** | Diferidas, solo como contingencia aprobada |
| Entradas de alimentación | Dos con OR-ing | Una entrada protegida, sin redundancia | Una entrada protegida |
| Front-end de referencia para estimar |2×TDS/LTC/PFET + NIS |1×TDS/LTC/PFET + NIS, con riesgo de clamp aún por resolver | Igual que B; no se omite protección |
| Bucks |3.3 V y5 V |3.3 V y5 V por DO |Solo3.3 V si no queda ninguna carga5 V |
| Programación | SWD, reset/BOOT, soporte mínimo | Igual | Igual |
| Renuncias frente al producto | Ninguna prevista; cumplimiento aún no validado | Un RS-485, CAN, cuatro DI y redundancia | Lo anterior más dos DO y rail5 V |
| Viabilidad con26–30 h | No defendible | Condicional y ajustada incluso en extremo bajo | Marginal en extremo favorable; no garantizada |

En B/C se estima reutilizar una rama LTC/DMP existente, no diseñar de cero una
entrada distinta. **Quitar una entrada no corrige el margen del LTC restante.**
Una alimentación externa regulada con protecciones comprobadas puede estudiarse
como alternativa, pero no se incluye como ahorro automático ni se instala una
fuente hipotética para hacer caber las horas.

El mayor ahorro demostrable por estructura de trabajo es **diferir las cuatro DI
y CAN-FD**, porque evita cerrar redes de campo, aislamiento, protección y routing
adicionales. Aproximadamente6–10 h base; segundo RS-485 ahorra1–2 h; la segunda
rama de entrada1–2 h, porque comparte tipos de CAD con la primera. Son ahorros
orientativos que se solapan con colocación/revisión; no sumarlos mecánicamente
contra los intervalos completos. No se ahorra todo el tiempo de homologar LTC/PFET
al dejar solo una rama. Ethernet y alimentación siguen en la ruta crítica.

**Conservar DO en B.** La definición de salida y el control5 V ya tienen análisis
útil. Completar dos BSP75N+traductor puede requerir2–4 h marginales entre selección,
CAD simple, esquemático y routing. Al conservar además un buck5 V que C elimina,
el costo marginal conjunto es del orden de **4–7 h**, dependiente de la validación
del rail a carga muy ligera. No es cero ni motivo para eliminarlas primero.
Si el viernes el rail5 V o el estado seguro no cierran, reconsiderar C como
contingencia explícita; no retirar DO para aparentar que se resolvió Ethernet.

## 10. Horas pendientes por escenario

Trabajo ya aprovechable: inventario, datasheets, arquitectura, corrientes
condicionadas, planteamiento del budget, pérdidas de conducción y elección de
familias. No se asignan horas históricas ficticias ni se restan dos veces.
**Esquemático, ERC, placement, routing y DRC demostrados del gateway: ninguno.**

| Actividad pendiente | A (h) | B (h) | C (h) |
|---|---:|---:|---:|
| Diseño eléctrico, selección de pasivos, cierre de pines y comprobaciones de alimentación |8–12 |5–8 |4–6 |
| Preparación/verificación de símbolos |2–3 |1.5–2.5 |1–2 |
| Preparación/verificación de footprints |4–6 |2.5–4 |2–3 |
| Esquemático completo |5–7 |3.5–5 |3–4 |
| ERC y revisión eléctrica cruzada |2–3 |1.5–2 |1.5–2 |
| Placement |3–4 |2–3 |1.5–2.5 |
| Routing y planos |8–12 |5–8 |4–6 |
| DRC y revisión visual/retornos/térmica de layout |2–3 |1.5–2.5 |1.5–2 |
| Documentación y fabricación |1.5–2 |1–1.5 |1–1.5 |
| **Subtotal** |**35.5–52** |**23.5–36.5** |**19.5–29** |
| Margen de correcciones25 % |8.9–13 |5.9–9.1 |4.9–7.3 |
| **Total calculado** |**44.4–65** |**29.4–45.6** |**24.4–36.3** |
| **Intervalo de planificación redondeado hacia arriba** |**45–65** |**30–46** |**25–37** |

Hipótesis: una persona, Altium ya operativo, acceso a los portales CAD, paquetes
de montaje razonables elegidos pronto, cuatro capas, placa compacta sin mecánica
especial ni BGA/via-in-pad obligatorio, una iteración menor de correcciones.
Selección incluye cálculos y validación dirigida, no ensayo físico de placa.
La revisión ERC no reemplaza revisión de datasheet, ni DRC verifica la lógica del circuito.

Los mínimos suponen que los P0 se resuelven con referencias existentes y no hay
que rediseñar la protección. Acceso CAD fallido, una nueva topología de protección,
iteraciones mayores de conversión o cambio a dos capas pueden exceder el máximo.
No se supone trabajo en paralelo de otros diseñadores. Fabricación, compra,
montaje y validación física quedan fuera del plazo de archivos terminados.

Si se consiguen **seis horas efectivas de cierre técnico antes del sábado**,
quedarían aproximadamente A39–59, B24–40 o C19–31 h. Se trata de restar trabajo
completado y revisado, no meramente tiempo transcurrido. Con20–24 h de fin de
semana, B/C solo caben en la parte favorable, mientras A sigue fuera.

## 11. Decisiones y plan para jueves/viernes

### Antes del sábado: condiciones de arranque

1. Aprobar A/B/C; preferencia B con ambas DO. Conservar el H723. Registrar renuncias
   de B/C aparte del maestro y confirmar si se necesita1 o2 RS-485 este fin de semana.
2. Resolver el criterio de transitorios de entrada y la coordinación TDS/LTC.
   No convertir el trade-off de40 V en afirmación de protección garantizada.
3. Cerrar MPN y paquetes de PHY/transceivers/traductor/LTC/BSP, variante de cada
   buck y jack/magnetics/relojes exactos. La familia LMR no queda cuestionada por
   falta de resultados FB; lo pendiente es su implementación concreta.
4. Congelar pinout LQFP100, dirección de reloj RMII y estados seguros DO/DE/STBY.
5. Confirmar fuente/carga, montaje, capas, reglas del fabricante y acceso a CAD.
   Recursos críticos necesitan estar homologados antes del layout, aunque no
   todos puedan completarse en las cuatro horas del viernes.
6. Acordar fecha de revisión ERC/eléctrica y DRC/fabricación. Si no hay P0 cerrado,
   no prometer paquete fabricable el domingo.

### Jueves5: dos horas de preparación propuesta

| Tiempo | Tarea ejecutable tras aprobación | Resultado verificable |
|---|---|---|
|0:00–0:30 | Decidir B/C y límites de prueba/entrada; revisar P0 del front-end | Registro de alcance y responsable por bloqueo |
|0:30–1:15 | Revisar MPN/encapsulados y tabla de reservas H723/RMII/SWD | Lista de pedidos candidata y conflictos identificados |
|1:15–2:00 | Confirmar acceso Altium/portales, reglas del fabricante y referencias Ethernet | Carpeta de fuentes trazables y lista de faltantes; sin dibujar esquemático |

### Viernes6: cuatro horas concretas

| Tiempo | Tarea | Salida y punto de decisión |
|---|---|---|
|0:00–0:45 | Cerrar alimentación mínima y conteo de pines H723 usando D13/AN5419; fijar reloj y reservas | Hoja de pinout y lista de desacoplos/VCAP/reset/BOOT, con TBD explícitos |
|0:45–1:30 | Obtener y cotejar CAD prioritario H723/PHY; anotar pines/pads/paquetes; pedir acceso humano al portal si falta | Recursos descargados identificados y estado de homologación, sin importación ciega |
|1:30–2:30 | Resolver referencia Ethernet: leader/follower, straps, RBIAS, magnetics/jack y protección | Lista de conexiones/pasivos para revisión; si jack o reloj siguen abiertos, Ethernet continúa P0 |
|2:30–3:30 | Cerrar BOM y comprobaciones prioritarias de bucks; comparar FB con AR realmente disponible; decidir EN/PG y arranque eFuse | Tabla de pasivos por rail y resultado documentado de comprobaciones; no declarar simulación ejecutada si no lo fue |
|3:30–4:00 | Revisar coordinación TDS/LTC y estado seguro DO; consolidar P0 pendientes y horas restantes | Decisión de continuar/replanificar; DO se mantienen salvo bloqueo concreto demostrado |

Este plan prioriza la ruta crítica; **no afirma que45 min homologuen100 pines más
todo el PHY**, ni que1 h valide dos bucks desde cero. Si se acaba una franja con
TBD, registrarlo y consumir la estimación restante; no trasladar la incertidumbre
al routing. Las cuatro horas no alcanzan para todos los trabajos previos de B.
Si jueves no resolvió protección, se adelanta esa revisión el viernes desplazando
CAD/bucks, con el correspondiente aumento de trabajo del sábado.

Después de aprobación y de cerrar bloqueos: sábado debería terminar esquemático,
ERC revisado, recursos CAD homologados y colocación de bloques críticos. Si no
ocurre, replanificar antes de dedicar domingo a routing. Domingo se reserva a
routing completo, planos, DRC/revisión visual y paquete de fabricación.

## 12. Criterio de terminación y recomendación para revisión

«Terminado» exige esquemático completo del alcance aprobado, ERC y revisión
eléctrica con excepciones justificadas, footprints verificados, placement,
conexiones100 % rutadas, planos, DRC revisado, inspección de Gerber/Excellon,
notas/stackup, BOM consolidada con MPN/cantidad y documentación mínima de montaje,
alimentación y programación. Nada de ello acredita fabricación o validación física.

**Recomendación:** aprobar el estudio de B conservando ambas DO, congelar alcance
y cerrar los P0 antes de comprometer la entrega. A requiere aproximadamente
45–65 h y no cabe en26–30 h. B reduce trabajo real sin migrar MCU, pero necesita
30–46 h; ampliar plazo es la opción más defendible. C,25–37 h, es contingencia
para una entrega mínima y solo cabe en el extremo favorable tras cerrar fuentes,
CAD y Ethernet. Si el domingo 8 se exige un paquete fabricable revisado,
no prometer A ni ocultar pendientes bajo resultados WEBENCH de otra variante.

La simplificación propuesta no sustituye Rev. A. Esta auditoría se detiene para
revisión humana; no se inició esquemático/PCB, no se implementó firmware ni se
hizo commit o push.
