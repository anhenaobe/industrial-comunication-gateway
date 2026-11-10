# Auditoría de la librería del profesor

Fecha: 2026-11-05. Estado: inventario documental; revisión humana pendiente.

## Resultado y alcance

Se encontró e inspeccionó `C:/dev/7mo/design/industrial-linux-gateway/shared_lib (1).IntLib`.
Es la librería suministrada en la raíz del proyecto y la base de esta auditoría;
su procedencia docente debe ratificarse. **No permite completar por sí sola el gateway:**
faltan Ethernet y RS-485, además de etapas industriales de E/S y alimentación de 24 V verificadas.

| Recuento de esta IntLib | Resultado |
|---|---:|
| Entradas de símbolo | 71 |
| Componentes seleccionables, excluyendo `template` | 70 |
| Footprints distintos con stream `Data` propio | 37 |
| Componentes con enlace a footprint encontrado | 70/70 |
| Entradas con cuerpo 3D detectado, incluidas extrusiones CAD | 68/71 |
| Streams de modelos 3D embebidos numerados | 21 |
| MCU o módulos MCU | 2 |
| PHY / controladores Ethernet / RJ45 o magnetics | 0 |
| Transceivers RS-485 / CAN / CAN-FD | 0 |
| Receptores DI industriales / optoacopladores / aisladores / traductores lógicos dedicados | 0 |

Los recuentos son de recursos CAD, no de unidades físicas ni de MPN comprables.
Los seis headers genéricos no consignan MPN. La plantilla tampoco lo consigna.
Hay footprints compartidos entre distintos componentes; no son 70 encapsulados diferentes.

## Evidencia y método reproducible

- Archivo original: [shared_lib (1).IntLib](../../shared_lib%20%281%29.IntLib), 1 772 032 bytes.
- SHA-256: `91594EDE8AADF6449FFF5B44B7443DEAFEB73CFAF0BC1EB1FF434D8AC1FB6159`.
- [CSV completo](library_inventory.csv): 71 filas, una por entrada, incluida la plantilla identificada.
- [Metadatos extraídos](evidence/shared_lib_metadata.json): parámetros originales,
  asociaciones de modelos, streams y hashes de las bibliotecas embebidas.
- [Extractor de auditoría](evidence/extract_library_inventory.py): Python y `olefile==0.47`.
  Ejecutar desde la raíz con un entorno que contenga esa dependencia. En esta sesión se
  utilizó `C:/dev/tools/gateway-zephyr-venv/Scripts/python.exe` con dependencia aislada
  en `C:/dev/tmp/gateway-audit-python`; no se instaló nada en el firmware.

Se abrió el contenedor OLE, se descomprimieron en memoria los streams zlib
`SchLib/0.schlib` y `PCBLib/0.pcblib`, y se leyeron sus directorios OLE internos.
Los registros de símbolo `RECORD=1`, parámetros `RECORD=41` y modelos `RECORD=45`
permiten recuperar referencia, MPN, fabricante y asociación PCB. Se cotejó el nombre
del modelo con el nombre original contenido en el stream del footprint; el nombre
del storage puede reemplazar `*` por `_`, por ejemplo en inductores.

**Símbolo «sí»** significa stream de datos del símbolo encontrado.
**Footprint «sí»** significa asociación explícita y stream PCB correspondiente encontrado.
**3D «sí»** significa cuerpo CAD detectado en ese footprint, que puede ser una
extrusión o un modelo STEP enlazado; el CSV conserva el detalle. **3D «no»** significa
sin cuerpo detectado por este método. No se garantiza exactitud mecánica, orientación,
pinout ni que un STEP genérico corresponda al MPN. El JSON conserva los campos de los cuerpos.
No se utilizó una búsqueda de cadenas sueltas como prueba de asociación.

Los campos fabricante, MPN y función son transcripciones de la librería, no
homologaciones del componente. Un enlace LCSC en el CSV es referencia técnica de
origen, **no evidencia actual de precio o stock**. No se corrigieron silenciosamente
las contradicciones del CAD.

## Clasificación del inventario

| Categoría | Cantidad | Contenido relevante |
|---|---:|---|
| Procesamiento | 3 | STM32F030C8T6TR; ESP32-C3-WROOM-02-N4; Flash ZD25WQ16BTIGR |
| Comunicaciones | 1 | CP2102N-A02-GQFN20R, puente USB-UART; no convierte a RS-485 |
| E/S | 3 | DN2302S; AP2301; SRD-05VDC-SL-C |
| Alimentación | 28 | 3 DC/DC, 1 LDO, 1 cargador, 4 TVS, 2 Schottky, 5 inductores, 1 ferrita, 11 capacitores |
| Soporte | 35 | 6 conectores, 6 headers, 19 resistencias, 3 LEDs, 1 pulsador |
| Plantilla | 1 | `template`, fuera de selección |

### Procesamiento y comunicaciones

| MPN exacto según CAD | Fabricante según CAD | Footprint asociado | Evaluación |
|---|---|---|---|
| STM32F030C8T6TR | STMicroelectronics | LQFP48_7x7mm | MCU Cortex-M0, candidato inspeccionado pero no recomendado para migrar directamente la PoC con red |
| ESP32-C3-WROOM-02-N4 | Espressif Systems | ESP32-C3-WROOM-02-N4 | Mejor candidato de la librería para estudiar Ethernet SPI; Ethernet y RS-485 externos faltan |
| ZD25WQ16BTIGR | Zetta | SOIC_8_3.9mm | Flash SPI, diferible |
| CP2102N-A02-GQFN20R | Silicon Labs | WFQFN_20_EP_3X3MM | Consola/carga serial opcional; no es programador SWD/JTAG |

No hay microprocesador Linux identificado. Ninguno de los dos MCU encontrados
ofrece Ethernet MAC integrada. Wi-Fi del ESP32-C3 no satisface el requisito Ethernet.
El STM32F429ZIT6 de la PoC y STM32H723VET6 de Rev. A **no aparecen en esta IntLib**.

### E/S y alimentación

| Recurso encontrado | Uso preliminar / restricción |
|---|---|
| DN2302S, Doeshare, SOT_23_3 | Nombre CAD indica MOSFET N de 20 V: descartar como switch directo de carga de 24 V |
| AP2301, ALLPOWER, SOT_23_3 | Nombre CAD indica PFET de 30 V: no garantiza margen para 18–30 V y transitorios |
| SRD-05VDC-SL-C, Ningbo Songle Relay | Relé de bobina 5 V; no aceptar «15 A» del nombre CAD como corriente admisible de cualquier carga DC |
| TPS564201DDCR, TI, SOT_23_6 | Buck, entrada recomendada 4.5–17 V; no admite entrada nominal 24 V |
| TPS56528DDAR, TI, SOIC_8_3.9mm_EP | Buck, entrada recomendada 4.5–18 V; no admite 24 V |
| MT3608B, XI'AN Aerosemi Tech, SOT_23_6 | Nombre BOOST pero descripción «BUCK»: resolver con datasheet exacto antes de usar |
| AMS1117-3.3, UMW, SOT_223 | Posible regulación desde 5 V; falta verificar corriente, estabilidad y disipación del fabricante exacto |
| TP4056, YONGYUTAI | Cargador de batería; no es regulador industrial de 24 V |
| SMF12CA; LESD5Z3.3T1G; USBLC6-2SC6; SMF5.0CA | TVS de baja tensión; no sustituyen la protección de entrada industrial |
| PSBD1DF40V1H; SS34-TD | Schottky; comprobar tensión inversa, corriente, térmica y encapsulado exactos |

Hay resistencias 0603, incluida 120 Ω, pero su presencia no valida una terminación
RS-485: potencia, tolerancia y topología deben dimensionarse. Hay capacitores de
6.3/10/16/25/35/50 V; no todos sirven para el rail de campo. El 100 nF disponible
es Y5V −20/+80 % según CAD; verificar capacidad efectiva y temperatura, no asumir
equivalencia con un desacoplo X7R. Inductores y ferrita requieren curva de saturación,
DCR y compatibilidad con el regulador escogido.

### Soporte y recursos ausentes

Conectores de bornera de 2/3 posiciones, JST, jack, mini-USB y USB-C; headers
de 2 a 7 pines a 100 mil; LEDs verde/rojo/RGB y pulsador. Un header de 5/6 pines
podría servir para depuración con pinout propio aprobado; **no se encontró un
conector SWD estándar dedicado**. No se encontraron cristales u osciladores
discretos; el módulo Espressif integra recursos de reloj, que deben contrastarse
con su datasheet. El Ethernet externo necesitará su propia solución de reloj.

No aparecen THVD1420, ATA6561, DP83826I, ISO1212, BSP75N, SN74LVC2T45,
LTC4414, DMP6023LSS-13, TDS3011P, NIS3071MT4TWG ni LMR36015 de Rev. A.
«Ausente» aquí se limita a la IntLib auditada, no a todo el laboratorio o mercado.

## Localización y trabajos anteriores

La rama inicial es `main`, con seguimiento `origin/main`. `git status --short --branch`
mostró modificaciones previas en `.gitignore`, CMake, README y `prj.conf` de
`firmware/poc`, además de `.vscode/`, `platformio.ini`, `zephyr/`, la IntLib y
`converter_pcb_layout_appli-e (1).pdf` sin seguimiento. Se conservaron.
No se encontraron instrucciones AGENTS.md aplicables en la ruta del proyecto.

El documento solicitado como `docs/industrial_linux_gateway_requirements.md`
no existe: el maestro real es [industrial_gateway_requirements.md](../industrial_gateway_requirements.md).
Se revisaron ese maestro, [proof_of_concept.md](../proof_of_concept.md),
el README y fuentes de la PoC, y las BOM de `docs/sources/webench/`.
No hay SchDoc/PcbDoc/PrjPcb de gateway versionados ni encontrados en esta raíz.
Las BOM WEBENCH son parciales: diseño histórico LMR66420 y LMR36015AR de 5 V;
no constituyen la BOM completa ni validan la propuesta LMR36015FB vigente.

La búsqueda por extensiones CAD en `C:/dev` y la inspección de directorios vecinos
encontró también:

- `C:/dev/7mo/design/PCB_Project/`: `Sheet1.SchDoc`, proyecto y `lib/Schlib2.SchLib`,
  `PcbLib2.PcbLib`, `Integrated_Library1.LibPkg` y su IntLib; modelos STEP y CP2102N de 24 pines.
- `C:/dev/7mo/design/electronic-design-dc-dc/`: SchDoc/PcbDoc de buck-boost,
  `entregable/Schlib1.SchLib`, `PcbLib1.PcbLib`, bibliotecas integradas y recursos descargados
  de pasivos, TPS61175PWP y LMZ10505TZX-ADJNOPB, entre otros.
- `C:/dev/7mo/design/Datasheets_industrial_gateway/`: referencias técnicas del baseline,
  no evidencia de recursos CAD o existencias.

Estos son trabajos vecinos, **no se atribuyen al profesor ni se suman al inventario**:
no se ha demostrado que formen parte de la librería autorizada o de este gateway.
Si se pretende usarlos, confirmar directorio fuente autorizado y auditar cada
símbolo/footprint. No se identificó DbLib suministrada ni una librería KiCad del gateway.
La búsqueda global tuvo accesos denegados en algunos directorios ajenos; no se
afirma exhaustividad de todo el disco ni de perfiles no inspeccionados.
Las rutas `D:/Alitum_libraries/shared_lib/...` presentes dentro de la IntLib son
rutas históricas de compilación, no ubicaciones locales comprobadas.

## Limitaciones y extracción en Altium

La inspección binaria identifica inventario y enlaces de forma útil, pero no
interpreta todas las primitivas gráficas ni valida esquemático, pin types,
pad stacks, máscaras, numeración, orientación o courtyard. No se ejecutó ERC/DRC
ni se abrió o editó un diseño CAD. El PDF de layout adjunto no se utilizó como
regla de fabricación ni como prueba de disponibilidad de componentes.

Para cerrar la verificación antes de dibujar:

1. Abrir una copia de la IntLib en Altium y elegir la extracción de las librerías
   fuente cuando el programa lo ofrezca; conservar el original y su hash.
2. En SCH Library/PCB Library, cotejar las 71 entradas y 37 footprints con el JSON;
   exportar parámetros mediante el panel de parámetros/listado disponible en esa versión.
3. Abrir cada candidato y su modelo enlazado; contrastar todos los pines/pads con el
   datasheet exacto, incluidas partes múltiples, tierras y pads expuestos.
4. Revisar dimensiones, pitch, taladros, máscara/pasta y vistas 2D/3D. Un STEP
   «step_temp» o un cuerpo extruido no valida dimensiones. Registrar correcciones
   propuestas aparte, sin crear footprints genéricos por semejanza.
5. Resolver inconsistencias: MT3608B BOOST/BUCK; inductor CYA0630-10UH con descripción
   2.2 µH y tamaño distinto; TVS SMF12CA con referencia SOD_123 pero enlace SOD_123FL;
   jack 2.1 mm frente al MPN `HC-DC-005-2.0T`.

## Disponibilidad física y comercial

**Presente en librería**: probado por los recursos anteriores.
**Disponible físicamente**: no verificado para ninguna fila; se necesita inventario
del laboratorio con MPN, cantidades y evidencia del docente.
**Disponible comercialmente**: no verificado como compra ejecutable en el CSV.
Se consultaron referencias web, pero no se obtuvo cotización comparable completa
de ambos MCU frente al H723, con stock, cantidad, moneda, envío y plazo a Colombia.
El enlace de proveedor guardado en CAD no acredita existencias actuales.

Fuentes técnicas consultadas el 2026-11-05:

- [STM32F030, ST DS9773](https://www.st.com/resource/en/datasheet/stm32f030c8.pdf).
- [ESP32-C3-WROOM-02, Espressif](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html).
- [TPS564201, TI](https://www.ti.com/product/TPS564201).
- [TPS56528, TI](https://www.ti.com/lit/ds/symlink/tps56528.pdf).

La evaluación de arquitectura y fuentes Zephyr están en
[simplified_gateway_feasibility.md](simplified_gateway_feasibility.md).
