"""Read-only Altium IntLib metadata audit; requires olefile 0.47.

Run from repository root with a Python environment containing olefile:
  python docs/hardware/evidence/extract_library_inventory.py
Does not create CAD resources. Presence checks do not validate geometry or pinout.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zlib

import olefile

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "shared_lib (1).IntLib"
OUT = ROOT / "docs/hardware"


def fields(record):
    return {k.lower(): v for k, v in
            (part.split("=", 1) for part in record.split("|") if "=" in part)}


def records(data):
    return [fields(x.decode("latin1")) for x in
            re.findall(rb"\|RECORD=[^\x00]+", data)]


def category(ref):
    if ref.startswith(("MCU_", "IC_STM32")):
        return "Procesamiento / MCU"
    if "FLASH" in ref:
        return "Procesamiento / memoria"
    if "USB2UART" in ref:
        return "Comunicaciones / USB-UART"
    if ref.startswith(("Q_", "Relay_")):
        return "Entradas y salidas / transistor o relé"
    if ref.startswith(("DCDC_", "LDO_", "IC_BAT", "TVS_", "D_", "Inductor_", "FB_", "Cap_")):
        return "Alimentación / " + ref.split("_")[0]
    return "Soporte / " + ref.split("_")[0]


def suitability(ref):
    if "ESP32" in ref:
        return "Candidato condicionado; sin MAC Ethernet; necesita controlador SPI ausente y cierre de GPIO/JTAG"
    if "STM32F030" in ref:
        return "No recomendado para migración directa PoC Zephyr/IP: 64 KiB Flash y 8 KiB RAM; sin MAC"
    if ref.startswith("Q_NFET"):
        return "No apto para conmutación directa de cargas de 24 V: nombre CAD indica 20 V"
    if ref.startswith("Q_PFET"):
        return "No aprobar para entrada 18–30 V: nombre CAD indica 30 V sin margen de transitorios"
    if ref.startswith("TVS_"):
        return "Protección de baja tensión; no sustituye automáticamente TVS de alimentación 24 V ni de RS-485"
    if ref.startswith("DCDC_SW_BUCK"):
        return "Útil con entrada de baja tensión; TPS564201 17 V / TPS56528 18 V: no conectar a 24 V"
    if ref.startswith("DCDC_SW_BOOST"):
        return "Boost; descripción CAD dice BUCK: contradicción a resolver; no sustituye buck 24 V"
    if ref.startswith("LDO_"):
        return "Posible 5 V a 3.3 V; verificar dropout, estabilidad y disipación; no entrada directa 24 V"
    if ref.startswith("Relay_"):
        return "Posible DO de contacto; requiere driver, flyback, corriente DC/carga verificados; cambia DO Rev. A"
    if ref.startswith("IC_BAT"):
        return "Cargador Li-ion; fuera de alcance"
    if "FLASH" in ref:
        return "Memoria externa diferible"
    if "USB2UART" in ref:
        return "Consola/carga opcional; no es RS-485 ni depurador JTAG/SWD"
    if ref == "template":
        return "Plantilla; no es componente seleccionable"
    return "Reutilización condicionada a valor, ratings, pinout y dimensiones; no validado eléctricamente"


with olefile.OleFileIO(SOURCE) as outer:
    embedded = {}
    for name in ("SchLib/0.schlib", "PCBLib/0.pcblib"):
        raw = outer.openstream(name).read()
        assert raw[0] == 2
        embedded[name] = zlib.decompress(raw[1:])
    outer_streams = [{"path": "/".join(p), "bytes": outer.get_size(p)}
                     for p in outer.listdir()]

sch = olefile.OleFileIO(io.BytesIO(embedded["SchLib/0.schlib"]))
pcb = olefile.OleFileIO(io.BytesIO(embedded["PCBLib/0.pcblib"]))
footprints = {}
for path in pcb.listdir():
    if len(path) != 2 or path[-1] != "Data" or path[0] in ("Library", "FileVersionInfo"):
        continue
    data = pcb.openstream(path).read()
    # First PCB record contains the original pattern name (storage names sanitize '*').
    n = int.from_bytes(data[:4], "little")
    assert data[4] + 1 == n
    name = data[5:4+n].decode("latin1")
    models = [fields(x.decode("latin1")) for x in
              re.findall(rb"V7_LAYER=[^\x00]+", data)
              if b"MODEL.MODELTYPE=" in x]
    footprints[name] = {"storage": "/".join(path), "bytes": len(data), "bodies": models}

components = []
rows = []
for path in sch.listdir():
    if len(path) != 2 or path[-1] != "Data":
        continue
    rr = records(sch.openstream(path).read())
    head = next(r for r in rr if r.get("record") == "1")
    ref = head["libreference"]
    params = {r.get("name", "").lower(): r.get("text", "") for r in rr if r.get("record") == "41"}
    models = [r for r in rr if r.get("record") == "45" and r.get("modeltype") == "PCBLIB"]
    names = [m["modelname"] for m in models]
    found = [footprints[n] for n in names if n in footprints]
    components.append({"reference": ref, "symbol_stream": "/".join(path),
                       "head": head, "parameters": params, "models": models})
    notes = ["Metadatos CAD; fabricante/MPN transcritos, no autenticados. Pinout y geometría pendientes de Altium/datasheet."]
    if not params.get("manufacturer part number"):
        notes.append("MPN no consignado; referencia CAD genérica.")
    if ref.startswith("Inductor_10uH_4A"):
        notes.append("Nombre 10uH/7.2x6.6; descripción dice 2.2uH/5.8x5.2: inconsistencia.")
    if ref.startswith("TVS_12V"):
        notes.append("Referencia menciona SOD_123; modelo enlazado SOD_123FL.")
    if ref.startswith("Con_Power"):
        notes.append("Nombre 2.1mm frente a MPN HC-DC-005-2.0T: verificar diámetro real.")
    row = dict(referencia_cad=ref, mpn=params.get("manufacturer part number") or "no consignado",
               fabricante=params.get("manufacturer") or "no consignado", categoria=category(ref),
               funcion=head.get("componentdescription", "no consignada"),
               encapsulado_referencia_cad="; ".join(names) or "no verificado",
               simbolo="sí", footprint=("sí" if names and len(found) == len(names) else "no" if not names else "no verificado"),
               modelo_3d="sí" if any(f["bodies"] for f in found) else "no",
               detalle_3d="; ".join(sorted({b.get("model.name", "") or "cuerpo extruido CAD" for f in found for b in f["bodies"]})) or "no encontrado",
               archivo=str(SOURCE), ruta_simbolo="SchLib/0.schlib::" + "/".join(path),
               ruta_footprint="; ".join("PCBLib/0.pcblib::" + f["storage"] for f in found),
               compatibilidad=suitability(ref), referencia_tecnica=params.get("componentlink1url") or "sin enlace en CAD",
               disponible_fisicamente="no verificado", disponible_comercialmente="no verificado",
               precio="sin cotización comparable", observaciones=" ".join(notes))
    rows.append(row)

evidence = dict(source=str(SOURCE), sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                outer_streams=outer_streams,
                embedded_sha256={k: hashlib.sha256(v).hexdigest() for k,v in embedded.items()},
                components=components, footprints=footprints,
                pcb_model_streams=[{"path": "/".join(p), "bytes": pcb.get_size(p)}
                                   for p in pcb.listdir() if "Models" in p])
(OUT / "evidence/shared_lib_metadata.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
with (OUT / "library_inventory.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(json.dumps(dict(symbols=len(rows), selectable=len(rows)-1, footprints=len(footprints),
                      linked=sum(r["footprint"] == "sí" for r in rows),
                      with_3d=sum(r["modelo_3d"] == "sí" for r in rows),
                      missing=[r["referencia_cad"] for r in rows if r["footprint"] != "sí"]), ensure_ascii=False))
