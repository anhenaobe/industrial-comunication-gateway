# Industrial Communication Gateway

**Diseño Electrónico · Documento preparatorio de firmware**

<style>
@page { size: A4; margin: 16mm; }
@media print {
  body { font-family: Arial, sans-serif; font-size: 10pt; line-height: 1.16; color: #172333; }
  h1 { font-size: 17pt; margin: 0 0 5pt; }
  h2 { font-size: 13pt; margin: 9pt 0 5pt; }
  h3 { font-size: 10.5pt; margin: 7pt 0 3pt; }
  p { margin: 4pt 0; }
  table { width: 100%; border-collapse: collapse; font-size: 9pt; }
  th, td { border: 0.5pt solid #bec8d2; padding: 4pt; text-align: left; }
  th { background: #edf2f6; }
  pre { font-size: 8.5pt; line-height: 1.1; padding: 5pt; white-space: pre-wrap; }
  tr, pre { break-inside: avoid; }
}
</style>

## Página 1 · Producto, objetivo y hardware

**La documentación precede a la implementación. NOT IMPLEMENTED / NOT VALIDATED:**
esta propuesta académica no presenta firmware desarrollado ni resultados experimentales.

### Producto y propósito

El **Industrial Communication Gateway** integra equipos y señales industriales con
una red IP. Su función principal es adquirir, validar, procesar, diagnosticar y
transmitir información de campo hacia sistemas de supervisión. Resuelve la
dificultad de reunir interfaces industriales diferentes en un mismo camino de
comunicación y diagnóstico. Lo utilizarían integradores de automatización, personal
de mantenimiento e ingenieros de supervisión de equipos industriales.

### Plataforma de Product Rev. A · DECIDED

| Bloque | Arquitectura y función |
|---|---|
| Procesamiento y RTOS | STM32H723VET6 con Zephyr. |
| Ethernet cableado | MAC integrado en STM32 y PHY externo DP83826I, mediante RMII. |
| RS-485 | 2 × THVD1420 para dos buses independientes half-duplex. |
| CAN-FD | Controlador FDCAN del STM32 y transceiver ATA6561. |
| Entradas digitales | 4 canales industriales aislados de 24 V mediante 2 × ISO1212; reciben señales de sensores o dispositivos externos. |
| Salidas digitales | 2 × BSP75N: dos canales low-side de 24 V / 500 mA nominales por canal para cargas o actuadores externos. Control mediante SN74LVC2T45. |
| Alimentación | Dos entradas posibles de 18–30 VDC; OR-ing LTC4414 + DMP6023LSS-13, supresión TDS3011P, protección NIS3071MT4TWG y conversión buck síncrona LMR36015 → 3.3 V / LMR36015 → 5 V. |
| Mantenimiento y diagnóstico | Interacción prevista desde PC; interfaz concreta por especificar. |

Los sensores y actuadores son **externos**: las DI adquieren sus señales y las
DO controlan sus cargas. Sus modelos dependen de la aplicación industrial.

### Producto y demostrador

**Product Rev. A:** arquitectura industrial completa definida por los requisitos.
**PoC:** demuestra inicialmente PC → USB-RS485 → bus/transceiver RS-485 →
STM32/Zephyr → Ethernet → PC. No necesita CAN-FD, DI/DO ni la alimentación
industrial completa. Se orienta a NUCLEO-H723ZG, pendiente de confirmar placa y
conexiones; su PHY de placa no equivale al DP83826I del producto. Ambos PC pueden
ser el mismo equipo. La PoC no es un producto comercial terminado.

**DECIDED para la PoC:** RS-485 unidireccional, sin ACK, NACK ni retransmisiones;
CRC-16, secuencia diagnóstica y payload máximo de 256 bytes. **PROPOSED:** UDP y
framing binario exacto. La reutilización del código en Rev. A es un requisito
de diseño; la portabilidad no está validada.

<div style="break-before: page; page-break-before: always;"></div>

## Página 2 · Arquitectura y comportamiento del firmware

**Organización modular:** transporte UART/RS-485; parser y validación; enrutador/cola;
transporte Ethernet; supervisor/diagnóstico. Base en C y APIs Zephyr, con hardware
configurado mediante DeviceTree/Kconfig cuando corresponda y lógica separada de drivers.

| Momento / función | Comportamiento esperado de la PoC |
|---|---|
| Encendido | Inicializar recursos, UART y Ethernet; preparar buffers y mensajes; establecer estado según disponibilidad. |
| Recepción | Identificar tramas completas, limitar payload, verificar CRC-16 y evaluar secuencia; descartar inválidas. |
| Control del flujo | Gestionar buffers/colas acotados y admisión a red. Saturación o red ausente requieren descarte controlado; política detallada propuesta. No controla actuadores en esta PoC. |
| Envío y datos | Transmitir mensajes válidos al PC; mantener mensajes y contadores en RAM. El PC puede verificarlos y registrarlos. |
| Monitoreo | Detectar errores UART, tramas malformadas/incompletas, CRC inválido, saltos/duplicados, saturación, fallos de envío y pérdida/recuperación de red. |

```text
PC TRANSMISOR
  ↓ USB-RS485 → BUS → TRANSCEIVER RS-485
  ↓ STM32 / UART RX
  ↓ PARSER + CRC-16 + SECUENCIA → error: descarte y diagnóstico
  ↓ COLA DE MENSAJES VÁLIDOS
  ↓ ETHERNET / UDP (PROPOSED)
  ↓ PC RECEPTOR: verificación y registro
```

UDP no garantiza entrega ni orden; CRC no garantiza autenticidad. Los contadores
no miden todas las pérdidas. No se declara persistencia implementada en la PoC:
el registro de prueba reside en el PC; la persistencia prevista para Rev. A
requiere especificar alcance y soporte.

**Estados propuestos:** INITIALIZATION prepara recursos; NETWORK_WAIT espera red
sin detener RX; OPERATIONAL recibe y transmite; DEGRADED mantiene funciones sanas
ante fallos/saturación; ERROR_RECOVERY solo aplica a recursos recuperables mediante
una acción concreta, por ejemplo rearmar RX o recrear un socket.

**Mayor desafío técnico:** recibir tramas RS-485 y enviarlas por Ethernet
concurrentemente, gestionando buffers, latencias, fallos y recuperación. UART no
debe quedar bloqueada esperando Ethernet: colas acotadas desacoplan ambos caminos;
no se ejecutan operaciones de red bloqueantes en interrupciones/callbacks UART.

**Pendientes y primeras pruebas:** confirmar Nucleo/periféricos y transceiver,
niveles y conexiones; fijar UART y Ethernet; aprobar el formato binario completo.
Primero verificar recepción UART y conectividad Ethernet por separado, después
RS-485 y la integración completa, incluyendo errores y desconexión del enlace.

**Documentación para desarrollar:** ya existen [requisitos](industrial_gateway_requirements.md),
[arquitectura y módulos](firmware_architecture_poc.md) y [alcance PoC](proof_of_concept.md),
con flujo, estados, interfaces y plan de pruebas inicial. Deben completarse
requisitos funcionales/no funcionales verificables, protocolo, configuración de
periféricos/memoria, criterios de aceptación y manual de compilación, programación,
carga y depuración.

**Firmware mínimo funcional:** Zephyr en una placa STM32H723, capaz de recibir una
trama RS-485, verificar CRC-16, identificar su secuencia y transmitir datos válidos
por Ethernet a un PC que los verifique y registre. Demostraría el camino completo
de comunicaciones, sin validar todas las funciones de Product Rev. A.
