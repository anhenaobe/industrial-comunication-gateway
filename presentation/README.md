# Presentación NABC

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

El script crea el PPTX con formas y texto nativos editables, exporta el PDF y genera los previews PNG.
