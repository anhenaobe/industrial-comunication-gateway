# Cierre de ejecución Rev1 — 2026-11-10

**NO-GO — VERIFIED EXTERNAL BLOCKER**

Base comprobada: HEAD 9ff3fdf, rama main. Se conservaron los cambios CAD y firmware preexistentes. No se hizo commit, push, ECO ni edición del PCB. No se reescribieron binarios Altium.

## Recuperación ejecutada

1. `doctor --probe-backends`, fuera del sandbox, reprodujo transport_closed (2fd4da95ec6740f0a8ab71e7fc432321).
2. El arranque de `eda_stdio.py --help` aisló la causa: `Generated script was changed: .../scripts/eda-7edd5178d4b869e7/ElectronicsAI-EDA.PrjScr`.
3. Se preservó con comparación SHA256 el proyecto generado en `tmp/ElectronicsAI-EDA.preserved-*.PrjScr` y junto al original con sufijo `.preserved-*`. El generador oficial reconstruyó exclusivamente ese proyecto de ejecución. No se alteraron fuentes del plugin, configuración de seguridad ni marcadores de propiedad.
4. `doctor --probe-backends` pasó: ready=true, 457 herramientas. Se abrió una sesión nueva del servidor oficial `plugin_runtime.py serve`, conservando sus checkpoints.
5. `app_context` no pudo obtener sesión nativa: `EDA did not answer, but native shutdown is not confirmed`. `app_list_open_dialogs`: PID 1716, blocked=false, cero diálogos.
6. En el IDE se observó Stop deshabilitado y se inició Run. El log registró un ping respondido, seguido de `engine_idle_release`; el coordinador no pudo retomar la sesión. El último acceso visual falló con `no monitor found for window`.
7. `app_detach` fue rechazado antes de despacho por el checkpoint: `Pre-edit checkpoint cannot verify Altium context; edit was not dispatched`. No se eludió esa protección.

**Acción externa necesaria:** restablecer un escritorio Windows interactivo accesible; en el IDE de Altium detener únicamente el script ElectronicsAI si sigue activo, cerrar y reabrir su proyecto generado e iniciar `Dispatcher.pas > StartMCPServer`. Reconectar Electronics AI y comprobar `app_context` con bridge_answering=true y script_version_match=true. Si vuelve a aparecer la negativa de traspaso de sesión, guardar el trabajo y reiniciar Altium normalmente para eliminar la sesión de motor anterior; no borrar manualmente marcadores. El problema restante es la sesión del motor nativo, no una decisión de componentes.

## Resultados independientes completados

- Lectura de las cinco hojas guardadas y jerarquía; 134 componentes. Verificación de cobre/modelos con el lector oficial: 49 footprints en PcbLib y todos los modelos current referencian un footprint existente. Todos los pines eléctricos encuentran un pad del mismo nombre. MP1/MP2 de J2 son pads mecánicos adicionales. Esto no prueba resolución de modelos en Altium: quedan propietarios huérfanos y C1/C2 duplicados.
- R5/R7 = 100k/43,2k y R8/R10 = 100k/24,9k: objetivos típicos de 3,315 V y 5,016 V con referencia de 1 V. Las etiquetas B3_SW y B5_SW son distintas; NC3 y SW12 llevan la etiqueta correspondiente en cada buck. La unión por etiquetas y entre hojas requiere compilación.
- La corrección guardada UVLO/OVP conserva R1.1/R3.2/U1.2 en UVLO y R3.1/R4.1 en la etiqueta OVP; U1.3 tiene OVP. EF_RTN incluye U1.5/11 y R4.2, separado de GND en la extracción geométrica. No es evidencia de compilación.
- C16/C61 ya son C0805C225K5RACTU de 2,2 µF/50 V en VCC de los reguladores; no están sobre 24 V. No necesitan la sustitución por sobretensión descrita en auditorías antiguas.
- **C2: Fitted, conservar.** Es el C5750 de bypass entre entrada TPS y GND, no el CIN de un buck. El proyecto guardado no lo excluye de Rev1_Assembly y `IN_BULK` del BOM es REQUIRED, cantidad 1. La nota heredada que decía C2 DNP queda invalidada. No fue necesario editar la variante para mantenerlo montado.

## Decisión eléctrica de los bancos de potencia

TI SNVSB49D §10.1 exige considerar capacitancia efectiva; §10.2.1.2.6 requiere 4,7 µF mínimos de entrada. La curva local `libraries/sources/academic_freeze/TDK_exact.pdf`, página 2, corresponde al **C5750X7R2A475K230KA**. A 30 V permite una lectura conservadora de 3,5 µF por pieza (curva típica, no garantía). Aplicando 10 % de tolerancia y 15 % de temperatura, dos piezas dan **5,355 µF**, frente a **2,678 µF** con una. La curva ya incluye polarización: no volver a aplicar un factor de bias.

**Configuración seleccionada:** dos C5750X7R2A475K230KA por buck, más los dos bypass 220 nF/100 V existentes por buck; conservar C2 aguas arriba. El BOM ya exige cinco C5750 en total. La captura guardada solo tiene C2/C12/C60: hay que colocar una segunda pieza junto a C12 y otra junto a C60 mediante la sesión nativa recuperada. No se declaran colocadas.

Con corriente de salida límite de 1,5 A y D=5/18, la corriente RMS de entrada aproximada es 0,672 A por banco, o 0,336 A por pieza con reparto igual. Para 3,3/18 es 0,580 A/banco. La curva de calentamiento TDK a 1 MHz cubre corrientes por pieza muy superiores; el margen académico es adecuado, sujeto a colocación de ambos condensadores junto a VIN/PGND. La comprobación de ripple de la placa real pertenece a bring-up.

**Salida:** conservar cuatro C3225X7R1C156M250AB por riel, 60 µF nominales. TI Table 10-1 expresa explícitamente COUT como capacitancia *rated*, con mínimo de 30 µF para 1 MHz y ejemplo nominal de 45 µF; no exige exactamente tres piezas. §10.2.1.2.5 permite aumentar el banco dentro de su límite. Esta decisión no confunde los 60 µF nominales con capacitancia efectiva medida. No se extrajo en esta ejecución una curva exacta de bias de salida: la aceptación usa el criterio de capacitancia nominal expresamente indicado por TI, manteniendo el mismo dieléctrico y tensión de los componentes ya seleccionados; no certifica respuesta transitoria medida.

CVCC conserva la selección académica anterior de 2,2 µF/50 V. Su ficha exacta se leyó; no se inventó una curva de bias ausente ni se convirtió la hipótesis de retención del informe anterior en una medición.

## TDS3311 y TPS

D2 guardado es **TDS3311P.C**, no TDS3011P. Se comprobó su identidad y conexiones: 4/5/6 al nodo de entrada TPS después de D1.K; 1/2/3 a GND. El PDF Semtech Rev2.4 pp7–9 identifica DFN 1,6 × 1,6, paso 0,5 mm y lands 0,30 × 0,65 mm, separación entre centros de filas 1,45 mm: coincide con `GW_TDS3311P_SEMTECH` leído del PcbLib. Máscara +0,025 mm y pasta 1:1 son elecciones del proceso académico. La ficha contempla 33 V de trabajo y clamp máximo de 42 V para el pulso especificado de 35 A; no sustituye protección continua de sobretensión.

Las dos descargas locales llamadas TDS3011P contienen realmente TDS3011P. El portal oficial enlazó una respuesta HTML, que se rechazó como PDF. Se consultó el documento original Semtech alojado por Arrow; su descarga directa se interrumpió por ConnectionResetError, por lo que no se afirma haber archivado un PDF nuevo.

El footprint EPU de U1 ya tiene cinco piezas de cobre llamadas **11**, incluida la central de 1,65 × 2,40 mm y cuatro extensiones; las diez terminales restantes tienen paso de 0,5 mm. Hay ventanas explícitas en Top Paste y expansión negativa para evitar pasta automática sobre EP. Se conserva esta implementación heredada; no se creó otro footprint. La propagación real de EF_RTN y las cuatro advertencias térmicas **no pudieron validarse sin el editor**.

## Verificación nativa

| Prueba | Resultado de esta ejecución |
|---|---|
| Compilación / ERC | No ejecutables: sesión nativa no disponible |
| Missing component models | Conteo nativo no obtenido; no se informa cero |
| Modelos current | Offline: C1/C2 tienen dos; demás instancias uno |
| Pin/pad | Offline: ningún pin eléctrico sin pad del mismo nombre; transferencia no verificada |
| TPS EP / ECO preview | No verificados; ECO no ejecutado |
| Ediciones nativas / modelos reparados | Ninguna: bloqueo antes de despacho |
| Integridad | Solo lecturas de CAD en esta ejecución; no se guardaron/reabrieron hojas ni se regeneraron UID |

Evidencia reproducible local en `tmp/closure_offline/`: `native_saved_state.json`, `library_mapping.json`, `footprints_geometry.json` y extracción/render de las fichas locales. Respuestas y esquemas de la sesión recuperada en `tmp/electronics_session/`.

Fuentes: [TI SNVSB49D](https://www.ti.com/lit/ds/symlink/lmr36015.pdf), [TDK C3225 exacto](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1C156M250AB), [Semtech producto y código de pedido](https://www.semtech.com/products/circuit-protection/surgeswitch/tds3311p), [Semtech Rev2.4](https://static6.arrow.com/aropdfconversion/7cbd31023a55764967a21d3a9d33bd70389c578f/tds3311pc.pdf).
