param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)

$ErrorActionPreference = 'Stop'

$outDir = Join-Path $RepoRoot 'presentation'
$renderDir = Join-Path $outDir 'assets\rendered_slides'
$pptxPath = Join-Path $outDir 'industrial_communication_gateway_nabc.pptx'
$pdfPath = Join-Path $outDir 'industrial_communication_gateway_nabc.pdf'
$previewPath = Join-Path $outDir 'industrial_communication_gateway_nabc_preview.png'
$sourcePath = Join-Path $RepoRoot 'docs\presentation_nabc.md'
$competitorPath = Join-Path $RepoRoot 'docs\competitor_references.md'

if (-not (Test-Path -LiteralPath $sourcePath)) { throw "Missing source: $sourcePath" }
if (-not (Test-Path -LiteralPath $competitorPath)) { throw "Missing source: $competitorPath" }

New-Item -ItemType Directory -Force -Path $outDir, $renderDir | Out-Null
Get-ChildItem -LiteralPath $renderDir -File -ErrorAction SilentlyContinue | Remove-Item -Force

function RGB([string]$hex) {
    $h = $hex.TrimStart('#')
    $r = [Convert]::ToInt32($h.Substring(0,2),16)
    $g = [Convert]::ToInt32($h.Substring(2,2),16)
    $b = [Convert]::ToInt32($h.Substring(4,2),16)
    return $r + (256 * $g) + (65536 * $b)
}

$C = @{
    Bg       = RGB '#08111F'
    Surface  = RGB '#152239'
    Surface2 = RGB '#0E1B2E'
    Text     = RGB '#F0F4F8'
    Muted    = RGB '#9EAAB8'
    Cyan     = RGB '#20C5E8'
    Blue     = RGB '#3B82F6'
    Orange   = RGB '#F59E0B'
    Green    = RGB '#34D399'
    Red      = RGB '#FB7185'
    Grid     = RGB '#263852'
}

$ppLayoutBlank = 12
$msoTextOrientationHorizontal = 1
$msoShapeRectangle = 1
$msoShapeRoundedRectangle = 5
$msoShapeOval = 9
$msoConnectorStraight = 1
$msoConnectorElbow = 2
$msoTrue = -1
$msoFalse = 0
$msoAlignLeft = 1
$msoAlignCenter = 2
$msoAlignRight = 3
$msoAnchorTop = 1
$msoAnchorMiddle = 3
$msoArrowheadTriangle = 3

function Set-SlideBackground($slide, [int]$color) {
    $slide.FollowMasterBackground = $msoFalse
    $slide.Background.Fill.ForeColor.RGB = $color
    $slide.Background.Fill.Solid()
}

function Add-Text($slide, [string]$text, [float]$x, [float]$y, [float]$w, [float]$h,
                  [float]$size = 18, [int]$color = $C.Text, [bool]$bold = $false,
                  [int]$align = $msoAlignLeft, [int]$valign = $msoAnchorTop,
                  [string]$name = '') {
    $shape = $slide.Shapes.AddTextbox($msoTextOrientationHorizontal, $x, $y, $w, $h)
    if ($name) { $shape.Name = $name }
    $shape.Fill.Visible = $msoFalse
    $shape.Line.Visible = $msoFalse
    $shape.TextFrame2.AutoSize = 0
    $shape.TextFrame2.WordWrap = $msoTrue
    $shape.TextFrame2.MarginLeft = 0
    $shape.TextFrame2.MarginRight = 0
    $shape.TextFrame2.MarginTop = 0
    $shape.TextFrame2.MarginBottom = 0
    $shape.TextFrame2.VerticalAnchor = $valign
    $safeText = $text -replace "`r?`n", "`r"
    $shape.TextFrame2.TextRange.Text = $safeText
    $shape.TextFrame2.TextRange.Font.Name = 'Aptos'
    $shape.TextFrame2.TextRange.Font.Size = $size
    $shape.TextFrame2.TextRange.Font.Bold = $(if($bold){$msoTrue}else{$msoFalse})
    $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $color
    $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = $align
    return $shape
}

function Add-Box($slide, [string]$text, [float]$x, [float]$y, [float]$w, [float]$h,
                 [int]$fill = $C.Surface, [int]$line = $C.Grid, [float]$size = 18,
                 [int]$textColor = $C.Text, [bool]$bold = $false, [bool]$rounded = $true,
                 [int]$align = $msoAlignCenter, [string]$name = '') {
    $geometry = $(if($rounded){$msoShapeRoundedRectangle}else{$msoShapeRectangle})
    $shape = $slide.Shapes.AddShape($geometry, $x, $y, $w, $h)
    if ($name) { $shape.Name = $name }
    $shape.Fill.ForeColor.RGB = $fill
    $shape.Fill.Solid()
    $shape.Line.ForeColor.RGB = $line
    $shape.Line.Weight = 1.25
    $shape.TextFrame2.AutoSize = 0
    $shape.TextFrame2.WordWrap = $msoTrue
    $shape.TextFrame2.MarginLeft = 8
    $shape.TextFrame2.MarginRight = 8
    $shape.TextFrame2.MarginTop = 5
    $shape.TextFrame2.MarginBottom = 5
    $shape.TextFrame2.VerticalAnchor = $msoAnchorMiddle
    $safeText = $text -replace "`r?`n", "`r"
    $shape.TextFrame2.TextRange.Text = $safeText
    $shape.TextFrame2.TextRange.Font.Name = 'Aptos'
    $shape.TextFrame2.TextRange.Font.Size = $size
    $shape.TextFrame2.TextRange.Font.Bold = $(if($bold){$msoTrue}else{$msoFalse})
    $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $textColor
    $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = $align
    return $shape
}

function Add-Line($slide, [float]$x1, [float]$y1, [float]$x2, [float]$y2,
                  [int]$color = $C.Cyan, [float]$weight = 2, [bool]$arrow = $true,
                  [bool]$dashed = $false, [bool]$elbow = $false) {
    if ($elbow) {
        $line = $slide.Shapes.AddConnector($msoConnectorElbow, $x1, $y1, $x2, $y2)
    } else {
        $line = $slide.Shapes.AddConnector($msoConnectorStraight, $x1, $y1, $x2, $y2)
    }
    $line.Line.ForeColor.RGB = $color
    $line.Line.Weight = $weight
    if ($arrow) { $line.Line.EndArrowheadStyle = $msoArrowheadTriangle }
    if ($dashed) { $line.Line.DashStyle = 4 }
    return $line
}

function Add-CircleNumber($slide, [int]$number, [float]$x, [float]$y, [int]$color = $C.Cyan) {
    $s = $slide.Shapes.AddShape($msoShapeOval, $x, $y, 32, 32)
    $s.Fill.ForeColor.RGB = $color
    $s.Fill.Solid()
    $s.Line.Visible = $msoFalse
    $s.TextFrame2.VerticalAnchor = $msoAnchorMiddle
    $s.TextFrame2.TextRange.Text = [string]$number
    $s.TextFrame2.TextRange.Font.Name = 'Aptos Display'
    $s.TextFrame2.TextRange.Font.Size = 16
    $s.TextFrame2.TextRange.Font.Bold = $msoTrue
    $s.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $C.Bg
    $s.TextFrame2.TextRange.ParagraphFormat.Alignment = $msoAlignCenter
    return $s
}

function Add-Chrome($slide, [string]$section, [string]$title, [int]$number) {
    Add-Text $slide $section 45 25 210 20 12 $C.Cyan $true | Out-Null
    Add-Text $slide $title 45 52 870 48 35 $C.Text $true | Out-Null
    $rule = $slide.Shapes.AddShape($msoShapeRectangle, 45, 110, 70, 3)
    $rule.Fill.ForeColor.RGB = $C.Cyan; $rule.Fill.Solid(); $rule.Line.Visible = $msoFalse
    Add-Text $slide ('{0:00}' -f $number) 885 505 30 18 11 $C.Muted $true $msoAlignRight | Out-Null
    Add-Text $slide 'INDUSTRIAL COMMUNICATION GATEWAY · REV. A' 45 505 360 18 10 $C.Muted $false | Out-Null
}

function Add-Notes($slide, [string]$sourceText) {
    try {
        $body = $slide.NotesPage.Shapes.Placeholders.Item(2)
        $body.TextFrame.TextRange.Text = "[Sources]`r`n$sourceText"
    } catch {
        # Notes are non-critical for rendering; source references remain in repository.
    }
}

function Add-Table($slide, $headers, $rows, $widths, [float]$x, [float]$y, [float]$rowH,
                   [float]$fontSize = 16, [int]$headerFill = $C.Surface) {
    $cols = $headers.Count
    $totalW = ($widths | Measure-Object -Sum).Sum
    $lineY = $y
    $cx = $x
    for ($col=0; $col -lt $cols; $col++) {
        Add-Box -slide $slide -text ([string]$headers[$col]) -x $cx -y $lineY -w $widths[$col] -h $rowH -fill $headerFill -line $C.Cyan -size $fontSize -textColor $C.Text -bold $true -rounded $false | Out-Null
        $cx += $widths[$col]
    }
    for ($r=0; $r -lt $rows.Count; $r++) {
        $cx = $x
        $fill = $(if($r % 2 -eq 0){$C.Surface2}else{$C.Surface})
        for ($col=0; $col -lt $cols; $col++) {
            $align = $(if($col -eq 0){$msoAlignLeft}else{$msoAlignCenter})
            $cellTextColor = $(if($col -eq 0){$C.Text}else{$C.Muted})
            $cellBold = [bool]($col -eq 0)
            Add-Box -slide $slide -text ([string]$rows[$r][$col]) -x $cx -y ($y + (($r+1)*$rowH)) -w $widths[$col] -h $rowH -fill $fill -line $C.Grid -size $fontSize -textColor $cellTextColor -bold $cellBold -rounded $false -align $align | Out-Null
            $cx += $widths[$col]
        }
    }
    return $totalW
}

$powerPoint = $null
$deck = $null
try {
    $powerPoint = New-Object -ComObject PowerPoint.Application
    $deck = $powerPoint.Presentations.Add($msoFalse)
    $deck.PageSetup.SlideWidth = 960
    $deck.PageSetup.SlideHeight = 540

    # 1 — Cover
    $s = $deck.Slides.Add(1, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    $bar = $s.Shapes.AddShape($msoShapeRectangle, 0, 0, 11, 540)
    $bar.Fill.ForeColor.RGB = $C.Cyan; $bar.Fill.Solid(); $bar.Line.Visible = $msoFalse
    Add-Text $s 'INDUSTRIAL COMMUNICATION GATEWAY' 62 100 760 118 50 $C.Text $true | Out-Null
    Add-Text $s 'Integración de interfaces industriales con redes IP' 65 230 690 40 24 $C.Muted $false | Out-Null
    Add-Text $s 'REV. A  ·  FASE DE DISEÑO Y REQUISITOS' 65 306 500 24 16 $C.Cyan $true | Out-Null
    Add-Box $s 'STM32H723VET6  +  ZEPHYR RTOS' 65 366 510 54 $C.Surface $C.Cyan 22 $C.Text $true $true $msoAlignLeft | Out-Null
    Add-Text $s 'DECIDIDO · NO IMPLEMENTADO · NO VALIDADO' 66 438 520 22 14 $C.Orange $true | Out-Null
    Add-Text $s 'Fuente consolidada NABC · 2026-09-15' 65 500 360 16 10 $C.Muted | Out-Null
    Add-Notes $s "$sourcePath — Portada y baseline Rev. A."

    # 2 — Need
    $s = $deck.Slides.Add(2, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'N · NEED' 'Necesidad: adaptar el campo antes de IP' 2
    # connectors first
    Add-Line $s 230 245 302 245 $C.Cyan 2.5 $true | Out-Null
    Add-Line $s 505 245 575 245 $C.Cyan 2.5 $true | Out-Null
    Add-Line $s 760 245 810 245 $C.Cyan 2.5 $true | Out-Null
    Add-Box $s "RS-485`nCAN-FD`nDI/DO 24 V" 55 171 175 150 $C.Surface $C.Grid 22 $C.Text $true | Out-Null
    Add-Box $s "ADAPTAR`nprotección + señal" 302 181 203 128 $C.Surface2 $C.Cyan 18 $C.Text $true | Out-Null
    Add-Box $s "ADQUIRIR`nVALIDAR`nNORMALIZAR" 575 171 185 150 $C.Surface2 $C.Blue 18 $C.Text $true | Out-Null
    Add-Box $s "ETHERNET`nSERVER / SCADA" 810 181 125 128 $C.Surface $C.Cyan 15 $C.Text $true | Out-Null
    Add-Text $s 'La red superior necesita información normalizada, diagnóstico y continuidad ante cortes de enlace.' 120 358 720 40 20 $C.Text $false $msoAlignCenter | Out-Null
    Add-Box $s 'CASO INDUSTRIAL DEMOSTRADOR: TBD' 287 426 386 38 $C.Surface2 $C.Orange 16 $C.Orange $true | Out-Null
    Add-Notes $s "$sourcePath — §2 N — Need. Trazabilidad: §1.1; UC-01 a UC-05; F-01 a F-09."

    # 3 — Need to requirements
    $s = $deck.Slides.Add(3, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'N · NEED → REQUISITOS' 'Cada necesidad se traduce en un estado verificable' 3
    $headers = @('NECESIDAD','REQUISITO PRINCIPAL','ESTADO REAL')
    $rows = @(
        @('Integrar campo',"2 × RS-485 · 1 × CAN-FD`n4 DI 24 V · 2 DO","Objetivo Rev. A`nNo implementado"),
        @('Conectar red superior','Ethernet principal',"Decidido como función`nImplementación TBD"),
        @('Conservar datos','Persistencia + reintento',"Objetivo`nMedio/capacidad/política TBD"),
        @('Diagnosticar y mantener',"Logs · estado · configuración`nactualización · recuperación","Objetivo`nMecanismos TBD"),
        @('Interactuar con campo',"Protección + acondicionamiento`nAislamiento si se justifica","Objetivo`nNiveles/componentes TBD")
    )
    Add-Table $s $headers $rows @(210,395,265) 45 142 64 16 | Out-Null
    Add-Notes $s "$sourcePath — §3 Need → requisitos. Trazabilidad: D-11 a D-18; SR-COM, SR-IO, SR-DIA, SR-SAF y SR-MNT."

    # 4 — Approach architecture
    $s = $deck.Slides.Add(4, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'A · APPROACH' 'Rev. A se organiza en cinco dominios' 4
    $xs = @(45,225,405,585,765); $w=150; $y=178; $h=205
    for($i=0;$i -lt 4;$i++){ Add-Line $s ($xs[$i]+$w) 280 $xs[$i+1] 280 $C.Cyan 2.5 $true | Out-Null }
    Add-Box $s "FIELD DEVICES`n`nRS-485`nCAN-FD`nDI/DO 24 V" $xs[0] $y $w $h $C.Surface $C.Grid 18 $C.Text $true | Out-Null
    Add-Box $s "INDUSTRIAL`nINTERFACE / CARRIER`n`nProtection`nSignal conditioning`nIsolation — TBD" $xs[1] $y $w $h $C.Surface $C.Grid 16 $C.Text $true | Out-Null
    Add-Box $s "PROCESSING`nPLATFORM`n`nSTM32H723VET6`nZephyr RTOS`n`nDECIDIDO" $xs[2] $y $w $h $C.Surface2 $C.Cyan 15 $C.Text $true | Out-Null
    Add-Box $s "NETWORK`nINTERFACE`n`nEthernet principal`nSegundo Ethernet`nTBD" $xs[3] $y $w $h $C.Surface $C.Grid 16 $C.Text $true | Out-Null
    Add-Box $s "SERVER / SCADA`n`nDatos IP`nDiagnóstico`nComandos autorizados" $xs[4] $y $w $h $C.Surface $C.Grid 17 $C.Text $true | Out-Null
    Add-Text $s 'Pinout concreto · PHY · transceptores · almacenamiento · conectores · alimentación detallada: TBD' 75 422 810 26 15 $C.Muted $false $msoAlignCenter | Out-Null
    Add-Notes $s "$sourcePath — §4 Approach: arquitectura. Inspirado en $RepoRoot\docs\figures\industrial_gateway_architecture.drawio; contenido simplificado según NABC."

    # 5 — Workflow
    $s = $deck.Slides.Add(5, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'A · APPROACH' 'El flujo separa adquisición y comando autorizado' 5
    Add-Text $s 'ADQUISICIÓN' 45 142 180 22 17 $C.Cyan $true | Out-Null
    $topLabels = @('Field','Acquire','Validate','Normalize',"Persist`nif required",'Ethernet',"Server /`nSCADA")
    $topX = @(45,170,295,420,545,670,795)
    for($i=0;$i -lt 6;$i++){ Add-Line $s ($topX[$i]+100) 213 $topX[$i+1] 213 $C.Cyan 2 $true | Out-Null }
    for($i=0;$i -lt 7;$i++){ Add-Box $s $topLabels[$i] $topX[$i] 179 100 68 $C.Surface2 $C.Cyan 16 $C.Text ($i -eq 3) | Out-Null }
    Add-Text $s 'COMANDO AUTORIZADO' 45 302 250 22 17 $C.Orange $true | Out-Null
    $cmdLabels = @("Server /`nSCADA",'Ethernet',"Protocol`nhandler","Field`ninterface",'Device')
    $cmdX = @(115,285,455,625,795)
    for($i=0;$i -lt 4;$i++){ Add-Line $s ($cmdX[$i]+110) 375 $cmdX[$i+1] 375 $C.Orange 2 $true | Out-Null }
    for($i=0;$i -lt 5;$i++){ Add-Box $s $cmdLabels[$i] $cmdX[$i] 341 110 68 $C.Surface $C.Orange 16 $C.Text $false | Out-Null }
    Add-Text $s 'Capacidad prevista. No se asume control crítico en tiempo real; estados seguros y latencias permanecen TBD.' 95 446 770 35 16 $C.Muted $false $msoAlignCenter | Out-Null
    Add-Notes $s "$sourcePath — §5 Approach: funcionamiento previsto. No existe firmware validado."

    # 6 — Benefits
    $s = $deck.Slides.Add(6, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'B · BENEFITS' 'Beneficios esperados, aún no demostrados' 6
    $benefits = @(
        'Integración de RS-485, CAN-FD y DI/DO',
        'Adaptación de equipos legacy hacia IP',
        'Persistencia y reenvío según política TBD',
        'Diagnóstico y mantenimiento desde requisitos',
        'Protección y testabilidad ajustables al caso',
        'Plataforma embebida alineada con el alcance'
    )
    for($i=0;$i -lt $benefits.Count;$i++){
        $yy=148+($i*49)
        $dot=$s.Shapes.AddShape($msoShapeOval,55,$yy+6,12,12); $dot.Fill.ForeColor.RGB=$C.Cyan; $dot.Fill.Solid(); $dot.Line.Visible=$msoFalse
        Add-Text $s $benefits[$i] 82 $yy 505 34 18 $C.Text ($i -lt 2) | Out-Null
    }
    Add-Box $s "BENEFICIOS DEMOSTRADOS`n`nNinguno todavía a nivel de producto completo." 620 153 285 120 $C.Surface2 $C.Orange 20 $C.Text $true | Out-Null
    Add-Text $s "No se afirma:`nmenor coste · menor consumo · menor tamaño`nmayor robustez · rendimiento superior" 640 307 250 105 17 $C.Muted $false $msoAlignLeft | Out-Null
    Add-Notes $s "$sourcePath — §6 B — Benefits. Beneficios esperados y limitaciones explícitas."

    # 7 — Competition
    $s = $deck.Slides.Add(7, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'C · COMPETITION' 'La madurez comercial es la referencia' 7
    $models = @(
        @('SIEMENS','SIMATIC IOT2050 M.2','6ES7647-0BB00-1YA2'),
        @('MOXA','UC-2112-LX','UC-2100 Series'),
        @('ADVANTECH','UNO-2271G V2','Unidad base + expansión')
    )
    $mx=@(55,350,645)
    for($i=0;$i -lt 3;$i++){
        Add-Text $s $models[$i][0] $mx[$i] 160 250 22 16 $C.Cyan $true | Out-Null
        Add-Text $s $models[$i][1] $mx[$i] 194 250 50 24 $C.Text $true | Out-Null
        Add-Text $s $models[$i][2] $mx[$i] 248 250 25 14 $C.Muted | Out-Null
        $rule=$s.Shapes.AddShape($msoShapeRectangle,$mx[$i],286,250,2);$rule.Fill.ForeColor.RGB=$C.Grid;$rule.Fill.Solid();$rule.Line.Visible=$msoFalse
        Add-Text $s "Producto comercial documentado`nSoporte e instalación`nExpansión y datos ambientales" $mx[$i] 310 250 90 15 $C.Text | Out-Null
    }
    Add-Box $s 'NUESTRO PROYECTO: diseño/requisitos · sin prototipo completo · sin certificaciones' 115 430 730 40 $C.Surface2 $C.Orange 16 $C.Orange $true | Out-Null
    Add-Text $s 'Fuentes oficiales y limitaciones registradas en competitor_references.md' 225 482 510 16 10 $C.Muted $false $msoAlignCenter | Out-Null
    Add-Notes $s "$sourcePath — §7 C — Competition.`r`n$competitorPath — referencias oficiales y limitaciones por variante."

    # 8 — Competitive comparison
    $s = $deck.Slides.Add(8, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'C · MATRIZ' 'Ajuste potencial, no superioridad global' 8
    $headers=@('CRITERIO','NUESTRO GATEWAY','SIEMENS','MOXA','ADVANTECH')
    $rows=@(
        @('RS-485','2 objetivo','1 COM config.','2 COM config.','Expansión'),
        @('CAN-FD','1 objetivo','No doc. integrado','No documentado','CAN exp.; FD no verif.'),
        @('DI/DO','4 DI 24 V + 2 DO','Arduino; adaptación','No documentado','Expansión'),
        @('Ethernet','Principal; 2.º TBD','2 × Gigabit','100 Mb/s + Gigabit','2 × Gigabit'),
        @('Plataforma','STM32H723 / Zephyr','AM6548 / Linux','Cortex-A8 / MIL','Intel x86 / Win./Ubuntu'),
        @('Madurez','Diseño; no validado','Comercial','Comercial','Comercial')
    )
    Add-Table $s $headers $rows @(105,225,170,170,200) 45 137 46 13.5 | Out-Null
    Add-Box $s 'Mejor ajuste potencial al conjunto específico de requisitos — sujeto a diseño y validación.' 95 460 770 34 $C.Surface2 $C.Cyan 16 $C.Text $true | Out-Null
    Add-Notes $s "$sourcePath — §8 C — Comparación relevante.`r`n$competitorPath — matriz breve y reglas de comparación."

    # 9 — Scope and current status
    $s = $deck.Slides.Add(9, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'ESTADO ACTUAL' 'Plataforma decidida; producto aún no validado' 9
    $colX=@(45,350,655)
    $titles=@('DECIDIDO','TBD','NO IMPLEMENTADO / VALIDADO')
    $colors=@($C.Green,$C.Orange,$C.Red)
    $body=@(
        "STM32H723VET6 + Zephyr`n`nEthernet principal como función`n`nInterfaces objetivo como alcance",
        "Pinout y periféricos concretos`n`nSegundo Ethernet`n`nCoste · consumo · tamaño · desempeño",
        "Esquemático y PCB`n`nFirmware y prueba simultánea`n`nPrototipo completo y certificaciones"
    )
    for($i=0;$i -lt 3;$i++){
        Add-Text $s $titles[$i] $colX[$i] 150 260 24 16 $colors[$i] $true | Out-Null
        Add-Box $s $body[$i] $colX[$i] 188 260 216 $C.Surface2 $colors[$i] 18 $C.Text $false $true $msoAlignLeft | Out-Null
    }
    Add-Box $s 'SUFICIENCIA TOTAL DE PINES: VALIDADA EXTERNAMENTE · ASIGNACIÓN CONCRETA: TBD' 105 438 750 40 $C.Surface $C.Cyan 16 $C.Text $true | Out-Null
    Add-Notes $s "$sourcePath — §9 Alcance y estado actual. Estados preservados sin inferencias."

    # 10 — Roadmap
    $s = $deck.Slides.Add(10, $ppLayoutBlank); Set-SlideBackground $s $C.Bg
    Add-Chrome $s 'PRÓXIMOS PASOS' 'Rev. A: de requisitos cerrados a evidencia' 10
    $road = @(
        'Cerrar caso demostrador y TBD críticos',
        'Congelar periféricos, pinout y alimentación',
        'Seleccionar interfaces y almacenamiento',
        'Desarrollar esquemático y validar presupuestos',
        'Desarrollar firmware mínimo en Zephyr',
        'Diseñar y fabricar PCB Rev. A',
        'Probar y construir matriz requisito → evidencia'
    )
    $rx=@(55,285,515,745,745,515,285); $ry=@(165,165,165,165,330,330,330)
    # connectors first
    for($i=0;$i -lt 3;$i++){ Add-Line $s ($rx[$i]+180) 217 $rx[$i+1] 217 $C.Cyan 2 $true | Out-Null }
    Add-Line $s 835 254 835 300 $C.Cyan 2 $true | Out-Null
    for($i=4;$i -lt 6;$i++){ Add-Line $s $rx[$i] 382 ($rx[$i+1]+212) 382 $C.Cyan 2 $true | Out-Null }
    for($i=0;$i -lt 7;$i++){
        Add-CircleNumber $s ($i+1) $rx[$i] $ry[$i] | Out-Null
        Add-Text $s $road[$i] ($rx[$i]+42) ($ry[$i]-3) 170 66 16 $C.Text ($i -eq 6) | Out-Null
    }
    Add-Text $s 'Sin fechas inventadas · cada cierre debe producir evidencia revisable.' 220 467 520 22 15 $C.Muted $false $msoAlignCenter | Out-Null
    Add-Notes $s "$sourcePath — §10 Próximos pasos. Secuencia sintetizada sin añadir fechas."

    # Core properties
    try {
        $deck.BuiltInDocumentProperties.Item('Title').Value = 'Industrial Communication Gateway — NABC'
        $deck.BuiltInDocumentProperties.Item('Subject').Value = 'Rev. A — fase de diseño y requisitos'
        $deck.BuiltInDocumentProperties.Item('Author').Value = 'Equipo del proyecto'
    } catch {
        # Some Office installations do not expose built-in properties through COM.
    }

    $deck.SaveAs($pptxPath, 24)
    $deck.Export($renderDir, 'PNG', 1920, 1080)
    $deck.SaveAs($pdfPath, 32)

    # Contact sheet / montage from rendered slide PNGs.
    Add-Type -AssemblyName System.Drawing
    $slides = Get-ChildItem -LiteralPath $renderDir -File -Filter '*.PNG' | Sort-Object {
        if ($_.BaseName -match '(\d+)$') { [int]$Matches[1] } else { 999 }
    }
    $thumbW=620; $thumbH=349; $gap=20; $cols=2; $rows=[math]::Ceiling($slides.Count/$cols)
    $canvas = New-Object System.Drawing.Bitmap (($thumbW*$cols)+($gap*($cols+1))), (($thumbH*$rows)+($gap*($rows+1)))
    $g=[System.Drawing.Graphics]::FromImage($canvas)
    $g.Clear([System.Drawing.Color]::FromArgb(8,17,31))
    $g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    for($i=0;$i -lt $slides.Count;$i++){
        $img=[System.Drawing.Image]::FromFile($slides[$i].FullName)
        $col=$i%$cols; $row=[math]::Floor($i/$cols)
        $dx=$gap+($col*($thumbW+$gap)); $dy=$gap+($row*($thumbH+$gap))
        $g.DrawImage($img,$dx,$dy,$thumbW,$thumbH)
        $img.Dispose()
    }
    $canvas.Save($previewPath,[System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $canvas.Dispose()
}
finally {
    if ($deck) { try { $deck.Close() } catch {} }
    if ($powerPoint) { try { $powerPoint.Quit() } catch {}; [void][Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint) }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}

Get-Item -LiteralPath $pptxPath, $pdfPath, $previewPath | Select-Object FullName, Length, LastWriteTime
