# Cierre final del esquemático — Academic Gateway Rev. 1

Fecha: 2026-11-10. Proyecto nativo: `hardware/academic_rev1/Industrial_Gateway_Academic.PrjPcb`
(Altium Designer 26.9.1, puente Electronics AI activo). Base git: `9ff3fdf` + cambios de esta entrega.

## Estado final

**GO FOR PCB TRANSFER**

Verificado en esta sesión contra Altium en vivo (no solo documentos):

| Verificación | Resultado |
|---|---|
| Compilación forzada del proyecto | OK |
| ERC: errores sin suprimir | **0** |
| ERC: "Missing component models" | **0** (antes 33) |
| ERC: "Nets with multiple names" | **0** (CHASSIS separado de GND) |
| Componentes con exactamente 1 footprint actual existente en `Gateway_Academic.PcbLib` | **136 / 136** (lectura de los .SchDoc guardados) |
| Footprints `GW_CAND_*` en uso | **0** |
| Esquema vs PCB1 (comparación de solo lectura) | 136 = 136 componentes |
| Pad térmico U1 (TPS26620) en PCB1 | 5 pads "11" + pin 5 en **EF_RTN** |

Advertencias que quedan (justificadas, no bloqueantes):
- *Nets with no driving source* (15): nets pasivos/divisores sin pin de salida (UVLO, OVP, FB, SENSE, DOx_GATE…). Es el tipo de pin, no una falta de conexión.
- *Nets with possible connection problems* (~33): pines IO del MCU/PHY contra puertos de dirección Input/Output. Cosmético.
- *Off-grid object* (~34): piezas de Power fuera de la grilla. Cosmético.
- 4 errores suprimidos con No-ERC, pines sin uso a propósito: U1.4 SHDN (pull-up interno), U5.1 ModeSelect, U5.26/U5.27 TX_D2/TX_D3 (RMII).

## Correcciones aplicadas (Claude + Codex, sesión 2026-11-09/10)

| Hoja | Elemento | Antes | Después |
|---|---|---|---|
| Ethernet | Power ports GND en C46.1 / C52.1 | Corto CHASSIS–GND | Eliminados; CHASSIS = J2.S1/S2, C46.1, C52.1, R34.2, C65.2 |
| Ethernet | Net label | `CHASIS` | `CHASSIS` |
| Ethernet | C64 | 1 nF suelto | Eliminado |
| Ethernet | R34 | 10 k | RC0603FR-071ML 1 MΩ (Not Fitted) |
| Field_IO | J9 | 1=B, 2=A | 1=A (U6.6), 2=B (U6.7), 3=GND |
| MCU | J3 / J8 | MPN TBD, footprint genérico | Würth 61300611121 / 61300211121, `GW_WRPHD_6X1/2X1_254_WURTH` |
| Power | C66, C67 | — | 2.º C5750X7R2A475K230KA por buck (CIN = 2 × 4,7 µF/100 V por buck) |
| Power | C1, C2 | Modelo PCB duplicado | Un único modelo actual |
| Todas | 33 instancias | Implementación PCB colgada de un parámetro/designador | Reparadas (`evidence/final_closure_rev1/models_repaired_native.json`) |
| Todas | 63 instancias | `GW_CAND_*` | Footprint verificado del fabricante |
| Power | U1 | `GW_DRC0010J_TI_TPS2662` (candidato) | `GW_DRC0010J_TI_TPS2662_EPU` |
| PrjPcb | Rev1_Assembly | 4 Not Fitted | 8 Not Fitted: C11, C20, R6, R9, R34, C65, R35, R36 |

## Footprints / modelos

- 49 footprints en `Gateway_Academic.PcbLib`, 34 en uso. Footprints de uso más frecuente: 0603 KEMET (35), RC0603 Yageo (28), C3225 TDK (8), 0805 KEMET (8), C5750 TDK (5), CL10 Samsung (5).
- A 18 footprints se les agregó contorno (Mechanical 1), courtyard (Mechanical 15, +0,25 mm), serigrafía con marca de pin 1 y cuerpo 3D extruido. El cobre no se modificó.
- **TPS26620 (DRC0010J):** el footprint `..._EPU` tiene el cobre exacto de TI (SLVSDT4F pp. 43–45). Los cuatro dedos del EP se renombraron de 11A–11D a «11», así que todo el EP hereda el pin 11. Comprobado en PCB1: las cinco piezas de cobre están en EF_RTN. Las advertencias de solape que quedan son entre pads del mismo net, a propósito.
- Pin↔pad: todos los pines eléctricos tienen un pad con el mismo designador. Excepción documentada: J2 MP1/MP2 son pads mecánicos.

## Potencia (condensadores)

- **CIN por buck:** 2 × C5750X7R2A475K230KA (4,7 µF/100 V) más 2 × 220 nF/100 V. Según la curva TDK de esta pieza, a 30 V quedan ≥3,5 µF por pieza. Con 10 % de tolerancia y 15 % de temperatura, el par da 5,36 µF efectivos, por encima de los 4,7 µF mínimos (TI SNVSB49D §10.2.1.2.6).
- **COUT:** 4 × C3225X7R1C156M250AB (15 µF/16 V) por riel, 60 µF nominales, sobre el mínimo nominal de 30 µF de TI Table 10-1.
- **CVCC:** C16/C61 = C0805C225K5RACTU (2,2 µF/50 V).
- **NC3:** U2.3 en B3_SW y U3.3 en B5_SW.
- **Realimentación:** 100 k/43,2 k da 3,315 V; 100 k/24,9 k da 5,016 V.
- **PG y CFF:** R6/R9 (pull-up de PG) y C11/C20 (CFF) quedan como posiciones Not Fitted.

## C2

**Montado.** Es el bypass C5750 aguas arriba del TPS, entre VIN_CLAMP y GND, no el CIN de un buck. No está en la lista Not Fitted y el BOM lo marca como REQUIRED.

## TDS3311P.C (D2)

- Pines 4/5/6 a VIN_CLAMP y 1/2/3 a GND.
- DFN 1,6 × 1,6 mm, paso 0,5 mm y lands 0,30 × 0,65 mm según Semtech Rev2.4 pp. 7–9. Coincide con `GW_TDS3311P_SEMTECH`.
- El PDF oficial no se pudo archivar localmente: Semtech solo lo entrega desde su [página de producto](https://www.semtech.com/products/circuit-protection/surgeswitch/tds3311p). No afecta a la transferencia.

## Transferencia a PCB

PCB1.PcbDoc ya contiene los 136 componentes. La transferencia no la ejecutó Claude, y Claude no modificó el PCB en esta sesión. Antes de rutear, el siguiente paso del usuario es correr *Design → Update PCB* y revisar el ECO, para traer cambios de esquema posteriores a esa transferencia, si los hay.

Pendiente no bloqueante para el académico:
- Alturas 3D aproximadas en TB002 y SS3P6L.
- El BOM aún lista el MPN FOJAN de R11/R16/R18/R24/R30. El usuario lo aprobó.
