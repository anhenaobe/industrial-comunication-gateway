from pathlib import Path
D=Path('docs/hardware')
def add(file,marker,body):
 p=D/file;t=p.read_text(encoding='utf-8').split(marker)[0].rstrip();p.write_text(t+'\n\n'+marker+'\n\n'+body+'\n',encoding='utf-8')
add('altium_library_preparation_report.md','## Ethernet75Ω closure — 2026-11-07',
 'Current inventory65symbols/36footprints. Added only CRCW080575R0FKEA and GW_CRCW0805_VISHAY_20035_REFLOW. '
 'All prior64symbols/35footprints unchanged by backend diff. C844859 exact identity verified by public catalog; '
 'C1511836 is the distinct C-suffix commodity version and was not substituted. Four ETH_RBOB instances retain '
 'their approved topology. File validation0errors/0warnings; native compilation not performed and IntLib stale. '
 'See [closure report](ethernet_75ohm_library_closure.md), source links, backup and readback under `evidence/ethernet_75ohm/`. '
 'No resistor CAD blocker remains; HV capacitors/chassis and TPS custom-pad issues remain separate.')
add('schematic_readiness_gate.md','## Ethernet75Ω CAD amendment — 2026-11-07',
 'ETH_RBOB quantity4 now uses CRCW080575R0FKEA/C844859, saved conventional resistor symbol and exact Vishay20035 '
 'reflow footprint GW_CRCW0805_VISHAY_20035_REFLOW. Resistor symbol/footprint status CAD_VERIFIED; '
 'no native schematic placement or hardware test occurred. The two high-voltage capacitor models and chassis '
 'implementation remain unresolved. Current65/36 source libraries are not a newly compiled IntLib. '
 'See [manual construction guide](schematic_construction_guide.md) and [resistor evidence](ethernet_75ohm_library_closure.md).')
p=D/'symbol_library_verification.md';t=p.read_text(encoding='utf-8');notice='> Historical TPS/symbol-style stage snapshot below. Current source inventory is65symbols/36footprints after the [Ethernet75Ω addition](ethernet_75ohm_library_closure.md); all objects from this snapshot remain unchanged.\n\n'
if '> Historical TPS/symbol-style stage snapshot below.' not in t:
 i=t.index('\n')+1;t=t[:i]+'\n'+notice+t[i:];p.write_text(t,encoding='utf-8')
