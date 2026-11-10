# Estado del proyecto — Gateway académico Rev. 1

Fecha de corte: 2026-11-09, archivos nativos guardados hasta las 20:04.

## Cómo se verificó

- Netlist geométrica offline de los `.SchDoc` guardados (Power, MCU, Ethernet,
  Field_IO, TopLevel), leída desde copias fuera del repo. **No es un compilado
  ni un ERC de Altium.** Antes del PCB hay que compilar en Altium y confirmar.
- Hojas de datos locales para los valores citados (`docs/hardware/evidence/`).
- Conteo actual: 127 componentes, 490 pines (Power 42, MCU 21, Ethernet 34,
  Field_IO 30). Incluye 6 componentes aún sin numerar en Field_IO.

## Cerrado desde el informe de Codex (`electrical_closure_rev1.md`)

| ID | Tema | Estado actual |
|---|---|---|
| N01 | Divisor UVLO/OVP del TPS26620 | Correcto en el archivo: R1/R3/R4 a U1.2/U1.3, retorno a `EF_RTN` separado de GND |
| N02 | C16 de 16 V sobre 24 V | Resuelto. En 24V solo quedan C12 y C60 (TDK 4,7 µF/100 V) y los 220 nF de 100 V |
| N03 | R21/R22 cruzando el aislamiento | Resuelto. R21.2/R22.2 van al borne de entradas; DI1/DI2 solo unen U8 con el MCU. Ningún net mezcla campo y lógica |
| N04 | Salidas digitales | Implementado: U9 eliminado; por canal NPN MMBT3904 + PMOS DMP2035U, base 4,7 k, gate 100 Ω, pull-up gate 4,7 k, pull-down 2,49 k en IN; BSP75N con S y S_TAB a GND |
| N05 | NC3 y CVCC de los buck | Resuelto. U2.3→`B3_SW`, U3.3→`B5_SW`; CVCC C16/C61 = 2,2 µF/50 V |
| N07 | C30 suelto | Resuelto. C30 en 3.3V; se agregaron C62 (1 µF) y C63 (100 nF) |
| N10 | ESD sin numerar | Resuelto (D3) |
| N11 | PG de los buck hacia 24 V | Resuelto con variante `Rev1_Assembly`: R6, R9, C11, C20 = Not Fitted |
| — | Driver de las salidas: margen de 4,5 V | Peor caso ≈ 4,8 V en BSP75N.IN (V_PROT ≥ 4,5 V). Manejo a 5 V es el correcto: con VIN = 10 V la protección de cortocircuito solo cubre VDS ≤ 20 V |

Borne de entradas TB002-500-03BE: pin 1 = R21.2, pin 2 = R22.2, pin 3 = `FIELD_COM`.
Bornes de salidas TB002-500-02BE: alimentación (`DO_EXT_PLUS`/GND), DO1
(`DO_EXT_PLUS`/`DO1_DRAIN`), DO2 (`DO_EXT_PLUS`/`DO2_DRAIN`). Todos enlazados a los
footprints verificados `GW_TB002_500_2P/3P_SAMESKY`.

## Pendiente

### Eléctrico
- **N06 Ethernet:** C46/C52 (red Bob Smith) siguen a GND y el blindaje del RJ45
  (J2.S1/S2) está flotando. Falta definir el retorno a CHASSIS.
- **N08 buses:** RS-485 A/B (U6.6/7) y CANH/CANL (U7.6/7) no llegan a ningún conector.
- **CIN de los buck:** hay 3 TDK C5750 4,7 µF (C2, C12, C60) contra 5 previstos en
  `datasheet_inventory_rev1.csv`. Confirmar ≥ 4,7 µF efectivos por buck a 24 V.
- **Salida de los buck:** 4 × 15 µF por riel (C7 y C21 agregados) frente a 3 de la
  tabla 10-1 de TI. Probablemente aceptable; confirmar.
- **Carga de las salidas:** diseñar para ≤ 0,5 A por canal (BSP75N, I_LIM mín. 0,7 A a VIN = 5 V).

### CAD / bibliotecas
- Numerar los 6 componentes `R?` / `J?` de Field_IO.
- Sin footprint: C7, C12, C16, C21, C60, C61 y las instancias listadas en N12.
- J1 apunta a `CUI_TB002-500-02BE`, que no existe en el PcbLib; usar `GW_TB002_500_2P_SAMESKY`.
- SW1 y J3 con MPN "TBD".
- R24/R30 siguen como FOJAN 5 %; la guía pide RC0603FR-0710KL (solo BOM).
- Mapeo del pad térmico del TPS26620 (EP con 5 pads en `EF_RTN`) sin cerrar.
- 64 instancias aún enlazadas a footprints genéricos `GW_CAND_*`.

### Proyecto / documentación
- Sin compilado ni ERC después de los cambios. `PrjPcbStructure` desactualizado.
- `Power.SchDoc` no tiene símbolo de hoja en TopLevel; el significado de
  `HierarchyMode=0` no está verificado. Confirmar en Altium el alcance de nets.
- La hoja de datos local del TDS3311P.C es en realidad una página HTML.
- `datasheet_inventory_closure.md` marca "No local PDF" para TPD4E05U06,
  MMBT3904, DMP2035U y XAL4030/4040, aunque sí están en `libraries/sources/`.
- `PCB1.PcbDoc` sigue vacío.

## Siguientes pasos

1. Numerar (Tools → Annotate) y compilar; revisar que DI1/DI2, `DOx_GATE` y
   `DO_EXT_PLUS` aparezcan como aquí.
2. Retorno a CHASSIS en Ethernet y conectores de RS-485 y CAN.
3. ERC completo.
4. Footprints faltantes, J1, pad térmico del TPS y MPN de SW1/J3.
5. ECO hacia `PCB1.PcbDoc`.
