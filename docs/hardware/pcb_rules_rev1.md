# Reglas de diseño PCB — Rev1 académica (`hardware/academic_rev1/PCB1.PcbDoc`)

Fecha: 2026-11-10. Alcance: solo reglas y clases de red. No se movieron componentes ni se ruteó nada.
Entradas reutilizadas: `pcb_rules_proposal.csv`, `pcb_design_rules_audit.md`.
Copia previa del PcbDoc (fuera del repo): scratchpad de la sesión `PCB1.before_rules.PcbDoc`.

Placa: 2 capas (Top/Bottom), cobre 1 oz (1.378 mil), 152.4 × 101.6 mm, sin datos de dieléctrico en el stack.

## 1. Valores JLCPCB usados

Fuente: https://jlcpcb.com/capabilities/pcb-capabilities (consultada 2026-11-10).

| Parámetro | JLC (2 capas, 1 oz) | Usado en la regla |
|---|---|---|
| Ancho / separación mín. | 0.10 / 0.10 mm | 0.15 mm ancho mín., 0.20 mm separación general |
| Vía: taladro / diámetro mín. | 0.15 (pref. ≥ 0.2) / 0.25 mm | 0.3 / 0.6 mm (pendiente manual, ver §3.3) |
| Taladro PTH | 0.15 – 6.3 mm | HoleSize 0.203 – 6.299 mm |
| Anillo anular PTH | rec. ≥ 0.25, mín. 0.18 mm | 0.15 mm vía / 0.25 mm pad (manual) |
| Agujero–agujero, pads de distintas redes | 0.45 mm | 0.45 mm |
| Cobre–borde | 0.2 mm fresado, 0.4 mm V-score | 0.4 mm (manual) |
| Puente de máscara | 0.10 mm (verde) | 0.10 mm (manual; hoy 0.254) |
| Expansión de máscara | 1:1 | 0 mm (ya estaba) |
| Serigrafía–pad | 0.15 mm | 0.15 mm (manual; hoy 0.254) |
| Línea / altura de serigrafía | ≥ 0.15 / ≥ 1.0 mm | no verificable por DRC |
| FR-4 εr | 4.5 | 4.5 |

## 2. Corriente y ancho de pista

IPC-2221, capa externa (k = 0.048), 1 oz, ΔT = 10 °C, margen 1.5× sobre la corriente.
Vías: barril de 0.3 mm con 18 µm de cobre ≈ 0.71 A; barril de 0.4 mm ≈ 0.87 A (k interno, conservador).

| Clase / red | I nominal | I diseño (×1.5) | Capa | Ancho requerido | Ancho elegido (pref.) | Vías por cambio de capa |
|---|---|---|---|---|---|---|
| PWR_24V (F1 2 A) | 2.0 A | 3.0 A | Top/Bottom | 1.37 mm | **1.5 mm** | 5 × 0.3 mm o 4 × 0.4 mm |
| BUCK_SW (B3_SW, B5_SW) | 1.5 A | 2.25 A | Top | 0.92 mm | **1.0 mm** | evitar vías en el nodo SW (4 si es inevitable) |
| PWR_3V3 / PWR_5V | 1.5 A | 2.25 A | Top/Bottom | 0.92 mm | **1.0 mm** | 4 × 0.3 mm o 3 × 0.4 mm |
| DO1_DRAIN / DO2_DRAIN | 0.7 A | 1.05 A | Top/Bottom | 0.32 mm | **1.0 mm** | 2 × 0.3 mm |
| DO_EXT_PLUS (2 canales) | 1.4 A | 2.1 A | Top/Bottom | 0.84 mm | **1.0 mm** | 3 × 0.3 mm |
| ETH_DIFF | señal | — | Top | — | 0.6 mm (impedancia) | — |
| Resto (señal) | < 0.1 A | — | — | — | 0.2 mm | 1 × 0.3 mm |

El mínimo de 0.3 mm en las clases de potencia solo sirve para el estrechamiento en pines de paso fino. El ancho de corriente debe recuperarse a menos de unos 2 mm del pad.

## 3. Reglas

### 3.1 Clases de red y pares diferenciales

| Clase | Redes |
|---|---|
| PWR_24V | NetF1_1, NetD1_1, NetC1_2, 24V |
| PWR_3V3 | 3.3V |
| PWR_5V | 5V |
| BUCK_SW | B3_SW, B5_SW |
| DO_PWR | DO_EXT_PLUS, DO1_DRAIN, DO2_DRAIN |
| ETH_DIFF | MDI_TXP, MDI_TXN, MDI_RXP, MDI_RXN |
| CHASSIS | CHASSIS |
| FIELD_ISO | FIELD_COM, SENSE1, SENSE2, NetR20_1, NetR23_1, NetJ4_1, NetJ4_2 |

Pares diferenciales: MDI_TX (MDI_TXP/TXN) y MDI_RX (MDI_RXP/RXN).

### 3.2 Reglas aplicadas en el PcbDoc (verificadas por relectura)

| Regla | Ámbito 1 / ámbito 2 | Valor | Prioridad |
|---|---|---|---|
| CLR_FIELD_ISO | InNetClass('FIELD_ISO') / (Not InNetClass('FIELD_ISO')) And (Not InComponent('U8')) | 3.7 mm | 1 |
| CLR_CHASSIS_GND | InNetClass('CHASSIS') / InNet('GND') | 1.0 mm | 2 |
| Clearance_FinePitch (original, recreada sin cambios) | U4, U3, U2, U8, D3, U5 / All | 0.15 mm | 3 |
| CLR_PWR_24V | InNetClass('PWR_24V') / All | 0.3 mm | 4 |
| CLR_DO_PWR | InNetClass('DO_PWR') / All | 0.3 mm | 5 |
| Clearance (general) | All / All | 0.2 mm | 6 |
| W_ETH_DIFF | InNetClass('ETH_DIFF') | 0.25 / 0.6 / 0.8 mm | 1 |
| W_DO_PWR | InNetClass('DO_PWR') | 0.3 / 1.0 / 3.0 mm | 2 |
| W_PWR_5V | InNetClass('PWR_5V') | 0.3 / 1.0 / 3.0 mm | 3 |
| W_PWR_3V3 | InNetClass('PWR_3V3') | 0.3 / 1.0 / 3.0 mm | 4 |
| W_BUCK_SW | InNetClass('BUCK_SW') | 0.3 / 1.0 / 2.0 mm | 5 |
| W_PWR_24V | InNetClass('PWR_24V') | 0.3 / 1.5 / 3.0 mm | 6 |
| Width (por defecto) | All | 0.152 / 0.203 / 2.007 mm | 7 |
| DP_ETH_DIFF | IsDifferentialPair | separación 0.15 / 0.15 / 0.25 mm; ancho 0.25 / 0.6 / 0.8 mm; desacople máx. 12.7 mm | 1 (DiffPairsRouting original pasa a 2) |
| HoleSize | All | 0.203 – 6.299 mm | 1 |
| HoleToHoleClearance | All / All | 0.45 mm | 1 |
| ComponentClearance | All / All | 0.254 mm (sin cambios) | 1 |

Notas:
- Los anchos van en mil enteros en el puente, así que 0.15 / 0.2 / 2.0 mm quedan como 0.152 / 0.203 / 2.007 mm.
- Impedancia ETH: 0.6 mm de ancho con 0.15 mm de separación sobre h ≈ 1.53 mm da unos 116 Ω diferenciales (fórmula cerrada IPC-2141/Wadell, ±10 %). Un par de 100 Ω exige unos 0.9–1.0 mm de ancho, lo que no es práctico junto al QFN-32 de 0.5 mm de U5. Es la geometría más cercana practicable. Para 100 Ω reales hacen falta 4 capas (referencia a ~0.2 mm).

### 3.3 Reglas pendientes de introducir a mano (Rules and Constraints Editor)

El puente de Electronics AI no puede crear o escribir estos tipos de regla en AD26: vía, anillo, borde, máscara, serigrafía y conexión a polígono. Hay que introducirlos a mano.

| Regla | Valor objetivo |
|---|---|
| RoutingVias (All) | taladro 0.2 / 0.3 / 0.5 mm, diámetro 0.45 / 0.6 / 1.0 mm (hoy 0.711 / 1.27 mm) |
| RV_POWER (nueva; PWR_24V, PWR_3V3, PWR_5V, DO_PWR) | taladro 0.4 mm, diámetro 0.8 mm |
| MinimumAnnularRing (nueva) | 0.15 mm |
| BoardOutlineClearance (nueva) | 0.4 mm |
| MinimumSolderMaskSliver | 0.10 mm (hoy 0.254) |
| SilkToSolderMaskClearance | 0.15 mm (hoy 0.254) |
| SilkToSilkClearance | 0.15 mm (hoy 0.254) |
| PolygonConnect (All) | relieve térmico, conductor 0.254 mm, 4 radios, separación 0.254 mm (ya estaba) |
| PC_DIRECT (nueva, prioridad mayor) | conexión directa para los pads U1-11 (RTN_EP), U2-1/11 y U3-1/11 (PGND), U10-S_TAB, U11-S_TAB |
| Clearance (todas) | confirmar que está marcado "Ignore pad to pad clearances within a footprint" |

## 4. Supuestos

1. Cobre exterior de 1 oz (confirmado en el stack). FR-4 de 1.6 mm, h ≈ 1.53 mm, εr = 4.5 y metalizado de vía de 18 µm, todo supuesto.
2. Corriente de PWR_24V = fusible F1 (Littelfuse 0451002.MRL, 2 A). BUCK_SW, 3V3 y 5V = 1.5 A, la capacidad del LMR36015. DO: 0.7 A por canal; DO_EXT_PLUS se dimensiona para los 2 canales a la vez.
3. FIELD_ISO usa 3.7 mm, el CLR/CPG del ISO1212 DBQ-16 (TI SLLSEY7G, §5.6, p. 7), en lugar de los 2.0 mm pedidos. Se excluye el cuerpo de U8: su barrera la fija el encapsulado, y los pads SUB 12/13 son NC sin red en el PCB.
4. U2 y U3 (RNX0012A) no tienen EP, así que la conexión directa se aplica a los pines PGND 1/11.
5. U1 no está en Clearance_FinePitch (regla original sin tocar). Si sus pines de paso fino violan la separación de 0.3 mm de PWR_24V, la solución es añadir U1 a esa regla.
6. Máscara verde y sin V-score; aun así se usa 0.4 mm de cobre a borde por conservadurismo.
7. EF_RTN y GND quedan sin clase y se asume que se resolverán con pour.
8. La pista de serigrafía de 0.15 mm y el texto de 1.0 mm no son comprobables por DRC; quedan como recomendación.

## 5. DRC (una sola ejecución, 2026-11-10 22:42)

Informe: `hardware/academic_rev1/Project Outputs for Industrial_Gateway_Academic/Design Rule Check - PCB1.drc`.

**Cobertura incompleta.** Altium detuvo el DRC al llegar a su límite de 500 violaciones ("More than 500 violations detected, DRC was stopped"). Además, el informe da 0 en Un-Routed Net, pero las estadísticas de la placa muestran 335 conexiones sin rutear. El resultado no es una pasada limpia.

| Regla | Violaciones |
|---|---|
| Las 6 de clearance (FIELD_ISO, CHASSIS_GND, FinePitch, PWR_24V, DO_PWR, general) | 0 (la placa casi no tiene cobre ruteado: solo se comparan pads con pads) |
| Short-Circuit | 0 |
| Las 7 de ancho | 0 (no hay pistas de cobre) |
| HoleSize, HoleToHole | 0 |
| MinimumSolderMaskSliver (0.254 mm) | 0 |
| **SilkToSolderMaskClearance (0.254 mm)** | **≥ 500 (tope)** |
| SilkToSilk, NetAntennae, Height | 0 (no fiable por la parada) |

Desglose de las 500 de serigrafía a máscara:
- 191 están entre 0.15 y 0.254 mm. Desaparecen al poner el valor de JLC de 0.15 mm (§3.3).
- 92 están por debajo de 0.15 mm.
- 217 son colisiones: 175 de contorno de footprint sobre el pad y 42 de designador sobre el pad.
- Más afectados: U5 (37), U4 (33), C13, C52, R15, C46, C58, C61, R7, C50.

No se encontraron errores de definición de reglas que corregir. El valor de serigrafía a máscara está desfasado respecto a JLC, pero no se pudo escribir por el puente (§3.3).

### Conflictos de colocación / footprint (no corregidos)

1. **Pads SMT taladrados** (aviso del DRC). Los conectores J1, J2 (incluidos S1/S2/MP1/MP2), J3, J4, J5, J6, J7, J8, J9 y J10 tienen pads con taladro definidos en Top Layer en vez de Multi-Layer. Así no habría cobre ni anillo en Bottom en ninguno de los conectores de agujero pasante. Hay que corregir los footprints antes de rutear.
2. **Serigrafía sobre pads**: hay 175 contornos de footprint que cortan pads. Es un problema de librería, sobre todo en U5, U4 y en los pasivos 0603/0805; JLC recorta la serigrafía, pero conviene limpiarlo. Hay además 42 designadores sobre pads, que se arreglan moviendo texto, no componentes.
3. **Pendiente de verificar al rutear**: separación de 0.3 mm en los pines de U1 (supuesto 5), y separación de 1 mm entre CHASSIS y GND en el entorno de C46, C52, C65, R34 y J2-S1/S2.
4. **Siguiente DRC**: aplicar §3.3, subir el límite de violaciones del DRC (Tools > Design Rule Check > Stop when … violations found) y activar la comprobación de redes sin rutear para tener cobertura completa.
