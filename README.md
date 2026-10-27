# Industrial Communication Gateway

Gateway embebido para adquirir, normalizar y comunicar datos entre interfaces
industriales y una red IP, basado en **STM32H723VET6 + Zephyr RTOS**.

## Arquitectura actual

- **Ethernet:** 1 × DP83826I, 10/100, conectado al MAC mediante RMII.
- **RS-485:** 2 × THVD1420, buses independientes half-duplex.
- **CAN-FD:** 1 × ATA6561, VCC = 5 V y VIO = 3.3 V.
- **Digital inputs:** 2 × ISO1212, cuatro DI aisladas de 24 V.
- **Digital outputs:** 2 × BSP75N low-side, hasta 500 mA por canal.
- **Control de DO:** SN74LVC2T45, traducción activa 3.3 V → 5 V, A → B.

## Alimentación

Dos entradas físicas, adaptador externo y gabinete industrial, admiten
**18–30 VDC**, con **24 V nominales**, y pueden conectarse simultáneamente.
Cada entrada utiliza **TDS3011P** junto al conector y una rama
**LTC4414 + DMP6023LSS-13** para ideal-diode OR-ing sin prioridad explícita.

Las ramas convergen en **24V_OR**. Un canal de **NIS3071MT4TWG Auto-Retry**
genera **24V_SYS**, que alimenta campo de 24 V y los bucks **LMR36015 → 3.3 V**
y **LMR36015 → 5 V**. R_LIM = **43.2 kΩ** proporciona **ITH ≈1.4 A**, estimado
de la curva MT3/MT4 del datasheet.

El TDS3011P especifica VC = **40 V máximo** bajo su ensayo de surge. Ese valor
coincide con el absoluto del LTC4414: el diseño acepta ese trade-off y requiere
un lazo conector–TDS–GND corto; no afirma margen garantizado por debajo de 40 V.

Los cálculos de consumo, pérdidas y capacidades de los reguladores se detallan
en el documento técnico. Las capacidades de diseño de **0.7 A en 3.3 V** y
**0.1 A en 5 V** se distinguen del consumo estimado de las cargas.

## Documentación

- [Diseño técnico actual y Power Budget](docs/industrial_gateway_requirements.md)
- [Arquitectura editable](docs/figures/industrial_gateway_architecture.drawio)
- [Diagrama de contexto](docs/figures/industrial_gateway_context.drawio)
- [Organigrama de firmware](docs/figures/industrial_gateway_firmware_organigram.drawio)
- [Fuentes locales WEBENCH](docs/sources/webench/)
- [Proof of Concept](docs/proof_of_concept.md)
- [Arquitectura de firmware PoC](docs/firmware_architecture_poc.md)
- [Documento preparatorio de firmware para Diseño Electrónico](docs/firmware_session_brief.md)
- [Presentación NABC](docs/presentation_nabc.md)
- [Competidores y fuentes oficiales](docs/competitor_references.md)

La colección local de datasheets se encuentra en
`C:/dev/7mo/design/Datasheets_industrial_gateway`. Las alternativas fuera del
baseline se conservan en su subcarpeta `revision_posterior`.

## Project Status

The project is currently in the electronic-design phase. Documented component
selections represent the current design baseline and do not imply physical
hardware validation.
