# Auditoría del proyecto Industrial Gateway

**Repositorio:** `anhenaobe/industrial-linux-gateway`

**Fecha de auditoría:** 2026-09-15

**Alcance:** repositorio completo, documentación técnica, diagramas, presentación y comparación con competidores.
**Restricciones observadas:** auditoría documental; no se modificaron los artefactos técnicos, no se seleccionó una plataforma de procesamiento y no se realizó ningún commit.

> **Nota de vigencia (actualizada el 2026-09-15):** este archivo conserva la auditoría del estado anterior a la decisión D-18 y debe leerse como una instantánea histórica. Después de la auditoría se decidió **STM32H723VET6 + Zephyr RTOS** como baseline de Rev. A, se creó la fuente NABC y se incorporaron referencias competitivas. Las frases de este informe que presentan la plataforma como abierta, o MYC-YM6231/Linux como baseline vigente, quedaron superadas por la revisión 0.4 del [documento maestro](industrial_linux_gateway_requirements.md). Los hallazgos no deben borrarse porque documentan el punto de partida.

## Resumen ejecutivo

El proyecto tiene una base técnica útil, pero todavía no está listo para cumplir la entrega NABC solicitada por el profesor.

Los problemas principales son:

1. no existe una presentación en el repositorio ni un enlace a una presentación externa;
2. no existe una sección de competencia, matriz competitiva ni referencias oficiales;
3. el documento maestro mantiene MYC-YM6231/Linux como baseline aceptado, mientras el diagrama más reciente deja abierta la plataforma entre Linux MPU/SoM y Zephyr MCU;
4. los diagramas están presentes únicamente en el árbol local y no están versionados en Git;
5. los beneficios son deducibles de los requisitos, pero no están formulados ni trazados como argumentos NABC;
6. no hay evidencia para afirmar menor coste, tamaño, consumo o mayor robustez.

El enfoque funcional del gateway sigue siendo pertinente: integración de interfaces industriales heterogéneas, adquisición y normalización de datos, comunicación IP, persistencia, diagnóstico y mantenimiento. La siguiente revisión debe reconciliar todos los artefactos alrededor de una plataforma todavía abierta y convertir esa base en una presentación breve, visual y verificable.

## 1. Inventario del repositorio

El repositorio remoto es público y su rama principal observada coincide con el commit local `afcd2f3`.

```text
industrial-linux-gateway/
├── LICENSE
└── docs/
    ├── industrial_linux_gateway_requirements.md
    └── figures/                                  ← sin seguimiento en Git
        ├── industrial_gateway_architecture.drawio
        ├── industrial_gateway_architecture.svg
        └── .$industrial_gateway_architecture.drawio.bkp
```

| Artefacto | Versión y estado identificado |
|---|---|
| Documento de requerimientos | Rev. 0.3, fecha interna 2026-09-13; último commit 2026-09-14. Es el documento maestro publicado, pero su estado arquitectónico está desactualizado. |
| `industrial_gateway_architecture.drawio` | Última modificación local: 2026-09-14 16:11. Es la versión editable más reciente encontrada y refleja la selección abierta. |
| `industrial_gateway_architecture.svg` | Última modificación local: 2026-09-14 10:56. Conserva el contenido funcional genérico, pero una disposición anterior. |
| `.$industrial_gateway_architecture.drawio.bkp` | Respaldo de edición anterior. No debe presentarse como otro documento vigente. |
| Decision Register | Está dentro del documento maestro, §2.3; no existe como archivo independiente. |
| Otros diagramas | Tres diagramas Mermaid dentro del documento: arquitectura funcional, procesamiento y alimentación. |
| README | No encontrado. |
| Presentación | No encontrada; tampoco se encontró un enlace a una presentación externa. |
| PDFs, PPTX, documentación adicional o material NABC independiente | No encontrados. |
| Esquemático, PCB, firmware, BOM o resultados de pruebas | No encontrados. |

Solo `LICENSE` y el documento de requerimientos estaban versionados al realizar la auditoría. La presencia local de las figuras no demuestra que el profesor pueda acceder a ellas desde el repositorio.

La desactualización del SVG no se dedujo únicamente de las fechas: su bloque de procesamiento tiene ancho 360 frente a 377 en el `.drawio`, y el panel de alimentación 1020 frente a 1150. Su geometría coincide con el respaldo anterior en los elementos contrastados.

## A. Cumplimiento de las instrucciones del profesor

Las calificaciones siguientes corresponden al material existente en el momento de la auditoría.

| Criterio | Resultado | Evidencia |
|---|---|---|
| Repositorio accesible | **PASS** | GitHub confirma un repositorio público y las referencias remotas son accesibles. |
| Presentación disponible | **FAIL** | No existe en el repositorio ni hay un enlace que permita localizarla. |
| Enfoque NABC | **PARTIAL** | Hay material para Need y Approach; Benefits está implícito y Competition está ausente. |
| Documento de requerimientos | **PARTIAL** | Existe una especificación extensa y trazable, pero contiene decisiones arquitectónicas desactualizadas. |
| Diagrama de bloques | **PARTIAL** | Existe localmente y contiene los bloques necesarios; no está publicado ni alineado con el documento maestro. |
| Competidores comerciales | **FAIL** | No hay comparación con Siemens, Moxa o Advantech. |
| Enlaces oficiales | **FAIL** | El documento técnico no incluye referencias a fabricantes competidores. |
| Análisis de beneficios | **PARTIAL** | Hay requisitos que permiten justificar beneficios, pero no una argumentación comparativa explícita. |
| Consistencia técnica | **FAIL** | Documento y diagrama describen estados diferentes de selección de plataforma. |

### N — Need

**Evaluación: PARTIAL, con una base técnica sólida.**

La sección §1.1 del documento explica correctamente:

- la coexistencia de RS-485, CAN y señales industriales;
- las diferencias eléctricas, de protocolo, tierras, protección y temporización;
- por qué conectar físicamente esos equipos a Ethernet no resuelve su integración;
- la necesidad de adquirir, validar, normalizar, registrar y comunicar datos;
- la importancia del diagnóstico, mantenimiento y recuperación.

El Need evita lenguaje promocional vacío. Sin embargo, falta concretar quién necesita el gateway, en qué instalación y qué consecuencias observables produce el problema. “Técnico/usuario” es demasiado amplio para una presentación defendible.

El propio documento reconoce esta ausencia en `S-01`, `TBD-02`, `TBD-03` y `R-02`: todavía no están definidos el equipo demostrador, el protocolo y el caso de uso real.

### A — Approach

**Evaluación: PARTIAL.**

La documentación contempla RS-485, CAN-FD, entradas y salidas digitales, protección, posible aislamiento, procesamiento, Ethernet, almacenamiento, logging, diagnóstico, configuración y mantenimiento.

El `.drawio` sigue la organización requerida:

```text
FIELD DEVICES
→ INDUSTRIAL INTERFACE / CARRIER
→ PROCESSING PLATFORM
→ NETWORK
→ SERVER / SCADA
```

El diagrama vigente localmente plantea correctamente:

```text
PROCESSING PLATFORM
→ Linux MPU/SoM OR Zephyr MCU
→ Selection TBD
```

El problema es que el documento técnico sigue desarrollando una arquitectura basada en MYC-YM6231, Linux, eMMC integrada en el SoM y alimentación específica de 5 V.

### B — Benefits

**Evaluación: PARTIAL.**

Son defendibles como beneficios previstos:

- integración de interfaces industriales heterogéneas;
- adaptación de equipos legacy hacia redes IP;
- conservación y reenvío de datos ante pérdida de red;
- diagnóstico y mantenimiento reproducibles;
- protección de las interfaces de campo;
- diseño orientado a fabricación y prueba;
- posibilidad de ajustar el hardware al caso de uso real.

Todavía no pueden afirmarse como resultados:

- menor coste;
- menor consumo;
- menor tamaño;
- menor complejidad de software;
- mayor robustez;
- mejor rendimiento.

No hay BOM, mediciones, prototipo ni resultados comparativos que demuestren esas afirmaciones. `NF-08` exige considerar fabricación y prueba, pero no demuestra fabricación económica.

### C — Competition

**Evaluación: FAIL.**

No existe una sección competitiva, una matriz, un análisis de diferencias ni referencias oficiales. Esta es una de las carencias más directas frente a la instrucción del profesor.

## B. Hallazgos críticos

### 1. El documento maestro declara una decisión que actualmente está abierta

La línea 15 del documento establece MYC-YM6231 como `ACCEPTED / BASELINE FOR REV A`.

La aclaración de que no es una selección definitiva para producción comercial no equivale a mantener abierta la plataforma para Rev. A. La decisión antigua se repite en hechos, decisiones, arquitectura, requisitos, riesgos y próximos pasos.

### 2. El material que mejor refleja la arquitectura actual no está publicado

El `.drawio` ya dice `Linux MPU/SoM OR Zephyr MCU — Selection TBD`, pero `docs/figures/` no estaba bajo seguimiento de Git. El profesor solo tendría acceso al documento que conserva la arquitectura anterior.

### 3. Falta el entregable principal

No existe una presentación. Por ello no pueden cumplirse ni verificarse su estructura NABC, su extensión, legibilidad, inclusión del diagrama o referencias.

### 4. La diferenciación comercial carece de evidencia

El proyecto puede buscar un mejor ajuste al conjunto RS-485 + CAN-FD + DI/DO + Ethernet, pero falta demostrar:

- que esas interfaces corresponden a un caso real;
- que pueden funcionar simultáneamente;
- que el procesamiento y almacenamiento son suficientes;
- que el coste total resulta favorable.

### 5. La selección de plataforma necesita validación explícita

No existe en el repositorio un estudio del STM32H723VET6, una asignación de pines ni un presupuesto de recursos. Debe mantenerse como candidato en evaluación hasta validar pinout, periféricos simultáneos, memoria, comunicaciones, almacenamiento y recuperación.

## C. Discrepancias entre archivos

### Decisiones principales

| Tema | Documento maestro | Diagrama actual | Clasificación |
|---|---|---|---|
| Plataforma | MYC-YM6231 aceptado; `H-01`, `D-07` | Linux MPU/SoM o Zephyr MCU, TBD | **Obsoleta** la selección documental como estado actual. |
| Linux | `D-01`, §3.2 y varios `SR-LNX` lo obligan | Una alternativa | **Obsoleto** como obligación universal. |
| SoM | Obligatorio en solución, interfaces, mecánica y mantenimiento | MPU/SoM o MCU | **Parcialmente vigente**; conservar funciones y revisar implementación. |
| Cortex-M4F interno | `D-09`: reservado, Planned | No se presupone | **Obsoleto** como recurso común; conservar como historia de la opción MYC. |
| PRU | `D-10`: Deferred | No se presupone | **Obsoleta** como capacidad transversal. |
| eMMC integrada | `H-06`, §2.2, `SR-LNX-03` | Almacenamiento genérico | **Obsoleta** como obligación; persistencia sigue vigente. |
| Dos Gigabit Ethernet | Objetivo preliminar `D-11`; segundo puerto Should | Ethernet principal y segundo Target/TBD, sin fijar Gigabit | **Requiere decisión** sobre cantidad, velocidad y topología. |
| Alimentación del procesamiento | 5 V para MYC; `SR-PWR-06` | Tensión y presupuesto TBD | **Obsoleta** la tensión impuesta a cualquier alternativa. |
| MCU externo adicional | Excluido por `D-08` | Plataforma MCU posible | **Requiere decisión**: MCU auxiliar y MCU principal son conceptos diferentes. |
| STM32H723VET6 | No aparece | No aparece | **Requiere evaluación documentada**, no selección. |

El documento no obliga a utilizar M4F o PRU: ya contiene cautelas y exclusiones de dependencia. Los dos Ethernet tampoco están totalmente congelados; aparecen como objetivo preliminar. Aun así, deben revisarse tras reabrir la plataforma.

### Clasificación por secciones

| Secciones | Clasificación | Qué conservar o corregir |
|---|---|---|
| Portada y estado; §1.2–1.4 | **Parcialmente vigentes** | Conservar propósito industrial; revisar Linux/SoM, alcance y recursos específicos. |
| §1.1, §1.5–1.6 | **Vigentes en lo esencial** | Problema, estados y verificación útiles; neutralizar la referencia final a cómputo Linux. |
| §2.1–2.5 | **Parcialmente vigentes / requieren decisión** | Actualizar hechos, baseline, candidatos y supuestos; registrar reapertura de plataforma. |
| §3.1–3.2 | **Obsoletas como arquitectura actual** | Mermaid fija MYC/Linux y reparto A53/M4F/PRU. |
| §3.3 | **Requiere decisión** | Aclarar que la política sobre MCU auxiliar no excluye una plataforma MCU principal. |
| §3.4–3.9 | **Parcialmente vigentes** | Conservar bloques y funciones; revisar 5 V, eMMC, SocketCAN, consola y logs Linux. |
| §4–6 | **Mayormente vigentes** | Concretar caso real; revisar `F-08`, `F-16`, `NF-06` y prioridades de interfaces. |
| §7.1–7.5 | **Parcialmente vigentes** | Revisar dependencias de MYC/SoM/Linux; mantener protección, comunicación, persistencia y diagnóstico. |
| §7.6–7.7 | **Vigentes** | Protección y ambiente están correctamente planteados como requisitos pendientes de parámetros. |
| §7.8–7.10 | **Parcialmente vigentes** | Revisar referencias a SoM y reemplazabilidad; mantener mantenimiento y testabilidad. |
| §7.11 | **Vigente y prioritario** | El presupuesto de recursos es necesario para comparar alternativas. |
| §8–12 | **Parcialmente vigentes** | Actualizar trazabilidad, validación, riesgos, limitaciones y TBD dependientes de plataforma. |
| §13 | **Vigente pero incompleta** | Añadir la decisión Linux/Zephyr y sus criterios. |
| §14 | **Parcialmente vigente** | La primera tarea valida únicamente MYC; debe ampliarse a las alternativas. |
| §15 | **Vigente como registro histórico** | Conservar revisiones anteriores y añadir el cambio de estado futuro. |

Los requisitos más directamente afectados son `SR-PWR-06`, `SR-COM-06`, `SR-LNX-01`, `SR-LNX-03`, `SR-LNX-05`, `SR-LNX-06`, `SR-LNX-08`, `SR-LNX-10`, `SR-LNX-12`, `SR-DIA-08`, `SR-MEC-01`, `SR-MEC-06` y `SR-MNT-04`.

### Tratamiento recomendado del Decision Register

- `D-01`: parcialmente vigente. Conservar la separación entre campo y procesamiento; reemplazar Linux obligatorio por una decisión abierta.
- `D-06`: conservar como decisión histórica ya marcada Superseded. No reactivarla silenciosamente.
- `D-07`: obsoleta como decisión vigente. Marcar Superseded mediante una nueva decisión de reapertura, sin borrar la justificación histórica.
- `D-08`: requiere revisión. Habla de un MCU externo adicional, no de un MCU como plataforma principal.
- `D-09` y `D-10`: conservar como decisiones históricas aplicables a la alternativa MYC; no tratarlas como capacidades comunes.
- `D-11`: requiere decisión. Dos interfaces Gigabit siguen siendo un objetivo preliminar sin justificación renovada.
- `D-02` a `D-05` y `D-12` a `D-16`: funcionalmente vigentes o preliminares según su estado registrado.
- `D-17`: mantenimiento desde PC sigue vigente; SSH debe quedar condicionado a la plataforma.

## D. Información faltante

1. Caso industrial concreto: instalación, usuario, equipo, protocolo y consecuencia observable del problema.
2. Demostrador mínimo: qué adquirirá, qué enviará al servidor y si ejecutará comandos.
3. Carga representativa: nodos, tasas, latencia, tráfico concurrente y retención.
4. Validación de plataformas: matriz de pinout y recursos para cada candidata, incluyendo STM32H723VET6.
5. Ethernet: justificación de uno o dos puertos y velocidad necesaria.
6. Almacenamiento: capacidad, resistencia, política de entrega y comportamiento ante pérdida de alimentación.
7. DI/DO y protección: umbrales, cargas, estados seguros, entorno y aislamiento.
8. Beneficios cuantificables: presupuesto de coste, tamaño y consumo si se quieren utilizar como argumentos.
9. Evidencia de implementación: distinguir explícitamente objetivo, implementado y probado.
10. Presentación y referencias enlazadas: documento, figura y comparación comercial accesibles desde una entrada común.

## E. Cambios recomendados

### Prioridad 1: reconciliar el estado técnico

- Registrar una nueva decisión: plataforma abierta entre Linux MPU/SoM y Zephyr MCU.
- Marcar como Superseded las decisiones anteriores que dejen de aplicar, conservando justificación e historia.
- No reactivar silenciosamente `D-06` ni borrar `D-07`.
- Separar requisitos funcionales de implementaciones como Linux, SocketCAN, eMMC y SoM.
- Mantener STM32H723VET6 como candidato sujeto a validación.
- Conservar equivalencias y trazabilidad si se reorganiza la familia `SR-LNX`.

### Prioridad 2: preparar la evidencia NABC

- Seleccionar el caso demostrador.
- Definir entre tres y cinco beneficios, cada uno vinculado a requisitos.
- Incorporar comparación comercial con variantes identificadas.
- Resolver las discrepancias del diagrama y regenerar su exportación.
- Publicar conjuntamente documento, diagrama y presentación.

### Prioridad 3: demostrar las ventajas

No utilizar coste, consumo o tamaño como superioridades hasta disponer de estimaciones comparables o mediciones. El coste debe incluir interfaces adicionales, protección, alimentación, PCB, montaje y pruebas; comparar únicamente el precio del MCU sería insuficiente.

Formulación defendible:

> El proyecto busca integrar las interfaces necesarias para un caso industrial concreto, con electrónica de campo y mantenimiento definidos desde los requisitos. Su ventaja potencial es el ajuste a ese caso; coste, consumo y robustez permanecen pendientes de validación.

## F. Propuesta de estructura final de presentación

Se recomienda una presentación de diez diapositivas.

| # | Diapositiva | Contenido |
|---:|---|---|
| 1 | Portada | Proyecto, equipo, curso y enlace al repositorio. |
| 2 | Need | Usuario, instalación y problema concreto de integración. |
| 3 | Need → requisitos | Cuatro o cinco necesidades verificables con IDs. |
| 4 | Approach: arquitectura | Cinco dominios y plataforma abierta. Diagrama simplificado o vista legible del maestro. |
| 5 | Approach: funcionamiento | Adquisición, normalización, persistencia, envío y comandos autorizados. |
| 6 | Benefits | Tres o cuatro beneficios previstos y su respaldo técnico. |
| 7 | Competition | Tres soluciones comerciales, qué resuelven bien y enlaces oficiales. |
| 8 | Comparación | Matriz corta y conclusión sobre ajuste a requisitos. |
| 9 | Alcance y estado | Objetivos Rev. A, pendientes y expansión futura. STM32 como candidato. |
| 10 | Próximos pasos | Caso demostrador, pinout/recursos, plataforma, implementación y pruebas. |

Las fuentes pueden aparecer como enlaces discretos en las diapositivas 7 y 8 y completas en notas o en el documento técnico.

## G. Competidores y fuentes oficiales

### Alcance recomendado de la comparación

Para evitar mezclar características de variantes, se proponen estas referencias:

- Siemens SIMATIC IOT2050 M.2, `6ES7647-0BB00-1YA2`;
- Moxa UC-2112-LX, dentro de la familia UC-2100;
- Advantech UNO-2271G V2, diferenciando unidad base y expansiones.

### Siemens SIMATIC IOT2050 M.2

- **Fabricante:** Siemens.
- **Modelo:** SIMATIC IOT2050 M.2, `6ES7647-0BB00-1YA2`.
- **Procesamiento:** TI AM6548 HS, cuatro núcleos, 1 GHz.
- **Memoria y almacenamiento:** 2 GB DDR4; 16 GB eMMC.
- **Sistema operativo:** Linux mediante imagen de ejemplo y SIMATIC Industrial OS basado en Debian.
- **Ethernet:** dos interfaces Gigabit.
- **Serial:** un COM configurable como RS-232/422/485.
- **CAN:** no documentado como interfaz integrada en las fuentes consultadas.
- **I/O industrial:** la interfaz Arduino de 3,3/5 V no equivale a entradas o salidas industriales de 24 V.
- **Alimentación:** 12/24 VDC; rango documentado de 9 a 36 VDC para la variante referenciada.
- **Expansión:** Arduino y M.2 B/E.
- **Características industriales:** montaje DIN o pared, documentación de mantenimiento, especificaciones EMC e IP20.
- **Dimensiones:** no transcritas con suficiente confianza; consultar el plano dimensional oficial antes de publicar una cifra.
- **Precio:** N/A.
- **Página oficial:** https://sieportal.siemens.com/en-ww/products-services/detail/6ES7647-0BB00-1YA2
- **Manual oficial consultado:** https://cache.industry.siemens.com/dl/files/073/109974073/att_1295970/v1/iot2050_operating_instructions_en_en-US.pdf
- **Soporte oficial:** https://support.industry.siemens.com/forum/SA/en/posts/iot2050-forum-topics-overview/332396/?page=0&pageSize=10

### Moxa UC-2100 Series — referencia UC-2112-LX

- **Fabricante:** Moxa.
- **Modelo:** UC-2112-LX dentro de la familia UC-2100.
- **Procesamiento:** Armv7 Cortex-A8, 1 GHz.
- **Memoria y almacenamiento:** 512 MB RAM; 8 GB eMMC; microSD.
- **Sistema operativo:** Moxa Industrial Linux 1, Debian 9, kernel 4.4; soporte de largo plazo indicado hasta 2027.
- **Ethernet:** un puerto 10/100 y un puerto 10/100/1000.
- **Serial:** dos puertos configurables RS-232/422/485.
- **CAN:** no documentado.
- **I/O industrial:** no documentado.
- **Alimentación:** 9 a 48 VDC; consumo especificado de 4 W para la familia.
- **Expansión:** microSD en UC-2112; mPCIe pertenece a otra variante de la familia.
- **Características industriales:** watchdog, consola, opciones de temperatura amplia y certificaciones en variantes específicas.
- **Dimensiones UC-2112-LX sin orejas:** 77 × 111 × 25,5 mm.
- **Precio:** N/A.
- **Página oficial:** https://www.moxa.com/en/products/industrial-computing/arm-based-computers/uc-2100-series
- **Ficha oficial:** https://www.moxa.com/Moxa/media/PDIM/S100000581/moxa-uc-2100-series-datasheet-v1.2.pdf

La familia no es uniforme: UC-2101 tiene un COM; UC-2102 no presenta COM de campo; UC-2104 incorpora mPCIe; UC-2111 y UC-2112 ofrecen dos COM. No se deben combinar esas capacidades como si pertenecieran a una sola unidad.

### Advantech UNO-2271G V2

- **Fabricante:** Advantech.
- **Modelo/familia:** UNO-2271G V2.
- **Procesamiento:** Intel Celeron N6210 de dos núcleos o Pentium N6415 de cuatro núcleos.
- **Memoria y almacenamiento:** 4/8 GB RAM; 32/64 GB eMMC según variante y revisión; expansión mSATA/mPCIe.
- **Sistema operativo:** Windows 10/11 IoT y Ubuntu según configuración.
- **Ethernet:** dos interfaces Gigabit.
- **Serial:** disponible mediante expansión; no debe atribuirse a la unidad base.
- **CAN:** módulos CAN documentados mediante expansión; no se verificó CAN-FD.
- **I/O industrial:** módulos de E/S digital disponibles mediante expansión.
- **Alimentación:** 10 a 30 VDC.
- **Características industriales:** fanless, TPM 2.0, watchdog, IP30 y montaje DIN opcional.
- **Dimensiones de la unidad base AE:** aproximadamente 100 × 70 × 30 mm.
- **Temperatura:** −20 a 60 °C con condición documentada de flujo de aire de 0,7 m/s.
- **Precio:** N/A.
- **Página oficial:** https://www.advantech.com/en-us/products/1-2mlj9a/uno-2271g-v2/mod_a7b043d4-20e9-4276-ad94-2492f00e110e
- **Portal oficial de manuales:** https://www.advantech.com/en-us/support/details/manual-?id=1-27JYFV8
- **Ficha AE y expansiones consultada:** https://advdownload.advantech.com/productfileusa/PIS/UNO-2271G%20V2/file/UNO-2271G-V2_DS(020822)20220208162318.pdf

Las dimensiones anteriores corresponden a documentación AE y no deben extrapolarse automáticamente a una variante BE. Apareció indexada una ficha de marzo de 2026, pero su URL directa devolvió 404; por tanto no se consideró una referencia utilizable para cerrar especificaciones.

### Matriz competitiva propuesta

“Objetivo” describe intención del proyecto, no capacidad construida o validada. “No documentado” no significa imposibilidad mediante accesorios.

| Criterio | Nuestro gateway | Siemens IOT2050 M.2 | Moxa UC-2112-LX | Advantech UNO-2271G V2 |
|---|---|---|---|---|
| RS-485 | 2 canales objetivo | 1 COM configurable | 2 COM configurables | Mediante expansión |
| CAN-FD | 1 canal objetivo | No documentado integrado | No documentado | No verificado; CAN por expansión |
| DI/DO industrial | 4 DI de 24 V + 2 DO objetivo | Arduino; requiere adaptación | No documentado | Mediante módulos |
| Ethernet | Principal; segundo y velocidad TBD | 2 × Gigabit | 1 × 100 Mb/s + 1 × Gigabit | 2 × Gigabit |
| Alimentación | 24 V nominal; rango TBD | 9–36 VDC | 9–48 VDC | 10–30 VDC |
| Procesamiento/SO | Linux MPU/SoM o Zephyr MCU; TBD | AM6548 / Linux | Cortex-A8 / MIL | Intel x86 / Windows o Ubuntu |
| Expansión | Alcance por definir | Arduino y M.2 | microSD; mPCIe en otra variante | mPCIe y módulos apilables |

### Análisis competitivo

#### Qué hacen mejor las soluciones comerciales

Ofrecen equipos terminados, documentación de instalación, soporte, opciones de expansión y especificaciones ambientales verificables. Esa madurez supera lo demostrado actualmente por el proyecto, que aún carece de esquema, PCB y ensayos.

#### Qué hace diferente nuestro proyecto

Propone diseñar la electrónica de campo alrededor del conjunto de interfaces requerido. Esto permite controlar conectores, protección, diagnóstico y recursos de procesamiento desde el caso de uso.

#### Ventajas potenciales

- Integrar el conjunto requerido sin depender de varios módulos adicionales.
- Ajustar procesamiento y almacenamiento a una carga definida.
- Diseñar protección y testabilidad específicas.
- Reducir recursos sobrantes si la evaluación demuestra que no son necesarios.

Son hipótesis de diseño, no ventajas económicas o técnicas confirmadas.

#### Limitaciones frente a los competidores

- Viabilidad simultánea de interfaces pendiente.
- Menor madurez y ausencia de validación industrial.
- Sin certificaciones del producto.
- Sin ecosistema propio de soporte comercial.
- Coste total, consumo y dimensiones desconocidos.
- Una alternativa MCU podría limitar servicios y expansión; debe evaluarse contra la carga real.

La modularidad y la adaptación de interfaces legacy no son exclusivas del proyecto: los competidores también ofrecen comunicaciones industriales y expansión. La diferenciación debe centrarse en el ajuste concreto y demostrado.

### Propuesta de sección “Competitor References”

Cada referencia debe registrar fabricante, variante, título, revisión, URL, fecha de consulta, páginas o secciones utilizadas y limitaciones.

| Fuente | Estado de acceso observado |
|---|---|
| Siemens: ficha de producto en SiePortal | La URL responde; la página requiere JavaScript. |
| Siemens: manual de julio de 2024 | PDF oficial accesible y consultado. |
| Moxa: página de producto y ficha v1.2 | Accesibles y consultadas. |
| Advantech: página actual del producto | Accesible y consultada. |
| Advantech: portal de manuales | Distingue documentación AE y BE; incluye revisiones de 2026. |
| Advantech: ficha AE accesible | Útil para la variante documentada, pero no debe etiquetarse como última revisión de toda la familia. |

## H. Requisitos que respaldan cada parte de NABC

Los IDs siguientes existen en el documento maestro. Los que contienen referencias a Linux o SoM necesitan neutralización o tratamiento por alternativa.

| Parte | Argumento | Respaldo concreto |
|---|---|---|
| **Need** | Integrar equipos industriales con redes IP | `UC-01`, `F-01–04`, `NF-01`, `SR-COM-01/02` |
| **Need** | Mantener datos durante interrupciones | `UC-02`, `F-05/06`, `NF-02` |
| **Need** | Diagnosticar y mantener el equipo | `UC-04/05`, `F-08/09`, `NF-05–07` |
| **Approach** | RS-485, CAN-FD y DI/DO | `D-12–14`, `SR-COM-03/04`, `SR-IO-01/02` |
| **Approach** | Alimentación y protección | `SR-PWR-01–05`, `SR-SAF-02–04/07` |
| **Approach** | Procesamiento y separación de funciones | `SR-LNX-02/11`, `SR-PER-01–03` |
| **Approach** | Persistencia, diagnóstico y mantenimiento | `SR-LNX-04`, `SR-DIA-01/04/06`, `SR-MNT-01–03` |
| **Benefits** | Integración heterogénea | `F-01–04`, `SR-COM-02–04`, `SR-IO-01/02` |
| **Benefits** | Recuperación de transferencias | `F-05/06`, `NF-02`, `SR-LNX-04`, `SR-COM-07` |
| **Benefits** | Electrónica de campo protegida | `NF-09`, `SR-PWR-02–05`, `SR-SAF-02–04` |
| **Benefits** | Servicio reproducible | `NF-05/07`, `SR-DIA`, `SR-MNT` |
| **Benefits** | Fabricabilidad y testabilidad | `NF-08`, `SR-MEC-03`, `SR-TST-01–05` |
| **Competition** | Criterios para comparar ajuste | `SR-COM`, `SR-IO`, `SR-PWR-01`, `SR-MNT`, `SR-MEC`, `SR-PER` |

La trazabilidad existente en §8 conecta necesidades y requisitos, pero todavía falta el enlace:

```text
afirmación de la diapositiva
→ requisito
→ bloque de arquitectura
→ evidencia o estado pendiente
```

Un requisito respalda que un beneficio es buscado; su cumplimiento debe respaldarse con pruebas antes de presentarlo como obtenido.

## 8. Auditoría específica del diagrama de bloques

Se revisaron contenido XML, geometría, estilos y conexiones. La legibilidad de una renderización completa no pudo validarse visualmente durante la auditoría; las observaciones geométricas y de conectividad sí fueron comprobadas.

| Criterio | Resultado |
|---|---|
| Cinco dominios claramente identificados | **PASS** |
| RS-485, CAN-FD, DI/DO, protección y aislamiento TBD | **PASS** |
| Procesamiento abierto, sin MCU seleccionado | **PASS** |
| Flujo de adquisición | **PASS**, con aclaración pendiente sobre persistencia |
| Flujo completo de comandos | **PARTIAL** |
| Alimentación | **PARTIAL** |
| Diferenciación baseline/TBD/futuro | **PARTIAL** |
| Consistencia con documento maestro | **FAIL** |
| Sincronización SVG–Drawio | **FAIL** en disposición; contenido funcional alineado |

Discrepancias concretas:

1. **Comandos hacia RS-485 y CAN-FD:** los extremos son bidireccionales, pero los tramos internos conector → protección → aislamiento → front-end solo muestran flechas de entrada. El retorno de comandos queda gráficamente incompleto.
2. **Alimentación:** `processing_rail → aux_rails` sugiere que los auxiliares derivan del rail de procesamiento, aunque esa topología no está decidida. Tampoco se explicitan las cargas alimentadas por cada dominio.
3. **Estados:** la línea discontinua significa simultáneamente Target, TBD, opcional y servicio. El comando interno también usa esa línea. Conviene separar estado de implementación y tipo de flujo.
4. **Persistencia:** la única trayectoria completa pasa por logging y almacenamiento antes de llegar a red. Debe aclararse si almacenar antes de transmitir es una política requerida o solo un ejemplo.
5. **Funciones transversales:** configuración no tiene conexiones; diagnóstico y actualización no muestran claramente su relación con los servicios centrales.
6. **Legibilidad en presentación:** abundan textos de 9–11 px. El diagrama puede servir como figura técnica ampliable, pero existe un riesgo claro de ilegibilidad al colocarlo completo en una diapositiva.

El SVG comparte las etiquetas funcionales del `.drawio`, pero conserva una geometría anterior. Debe regenerarse después de corregir el editable y comprobarse en el formato final de presentación.

## I. Archivos que deberían modificarse posteriormente

| Archivo | Cambio recomendado |
|---|---|
| `docs/industrial_linux_gateway_requirements.md` | Reconciliar plataforma, decisiones, requisitos dependientes, trazabilidad, riesgos y próximos pasos; incorporar referencias competitivas. |
| `docs/figures/industrial_gateway_architecture.drawio` | Corregir retorno de comandos, convenciones de estado y distribución funcional de alimentación; aclarar persistencia y funciones transversales. |
| `docs/figures/industrial_gateway_architecture.svg` | Regenerar desde el editable revisado y verificar legibilidad en el destino. |
| `README.md` — nuevo | Crear una entrada al proyecto con estado actual y enlaces a requerimientos, diagrama y presentación. |
| Presentación — nueva | Crear diez diapositivas con NABC, trazabilidad y comparación oficial. |
| Referencias competitivas — sección o archivo nuevo | Registrar variantes, fuentes, revisiones, fecha de consulta y límites de la comparación. |
| Respaldo `.bkp` | Mantener identificado como respaldo; no usarlo como entrega ni como fuente normativa. |

## Conclusión

El enfoque funcional del gateway es pertinente, pero la entrega está incompleta y el estado de arquitectura está desincronizado. La documentación técnica explica adecuadamente la necesidad industrial y contiene buena materia prima para el Approach y los Benefits. Falta convertirla en una narrativa NABC, incorporar una competencia honesta basada en fuentes oficiales y reconciliar todo el repositorio con el estado actual:

```text
PROCESSING PLATFORM
→ Linux MPU/SoM OR Zephyr MCU
→ selection TBD
```

El STM32H723VET6 debe registrarse únicamente como candidato en evaluación hasta completar la validación de pinout y recursos. Las decisiones históricas deben conservarse y marcarse como Superseded cuando corresponda.

La posición competitiva defendible es “mejor ajuste potencial a este conjunto específico de requisitos”, no “mejor producto industrial”.
