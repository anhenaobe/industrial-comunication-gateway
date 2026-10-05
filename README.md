# Industrial Communication Gateway

Gateway embebido para adquirir, normalizar, diagnosticar y comunicar datos entre interfaces industriales y una red IP. El diseño de Rev. A se centra en el conjunto objetivo de interfaces definido por los requisitos; no se presenta como un producto comercial terminado.

## Status

**Design / requirements phase**

- Plataforma Rev. A: **STM32H723VET6 + Zephyr RTOS**, arquitectura sin cambios.
- Componentes: **SELECTED / PROVISIONAL DESIGN BASELINE**; selección suficiente para iniciar la extracción de consumos y el power budget, todavía pendientes.
- Suficiencia total de pines para las interfaces previstas: **validada externamente**.
- Asignación concreta de pines/periféricos: **TBD**.
- No PCB fabricated.
- No firmware validated.
- No complete prototype yet.

La selección de plataforma está decidida, pero todavía no equivale a implementación ni validación funcional.

## Arquitectura Rev. A

```text
FIELD DEVICES
    ↓
INDUSTRIAL INTERFACE / CARRIER
    ↓
STM32H723VET6 + ZEPHYR RTOS
    ↓
NETWORK INTERFACE
    ↓
SERVER / SCADA
```

Interfaces y funciones objetivo:

- PROCESSING: **STM32H723VET6**;
- NETWORK: **1 × DP83826I**, PHY Ethernet externo 10/100, RMII previsto;
- INDUSTRIAL COMMUNICATION: **2 × THVD1420**, RS-485 independientes half-duplex;
- **1 × ATA6561**, transceiver CAN-FD (VCC 5 V / VIO 3.3 V);
- INDUSTRIAL I/O: **2 × ISO1212 → 4 DI aisladas de 24 V**;
- **2 × BSP75N → 2 DO LOW-SIDE**, 24 V / 500 mA nominales por canal;
- almacenamiento persistente, tecnología y capacidad TBD;
- diagnóstico, configuración y mantenimiento desde PC;
- segundo Ethernet sujeto a justificación: TBD.

Esta selección es provisional: no representa hardware fabricado, circuito probado ni validación física. El power budget, los reguladores/DC/DC, la adaptación STM32 3.3 V → control BSP75N ≈5 V, los pasivos/protecciones específicos, el almacenamiento, los conectores, el esquemático y PCB finales siguen pendientes. Las protecciones del BSP75N requieren aproximadamente VIN ≥ 4.5 V; no asumir control directo desde GPIO de 3.3 V.

Se identifican rails mínimos de 3.3 V, 5 V y campo de 24 V. La tabla inicial de power budget y el detalle de componentes están en §3.4–3.6 del documento maestro.

## Documentación

- [Requisitos técnicos y Decision Register](docs/industrial_linux_gateway_requirements.md)
- [Proof of Concept: alcance y criterios de éxito](docs/proof_of_concept.md)
- [Fuente de presentación NABC](docs/presentation_nabc.md)
- [Competidores y fuentes oficiales](docs/competitor_references.md)
- [Diagrama de arquitectura editable](docs/figures/industrial_gateway_architecture.drawio)
- [Auditoría NABC del estado previo](docs/auditoria_nabc_2026-09-15.md)

El `.drawio` es la fuente normativa del diagrama. El SVG debe regenerarse desde esa fuente; el export anterior se retiró porque aún representaba la selección de plataforma como TBD y la exportación local no produjo un reemplazo verificable.

La arquitectura MYC-YM6231/Linux se conserva únicamente como historia de diseño en el Decision Register. La decisión vigente es D-18.

## Próximos pasos

El siguiente paso es extraer formalmente los consumos de los componentes seleccionados y construir el power budget. Después: seleccionar reguladores, definir adaptación de las DO y pasivos/protecciones; cerrar el demostrador, pinout y almacenamiento; desarrollar esquemático y firmware mínimo; diseñar, fabricar y probar la PCB Rev. A.

El nombre remoto `industrial-linux-gateway` es histórico. Un posible cambio a un nombre neutral queda **TBD** y no se ha realizado.
