# Gateway académico — preparación para Altium

Revisión propuesta, 2026-11-05. STM32H723VET6 conservado. Rev. A y el firmware
permanecen intactos. Esta carpeta contiene recursos reales de preparación;
**contiene ahora un PrjPcb académico y bibliotecas editables; no contiene un esquemático del gateway ni PCB**.

Actualización 2026-11-06: `Industrial_Gateway_Academic.PrjPcb` referencia las
bibliotecas locales `libraries/Gateway_Academic.SchLib` (37 símbolos) y
`libraries/Gateway_Academic.PcbLib` (15 footprints). El paquete
`libraries/Gateway_Academic.LibPkg` está preparado; IntLib/compilación y colocación
nativa pendientes. Estado final **Conditional**. Ver
[`altium_library_preparation_report.md`](../../docs/hardware/altium_library_preparation_report.md)
para cobertura, fuentes y la lista final de componentes inconclusos.

## Archivos utilizables

- `libraries/Professor_shared.SchLib` y `.PcbLib`: fuentes nativas extraídas sin
  cambios de la IntLib del profesor: 71 entradas de símbolo, incluida plantilla,
  y 37 footprints. Extracción y asociaciones comprobadas; geometría no homologada.
- `libraries/SS3P6L-M386A.{SchLib,PcbLib}`: recurso existente del diodo Vishay,
  candidato a protección de polaridad de la única entrada; no seleccionado definitivamente.
- `libraries/CL10B103KA8WPNC.{SchLib,PcbLib}`: recurso existente de capacitor,
  útil para evaluar bypass/filtro de baja tensión, **no sustituto del CIN de DI de 100 V**.
- `libraries/library_manifest.json`: procedencia, hashes y límites de verificación.
- `libraries/sources/`: paquete oficial TI DP83826EVM, esquema de referencia,
  guía/BOM, guía oficial CAN Microchip, datasheet Vishay y fichas exactas Yageo/KEMET.
  `acquisition_manifest.json` registra URL, tamaño y SHA-256. Los Gerbers dentro
  del ZIP TI son del EVM, **no fabricación de nuestro gateway**.
- `mcu_pin_reference.csv`: los 100 pines físicos LQFP100, cotejados con DS13313
  Rev.5 tabla 7 y visualmente con figura 5. Hay cinco VDD, cinco VSS y dos VCAP.
- `pin_reservations.csv`: 32 reservas propuestas, sin pines repetidos. RMII usa
  PB11/12/13; RS-485 usa USART3 PD8/9; CAN usa FDCAN1 PB8/9. Evita conflictos
  con FDCAN2 y el pinout de la Nucleo de 144 pines. No es un DTS ni pinout aprobado.
- `interface_pin_checks.csv`: correspondencia de los 8 pines THVD1420, 8 ATA6561
  y 16 ISO1212. `reference_connections.csv` añade nueve conexiones de pasivos de
  referencia, cotejadas con los diagramas. No son una netlist de placa liberada.
- `passive_worklist.csv`: 39 grupos de pasivos, cantidades del alcance académico,
  fuentes y estados. Los valores guía y selecciones abiertas están identificados.
- `cad_queue.csv`: cola de adquisición/verificación para 18 componentes o grupos.
- `electrical_screening.json`: presupuesto reducido y cálculos de cribado de DI/bucks.
- `prepare_data.py`: regenera las tablas y comprueba cobertura, exclusividad de
  pines y hashes; `preparation_checks.json` conserva el resultado.

## Alcance propuesto y cierre eléctrico

Se mantienen H723/Zephyr, DP83826I, un THVD1420, ATA6561, un ISO1212/dos DI,
dos BSP75N con adaptación, entrada única 18–30 V, 3.3/5 V y SWD. Se difieren
segundo RS-485, dos DI, redundancia, memoria externa y expansión. Ninguna de
estas propuestas cambia el maestro original.

| Bloque | Cerrado en este avance | Falta para liberarlo / dibujarlo definitivamente |
|---|---|---|
| STM32 mínimo | Tabla física completa y reserva sin solapamientos; conteo de cinco bypass VDD y dos VCAP | Símbolo/footprint, MPN de capacitores, HSE, NRST/BOOT y red analógica completa |
| Alimentación | Presupuesto académico recalculado; límites de cribado de ambos bucks | Front-end, inductores/derating/capacitancia efectiva, estabilidad, térmica, inrush y CAD |
| Ethernet | Esquema/ensamblaje/BOM oficiales descargados; componentes MDI de referencia identificados | Modo/straps, reloj, jack/magnetics y ESD cotejados; todo CAD principal |
| RS-485 | Mapeo de 8 pines y dirección DE+/RE; USART reservado | Pulls, terminación/rating, protección y CAD |
| CAN-FD | Mapeo de 8 pines y dos bypass de 100 nF respaldados por guía oficial | Terminación/rating, pulls seguros, TVS, conector y CAD |
| DO | Dos comandos reservados; BSP75N de Diodes y tab source identificados | Nivel alto garantizado con tolerancias/corriente, OFF al arranque, carga real, térmica y CAD |
| DI | Red funcional Type 3: 562 Ω/1 kΩ/10 nF, pinout y conexión SENSE/IN comprobados visualmente | MPN y footprint MELF, reglas de aislamiento, conectores y revisión de transitorios |

**Bloques completos liberados eléctricamente: cero. Bloques dibujados: cero.**
Las redes funcionales CAN/DI y las reservas del MCU ya tienen datos para iniciar
su captura cuando se revisen sus recursos, pero sus interfaces/protecciones no
se presentan como cerradas. No se ejecutó ERC/DRC ni validación física.

### Reutilización y nuevos pasivos

- Reutilizables para evaluación: resistencias de baja potencia de 0 Ω, 10 kΩ,
  1 kΩ y otros valores disponibles; capacitores de baja tensión con ratings
  adecuados; borneras, headers, pulsador y LEDs. Cada uso depende de potencia,
  tolerancia, pinout y dimensión. El 100 nF Y5V del profesor no se aprueba como
  reemplazo automático del X7R; el 120 Ω de 0.1 W no se homologa como terminación
  industrial universal.
- CAN añade dos bypass de 100 nF y terminación seleccionable de 120 Ω, más
  pulls/protección por cerrar. La reserva de 22 µF del ejemplo Microchip depende
  del regulador; no es un requisito fijo ni un capacitor que deba añadirse a ciegas.
- DI añade dos RSENSE de 562 Ω/1 %, dos RTHR de 1 kΩ **MELF ≥0.25 W**, dos CIN
  de 10 nF y un bypass lógico de 100 nF. Se obtuvieron fichas de
  `RC0603FR-07562RL` y `C0603C103K1RACTU`; MPN MELF y homologación CAD siguen abiertos.
  La potencia DC pequeña no permite sustituir RTHR por el 0603/0.1 W existente:
  su función de limitación de surge exige comprobar pulso y tensión.
- ISO1212: SUB1/SUB2 necesitan tratamiento de islas flotantes según fabricante,
  no se conectan a GND/FGND ni entre sí. Mantener FGND separado de lógica;
  compartir referencias externas puede puentear el aislamiento del sistema.

### Bloqueos que siguen activos

1. **Altium sin control UI:** está instalado en `C:/Program Files/Altium/AD26/X2.EXE`,
   pero la API de aplicaciones respondió `native pipe is unavailable` y no pudo
   inventariar ventanas. No se pudo abrir, importar, dibujar ni verificar guardado
   en la aplicación. Los archivos nativos preparados no se han probado abriéndolos.
2. **Protección de entrada:** para entrada única se propone retirar OR-ing/LTC4414
   y evaluar Schottky SS3P6L + protección TDS/eFuse. Evita depender del LTC de
   máximo absoluto 40 V, pero **no queda aprobado**: falta térmica del diodo,
   polaridad, inrush, coordinación de surge/OV continua y retorno. El TDS solo
   no limita una sobretensión continua arbitraria. No se ha sustituido la arquitectura.
3. **Bucks FB:** el cribado usa las guías 6.8/10 µH, tolerancia supuesta de L ±20 %
   y oscilador 0.85–1.15 MHz. A 30 V produce ΔIpp ≈0.635/0.613 A; el rail 5 V/0.1 A
   tiene valle negativo. Isat debe evaluarse frente al límite de corriente, no solo
   frente a Iload. No hay BOM física ni simulación FB nueva liberada.
4. **Control DO:** el BSP75N exige VIN ≥4.5 V para su protección térmica especificada;
   el SN74LVC2T45 no tiene OE. No se ha demostrado VOH con corriente real y peor
   caso de rails/temperatura; no extrapolar una curva típica como garantía ni añadir
   una resistencia serie que reduzca ese nivel. Las cargas y fabricación están consultadas,
   aún sin respuesta registrada. No se elimina ninguna DO.
5. **CAD principal:** faltan símbolos/footprints homologados de MCU, PHY,
   transceivers, receptor DI, BSP, traductor, bucks y eFuse. Copiar SO8/SOT223/QFN
   por nombre no resuelve el cotejo pin/pad; consultar `cad_queue.csv`.

## Plazo y siguiente acción

La nueva disponibilidad suma **34–36 h**, suponiendo que las dos jornadas de
12 h sean efectivas. Estimación pendiente, una persona y cuatro capas como
hipótesis: diseño/selección 6–8 h, símbolos 1.5–2.5 h, footprints 3–4 h,
esquemático 4–6 h, ERC/revisión 1.5–2 h, placement 2–3 h, routing 6–8 h,
DRC/visual 2–3 h y documentación/fabricación 1–1.5 h. Subtotal 27–38 h;
con 25 % de correcciones: **34–48 h** redondeadas.

34–36 h cubre solo el extremo favorable, sin holgura para rediseños o problemas
de importación. No es un compromiso de entrega. La auditoría previa de B no
incluía conservar CAN y dos DI; no se reutiliza su estimación sin ajuste.

Próxima acción concreta: resolver el front-end y seleccionar los pasivos físicos
de los dos LMR36015FB; en paralelo, adquirir/cotejar el símbolo H723 contra los
100 pines ya preparados. Con acceso UI operativo y bloqueos principales cerrados,
crear entonces el proyecto PCB **dentro de esta carpeta**, capturando MCU,
alimentación, Ethernet, RS-485, CAN, DO y DI en ese orden. No existe un proyecto
vacío presentado como progreso de esquemático.

Verificación reproducible:

```powershell
& C:/dev/tools/gateway-zephyr-venv/Scripts/python.exe hardware/academic_rev1/prepare_data.py
```

Fuentes: DS13313 Rev.5/AN5419 para MCU; SNVSB49D para bucks;
[TI DP83826EVM](https://www.ti.com/tool/DP83826EVM/),
[Microchip DS50002649A](https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/UserGuides/50002649A.pdf),
[ISO1212 SLLSEY7G](https://www.ti.com/lit/ds/symlink/iso1212.pdf),
Diodes DS33016 p.1/4 y TI SCES516N tabla5.5 para DO. Los datasheets locales
originales permanecen en `C:/dev/7mo/design/Datasheets_industrial_gateway/`.
