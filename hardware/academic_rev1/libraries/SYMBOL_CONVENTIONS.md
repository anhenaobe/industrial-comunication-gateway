# Gateway Academic schematic symbol convention

Use an IEC-oriented drafting style for new project-local symbols. Existing readable
professor-derived glyphs may retain their established orientation; do not edit the sources.

1. Classify the actual device before drawing it. Use conventional diode, Schottky,
   Zener/avalanche, NMOS/PMOS or NPN/PNP notation for the corresponding discrete device.
   Use IEC rectangular resistors, parallel capacitor plates and coil windings.
2. Use functional blocks for ICs, eFuses, smart switches and protection arrays whose
   internal circuitry would be misrepresented by a simple discrete symbol. A protective
   function alone does not make a device an ordinary TVS diode.
3. Keep every physical terminal and exposed pad. Distinct terminals must remain
   independently connectable, even when internally common. Never hide an extra anode
   or merge terminal identifiers to make a two-pin graphic.
4. Verify number, function, electrical type and footprint pad association against the
   exact manufacturer source. Record MPN, manufacturer, source and CAD status separately
   from electrical/application approval. A graphical edit must preserve these fields.
5. Orient simple parts left to right by default; diode anodes left, cathode right.
   Keep Schottky cathode hooks and both SS3P6L anodes visibly distinct. Use visible
   numbered semiconductor terminals. Passive two-terminal names/numbers may be hidden
   visually while retaining the actual pins and their identifiers.
6. Use the library's existing font, one-unit stroke and restrained colours. Keep
   reference designators above the body, labels clear of graphics, and connection tips
   on the 10-unit grid. Avoid unnecessary decoration and text inside small passive glyphs.
7. Before saving, preserve a backup. Read back the saved symbol and compare pin
   identities/types, MPN and footprint links with the baseline. Validate the library,
   review graphics, and compile when an authorized native environment is available.
   Do not propagate a library update into placed schematic/PCB objects automatically.

The reusable drafting helper is [symbol_style.py](../../../docs/hardware/evidence/symbol_style.py).
Electronics AI and future CAD authoring workflows should follow this convention.
It does not approve a package land pattern, ERC result or electrical circuit.


## Current passive pin-length exception (7 November2026)

For project-local resistor and capacitor symbols only, use pin length8 schematic
units (80mil), matching the shortest existing passive pins. Other families retain
their prior pin lengths. Keep the compact existing zigzag/plate graphics. This
shortening moves electrical tips toward the body; existing schematic instances
are not automatically updated. Tips can be off the100mil grid; a10mil snap grid
is needed for these new passive models. Review connectivity before any library
update of placed instances. See [verified change report](../../../docs/hardware/passive_pin_normalization.md).

##2026-11-08 closure additions

Keep the existing compactANSIzigzag resistors andtwo-plate capacitors with8-unit(80mil) pins. The closure changed model/verification metadata,not their graphics orconnectionpoints. New MMBT3904/DMP2035U use conventionalNPN/PMOS symbols. Functional AltiumIDs B/E/C andG/S/D deliberately match the exact manufacturerTOP-view positions;do not replace them with inferredgeneric numericpins. BSP remains the protected-deviceblock withIN/D/S/S_TAB. TDS/eFuse/otherIC blocks remain functionalblocks. No schematicinstance auto-update was performed.
