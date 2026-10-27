# Native Windows build using the existing PlatformIO Zephyr/module/toolchain packages.
# No package installation, west workspace mutation or flashing is performed here.
[CmdletBinding()]
param(
    [ValidateSet('dhcp', 'static')][string]$Profile = 'dhcp',
    [string]$PackageRoot = "$env:USERPROFILE\.platformio\packages",
    [string]$PythonEnv = 'C:\dev\tools\gateway-zephyr-venv',
    [string]$ExtraConf = ''
)
$ErrorActionPreference = 'Stop'
$buildDir = Join-Path $PSScriptRoot "build-$Profile"
$python = Join-Path $PythonEnv 'Scripts\python.exe'
$cmake = Join-Path $PythonEnv 'Scripts\cmake.exe'
$ninja = Join-Path $PythonEnv 'Scripts\ninja.exe'
$zephyrBase = Join-Path $PackageRoot 'framework-zephyr'
$armTools = Join-Path $PackageRoot 'toolchain-gccarmnoneeabi'
$dtc = Join-Path $PackageRoot 'tool-dtc\dtc.exe'
$modules = @("$zephyrBase/_pio/modules/hal/cmsis_6", "$zephyrBase/_pio/modules/hal/stm32")
foreach ($path in @($python, $cmake, $ninja, $dtc, "$armTools/bin/arm-none-eabi-gcc.exe") + $modules) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Required tool/module not found: $path" }
}
if ($ExtraConf -and -not (Test-Path -LiteralPath $ExtraConf)) { throw "Missing config: $ExtraConf" }
# Forward slashes avoid CMake interpreting Windows path backslashes as escapes.
$buildDir = $buildDir.Replace('\', '/')
$python = $python.Replace('\', '/')
$ninja = $ninja.Replace('\', '/')
$dtc = $dtc.Replace('\', '/')
$modules = $modules | ForEach-Object { $_.Replace('\', '/') }
$packageVersion = (Get-Content -LiteralPath "$zephyrBase/package.json" -Raw | ConvertFrom-Json).version
$env:ZEPHYR_BASE = $zephyrBase
$env:ZEPHYR_TOOLCHAIN_VARIANT = 'gnuarmemb'
$env:GNUARMEMB_TOOLCHAIN_PATH = $armTools
$env:PATH = "$PythonEnv\Scripts;$env:PATH"
$configs = @()
if ($Profile -eq 'static') { $configs += "$PSScriptRoot/static.conf" }
if ($ExtraConf) { $configs += (Resolve-Path -LiteralPath $ExtraConf).Path }
$cmakeArgs = @(
    '-G', 'Ninja', '-S', $PSScriptRoot, '-B', $buildDir,
    '-DBOARD=nucleo_f429zi/stm32f429xx',
    "-DPython3_EXECUTABLE=$python", "-DCMAKE_MAKE_PROGRAM=$ninja", "-DDTC=$dtc",
    "-DUSER_CACHE_DIR=$buildDir/.cache", "-DZEPHYR_MODULES=$($modules -join ';')",
    "-DBUILD_VERSION=pio-$packageVersion",
    "-DEXTRA_CONF_FILE=$($configs -join ';')"
)
& $cmake @cmakeArgs
if ($LASTEXITCODE -ne 0) { throw 'Zephyr CMake configuration failed' }
& $cmake --build $buildDir
if ($LASTEXITCODE -ne 0) { throw 'Zephyr compilation failed' }
