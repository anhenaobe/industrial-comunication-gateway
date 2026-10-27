# PoC M0/M1 — NUCLEO-F429ZI + Zephyr

Aplicación convencional Zephyr, versión 0.1.0, para **NUCLEO-F429ZI / STM32F429ZIT6**.
El producto Rev. A conserva **STM32H723VET6** y su PHY DP83826I. Esta placa PoC
utiliza su Ethernet de a bordo; no requiere hardware Ethernet adicional.

## Alcance y organización

- `src/main.c`: inicialización y coordinación en un único bucle de aplicación.
- `src/diagnostics.c`: identificación, uptime por consola y LED `led0` del DTS.
- `src/network.c`: configuración IPv4, estado del enlace, socket y heartbeat UDP.
- `Kconfig`: destino, puerto, intervalo y parámetros estáticos del banco.
- `prj.conf`: DHCP por defecto, **destino vacío = heartbeat UDP deshabilitado**.
- `static.conf`: ejemplo explícito para un enlace aislado con el PC.

Zephyr administra sus propios contextos de red y logging. No hay un hilo por
módulo. No se implementan UART de datos, parser, CRC ni router todavía: se añadirán
como módulos separados, sin registros STM32 en la lógica de aplicación. La
arquitectura documental anterior que menciona NUCLEO-H723ZG se conserva como
antecedente; la decisión de banco de esta iteración la sustituye solo para la PoC.

No hay espera de enlace o lease DHCP en `main`. Se consulta estado cada 100 ms;
sin red continúa el diagnóstico de M0. Se cierra el socket al perder disponibilidad
o cambiar IPv4 y se reintenta al recuperar red. Envíos con `ZSOCK_MSG_DONTWAIT`
y cola TX Zephyr habilitada; no se espera recepción ni ACK. Los mensajes de
enlace son estados observados por sondeo, no un registro exhaustivo de eventos.

## Hardware y conexiones

1. NUCLEO-F429ZI, cable USB de datos al conector **ST-LINK USB CN1**, PC y cable
   Ethernet al **RJ45 CN14**. Usar la alimentación USB prevista por la placa.
2. Comprobar la configuración física de fábrica conforme a UM1974: Ethernet
   requiere **JP6 y JP7 ON**. No modificar puentes sin contrastar revisión de placa.
3. USART3, **PD8 TX / PD9 RX**, está reservado para ST-LINK VCP: **115200, 8N1**,
   sin control de flujo. No compartir esta UART con RS-485.
4. Zephyr usa `led0` (LD1 verde) para actividad, si está disponible. El LED alterna
   cada segundo, incluso sin Ethernet; su disponibilidad no decide el éxito UDP.

El DTS instalado utiliza **168 MHz**, aunque el STM32F429 admite hasta 180 MHz.
No se modifica su configuración de reloj. El PHY de esta placa no se identifica
con el DP83826I del producto.

## Entorno local y compilación reproducible

Entorno inspeccionado: Windows nativo, sin WSL instalado. Se reutiliza
`%USERPROFILE%\.platformio\packages`: Zephyr **4.3.0** (paquete **3.40300.0**),
GNU Arm Embedded **12.3.1**, DTC **1.4.7** y OpenOCD **0.12.0**. No se encontró
Zephyr SDK ni STM32CubeProgrammer en PATH o en la ubicación estándar inspeccionada;
se usa `gnuarmemb`, no se necesita instalar el SDK para esta compilación.

Se preparó un entorno Python independiente en `C:\dev\tools\gateway-zephyr-venv`
con Python **3.14.4**, west **1.5.0**, CMake **4.4.4**, Ninja **1.13.2** y las
dependencias de generación DTS/Kconfig. No se altera ningún proyecto PlatformIO.
Solo si hay que reconstruir ese entorno, con acceso a PyPI:

```powershell
& C:\dev\tools\python\python.exe -m venv C:\dev\tools\gateway-zephyr-venv
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe -m pip install west==1.5.0 cmake==4.4.4 ninja==1.13.2 PyYAML==6.0.3 pykwalify==1.8.0 jsonschema==4.26.0 packaging==26.3 pyelftools==0.33 pyserial==3.5 intelhex==2.3.0
```

Desde la raíz del repositorio:

```powershell
# DHCP, sin destino UDP seleccionado: permite comenzar con M0.
& .\firmware\poc\build.ps1 -Profile dhcp
# Ethernet estática para el banco aislado descrito abajo.
& .\firmware\poc\build.ps1 -Profile static
```

El script acepta `-PackageRoot` y `-PythonEnv` si las ubicaciones son diferentes.
Invoca CMake/Ninja con `BOARD=nucleo_f429zi/stm32f429xx`, los módulos CMSIS 6 y HAL
STM32 ya instalados, `ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb` y caché dentro del build.
Los directorios `build-dhcp` / `build-static` están ignorados por Git. Allí quedan
`zephyr/zephyr.elf`, `zephyr.hex`, `zephyr.bin`, `zephyr.map`, `zephyr.dts` y `.config`.
No se necesita overlay: consola, LED, USART6 y MAC/MDIO ya figuran en el DTS oficial.

En un **workspace west convencional ya preparado**, con Zephyr 4.3.0 y sus
módulos correspondientes, la misma aplicación admite:

```powershell
west build -b nucleo_f429zi/stm32f429xx firmware/poc -d firmware/poc/build-west-dhcp -p always
west build -b nucleo_f429zi/stm32f429xx firmware/poc -d firmware/poc/build-west-static -p always -- -DEXTRA_CONF_FILE=static.conf
```

Esos comandos west son una alternativa, no el método local ejecutado: el paquete
PlatformIO no es un workspace west. Instalar `west` no crea ese workspace.

## IPv4 y receptor

**Conexión directa aislada:** configurar manualmente la NIC Ethernet del PC como
`192.0.2.1/24`, sin gateway, y compilar `-Profile static`. La placa utiliza
`192.0.2.2/24`, gateway `0.0.0.0`, destino `192.0.2.1:4242`. Son valores de ejemplo
para este banco, no una IP detectada del PC ni una arquitectura de producción.
Aplicar ese perfil solo después de preparar esa red aislada.

```powershell
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe scripts/poc_udp_receiver.py --bind 192.0.2.1 --port 4242
```

**LAN con DHCP:** conectar PC y placa a una LAN autorizada con servidor DHCP;
averiguar la IPv4 real de la NIC del PC (`ipconfig`). Crear `firmware/poc/pc.conf`
(ignorado) con el destino verificado. Sustituir el marcador por una IP real:

```ini
CONFIG_POC_DEST_IPV4="IP_REAL_DEL_PC"
CONFIG_POC_UDP_PORT=4242
CONFIG_POC_SEND_INTERVAL_MS=2000
```

```powershell
& .\firmware\poc\build.ps1 -Profile dhcp -ExtraConf firmware/poc/pc.conf
# Sustituir también IP_REAL_DEL_PC en este comando:
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe scripts/poc_udp_receiver.py --bind IP_REAL_DEL_PC --port 4242
```

Sin `--bind`, el receptor escucha solo `127.0.0.1` para pruebas locales.
No hay autodetección del destino, broadcast de heartbeat ni tráfico a una IP
por defecto en DHCP. DHCP y ARP sí utilizan el tráfico normal de configuración
de red. Permitir al Python receptor recibir UDP en el perfil de firewall del
banco; no deshabilitar globalmente el firewall. Ctrl+C cierra el socket.

Ejemplo de contenido diagnóstico (no es framing industrial RS-485):

```text
poc=gateway version=0.1.0 seq=0 uptime_ms=12345
```

`seq` es uint32 incremental por intento de envío, vuelve a cero al reiniciar y
desborda modularmente. Puede haber saltos. Un mensaje `accepted locally` en la
consola no prueba recepción: solo la salida real del receptor acredita llegada.
UDP no confirma entrega, orden ni unicidad.

## Programación y consola

No programar hasta conectar e identificar la Nucleo. OpenOCD está disponible y el
board tiene runners oficiales `stm32cubeprogrammer`, `openocd` y `jlink`.
Para el build local, desde la raíz (rutas convertidas a `/` para OpenOCD):

```powershell
$pkg = "$env:USERPROFILE/.platformio/packages"
$elf = (Resolve-Path firmware/poc/build-static/zephyr/zephyr.elf).Path.Replace('\', '/')
& "$pkg/tool-openocd/bin/openocd.exe" -s "$pkg/tool-openocd/openocd/scripts" -f "$pkg/framework-zephyr/boards/st/nucleo_f429zi/support/openocd.cfg" -c "program $elf verify reset exit"
```

Para DHCP sustituir `build-static` por `build-dhcp`. Si la ruta incluye espacios,
encerrar `$elf` entre llaves dentro de la cadena OpenOCD: `program {$elf} ...`.
En workspace west: `west flash -d firmware/poc/build-west-static -r openocd`.

```powershell
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe -m serial.tools.list_ports
# Sustituir COMx por el ST-LINK VCP identificado (no elegir puertos Bluetooth).
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe -m serial.tools.miniterm COMx 115200
```

Abrir consola y receptor, después pulsar RESET. Se espera identificación de
aplicación/versión, `alive uptime_ms=...` cada segundo, estados de red e IPv4,
y mensajes UDP cuando enlace, IPv4 y destino estén disponibles. Retirar el cable
Ethernet debe mantener `alive`; al restaurarlo se esperan nuevos intentos UDP.

Problemas frecuentes: ausencia de VCP (USB solo carga, drivers o conector equivocado),
consola ocupada o velocidad distinta, JP6/JP7/cable/switch sin enlace, conexión
directa usando DHCP sin servidor, NIC del PC en otra subred, destino incorrecto,
receptor enlazado a loopback, firewall o puerto distinto. El firmware imprime la
IP de la placa; comprobar separadamente la IP del PC. Si CMake conserva una
configuración antigua, usar un directorio de build nuevo o limpiar únicamente
el directorio generado correspondiente.

## Memoria y siguiente hito RS-485

El DTS separa SRAM DMA accesible: **192 KiB en 0x20000000–0x2002ffff**, de
**64 KiB CCM en 0x10000000**, accesible solo por CPU. No se coloca ningún buffer
en CCM ni se activa CCM como heap/stack. El driver Ethernet conserva su ubicación
y alineación oficiales. Revisar en cada build:

```powershell
& "$env:USERPROFILE/.platformio/packages/toolchain-gccarmnoneeabi/bin/arm-none-eabi-nm.exe" -S firmware/poc/build-static/zephyr/zephyr.elf | Select-String 'dma_(rx|tx)_(buffer|desc_tab)'
```

Los cuatro símbolos deben quedar íntegros en SRAM `0x200...`, no CCM. El buffer
de texto de 128 bytes vive en el stack normal y el stack de red lo copia; no se
entrega un puntero de vida corta directamente a DMA. No se añade memoria externa.

**Siguiente hito:** recepción de bytes por USART6 antes del parser. El DTS 4.3.0
reserva **TX PG14 / RX PG9**, 115200 como valor inicial de placa. UM1974 tabla 17:
PG14 = CN10 pin 14 / D1; PG9 = CN10 pin 16 / D0. Contrastar placa/revisión y
conectores antes de cablear. Aún no se valida ninguna recepción UART/RS-485.

Ruta futura: PC → USB-RS485 → A/B del transceiver → **RO → USART6 RX PG9**.
Para THVD1420 alimentado a 3.3 V, comprobar niveles y datasheet real del módulo:
**DE=0** deshabilita TX y **/RE=0** habilita recepción; fijar ambas señales,
sin entradas flotantes. DI del transceiver permanece definida y sin transmitir.
Usar GND común si el módulo no tiene aislamiento; si es aislado, respetar sus
dominios. Confirmar polaridad A/B, cableado, terminación en extremos y bias del
enlace. Nunca conectar A/B directamente al STM32 ni aplicar **24 V a la Nucleo**.
Buffers UART DMA futuros deben estar en SRAM accesible, con propiedad y vida útil
definidas. El protocolo seguirá siendo unidireccional PC→STM32, sin ACK/reintento,
CRC-16 y payload máximo 256; cerrar framing/variante CRC antes de implementarlo.

## Validación y fuentes

Comprobaciones ejecutadas el 2026-10-26:

| Comprobación | Resultado |
|---|---|
| Compilación DHCP, destino vacío | Correcta: 80 484 B flash / 36 176 B RAM; ELF, HEX y BIN generados |
| Compilación estática, banco aislado | Correcta: 77 504 B flash / 34 816 B RAM; ELF, HEX y BIN generados |
| Kconfig efectivo y ELF de ambos perfiles | Target correcto, consola UART, driver Ethernet HAL v2, cola TX; los cuatro buffers/descriptores DMA dentro de SRAM `0x200...` |
| Receptor Python | Cuatro pruebas correctas, incluido UDP IPv4 real por loopback |
| Detección de hardware | OpenOCD `adapter list` sin adaptadores; PnP y pyserial solo muestran COM3/COM4 Bluetooth |
| Programación, arranque, VCP, LED y UDP desde MCU | **No ejecutados: no se detectó la placa conectada** |

M0/M1 tienen compilación validada, pero no validación física. No se han probado
DHCP, tráfico Ethernet, ni recuperación de enlace con la Nucleo real. La revisión
de dirección/alineación en ELF no sustituye pruebas de DMA en hardware.

Pruebas del receptor, sin dependencias externas:

```powershell
& C:\dev\tools\gateway-zephyr-venv\Scripts\python.exe -B -m unittest discover -s scripts/tests -v
```

Incluyen un datagrama UDP real de loopback, impresión de emisor/secuencia,
texto arbitrario, control de terminal, puerto inválido, error de bind y cierre
ante `KeyboardInterrupt` simulado. No equivalen a recibir desde el MCU.
La comprobación física requiere programar, observar arranque/consola/LED,
recibir UDP desde la placa y probar desconexión/reconexión Ethernet.

- [Soporte oficial Zephyr](https://docs.zephyrproject.org/4.3.0/boards/st/nucleo_f429zi/doc/index.html).
- [NUCLEO-F429ZI](https://www.st.com/en/evaluation-tools/nucleo-f429zi.html).
- [Manual UM1974](https://www.st.com/resource/en/user_manual/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf).
- [Datasheet STM32F429](https://www.st.com/resource/en/datasheet/stm32f429zi.pdf).
- [RM0090, buses y memoria](https://www.st.com/resource/en/reference_manual/dm00031020-stm32f4-series-reference-manual-stmicroelectronics.pdf).
