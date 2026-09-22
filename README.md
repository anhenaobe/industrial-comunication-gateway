# Industrial Communication Gateway

Gateway embebido para adquirir, normalizar, diagnosticar y comunicar datos entre interfaces industriales y una red IP. El diseño de Rev. A se centra en el conjunto objetivo de interfaces definido por los requisitos; no se presenta como un producto comercial terminado.

## Status

**Design / requirements phase**

- Plataforma Rev. A decidida: **STM32H723VET6 + Zephyr RTOS**.
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

- 2 × RS-485;
- 1 × CAN-FD;
- 4 × entradas digitales industriales de 24 V;
- 2 × salidas digitales industriales;
- Ethernet principal;
- almacenamiento persistente, tecnología y capacidad TBD;
- diagnóstico, configuración y mantenimiento desde PC;
- segundo Ethernet sujeto a justificación: TBD.

No están seleccionados todavía el PHY, los transceptores, los front-ends, el almacenamiento, los conectores ni la topología detallada de alimentación.

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

Cerrar el demostrador y los TBD que condicionan el diseño; congelar periféricos/pinout y alimentación; seleccionar los componentes de interfaz y almacenamiento; desarrollar esquemático y firmware mínimo; diseñar, fabricar y probar la PCB Rev. A.

El nombre remoto `industrial-linux-gateway` es histórico. Un posible cambio a un nombre neutral queda **TBD** y no se ha realizado.
