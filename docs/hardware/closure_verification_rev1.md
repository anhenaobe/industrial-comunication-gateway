# Cierre nativo Academic Gateway Rev1

Fecha: 2026-11-10. Base git: 9ff3fdf. No se hizo commit ni push.

## Resultado actual

Esquema reparado, guardado y compilado en Altium AD26. **Pendiente exclusivamente la interacción del diálogo ECO** para terminar la validación de transferencia: el plugin abrió la previsión, pero su checkpoint rechazó pulsar Validate Changes con el modal abierto. No se ejecutó ECO. El PCB conserva su SHA256 previo.

## Cambios efectivos

| Hoja | Componente | Corrección |
|---|---|---|
| Power | C1, C2, C7, C12, C16, C17, C21, C60, C61, D1, R1–R4, U1 | Recolocados desde símbolos con implementación reconstruida; parámetros, posición, orientación y UID restaurados y verificados |
| Ethernet | C46, C52, C65, R12, R14, R17, R19 | Misma reparación de implementación, preservando conexiones y variante por UID |
| Field_IO | R21, R22 | Misma reparación sin modificar los nodos de entrada aislados |
| Power | C66, C67 | Dos C5750X7R2A475K230KA añadidos, uno en paralelo con C12 y otro con C60, entre 24V y GND |

No se sustituyeron MPN existentes. Se mantienen FOJAN, R36, arquitectura y asignaciones MCU. C16/C61 ya eran 2.2uF/50V en VCC de los bucks; no correspondía tratarlos como CIN de 16V sobre 24V. Se conservaron los drivers MMBT3904/DMP2035 y BSP75N; U9 está ausente.

Se creó `libraries/Gateway_Closure.SchLib` con 13 símbolos copiados sin alterar sus pines, para regenerar las implementaciones mediante el escritor oficial de Electronics AI. Se añadió al proyecto y se usó para las 24 instancias reparadas y los dos CIN nuevos. Después se limpiaron también los 13 enlaces equivalentes de Gateway_Academic.SchLib, con esa biblioteca cerrada; se conservaron todos sus símbolos y pines. No se generaron footprints nuevos en esta ejecución.

## Evidencia nativa

- 136 componentes, exactamente un modelo PCB current en cada instancia, incluidos los DNP.
- Cero Missing component models y cero errores ERC sin suprimir.
- Comparación del compilado antes/después de reparar modelos: ninguna conexión modificada.
- Tras C66/C67: todas las conexiones anteriores conservadas; ambos nuevos capacitores conectados a 24V/GND.
- Los 134 UID, posiciones y orientaciones originales se conservaron. No hay designadores duplicados o pendientes.
- Todos los pines eléctricos tienen pad homónimo en la PcbLib; MP1/MP2 de J2 son mecánicos.
- CHASSIS, FIELD_COM, EF_RTN y GND permanecen separados según la arquitectura. U1.5/11 están en EF_RTN.
- U2.3/12 están juntos en B3_SW; U3.3/12 en B5_SW, sin unir ambos nodos. Feedback 100k/43.2k y 100k/24.9k; R6/R9 Not Fitted.
- RS485: U6.6→J9.1/D4.2, U6.7→J9.2/D4.1; J9.3/D4.3→GND. CAN: U7.7→J10.1, U7.6→J10.2, J10.3→GND.
- Entradas ISO1212: R21/R22 al borne J4, sus retornos a FIELD_COM; salidas U8.4/5 al MCU. SUB1/SUB2 separados y flotantes.
- Driver DO: NPN activa PMOS desde 5V; gate pull-up y pull-down de entrada BSP garantizan OFF sin excitación MCU. Las cargas vuelven por GND y usan DO_EXT_PLUS separado de 24V.
- SWD, NRST y BOOT presentes en J3/J8. C2 se confirmó Fitted en la matriz nativa.

## Capacitores y montaje

Configuración final: C2 de bypass TPS; C12+C66 y C60+C67 como CIN de cada buck; dos 220nF/100V por buck; C16/C61 2.2uF/50V CVCC; cuatro C3225 de 15uF/16V por salida. La decisión de entrada usa la curva exacta TDK archivada: lectura conservadora 3.5uF a 30V por pieza, por 0.9 de tolerancia y 0.85 de temperatura: **5.355uF/banco**, superior al mínimo efectivo de 4.7uF de TI. El RMS conservador a 1.5A de salida es 0.672A/banco a 5V/18V, 0.336A/pieza con reparto igual; compatible con la curva de calentamiento TDK a 1MHz. Son estimaciones de diseño, no mediciones de laboratorio.

COUT suma 60uF nominales por riel; se conserva la selección de 16V X7R. TI Table10-1 expresa los valores de COUT como rated capacitance; sus tres piezas son un ejemplo, no un máximo de población. No se presenta la capacitancia nominal como una medición bajo polarización. El CVCC mantiene la selección académica previa, con margen sobre 1uF usando su hipótesis conservadora de retención; no se inventó una curva de fabricante ausente. El load-step y ripple de la placa montada pertenecen al bring-up.

La matriz Rev1_Assembly tiene 128 posiciones Fitted y ocho Not Fitted: C11, C20, R6, R9, R34, C65, R35, R36. C2, C66 y C67 están Fitted. El BOM por designador es `assembly_bom_rev1.csv`; final_bom/passive_bom/mapping se reconciliaron para FOJAN, cuatro COUT y EPU de U1.

## TDS y pad térmico

D2 guardado es TDS3311P.C. Pinout y land de la ficha Semtech Rev2.4 pp7–9 coinciden con el footprint: seis lands de 0.30×0.65mm, paso 0.5mm, centros de filas separados 1.45mm; 1/2/3→GND y 4/5/6→entrada del TPS después de D1. El original Semtech se consultó online; las dos descargas locales llamadas TDS3011P contienen el modelo 3011, no el 3311. No se sustituyó D2.

U1 usa GW_DRC0010J_TI_TPS2662_EPU: cobre EP central y cuatro extensiones, todos con designador 11, coherente con el pin11 compilado en EF_RTN. Hay ventanas explícitas de pasta. Las cuatro superposiciones de cobre describen la unión intencional del mismo pad, no terminales 11A–11D sin mapear. Altium admite varios pads con el mismo designador. La validación de la previsión ECO aún requiere la interacción del diálogo; no se afirma una transferencia ya ejecutada ni cobre aplicado al PCB.

## ERC restante, sin nuevas supresiones

| Cantidad | Categoría |
|---|---|
| 4 | Nets containing floating input pins |
| 19 | Nets with no driving source |
| 33 | Nets with possible connection problems |
| 36 | Off-grid object |
| 4 | Unconnected objects in net |

Cuatro errores están individualmente suprimidos desde la configuración heredada (U1.4 y U5.1/26/27). Los 92 warnings se justifican por objeto en `evidence/final_closure_rev1/erc_dispositions.csv`: redes analógicas/pasivas, tipos IO/dirección de puerto y geometría fuera de grid con continuidad compilada. No se desactivó ninguna categoría ERC para obtener el resultado.

Fuentes: TI SNVSB49D §§10.1/10.2.1.2.5–6 y Table10-1; TDK_exact.pdf p2; fuentes de pinout y land previamente archivadas en libraries/sources y cad_library_mapping.csv. [Semtech Rev2.4](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf). [Altium: varios pads con el mismo designador](https://www.altium.com/documentation/altium-designer/pcb/understanding-connectivity).
