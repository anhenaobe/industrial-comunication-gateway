# Figuras

`industrial_gateway_architecture.drawio` contiene la arquitectura funcional y
el Power Tree del baseline actual. Las selecciones eléctricas y los cálculos se
detallan en [el documento técnico](../industrial_gateway_requirements.md).

El Power Tree muestra las dos entradas, sus TDS3011P y ramas LTC4414 +
DMP6023LSS-13, el NIS3071MT4TWG y los dos bucks. Los TDS representan conexiones
en derivación a GND. Las flechas funcionales no son conexiones pin a pin.

Las exportaciones visuales deben generarse desde esta fuente editable.
Los archivos editoriales `.$*.bkp` están excluidos mediante `.gitignore`.

## Diagrama de bloques de hardware y firmware

[`industrial_gateway_firmware_block_diagram.drawio`](industrial_gateway_firmware_block_diagram.drawio)
complementa la figura general con el MCU central, sus periféricos internos y
las interfaces físicas externas de Rev. A en una página horizontal. Los seis
módulos funcionales son responsabilidades propuestas para desarrollo con Zephyr:
**NOT IMPLEMENTED / NOT VALIDATED**. No fija hilos, pines ni protocolos de aplicación.

La organización sigue el enfoque solicitado del capítulo 2, figura 2-3, de
*Making Embedded Systems*, segunda edición, de Elecia White. La selección de
componentes procede del [documento técnico local](../industrial_gateway_requirements.md);
la PoC unidireccional no limita los dos buses RS-485 half-duplex del producto.
El archivo contiene bloques y conectores editables, sin imágenes incrustadas.

## Contexto y organigrama de firmware

- [`industrial_gateway_context.drawio`](industrial_gateway_context.drawio): una sola entidad del producto y sus relaciones con equipos industriales, red superior, cargas, técnico mediante PC externo y las dos fuentes de energía. CU-01 a CU-03 son una síntesis académica; no sustituyen UC-01 a UC-06.
- [`industrial_gateway_firmware_organigram.drawio`](industrial_gateway_firmware_organigram.drawio): Gateway Application coordina cuatro grupos funcionales, con sus submódulos y dependencias de UART/USART, FDCAN, Ethernet y GPIO compartido para DI/DO. Zephyr es la plataforma de ejecución y servicios.

Ambas figuras representan el producto Rev. A completo y complementan el diagrama
de bloques; no se limitan a la PoC. La organización sigue las referencias
conceptuales de las figuras 2-1 y 2-4 del capítulo 2 de *Making Embedded Systems*,
segunda edición, de Elecia White. Son XML sin comprimir, con formas y conectores
editables, en una página por archivo. **PROPOSED / NOT IMPLEMENTED / NOT VALIDATED**.

La fuente principal es el [documento técnico local](../industrial_gateway_requirements.md),
complementado por la [PoC](../proof_of_concept.md) y su
[arquitectura de firmware](../firmware_architecture_poc.md). El antiguo
`docs/industrial_linux_gateway_requirements.md` está eliminado en el árbol de
trabajo; sus actores y UC-01 a UC-06 se consultaron en `HEAD` local como referencia
histórica, sin restaurar el archivo ni trasladar decisiones eléctricas anteriores.
Las condiciones de autorización, el origen de las órdenes de DO, los protocolos
de aplicación y el medio concreto de mantenimiento continúan pendientes.
