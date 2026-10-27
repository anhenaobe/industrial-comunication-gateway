# Industrial Communication Gateway Proof of Concept

## 1. Objective

Demostrar adquisición desde una interfaz industrial de campo, procesamiento mediante Zephyr y comunicación hacia una red IP/Ethernet con diagnóstico básico.

Esta Proof of Concept (PoC) es una implementación reducida para validar el flujo funcional principal del gateway. No representa el producto industrial completo, una Product Rev. A implementada ni evidencia de validación de todas las interfaces objetivo.

## 2. Relation with Product Rev. A

Product Rev. A y la PoC tienen propósitos y niveles de implementación diferentes. Los requisitos y decisiones vigentes del producto se mantienen en el documento técnico maestro; la PoC no los sustituye ni los reduce.

| Elemento | Product Rev. A | PoC |
|---|---|---|
| Propósito | Implementar el producto definido por los requisitos y decisiones de Rev. A. | Demostrar de forma limitada el flujo funcional principal del gateway. |
| Procesamiento | STM32H723VET6 con Zephyr RTOS. | NUCLEO-F429ZI (STM32F429ZIT6) con Zephyr; placa elegida para M0/M1. |
| Interfaces de campo | 2 × RS-485, 1 × CAN-FD, 4 entradas digitales industriales de 24 V y 2 salidas digitales industriales como arquitectura objetivo. | Un enlace RS-485 como interfaz inicial; CAN-FD y DI/DO no son necesarios para el alcance inicial. |
| Red | 1 × DP83826I, Ethernet 10/100 mediante RMII. | Un enlace Ethernet adecuado para transmitir los datos de la demostración. |
| Electrónica industrial | Protección, acondicionamiento, aislamiento donde se justifique y alimentación industrial según requisitos. | Módulos externos y adaptación limitada para pruebas controladas; no equivale a una etapa industrial validada. |
| Implementación física | PCB propia de Product Rev. A. | Tarjeta de desarrollo y módulos externos interconectados. |
| Validación | Validación eléctrica, funcional y de comunicaciones contra los requisitos del producto. | Validación funcional limitada al flujo y a los criterios de éxito definidos en este documento. |

## 3. Functional Flow

```text
PC TRANSMISOR
          ↓
  ADAPTADOR USB-RS485
          ↓
      BUS RS-485
          ↓
 TRANSCEIVER RS-485
          ↓
 UART STM32F429 + ZEPHYR
          ↓
 VALIDACIÓN Y PREPARACIÓN DE DATOS
          ↓
   ETHERNET CABLEADO
          ↓
     PC RECEPTOR
```

**DECIDED:** el PC transmisor simula el origen de datos; puede ser el mismo equipo que el PC receptor. El enlace RS-485 es unidireccional PC → STM32, sin ACK, NACK ni retransmisiones por RS-485. El firmware valida los datos antes de enviarlos por Ethernet. Se utiliza CRC-16, número de secuencia para diagnosticar discontinuidades y duplicados, y payload máximo de 256 bytes.

La [especificación de arquitectura de firmware](firmware_architecture_poc.md) distingue decisiones cerradas, propuestas de diseño y aspectos **NOT IMPLEMENTED / NOT VALIDATED**. El protocolo exacto de trama y el transporte sobre Ethernet se revisan allí; no se declara compatibilidad Modbus ni garantía de entrega extremo a extremo.

## 4. What does processing mean?

En la PoC, procesamiento significa:

- recepción de datos seriales;
- interpretación de trama y validación de integridad mediante CRC-16;
- diagnóstico de secuencia y preparación de datos para su transmisión por red;
- diagnóstico básico del flujo y de los errores observables.

La PoC no se define como controlador industrial crítico, controlador de seguridad ni sistema de control determinista de tiempo real. El alcance cerrado no incorpora comandos de retorno por RS-485. No exige normalización semántica ni una conversión de formato adicional a la preparación de la salida.

## 5. Proposed Hardware Blocks

Los siguientes bloques constituyen una selección preliminar para la PoC. No son una selección definitiva de componentes ni una BOM de Product Rev. A.

### Processing

- PoC sobre NUCLEO-F429ZI con Zephyr. Esta elección de placa de desarrollo no modifica el STM32H723VET6 del producto Rev. A.

### Industrial interface

- RS-485 transceiver module.

### Communication

- Ethernet cableado; el PHY de la Nucleo no debe confundirse con el DP83826I de Product Rev. A.

### Power

- alimentación propia de la tarjeta de desarrollo.

### Host

- PC simulador, servidor o equipo de visualización y registro.

La NUCLEO-F429ZI es la placa elegida para la PoC. El transceptor RS-485, sus conexiones y alimentación deberán verificarse antes de montar esa parte de la demostración.

## 6. PoC Scope

### Include

- comunicación RS-485;
- recepción de datos;
- interpretación del protocolo;
- transmisión mediante Ethernet;
- visualización básica o logging;
- diagnóstico básico suficiente para observar el flujo de datos y fallos de comunicación.

### Not include

- PCB final;
- envolvente industrial;
- etapa de protección de campo de 24 V;
- CAN-FD, salvo que se añada posteriormente mediante una decisión de alcance de la PoC;
- circuitos DI/DO finales;
- certificación industrial;
- validación simultánea de todas las interfaces de Product Rev. A.

## 7. Success Criteria

La PoC será exitosa si:

1. El MCU recibe los datos del PC transmisor mediante RS-485.
2. Interpreta las tramas y verifica CRC-16 antes del reenvío, con payload máximo de 256 bytes.
3. Diagnostica discontinuidades y duplicados mediante número de secuencia.
4. Envía los datos válidos mediante Ethernet cableado.
5. El PC receptor puede visualizar o registrar los datos de la demostración.

Son criterios por verificar, no resultados obtenidos; la recepción en la demostración no implica garantía de entrega de todos los mensajes.

El cumplimiento de estos criterios valida únicamente la PoC. No demuestra que Product Rev. A esté implementado, fabricado o validado.

## 8. Open Questions

- Confirmar el módulo RS-485 y sus conexiones al banco NUCLEO-F429ZI.
- Cerrar framing y parámetros de protocolo conforme a las propuestas de la especificación de firmware.
- Cerrar transporte Ethernet y configuración de red/host.
- Definir herramienta de registro y carga de ensayo para verificar los criterios de éxito.

Las respuestas deberán registrarse como decisiones de implementación de la PoC. No deberán convertirse automáticamente en requisitos o selecciones finales de Product Rev. A.
