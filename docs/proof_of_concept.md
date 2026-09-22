# Industrial Communication Gateway Proof of Concept

## 1. Objective

Demostrar adquisición desde una interfaz industrial de campo, procesamiento mediante Zephyr y comunicación hacia una red IP/Ethernet con diagnóstico básico.

Esta Proof of Concept (PoC) es una implementación reducida para validar el flujo funcional principal del gateway. No representa el producto industrial completo, una Product Rev. A implementada ni evidencia de validación de todas las interfaces objetivo.

## 2. Relation with Product Rev. A

Product Rev. A y la PoC tienen propósitos y niveles de implementación diferentes. Los requisitos y decisiones vigentes del producto se mantienen en el documento técnico maestro; la PoC no los sustituye ni los reduce.

| Elemento | Product Rev. A | PoC |
|---|---|---|
| Propósito | Implementar el producto definido por los requisitos y decisiones de Rev. A. | Demostrar de forma limitada el flujo funcional principal del gateway. |
| Procesamiento | STM32H723VET6 con Zephyr RTOS. | Tarjeta de desarrollo STM32H723 o equivalente compatible con la demostración; selección exacta preliminar. |
| Interfaces de campo | 2 × RS-485, 1 × CAN-FD, 4 entradas digitales industriales de 24 V y 2 salidas digitales industriales como arquitectura objetivo. | Un enlace RS-485 como interfaz inicial; CAN-FD y DI/DO no son necesarios para el alcance inicial. |
| Red | Ethernet principal; segundo Ethernet TBD. | Un enlace Ethernet adecuado para transmitir los datos de la demostración. |
| Electrónica industrial | Protección, acondicionamiento, aislamiento donde se justifique y alimentación industrial según requisitos. | Módulos externos y adaptación limitada para pruebas controladas; no equivale a una etapa industrial validada. |
| Implementación física | PCB propia de Product Rev. A. | Tarjeta de desarrollo y módulos externos interconectados. |
| Validación | Validación eléctrica, funcional y de comunicaciones contra los requisitos del producto. | Validación funcional limitada al flujo y a los criterios de éxito definidos en este documento. |

## 3. Functional Flow

```text
FIELD DEVICE / SIMULATOR
          ↓
        RS-485
          ↓
 RS-485 TRANSCEIVER
          ↓
   STM32 + ZEPHYR
          ↓
   DATA PROCESSING
          ↓
       ETHERNET
          ↓
 PC / SERVER / DASHBOARD
```

El dispositivo de campo podrá ser real o simulado. La selección de equipo, protocolo, hardware y herramienta de visualización permanece abierta hasta cerrar las preguntas de la sección 8.

## 4. What does processing mean?

En la PoC, procesamiento significa:

- recepción de datos seriales;
- interpretación del protocolo;
- conversión de formato;
- normalización de la información;
- preparación de datos para su transmisión por red;
- diagnóstico básico del flujo y de los errores observables.

La PoC no se define como controlador industrial crítico, controlador de seguridad ni sistema de control determinista de tiempo real. Un posible camino de comandos solo se incorporará si se delimita posteriormente y no modifica la función principal de adquisición, procesamiento y comunicación.

## 5. Proposed Hardware Blocks

Los siguientes bloques constituyen una selección preliminar para la PoC. No son una selección definitiva de componentes ni una BOM de Product Rev. A.

### Processing

- STM32H723 development board or equivalent.

### Industrial interface

- RS-485 transceiver module.

### Communication

- Ethernet.

### Power

- alimentación propia de la tarjeta de desarrollo.

### Host

- PC simulador, servidor o equipo de visualización y registro.

La tarjeta exacta, el transceptor, la implementación Ethernet y la alimentación de los módulos deberán verificarse antes de montar la demostración.

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

1. El MCU recibe datos mediante RS-485.
2. Los interpreta correctamente conforme al protocolo seleccionado.
3. Ejecuta procesamiento básico sobre la información recibida.
4. Envía la información mediante Ethernet.
5. Un PC puede visualizar o registrar los datos.

El cumplimiento de estos criterios valida únicamente la PoC. No demuestra que Product Rev. A esté implementado, fabricado o validado.

## 8. Open Questions

- ¿Qué tarjeta STM32 exacta se utilizará?
- ¿Cuál será el protocolo inicial, por ejemplo Modbus RTU?
- ¿Qué módulo RS-485 se utilizará?
- ¿Qué método o interfaz Ethernet proporcionará la tarjeta seleccionada?
- ¿Qué herramienta se utilizará para visualizar o registrar los datos?
- ¿Es necesario incorporar CAN-FD en una etapa posterior de la PoC?

Las respuestas deberán registrarse como decisiones de implementación de la PoC. No deberán convertirse automáticamente en requisitos o selecciones finales de Product Rev. A.
