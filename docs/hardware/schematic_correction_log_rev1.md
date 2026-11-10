# Academic Rev.1 — controlled correction log

> Actualización nativa 2026-11-10: ver [cierre y evidencia actual](closure_verification_rev1.md) y [BOM real por designador](assembly_bom_rev1.csv). Los pendientes de captura/modelos descritos debajo son históricos y quedan sustituidos por ese cierre; la validación del diálogo ECO sigue pendiente.


Initial read-only baseline: [schematic_audit_rev1.md](schematic_audit_rev1.md), saved before any native edit. All27 baseline findings remain preserved there. Four findings were corrected with eight individual property edits, without component replacement or wire regeneration.

## Before/after and evidence

| Finding / exact native file | Before | Applied correction | Verified result |
|---|---|---|---|
| A01 / Power.SchDoc | Both U2.12/U3.12 and L1/L2 switching ends shared SW | Two power ports at5600,5000 /8300,5300 → B3_SW; two at5600,3300 /8300,3600 → B5_SW | U2.12,L1.1,C10.1=B3_SW;U3.12,L2.1,C19.1=B5_SW; no shared switch node. TI SNVSB49D p4/Fig10-1 and guide2/3 |
| A03 / Power.SchDoc | U2/U3 VIN10 and EN9 on isolated Vin | Power port text Vin→24V at8500,5100 and8500,3400 | Both regulator VIN2/VIN10/EN9 now share TPS OUT10 net24V. Existing rail name preserved; no ground changes. TI p4 and guide2/3 |
| A09 / Ethernet.SchDoc | J2.2=TX+ with J2.1;T1.14 single-pin TX- | Label at9600,5000 TX+→TX- | J2.2 and T1.14 now TX-;J2.1/T1.16 remain TX+. Pulse HX1188FNL sheet2, Stewart CT710001 and guide6 |
| A12 / MCU.SchDoc | SWCLK label on PA12/71 | Move label7200,3500→actual PA14 electrical endpoint6400,4000 | U4.76=SWCLK;U4.71 becomes unused NetU4_71. PA13/72=SWDIO unchanged. ST DS13313 exact LQFP100/Table7/8 and guide4 |

Coordinates above are the native tool's schematic coordinate units, not PCB millimeters. The leftover wire stub at PA12 is now an unused single-pin net, reported by ERC; it is not a reassigned peripheral function. Debug header is still absent, so SWCLK/SWDIO remain single-pin debugger-access nets.

## Recovery and actual save behaviour

Before edits, Git status showed pre-existing firmware/poc changes and untracked hardware/docs. None were reverted. Project plus all five schematic sheets were copied to `hardware/academic_rev1/backups/native_schematic_audit_20261107/`; [SHA256 manifest](evidence/native_schematic_audit/correction_backups.json). Do not blindly restore over newer user work.

Native modifications each matched exactly one object, with no failed property writes. Connectivity was checked after the first separation and after the remaining batch. `proj_save` targeted the Academic project with `include_libraries=false`, reported verified. Saved CFB records were then independently read from disk and compared with the baseline, followed by native recompilation/ERC and a fresh437-pin net readback.

**Unexpected save effect:** Altium regenerated the `UNIQUEID` field on all437 pin records across Power/Ethernet/MCU/Field_IO, including the unedited Field_IO sheet. This was not requested. Editing stopped immediately upon detecting it; no speculative recovery or further native corrections were attempted. Component identities, designators, MPNs, electrical pin fields and model records did not change. TopLevel has no parsed record change, although its binary hash changed during project save. No claim of byte-identical preservation of unedited schematic files is made. The backups preserve the original identifiers. Before schematic-to-PCB transfer, review ECO identity association; do not accept an unexplained remove/re-add component ECO. No PCB changes were made.

The only non-UNIQUEID record differences are the eight intended label/power-object edits above. [Full saved-record diff](evidence/native_schematic_audit/saved_record_diff.json); [final pin table](evidence/native_schematic_audit/final_nets.json). All437 pin keys remain; exactly15 pin net-name records differ, entirely explained by the four corrections (including R6/R9 pull-up supply endpoints changing with Vin alias). No component/model selection changed. No professor library, source library, firmware or PCB was edited.

## Actual validation and remaining work

Native compilation returned `success:true`. Native ERC ran before and after corrections, each reporting105 violations; only100 detailed records were exposed by the tool. The returned errors changed as expected: TX- no longer single-pin; SWCLK now names pin76; PA12's leftover stub is newly reported. This is **not clean ERC**, and no DRC/electrical hardware test was performed. [Post ERC](evidence/native_schematic_audit/erc_after.json), [compile response](evidence/native_schematic_audit/compile_after.json). Five unexposed ERC details remain untriaged.

Remaining23 baseline findings are not claimed fixed. Native editing was halted because of the save identity side effect; use exact manual corrections in the initial report until that behaviour is understood. Priority:

1. Replace C7/C16 with selected100V input capacitors and populate the missing second4.7µF capacitor per buck. Correct upper feedback R5/R8 to100k exact selected MPN; retain R7=43.2k,R10=24.9k. Replace stale CVCC parts with selected2.2µF parts; implement per-buck NC3-to-SW12; reconcile PG/CFF DNP positions.
2. Correct DI R21/R22 free ends away from logic OUT1/2 to separate external field inputs, preserving FIELD_COM isolation; obtain separate ground-boundary approval before implementing the affected domain changes. Correct the Ethernet capacitor/chassis returns under the same restriction; do not silently ground shields.
3. Replace D2 with approved TDS3311P.C using its verified model, preserving shunt connections. Complete missing PHY ESD, bus/DI/DO connectors, SWD/reset access and explicit BSP wiring. Do not choose unknown connector pin numbering.
4. Bind missing instance footprint models locally, close TPS/custom-pad and other candidate package checks in the next footprint task. No mass footprint creation or global library update was performed.
5. Resolve four dummy TopLevel child filenames without guessing intended block mapping; retain established peripheral assignments. Complete loaded BSP drive/default-OFF acceptance separately; no driver substitution is approved here.

Status: **NO-GO for PCB transfer/power-up of the present circuit** until the critical/major electrical errors are closed. No industrial qualification requirement is involved.

Final checks: saved native readback and all437 compiled pin records matched the expected post-change state. PCB, project definition, professor libraries and all source SchLib/PcbLib hashes remained unchanged. `git diff --check` passed with pre-existing CRLF notices. No commit/push. The complete44-identity placed inventory plus6 additional concrete required-BOM identities is saved in Markdown/CSV.
