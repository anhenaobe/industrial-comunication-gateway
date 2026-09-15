# Industrial Communication Gateway — fuente NABC

**Formato objetivo:** 10 diapositivas breves.

**Estado:** contenido fuente; no equivale a una presentación visual final.

**Baseline Rev. A:** STM32H723VET6 + Zephyr RTOS, decidido; no implementado ni validado.

## 1. Portada

**Industrial Communication Gateway**

Integración de interfaces industriales con redes IP

Rev. A — fase de diseño y requisitos

Pie sugerido: repositorio accesible y fecha de revisión.

## 2. N — Need

- En un mismo entorno pueden coexistir RS-485, CAN-FD y señales digitales industriales.
- Esas interfaces no se conectan directamente a Ethernet: requieren adaptación eléctrica, adquisición y manejo de protocolo/datos.
- El sistema superior necesita información normalizada, diagnóstico y continuidad ante interrupciones de conectividad.
- El mantenimiento debe poder realizarse desde un PC mediante un medio controlado.
- **Caso industrial demostrador concreto: TBD.** No se atribuyen cliente, planta, pérdidas ni métricas no documentadas.

Trazabilidad: §1.1; UC-01 a UC-05; F-01 a F-09 del [documento maestro](industrial_linux_gateway_requirements.md).

## 3. N — Need → requisitos

| Necesidad | Requisitos principales | Estado |
|---|---|---|
| Integrar interfaces heterogéneas | 2 × RS-485, 1 × CAN-FD, 4 DI de 24 V, 2 DO | Objetivo Rev. A; no implementado |
| Conectar con red superior | Ethernet principal | Decidido como función; implementación TBD |
| Conservar datos durante cortes de enlace | Persistencia y política de reintento | Objetivo; medio/capacidad/política TBD |
| Diagnosticar y mantener | Logs, estado, configuración, actualización y recuperación | Objetivo; mecanismos TBD |
| Interactuar con campo industrial | Protección/acondicionamiento; aislamiento si se justifica | Objetivo; niveles y componentes TBD |

Trazabilidad: D-11 a D-18; SR-COM, SR-IO, SR-DIA, SR-SAF y SR-MNT.

## 4. A — Approach: arquitectura

```text
FIELD DEVICES
  RS-485 | CAN-FD | DI/DO 24 V
          ↓
INDUSTRIAL INTERFACE / CARRIER
  protección + acondicionamiento + aislamiento TBD
          ↓
PROCESSING PLATFORM
  STM32H723VET6 + Zephyr RTOS
          ↓
NETWORK INTERFACE
  Ethernet principal | segundo Ethernet TBD
          ↓
SERVER / SCADA
```

Usar visualmente el [diagrama de bloques](figures/industrial_gateway_architecture.drawio). La asignación concreta de pines, PHY, transceptores, almacenamiento, conectores y alimentación detallada permanece TBD.

Trazabilidad: D-18; §3; SR-COM-01 a 10; SR-LNX-01 a 11.

## 5. A — Approach: funcionamiento previsto

1. Adquirir señales o tramas desde la interfaz de campo.
2. Validar integridad y metadatos disponibles.
3. Normalizar según el caso de uso y protocolo que se cierre.
4. Registrar o persistir cuando la política lo requiera; no todo paquete debe escribirse antes de transmitirse.
5. Transmitir por IP al servidor/SCADA.
6. Exponer diagnóstico, configuración y mantenimiento controlados.
7. Recibir comandos autorizados cuando el caso de uso lo permita; estados seguros y latencias siguen TBD.

Zephyr deberá proporcionar o integrar networking, drivers, concurrencia, logging, almacenamiento, diagnóstico y actualización. No existe firmware validado.

Trazabilidad: §3.7–3.9; UC-01 a UC-05; SR-LNX-03 a 11.

## 6. B — Benefits

### Beneficios esperados de diseño

- Integración de RS-485, CAN-FD y DI/DO dentro de una arquitectura común.
- Adaptación de equipos industriales/legacy hacia una red IP.
- Persistencia y reenvío ante pérdida de conectividad, conforme a una política todavía TBD.
- Diagnóstico y mantenimiento considerados desde los requisitos.
- Electrónica de campo, protección y testabilidad ajustables al caso demostrador.
- Plataforma embebida dedicada alineada con el alcance actual.

### Beneficios demostrados

**Ninguno todavía a nivel de producto completo.** No se afirma menor coste, consumo, tamaño, mayor robustez ni rendimiento superior.

Trazabilidad: F-01 a F-09; NF-08 a NF-10; D-18; §8.1.

## 7. C — Competition

Referencias exactas:

- Siemens SIMATIC IOT2050 M.2, `6ES7647-0BB00-1YA2`.
- Moxa UC-2112-LX.
- Advantech UNO-2271G V2.

Los equipos comerciales ofrecen producto terminado, soporte, documentación de instalación, expansión y especificaciones ambientales. Nuestro proyecto está en diseño/requisitos, sin prototipo completo ni certificaciones.

Fuentes y limitaciones: [Competitor References](competitor_references.md).

## 8. C — Comparación relevante

| Criterio | Nuestro gateway | Siemens IOT2050 M.2 | Moxa UC-2112-LX | Advantech UNO-2271G V2 |
|---|---|---|---|---|
| RS-485 | 2 objetivo | 1 COM configurable | 2 COM configurables | Expansión |
| CAN-FD | 1 objetivo | No documentado integrado | No documentado | CAN por expansión; CAN-FD no verificado |
| DI/DO industrial | 4 DI 24 V + 2 DO objetivo | Arduino; requiere adaptación | No documentado | Expansión |
| Ethernet | Principal; segundo TBD | 2 × Gigabit | 100 Mb/s + Gigabit | 2 × Gigabit |
| Plataforma | STM32H723VET6 / Zephyr | AM6548 / Linux | Cortex-A8 / MIL | Intel x86 / Windows o Ubuntu |
| Madurez | Diseño; no validado | Comercial | Comercial | Comercial |

Mensaje defendible: **mejor ajuste potencial a este conjunto específico de requisitos**, sujeto a diseño y validación; no “mejor producto industrial”.

## 9. Alcance y estado actual

| Elemento | Estado real |
|---|---|
| STM32H723VET6 + Zephyr | Decidido por D-18 |
| Suficiencia total de pines | Validada externamente |
| Asignación concreta de pines/periféricos | TBD |
| Interfaces objetivo | Decididas como alcance; no implementadas |
| Segundo Ethernet | TBD; requiere justificación |
| Esquemático y PCB | No desarrollados/fabricados |
| Firmware y prueba simultánea de interfaces | No implementados/no validados |
| Coste, consumo, tamaño y desempeño | TBD; sin evidencia experimental |

## 10. Próximos pasos

1. Cerrar caso demostrador y requisitos TBD críticos.
2. Congelar periféricos/pinout y arquitectura de alimentación.
3. Seleccionar interfaces y almacenamiento.
4. Desarrollar esquemático y validar interfaces/presupuestos.
5. Desarrollar firmware mínimo en Zephyr.
6. Diseñar y fabricar PCB Rev. A.
7. Probar y construir la matriz requisito → evidencia.

Detalle completo: §14 del [documento maestro](industrial_linux_gateway_requirements.md).
