# Capacitor15?F/100V y normalizaci?n de pines R/C

Alcance final aclarado por el usuario: s?lo resistencias y capacitores. Las dem?s familias se conservaron exactamente como en el respaldo. La primera operaci?n amplia fue cancelada y restaurada antes de preparar el resultado final.

## Resultado

- Biblioteca: `hardware/academic_rev1/libraries/Gateway_Academic.SchLib`,67 s?mbolos.
- Pines R/C uniformes de8 unidades de s?mbolo (80mil):27 modelos modificados,8 R/C ya correctos sin cambio. S?lo cambi? `pins[].length`; identidades, MPNs, par?metros, tipos/n?meros de pin, origen del s?mbolo, gr?ficos y asociaciones de footprint permanecen iguales.
- Otros31 modelos id?nticos al respaldo, incluidos MCU, PHY, eFuses, transistores, inductores, diodos y conectores. GUID de biblioteca preservado.
- Nuevo s?mbolo `CC2220X7S100V156MN`,fabricanteTORCH,LCSC C54157533,capacitor cer?mico no polar15?F/100V,2220,toleranciaM=20%; terminales pasivos1/2. No selecci?n/reemplazo autom?tico de BOM.

## Evidencia del nuevo componente

[PDF local](../../hardware/academic_rev1/libraries/sources/cap15uf100v/C54157533.pdf),copia del archivo de Descargas;[identidad exacta en LCSC](https://www.lcsc.com/product-detail/C54157533.html). El PDF escaneado de familiaTORCH contiene en p1 los c?digos156=15?F,M=20%,100V y las dimensiones2220:5.70?0.50?5.00?0.50mm,Tmax4.20mm. No demuestra la altura exacta del MPN. S?lo enumeraCG/X7R/X5R; no cubre expl?citamenteX7S ni garantiza capacitancia efectiva bajo polarizaci?n. No proporciona land pattern recomendado. El s?mbolo registra estas limitaciones y **no tiene footprint asignado**; no se reutiliz? un footprintTDK s?lo por ser2220. Estado: s?mbolo listo,huella pendiente,aplicaci?n provisional.

## Uso y validaci?n

Al acortar un pin manteniendo su punto de uni?n al cuerpo, su extremo el?ctrico se acerca al cuerpo. **No se actualizaron instancias de esquem?tico**. No aplicar una actualizaci?n masiva sin revisar conexiones. Los extremos pueden quedar fuera de la rejilla100mil; usar rejilla10mil para estos s?mbolos (las coordenadas permanecen enteras en unidades10mil). Los trazos gr?ficos internos de los pasivos no fueron redise?ados; la propiedad de longitud de todos sus pines es la misma.

Lectura independiente del archivo final:67 s?mbolos;validaci?n estructural0 errores/0 avisos. Los27 cambios son exclusivamente longitudes de54 pines. Los otros39 s?mbolos originales no tienen diferencias; el nuevo capacitor agrega2 pines. No se compil? IntLib ni se ejecut?ERC/DRC. PcbLib,proyecto,BOM y bibliotecas docentes no se editaron. Comparaci?n de hashes y posibles guardados externos: [registro](evidence/pin_length_normalization/hash_changes.json). Respaldo y SHA256: [manifiesto](evidence/pin_length_normalization/backups.json). [Vista de s?mbolos guardados](evidence/pin_length_normalization/preview.svg).

## S?mbolos modificados

- `GW_C0603C104K5RACTU_dc5e12a5`
- `GW_C0805C475K4RACTU_82374e08`
- `GW_CL10A105KB8NNNC_c3932faa`
- `GW_C0603C225K8RACTU_46503424`
- `GW_C0603C103K1RACTU_97f3ee33`
- `GW_CL21A106KAYNNNE_c6e24382`
- `GW_C0603C202J5GACTU_fa733a70`
- `GW_C5750X7R2A475K230KA_5f18f946`
- `GW_C0805C224K1RACTU_e16e52b8`
- `GW_C3225X7R1C156M250AB_bb412b42`
- `GW_C0603C200J5GACTU_c75b007a`
- `MM204F1K00TKRTR3K0`
- `RC0603FR-0710KL`
- `RC0603FR-0762KL`
- `RC0603FR-0715KL`
- `C5750X7R2A475K230KA`
- `C0805C224K1RACTU`
- `C0805C225K5RACTU`
- `C0603C680J5GACTU`
- `C3225X7R1C156M250AB`
- `RC0603FR-0713K3L`
- `RC0603FR-07768KL`
- `RC0603FR-0733K2L`
- `RC0603FR-0730K1L`
- `C0603C103K1RACTU`
- `CRCW080575R0FKEA`
- `C1206C102KGRACAUTO`
