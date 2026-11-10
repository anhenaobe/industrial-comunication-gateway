import json,csv,re,hashlib,html,math
from pathlib import Path
R=Path.cwd();D=R/'docs/hardware';O=Path(__file__).parent
p=D/'input_protection_reference.md';text=p.read_text(encoding='utf-8')
section=(O/'current_section.md').read_text(encoding='utf-8')
text=text.split('## 10. Academic Revision')[0].rstrip()
head=text.index('## 1.')
text=('# Academic gateway: recovered 24 V input protection\n\n'
 'Updated2026-11-07. **Current prototype baseline is section10:** approved TPS26620DRCR component selection, '
 'retained0451002.MRL/SS3P6L/TDS3311P.C chain, proposed calculated external settings. '
 'Manual capture is conditional; TPS thermal-pad native check remains unfinished.\n\n'
 '**Sections1–9 are preserved historical engineering analysis.** Their NIS3071,62kΩ, '
 'TDS3011 and industrial approval blockers are superseded where section10 states the current decision. '
 'Do not use their provisional tables as the current BOM. No schematic,PCB,Rev.A or professor library was edited.\n\n'
 +text[head:]+'\n\n'+section+'\n')
p.write_text(text,encoding='utf-8')
rows=list(csv.DictReader((D/'final_bom.csv').open(encoding='utf-8-sig')))
subset=[r for r in rows if r['component_id'].startswith('IN_') or r['component_id'] in ['ACTIVE_TPS26620DRCR','ACTIVE_NIS3071MT4TWG'] or r['component_id'].startswith(('B3_CIN','B5_CIN','B3_CHF','B5_CHF','B3_CVCC','B5_CVCC','B3_COUT','B5_COUT'))]
with (D/'input_protection_bom.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(subset)
def addendum(path,marker,body):
 t=path.read_text(encoding='utf-8');t=t.split(marker)[0].rstrip();path.write_text(t+'\n\n'+marker+'\n\n'+body.rstrip()+'\n',encoding='utf-8')
addendum(D/'altium_library_preparation_report.md','## 2026-11-07 TPS26620 and symbol-convention update',
 '''Current saved inventory:64 symbols /35 footprints. TPS26620DRCR plus four exact
Yageo resistors and KEMET10nF added;13 existing discrete symbols redrawn; NIS3071
preserved with superseded metadata. No existing footprint changed in this stage.
Both libraries pass the file backend's structural validation with0errors/0warnings.
Readback and component-level comparisons are saved under `evidence/tps26620/`.

TPS thermal-pad copper geometry is saved as CAD_CANDIDATE, not fully released:
the backend rejected repeated pad11 for the copper tongues. Native custom-pad
conversion/net inheritance and rounded-region corner review remain unfinished.
See [current connection plan](input_protection_reference.md#10-academic-revision--approved-schematic-connection-plan)
and [graphics/pin-map verification](symbol_library_verification.md).

Backup before this stage: `hardware/academic_rev1/libraries/backups/tps26620_20261107T172600Z/`.
The preceding academic-freeze backup is `backups/academic_freeze_20261107T170417Z/`.
Professor libraries, schematic/PCB/project documents and LibPkg remain hash-identical.
Native compile, close/reopen, representative placement and schematic ERC were not run:
no new Altium automation session was opened. Existing IntLib remains stale; use the
project-local source libraries for manual capture and compile later in Altium.
''')
addendum(D/'schematic_readiness_gate.md','## Current input-protection amendment — TPS26620',
 '''This amendment supersedes the historical Single input and buck-capacitor gates
above for the supervised academic prototype only. The approved fuse/SS3P6L/TDS3311
chain now uses approved TPS26620DRCR, with13.3kΩ ILIM,10nF dVdT and768k/33.2k/30.1k
UV/OV ladder proposed and calculated. Input capacitor quantities/MPNs are recorded
in the latest BOM; no additional24V output bulk is selected. Each buck retains
2×4.7µF100V plus2×220nF100V input bypass,2.2µF50V VCC bypass and3×15µF16V output caps.
Schematic capture: CONDITIONAL GO for these explicit connections and prototype
bring-up assumptions; not electrically tested. TPS custom thermal-pad/native net
check is pending before PCB model release. IntLib compilation/ERC remain unperformed.
No earlier DO/clock/MCU or unrelated CAD blocker is silently closed.
See [current manual connection plan](input_protection_reference.md#10-academic-revision--approved-schematic-connection-plan).
''')
addendum(D/'manufacturer_layout_guidelines.md','## TPS26620DRCR and academic input amendment',
 '''Use TI SLVSDT4F §§11–12 and DRC0010J4218878/B, not NIS3071 land/paste geometry.
Keep IN/OUT loops short, local input and buck bypass returns to GND_PWR; setting
resistors/dVdT and exposed pad11 return to EF_RTN. Never merge EF_RTN with GND_PWR.
Solder the EP and separately connect pin5; optional0.2mm thermal-via implementation
requires assembler review. Saved manufacturer-dimension candidate includes explicit
paste windows; its four EP copper tongues still need native custom-pad11/net
inheritance verification. No footprint placement/routing or native rules were changed.
See [input reference section10](input_protection_reference.md) for source links,
mask/paste details and prototype capacitor choices. No industrial compliance claim.
''')
p=D/'passive_component_selection.md';t=p.read_text(encoding='utf-8')
start=t.index('All111 original requirement IDs')
end=t.index('\n\nThe BOM explicitly',start)
new='''All111 original requirement IDs remain. The current generator produces122
passive/auxiliary rows and10 active specifications, including one superseded NIS3071
row at quantity0 in final_bom.csv. The current eFuse is TPS26620DRCR. The29 mandatory
passive specifications comprise the historical26-specification scope plus the three
UV/OV ladder specifications; changing MPN/value bindings does not delete requirement IDs.
There are88 known mandatory passive placements, zero unresolved mandatory quantity
groups, and8 conditional placements. CAD active-specification rows retain blank
quantities to avoid counting them as passive placements. These are inventory counts,
not verification claims. See [current input plan](input_protection_reference.md) and
[regenerated counts](evidence/passive_selection_counts.json).'''
if end!=-1:t=t[:start]+new+t[end:]
t=t.replace('Every accepted change is in\n[bom_decisions.json](evidence/electrical_closure/bom_decisions.json).',
 'The generator applies [original closure decisions](evidence/electrical_closure/bom_decisions.json),\n'
 '[academic freeze](evidence/input_protection_freeze/bom_decisions.json), then the latest\n'
 '[TPS26620 decisions](evidence/tps26620/bom_decisions.json).')
start=t.index('Library resources now have');end=t.index('\n\nAvailability:',start)
t=t[:start]+'''Library resources now have64 symbols and35 footprints. Source libraries pass
file structural validation; the existing46-symbol/23-footprint compiled IntLib is
stale. TPS26620's thermal-pad native custom-shape/net inheritance check remains
unfinished. Six warnings from the historical compilation are not current validation.
CAD_CANDIDATE is independent of electrical/application approval. The graphics and
preserved pin/footprint mappings are documented in
[symbol_library_verification.md](symbol_library_verification.md). The BSP75N numbered
map remains unfinished; no schematic or PCB was modified.''' + t[end:]
p.write_text(t,encoding='utf-8')
print('Updated current reference, subset BOM, capture and CAD/layout addenda.')
