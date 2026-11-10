# Viabilidad de un gateway simplificado

Fecha: 2026-11-05. **PROPUESTA PENDIENTE DE APROBACIÓN; no modifica Product Rev. A.**

## 1. Restricciones y dictamen

La librería suministrada es la prioridad obligatoria. La auditoría identifica
70 componentes seleccionables con símbolos y footprints enlazados, pero **ninguna
arquitectura completa cumple Ethernet + RS-485 + E/S industriales usando solo
esa IntLib**. La recomendación es estudiar el ESP32-C3-WROOM-02-N4 como base,
condicionada a completar recursos autorizados; no seleccionar aún un MCU ni comenzar
el esquemático. El plazo de dos jornadas no es defendible mientras sigan abiertos
Ethernet, RS-485, acondicionamiento DI, protección DO y alimentación.

El alcance reducido propuesto es un MCU, un RS-485, Ethernet cableado, hasta dos
DI de campo y dos DO, alimentación de una sola entrada y programación/depuración.
No mantiene automáticamente prestaciones, aislamiento ni especificaciones de Rev. A.
El costo debe compararse a nivel BOM completa y PCB: un MCU barato con Ethernet
externo puede no reducir el costo total. No hay un ranking económico verificado.

Se usó la ubicación `docs/hardware/` solicitada para separar esta propuesta del
maestro real `docs/industrial_gateway_requirements.md`, que permanece intacto.
Inventario, rutas y método están en [library_inventory.md](library_inventory.md)
y [library_inventory.csv](library_inventory.csv).

## 2. MCU realmente encontrados

| Criterio | STM32F030C8T6TR | ESP32-C3-WROOM-02-N4 |
|---|---|---|
| CAD | Símbolo, footprint LQFP48 7×7 mm y cuerpo 3D | Símbolo, footprint del módulo y cuerpo 3D |
| CPU / firmware | Cortex-M0, hasta 48 MHz; firmware embebido viable | RISC-V, hasta 160 MHz; firmware embebido viable |
| Memoria | 64 KiB Flash / 8 KiB SRAM | N4: 4 MB Flash; SoC 400 KB SRAM, 16 KB para caché; no toda disponible a aplicación |
| UART / GPIO | USART, SPI y GPIO suficientes en principio para alcance reducido; falta asignación pin a pin | Dos UART en SoC; módulo expone hasta 15 GPIO; presupuesto ajustado con SPI y depuración |
| Ethernet MAC | No | No; Wi-Fi no equivale a Ethernet |
| Depuración | SWD; reservar SWDIO, SWCLK, NRST, referencia y GND | JTAG o USB Serial/JTAG equivalente; acceso real en módulo y pinout por cerrar; UART de carga no sustituye debug |
| Fabricación académica | LQFP48 exige verificar pitch/pads y capacidad de montaje | Módulo castellado reduce circuitería interna; exige land pattern, pad de GND y keepout de antena correctos |
| Zephyr 4.3.0 | Existe soporte de familia F030 y DTS X8; board propio para encapsulado C8 pendiente | Existe soporte ESP32-C3 y board de referencia; board propio WROOM-02 pendiente |
| Reutilización PoC | Misma familia de herramientas Arm/STM32, pero memoria insuficiente para el build actual | APIs Zephyr transferibles en principio; cambia arquitectura, toolchain, board y drivers de hardware |
| Costo menor que H723 | No demostrado con cotización comparable | No demostrado con cotización comparable |
| Evaluación | No recomendado para migración directa con IP Zephyr | Mejor candidato **condicionado**, sin selección definitiva |

Las capacidades se contrastaron con [ST DS9773](https://www.st.com/resource/en/datasheet/stm32f030c8.pdf)
y [datasheet del módulo Espressif](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html).
Los 15 GPIO del módulo incluyen pines de strapping y funciones compartidas; no
se debe trasladar el número total de GPIO del chip al módulo.

El README actual de la PoC registra builds anteriores de 80 484 B Flash / 36 176 B
RAM con DHCP y 77 504 B / 34 816 B estático. Ambos superan 64/8 KiB del F030C8.
Es evidencia documental previa, no medición nueva ni cota mínima universal.
Reducir memoria o cambiar a sockets offload sería otro trabajo de firmware, sin
garantía de caber y fuera de esta auditoría. No se descarta que el F030 ejecute
otras aplicaciones Zephyr pequeñas; se descarta recomendarlo para esta migración directa.

### Presupuesto de pines del C3 por resolver

Una estimación conservadora consume 6 señales para Ethernet SPI (SCK, MOSI, MISO,
CS, IRQ, RESET), 3 para UART RS-485 (TX, RX, dirección), 2 DI y 2 DO: **13 GPIO**.
USB Serial/JTAG podría consumir otros 2: total 15, sin consola UART adicional ni
LED de usuario dedicado. NRST/EN y BOOT requieren circuito propio. La asignación
debe resolver strapping, estados de arranque y funciones compartidas; no es
prueba de que el pinout cierre. JTAG externo de cuatro señales aumenta la presión.
Fijar permanentemente recepción RS-485, como en la PoC unidireccional, reduciría
señales pero cambiaría el alcance; no se supone aprobado.

## 3. Ethernet y drivers de la versión real

`firmware/poc/platformio.ini` fija `ststm32@19.5.0` y
`platformio/framework-zephyr@3.40300.0`. El archivo local
`C:/Users/justa/.platformio/packages/framework-zephyr/VERSION` confirma **4.3.0**.
La inspección siguiente se hizo contra ese árbol instalado, no contra `latest`.

| Ruta arquitectónica | Recursos y soporte | Resultado |
|---|---|---|
| A: MCU MAC → RMII → PHY → magnetics/RJ45 | `drivers/ethernet/Kconfig.stm32_hal`, `eth_stm32_hal.c`; PoC usa MAC STM32 | Ningún MCU con MAC ni PHY/RJ45 encontrado en la IntLib; no hay candidata A elegible |
| B: MCU → SPI → controlador MAC+PHY → magnetics/RJ45 | `Kconfig.w5500`, `eth_w5500.c`, binding `dts/bindings/ethernet/wiznet,w5500.yaml` | Ruta posible para C3, pero W5500 **no encontrado** y no seleccionado |
| Otra B con ENC28J60 | `Kconfig.enc28j60`, `eth_enc28j60.c` | Driver existe; componente **no encontrado**, no es alternativa CAD disponible |

W5500 y ENC28J60 se citan únicamente como ejemplos de extracción de requisitos
de firmware para una futura búsqueda autorizada. No se añadieron al inventario
ni se presentan como componentes disponibles. El W5500 usa modo **MACRAW** en
`eth_w5500.c` (líneas 438–441 del árbol inspeccionado): el driver Zephyr no implica
usar automáticamente sus sockets TCP/IP hardware para liberar RAM del F030.
La presencia del driver no demuestra integración, rendimiento ni prueba física.

MAC/RMII permite transferencia DMA y mayor caudal potencial, pero obliga a cerrar
reloj, straps, RMII y PHY. Ethernet SPI consume ancho de banda de SPI, CPU,
interrupciones y buffers; velocidad del enlace no es throughput de aplicación.
ENC28J60 es Ethernet 10 Mb/s; W5500 tiene enlace 10/100, sin prometer ese caudal
a través del firmware. Debe fijarse la tasa de datos industrial y latencia admisible.
Referencias de código oficiales fijadas a versión:
[STM32 HAL](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/ethernet/Kconfig.stm32_hal),
[W5500](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/ethernet/eth_w5500.c),
[ENC28J60](https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/drivers/ethernet/Kconfig.enc28j60).

### Migración desde NUCLEO-F429ZI

`src/main.c`, `network.c` y `diagnostics.c` emplean APIs Zephyr de kernel,
GPIO, red, DHCP y sockets. Son reutilizables conceptualmente; no hay port realizado.
`diagnostics.c` depende del alias `led0`; el board propio debe definirlo o aceptar
su ausencia. `network.c` necesita una interfaz Ethernet, no cambiarla silenciosamente
por Wi-Fi. Se deben redefinir DTS, Kconfig, reloj, consola, pinctrl y acceso de debug.
El entorno PlatformIO `ststm32` no compila el C3: se necesitarían herramientas y
módulos Espressif compatibles con Zephyr 4.3.0, cuya instalación/build no se ejecutó.

Referencia instalada: `boards/espressif/esp32c3_devkitm/` y su documentación.
Ese board usa módulo **MINI-1**, no es un footprint ni un pinout sustituto de
WROOM-02. Para F030 existe `dts/arm/st/f0/stm32f030X8.dtsi` con 64/8 KiB y
`boards/st/nucleo_f030r8`; R8 no equivale al encapsulado C8. El board
`others/stm32f030_demo` usa variante X4, tampoco es el candidato exacto.

La PoC actual implementa diagnóstico y heartbeat UDP; UART de datos, parser,
CRC y router siguen pendientes según el README revisado. No hay módulos RS-485
completos cuya migración pueda declararse validada. La compilación previa de la
NUCLEO tampoco prueba funcionamiento físico ni interoperabilidad con el C3.

## 4. Bloques originales y reutilización

| Bloque Rev. A | Situación frente a la librería / propuesta |
|---|---|
| STM32H723VET6 LQFP100 | No encontrado; permanece MCU oficial de Rev. A |
| MAC/RMII + DP83826I | PHY no encontrado; ruta SPI requeriría otros componentes |
| 2 × THVD1420 RS-485 | No encontrados; reducir a un canal requiere aprobación y recursos CAD |
| ATA6561 CAN-FD | No encontrado; proponer diferir CAN-FD completo |
| 2 × ISO1212 para 4 DI | No encontrados; 0–2 DI según alcance aprobado y acondicionamiento disponible |
| 2 × BSP75N + SN74LVC2T45 | No encontrados; no sustituir por DN2302S de 20 V sobre cargas de 24 V |
| Dos entradas 18–30 V, TDS3011P, LTC4414, DMP6023LSS-13, NIS3071 | No encontrados; proponer una sola fuente, sin suprimir protección necesaria |
| Bucks LMR36015 de 3.3/5 V | No encontrados; bucks encontrados no admiten 24 V |
| Pasivos, borneras, headers, LEDs | Hay recursos reutilizables de la librería, con verificación individual pendiente |
| BOM WEBENCH, cálculos y datasheets | Reutilizables como antecedentes; no migrar automáticamente pasivos ni presupuestos de otra arquitectura |

No hay esquemático/PCB propio del gateway identificado en el repositorio. Los
SchDoc/PcbDoc vecinos de PCB_Project y buck-boost no se consideran trabajo ya
validado del gateway ni recursos docentes autorizados. El presupuesto de potencia
original deberá recalcularse si se aprueba la propuesta.

## 5. Cambios de alcance, E/S y seguridad eléctrica

Se propone diferir segundo RS-485, CAN-FD, redundancia de alimentación,
almacenamiento externo, expansión y diagnóstico avanzado. La Flash externa
ZD25WQ16BTIGR encontrada puede omitirse si el almacenamiento interno satisface
el alcance aprobado. Conservar diagnóstico mínimo de enlace, errores y estado de salida.

**DI de 24 V:** no conectar al MCU. Se requiere fijar umbrales ON/OFF,
corriente, polaridad, filtro, aislamiento requerido y sobretensiones; luego
dimensionar resistencias por potencia y tensión, limitar/clamp de entrada y
proteger el GPIO. No hay receptor industrial u optoacoplador en la IntLib. Un
divisor resistivo por sí solo no demuestra inmunidad, aislamiento ni IEC 61131-2.
Omitir DI reduce alcance explícitamente; una bornera sin acondicionamiento no
puede documentarse como DI de 24 V funcional.

**Dos DO:** dos GPIO lógicos solo sirven para control de una etapa externa
compatible, con estado seguro por hardware durante reset/boot y desconexión.
No equivalen a dos salidas low-side 24 V/500 mA de Rev. A. Conservar esas cargas
exige switch con tensión y SOA adecuadas, corriente/térmica verificadas,
protección de cortocircuito y sobretensión, retorno de corriente y supresión
de energía inductiva. El DN2302S de 20 V no es sustituto válido.

El relé SRD-05VDC-SL-C permitiría estudiar dos salidas de contacto con bobina a
5 V y driver DN2302S en el lado de bobina, solo tras verificar sus límites a
3.3 V de gate y la corriente de bobina. Se requieren diodos flyback y protección
del circuito de contactos, límites DC por carga e aislamiento/clearance. No se
afirma que sus contactos mantengan 500 mA inductivos o autoprotecciones de BSP75N.
Esta variante no se aprueba ni se usa para rellenar otra arquitectura candidata.

**Alimentación:** el camino más corto a estudiar es una fuente externa regulada
de baja tensión para electrónica, con protección de entrada y regulación a 3.3 V.
Si se usa 5 V, AMS1117-3.3 es solo candidato: P ≈ (5−3.3)×I; a 300 mA serían
0.51 W, ejemplo de disipación, no consumo medido. Cerrar capacidad, transitorios,
estabilidad y térmica o escoger otro regulador autorizado. Las cargas de campo
seguirían necesitando fuente de 24 V separada y retornos/aislamiento definidos.
Esto renuncia a la entrada industrial única 18–30 V y requiere aprobación.
Conservar esa entrada obliga a conseguir un buck y protección adecuados; no
conectar 24 V a TPS564201/TPS56528 o al LDO por similitud funcional.
Los rangos se verificaron en [TI TPS564201](https://www.ti.com/product/TPS564201)
y [TI TPS56528](https://www.ti.com/lit/ds/symlink/tps56528.pdf).

## 6. Arquitecturas candidatas

**Candidatas completas viables con recursos actuales: cero.** No se inventan
tres alternativas. Solo hay una dirección condicional que merece avanzar a
revisión de recursos; los criterios de mínimo costo, mínimo tiempo y equilibrio
no producen tres circuitos distintos con esta evidencia.

| Elemento | Dirección C: equilibrio, condicionada a completar librería |
|---|---|
| MCU propuesto para evaluación | ESP32-C3-WROOM-02-N4, encontrado |
| Ethernet | Controlador MAC+PHY SPI y magnetics/RJ45: faltantes; MPN por decidir y auditar |
| RS-485 | Un transceiver de lógica compatible, protección, bias y terminación: faltantes; MPN por decidir |
| DI | Hasta 2 × 24 V, solo con etapa protegida verificada; actualmente bloqueada |
| DO | Dos controles con estado seguro; etapa industrial externa/propia aún por cerrar; relés son cambio de especificación opcional |
| Alimentación | Una entrada de baja tensión para lógica a estudiar; campo 24 V separado si se conserva; regulación y protección sin cerrar |
| Soporte reutilizable | Pasivos verificados, headers, borneras, pulsador y LEDs si el presupuesto de pines permite |
| Faltantes principales | Ethernet completo, RS-485, DI, DO industriales, alimentación/protección adecuadas y documentación CAD verificada |
| Riesgos | GPIO/boot/debug del módulo, migración RISC-V, red SPI sin ensayo, térmica, falta de referencias CAD completas |
| Renuncias | Segundo RS-485, CAN-FD, redundancia, 4 DI; probablemente entrada 18–30 V y DO autoprotegidas originales si se aprueba otra interfaz |
| Dificultad | Media-alta en esquemático y layout hasta cerrar interfaces; una solución modular externa reduce routing Ethernet pero cambia el alcance de la PCB |

«Mínimo costo» queda sin ganador: falta BOM cotizada. «Mínimo tiempo» requiere
recursos completos y referencias verificadas; hoy tampoco tiene ganador. Mantener
NUCLEO-F429ZI para pruebas de firmware es útil, pero una carrier con placa de
desarrollo no se considera automáticamente una PCB propia de MCU principal
equivalente al producto ni una alternativa basada enteramente en la librería.

## 7. Costo y complejidad

No se inventaron precios. Consulta web del 2026-11-05:
[ficha DigiKey del H723](https://www.digikey.com/en/products/detail/stmicroelectronics/STM32H723VET6/13171220),
[ficha Mouser del C3](https://www.mouser.com/en/ProductDetail/Espressif-Systems/ESP32-C3-WROOM-02-N4?qs=stqOd1AaK7%2FqjTZKEOgfUg%3D%3D)
y [ficha Mouser del H723](https://www.mouser.com/en/ProductDetail/STMicroelectronics/STM32H723VET6?qs=sPbYRqrBIVnD9Udgf5csJA%3D%3D).
Mouser rechazó la lectura directa con HTTP 403 y los resultados indexados
no bastan para cotización vigente comparable. No se utiliza stock de buscador
como disponibilidad garantizada. Falta precio comparable del F030 también.

Para aprobar costo menor, cotizar mismo día/proveedor/cantidad (por ejemplo 1 y
5 placas), moneda, stock y fecha, impuestos y envío a Colombia; incluir controlador
Ethernet, magnetics, reloj, regulación, protecciones, PCB de capas elegidas y montaje.
Registrar inventario físico separado con cantidades y MPN. El C3 integra Flash y
reloj del módulo, lo que reduce componentes de soporte, pero añade dependencia
de Ethernet SPI; el F030 conserva SWD y herramientas STM32, con alto riesgo de
reescritura por memoria. Ninguna de esas observaciones demuestra ahorro monetario.

## 8. Plazo de sábado y domingo

Estimación de planificación, no compromiso: **18–26 horas activas** para un
diseño reducido por una persona con experiencia, suponiendo alcance y recursos
cerrados antes del sábado. Una disponibilidad de 8–10 h diarias deja poco o
ningún margen. A continuación las horas son secuenciales, sin asumir equipo paralelo.

| Trabajo | Horas estimadas | Criterio de salida |
|---|---:|---|
| Cerrar pinout, potencia y revisión CAD final | 2–3 | MPN, pines y footprints aprobados |
| Esquemático reducido y revisión ERC | 4–6 | Sin pines funcionales/rails sin definir; excepciones justificadas |
| Reglas/stackup, borde y colocación | 3–4 | Conectores, dominios y desacoplos ubicados |
| Routing, retornos y planos | 6–9 | Todas las conexiones; integridad de retornos y potencia |
| DRC, fabricación, BOM y documentación | 3–4 | Revisión de salidas completa y trazable |

Sábado: pinout cerrado, esquemático/ ERC y colocación. Domingo: routing/planos,
DRC y exportaciones. Si al final del sábado no están cerrados ERC, modelos y
colocación, no es razonable prometer fabricación exportada al final del domingo.
No se contabilizan compra, fabricación, ensamble, bring-up ni ensayos físicos.

### Bloqueantes antes de comenzar

| Bloqueante | Evidencia necesaria para levantarlo |
|---|---|
| Librería insuficiente para Ethernet/RS-485 | Recursos adicionales del profesor o autorización de incorporación con auditoría de símbolo y footprint |
| DI/DO y fuente sin especificación cerrada | Tensión, corriente, cargas, aislamiento, protecciones y estado seguro aprobados |
| Pinout C3 sin cerrar | Tabla pin a pin sin conflictos SPI/UART/GPIO/strapping/debug |
| CAD sin homologación | Contraste pin/pad y dimensiones con datasheets; resolver inconsistencias del inventario |
| Proceso de fabricación desconocido | Fabricante, stackup, materiales, capas, pista/espacio/vías, impedancia y acabado confirmados |
| No existe BOM cotizada ni inventario físico | Proveedor/plazo y/o lista docente; no suponer unidades por tener CAD |

### Restricciones de layout y cuestiones resolubles durante el trabajo

- **Capas:** proponer cuatro capas para Ethernet discreto y retorno continuo;
  dos capas solo tras demostrar espacio, retornos e impedancia realizables.
  No se conoce el fabricante ni se fijó stackup. Más capas puede aumentar costo.
- **Reglas:** anchura/separación mínima, taladro/pad/anillo de vía, distancia
  cobre-borde y capacidades de máscara/pasta deben venir del fabricante. No fijar
  «6/6 mil» o una vía genérica como regla aprobada sin esa evidencia.
- **Ethernet:** pares MDI de impedancia diferencial conforme al PHY/controlador
  y stackup (habitualmente 100 Ω); magnetics, terminación, protección ESD,
  aislamiento y retorno de chasis según referencia exacta. En RMII además reloj
  y temporización; en SPI velocidades y retornos adecuados. Evitar cortes de
  plano bajo señales; no inventar matching universal sin datasheet.
- **Potencia:** loops del buck cortos, nodo SW contenido, desacoplos junto a
  pines, vías GND próximas, distribución por corriente y subida térmica, no por
  el mínimo de pista del fabricante. Recalcular presupuesto incluyendo picos
  del C3, Ethernet, transceiver y bobinas si las hubiera.
- **E/S:** TVS junto a entrada del conector con retorno corto, segregación
  de campo/lógica y aislamiento cuando corresponda; flyback/clamp y rutas de
  carga alejados de MCU/Ethernet. Ningún GPIO flotante que active una DO al boot.
- **Footprints:** pin 1, numeración, expuestos, taladros, orientación de conectores
  y variante exacta antes de routing. «Presente» no equivale a «verificado».
- **Módulo C3:** keepout/colocación de antena conforme al fabricante, incluso
  si Wi-Fi no se utiliza; no reutilizar land pattern de DevKitM/MINI-1.
- **Durante layout:** ubicación fina, distribución de desacoplos, número de
  vías de retorno y fan-out se pueden iterar con reglas aprobadas. Stackup,
  interfaces industriales y pines del MCU no deben improvisarse al rutear.

La terminación exige esquemático completo del alcance aprobado, ERC revisado,
footprints verificados, colocación y routing completos, planos de alimentación
y tierra, DRC revisado (incluidas conexiones sin rutear y excepciones), revisión
visual de Gerber/Excellon, stackup/notas de fabricación, BOM con MPN/cantidades,
planos mínimos de ensamble y fuente CAD identificada. **Exportar archivos no
demuestra que una placa esté fabricada, ensamblada ni validada.**

## 9. Recomendación como propuesta

Presentar el **ESP32-C3-WROOM-02-N4 + Ethernet SPI** como dirección preferente
para completar la evaluación, porque es el MCU encontrado con memoria más
razonable para Zephyr/IP y tiene recursos CAD asociados. No aprobarlo todavía:
primero cerrar pines, obtener recursos Ethernet/RS-485 autorizados y definir
E/S protegidas y alimentación. Con la librería estrictamente actual, el dictamen
es **no iniciar esquemático/PCB**. El F030C8 no es una salida rápida para reutilizar
el firmware de red existente.

## 10. Decisiones pendientes de aprobación humana

1. Confirmar que `shared_lib (1).IntLib` es la librería docente autorizada y
   proporcionar recursos adicionales para los bloques faltantes o aprobar su incorporación.
2. Aprobar el alcance reducido y las renuncias explícitas frente a Rev. A;
   definir si las DO siguen siendo industriales o son controles hacia etapa externa.
3. Resolver MCU/Ethernet después del presupuesto de pines y cotización completa,
   sin sustituir automáticamente STM32H723VET6 en el maestro.
4. Aprobar fuente, niveles/corrientes DI/DO, cargas, aislamiento/protecciones
   y estado seguro; confirmar reglas de fabricante y cantidad de capas.
5. Acordar si las dos jornadas empiezan después de estos cierres, y qué revisión
   técnica acepta ERC/DRC y paquete de fabricación.

**Punto de parada:** esta auditoría termina en revisión humana. No se implementó
firmware, no se dibujó esquemático ni PCB, y no se hizo commit o push.
