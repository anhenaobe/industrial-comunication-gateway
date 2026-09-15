# Competitor References

**Consulta:** 2026-09-15

**Propósito:** respaldar la sección Competition de la entrega NABC con fuentes oficiales del fabricante.

## Reglas de comparación

- Se compara una variante identificable, sin combinar características de otros miembros de la familia.
- `No documentado` no significa que una capacidad sea imposible mediante accesorios.
- Las capacidades del gateway propio son objetivos de diseño: no están implementadas ni validadas.
- Precio se deja `N/A` porque no se encontró una fuente oficial verificable y comparable.
- La posición defendible es mejor ajuste potencial al conjunto específico de requisitos, no superioridad global frente a productos comerciales.

## Siemens SIMATIC IOT2050 M.2

| Campo | Información respaldada por las fuentes oficiales consultadas |
|---|---|
| Fabricante / variante | Siemens, SIMATIC IOT2050 M.2, `6ES7647-0BB00-1YA2` |
| Procesamiento | TI AM6548 HS, cuatro núcleos, 1 GHz |
| Sistema operativo | Linux mediante imagen de ejemplo; SIMATIC Industrial OS basado en Debian |
| Memoria / almacenamiento | 2 GB DDR4; 16 GB eMMC |
| Ethernet | 2 × Gigabit Ethernet |
| Serial | 1 × COM configurable RS-232/422/485 |
| CAN | No documentado como interfaz integrada en las fuentes consultadas |
| I/O industrial | Interfaz Arduino de 3,3/5 V; no equivale a DI/DO industriales de 24 V |
| Alimentación | 12/24 VDC; rango documentado 9–36 VDC |
| Expansión / industrial | Arduino, M.2 B/E; montaje DIN o pared; especificaciones EMC e IP20 |
| Tamaño | N/A en esta comparación; revisar plano dimensional oficial antes de publicar una cifra |
| Precio | N/A |

Fuentes oficiales:

- [Página de producto Siemens](https://sieportal.siemens.com/en-ww/products-services/detail/6ES7647-0BB00-1YA2)
- [SIMATIC IOT2050 Operating Instructions, julio de 2024](https://cache.industry.siemens.com/dl/files/073/109974073/att_1295970/v1/iot2050_operating_instructions_en_en-US.pdf)

## Moxa UC-2112-LX

| Campo | Información respaldada por las fuentes oficiales consultadas |
|---|---|
| Fabricante / variante | Moxa, UC-2112-LX de la familia UC-2100 |
| Procesamiento | Armv7 Cortex-A8, 1 GHz |
| Sistema operativo | Moxa Industrial Linux 1; Debian 9, kernel 4.4; soporte indicado hasta 2027 |
| Memoria / almacenamiento | 512 MB RAM; 8 GB eMMC; microSD |
| Ethernet | 1 × 10/100 y 1 × 10/100/1000 |
| Serial | 2 × puertos configurables RS-232/422/485 |
| CAN | No documentado |
| I/O industrial | No documentado |
| Alimentación | 9–48 VDC; 4 W especificados para la familia |
| Expansión / industrial | microSD en UC-2112; watchdog, consola, variantes de temperatura amplia y certificaciones específicas |
| Tamaño | 77 × 111 × 25,5 mm sin orejas |
| Precio | N/A |

Fuentes oficiales:

- [Página de producto Moxa UC-2100](https://www.moxa.com/en/products/industrial-computing/arm-based-computers/uc-2100-series)
- [UC-2100 Series Datasheet v1.2](https://www.moxa.com/Moxa/media/PDIM/S100000581/moxa-uc-2100-series-datasheet-v1.2.pdf)

Limitación: mPCIe pertenece a otra variante de la familia; no se atribuye al UC-2112-LX.

## Advantech UNO-2271G V2

| Campo | Información respaldada por las fuentes oficiales consultadas |
|---|---|
| Fabricante / familia | Advantech, UNO-2271G V2 |
| Procesamiento | Intel Celeron N6210 de dos núcleos o Pentium N6415 de cuatro núcleos, según variante |
| Sistema operativo | Windows 10/11 IoT y Ubuntu, según configuración |
| Memoria / almacenamiento | 4/8 GB RAM; 32/64 GB eMMC según variante/revisión; expansión mSATA/mPCIe |
| Ethernet | 2 × Gigabit Ethernet |
| Serial | Mediante expansión; no atribuido a la unidad base |
| CAN | Módulos CAN mediante expansión; CAN-FD no verificado |
| I/O industrial | Mediante módulos de expansión |
| Alimentación | 10–30 VDC |
| Industrial | Fanless, TPM 2.0, watchdog, IP30 y montaje DIN opcional |
| Tamaño | Unidad base AE: aproximadamente 100 × 70 × 30 mm |
| Precio | N/A |

Fuentes oficiales:

- [Página de producto Advantech](https://www.advantech.com/en-us/products/1-2mlj9a/uno-2271g-v2/mod_a7b043d4-20e9-4276-ad94-2492f00e110e)
- [Portal oficial de manuales](https://www.advantech.com/en-us/support/details/manual-?id=1-27JYFV8)
- [Ficha UNO-2271G V2 AE y expansiones](https://advdownload.advantech.com/productfileusa/PIS/UNO-2271G%20V2/file/UNO-2271G-V2_DS(020822)20220208162318.pdf)

Limitación: tamaño y ficha corresponden a la unidad AE documentada; no se extrapolan a BE ni a toda revisión futura.

## Matriz breve para la presentación

`Objetivo` significa planeado, no construido o validado.

| Criterio | Nuestro gateway | Siemens IOT2050 M.2 | Moxa UC-2112-LX | Advantech UNO-2271G V2 |
|---|---|---|---|---|
| RS-485 | 2 canales objetivo | 1 COM configurable | 2 COM configurables | Mediante expansión |
| CAN-FD | 1 canal objetivo | No documentado integrado | No documentado | CAN por expansión; CAN-FD no verificado |
| DI/DO industrial | 4 DI de 24 V + 2 DO objetivo | Arduino; requiere adaptación | No documentado | Mediante módulos |
| Ethernet | Principal; segundo y velocidad TBD | 2 × Gigabit | 1 × 100 Mb/s + 1 × Gigabit | 2 × Gigabit |
| Procesamiento / SO | STM32H723VET6 / Zephyr; decidido, no validado | AM6548 / Linux | Cortex-A8 / Moxa Industrial Linux | Intel x86 / Windows o Ubuntu |
| Expansión | Alcance TBD | Arduino y M.2 | microSD | mPCIe y módulos apilables |
| Madurez demostrada | Diseño/requisitos; sin prototipo completo | Producto comercial documentado | Producto comercial documentado | Producto comercial documentado |

## Lectura competitiva honesta

Las soluciones comerciales ofrecen equipos terminados, documentación de instalación, soporte, expansión y especificaciones ambientales. Nuestro proyecto aún no tiene esa madurez, certificaciones ni ecosistema, y mantiene coste, consumo, dimensiones y rendimiento como desconocidos.

El enfoque propio es diferente porque parte de 2 × RS-485, 1 × CAN-FD, 4 DI de 24 V, 2 DO y una electrónica de campo diseñada para ese conjunto. Los beneficios son potenciales: integración directa de esas interfaces, control de protección y testabilidad, y ajuste del procesamiento a la carga que finalmente se valide. No se afirma que el producto sea globalmente superior ni más barato, pequeño, eficiente o robusto.
