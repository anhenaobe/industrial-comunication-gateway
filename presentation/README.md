# Presentación NABC

Los exports PPTX, PDF y PNG existentes y su generador actual corresponden a la presentación anterior a la baseline provisional de componentes del 2026-10-04; se conservan como material histórico. Para la selección vigente y los pendientes de potencia, consultar §3.4–3.6 de `docs/industrial_linux_gateway_requirements.md` y la fuente NABC actualizada.

Archivos generados:

- `industrial_communication_gateway_nabc.pptx`: presentación editable.
- `industrial_communication_gateway_nabc.pdf`: exportación para revisión.
- `industrial_communication_gateway_nabc_preview.png`: montaje de las diez diapositivas.
- `assets/rendered_slides/`: render individual usado para validación visual.

La fuente de verdad de contenido es `docs/presentation_nabc.md`. La presentación no modifica ni completa los TBD del documento.

## Regeneración

Requiere Microsoft PowerPoint para Windows:

```powershell
powershell -ExecutionPolicy Bypass -File presentation/src/generate_presentation.ps1
```

El contenido del generador requiere actualización antes de regenerar una presentación que refleje la baseline actual. El script crea el PPTX con formas y texto nativos editables, exporta el PDF y genera los previews PNG.
