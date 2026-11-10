from pathlib import Path
D=Path('docs/hardware')
def add(file,marker,text):
 p=D/file;t=p.read_text(encoding='utf-8').split(marker)[0].rstrip();p.write_text(t+'\n\n'+marker+'\n\n'+text+'\n',encoding='utf-8')
body='ETH_CBOB quantity2 now has saved C1206C102KGRACAUTO / GW_C1206_KEMET_C1076_DENSITY_B, verified C600002 identity and KEMET densityB reflow geometry. One capacitor per nodeA/B to CHASSIS; no topology change. CAD_VERIFIED is separate from provisional application/safety class. Current66symbols/37footprints validate with0errors/0warnings; prior65/36 objects unchanged. Native compilation not run, IntLib stale. [Details and local datasheet](ethernet_1nf_library_closure.md).'
for f in ['altium_library_preparation_report.md','schematic_readiness_gate.md']:add(f,'## Ethernet1nF CAD closure — 2026-11-07',body)
