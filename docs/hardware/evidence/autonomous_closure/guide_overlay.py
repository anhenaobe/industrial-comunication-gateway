"""Final current-baseline overlay used by the existing guide generator."""
import re
from pathlib import Path
O=Path(__file__).parent
def apply(out,D):
 out=out.replace('2026-11-07','2026-11-08',1)
 out=out.replace('The user draws, places and routes; this document update changes no native CAD.',
  'The user completes manual capture/placement/routing. This closure saved one localized Power-sheet wire/label repair; its compiled connectivity remains unverified. All other native findings below await local correction.')
 matrix='''| Subsystem | Selected design | Connection specification | Source CAD readiness | Native implementation dependency |
|---|---|---|---|---|
| Input |0451002.MRL/SS3P6L/TDS3311P/TPS26620|Defined,including RTN and startup|Connector resolved;TPS EP mapping candidate|Recompile saved UVLO repair;verify distinct UVLO/OVP|
|3.3V buck|LMR36015FBRNXR,6.8uH|Defined|RNX A/B/inductor/passive lands verified|NC3-to-SW;CIN/CVCC bank;DNP PG/CFF|
|5V buck|LMR36015FBRNXR,10uH|Defined|Same|Replace16V CIN before power;complete bank/CVCC|
|MCU|STM32H723VET6/internalLDO|Core/clock/boot/debug defined|MCU lands verified;exact SWD/BOOT headers saved;reset viaJ3|C30;one1uF/one100nF missing;BOOT model migration|
|Ethernet PHY/clocks|DP83826IRHBR + two independent Kyocera25MHz oscillators|RMII Leader and MCU bypass defined|PHY/clock/ESD/R/C source lands verified|Clock performance bringup;ESD flow-through/ECO;assembly review|
|Magnetics/RJ45|HX1188FNL/SS-7188S-A-NF|Defined;two separate chassis AC branches|Source lands/holes/orientation verified|Move cable-cap returns/shields toCHASSIS;mechanical envelope/edge placement|
|RS485|THVD1420DR/115200baud|Defined;end-only termination optional|Exact connector/header/120ohm model saved|Place/wire connector and optional jumper|
|CAN-FD|ATA6561-GAQW/1Mbit nominal,2Mbit data target|Defined|Same connector/termination resources|Place/wire connector;verify startup standby|
|Two DI|ISO1212DBQR/Type3|Defined;isolation unchanged|DBQ/Firstohm/connector source lands verified|Correct R21/R22 field-side connections;floating substrate islands|
|Two DO|BSP75NTA + two NPN/PMOS5V drivers|Defined with explicit engineering margin/bringup limits|BSP and new Diodes models verified|Migrate U9 locally;wire both BSPs and external supply/loads|

These are specification/library states,not a claim that the native sheets match them.
See [closure report](electrical_closure_rev1.md) and section15 for the actual remaining corrections.
'''
 out=re.sub(r'\| Subsystem \|.*?(?=Use project-local)',matrix+'\n',out,count=1,flags=re.S)
 out=re.sub(r'\(saved readback: \*\*.*?See \[symbol verification\]\(symbol_library_verification.md\)\.',
  '(saved readback: **76 symbols /48 footprints**). LibPkg source references remain project-local. Existing IntLib is stale and was not recompiled. File validation: SchLib0errors/0warnings; PcbLib0errors/4intentional TPS EP-subpad overlap warnings. No current native compilation,ERC,DRC,placement or electrical test is claimed. See [closure report](electrical_closure_rev1.md).',out,count=1,flags=re.S)
 start=out.index('Ground/net policy:');end=out.index('## 1.',start)
 out=out[:start]+'''Ground/net policy: actual native **GND** is the common non-isolated electronics/source/DO return; GND_PWR describes its power-return role,not a separate isolated net. The native **24V** net is the protected electronics rail called24V_ELEC below; they must be one electrical net,never two disconnected aliases. Native **3.3V** is the logic rail;5V is separate. Keep existing flat-sheet ports consistent and verify compiled memberships after any label change. **EF_RTN** is a separate TPS reference (pins5/11);never short it toGND. **FIELD_COM** is the isolated DI return. **CHASSIS** is the RJ45 shield/cable-capacitor AC domain;no DC logic-ground bond is selected. External DO positive isDO_EXT_PLUS,not24V_ELEC. No ferrite/net-tie/impedance is added merely to rename grounds.

'''+out[end:]
 out=re.sub(r'\b3V3\b','3.3V',out).replace('VCORE_CAP','VCAP')
 out=out.replace('TPS footprint candidate and connector numbering remain visible practical tasks.','TPS pad-net transfer remains a native verification task;inputconnector1=positive/2=GND is defined in section15.')
 out=out.replace('No exact connector terminal numbering is approved.','JDI physical/project numbering isdefined:1FIELD_DI1_PLUS,2FIELD_DI2_PLUS,3FIELD_COM;see section15.')
 out=out.replace('Jack contact/current ratings remain unqualified despite its accepted pin map; copper annuli/holes and assembly stock are not approved.','Jack holepattern/orientation isverified. Copperannuli areprototypechoices;body/boardedge placement andassemblystock still require the actualboard/assembler review. Contactratings are not independently requalified.')
 out=out.replace('Normally-open reset button would short NRST to GND only after exact contact-pair model is known.','Optional onboard reset button isDNP;use debugger or a momentary externalcontact betweenJ3.4(NRST) andJ3.5(GND).')
 # Retain all original authoritative pin tables and update only resolved limits.
 a=out.index('**CAD unfinished:**');b=out.index('### F.',a)
 out=out[:a]+'''**TPS source CAD:** original `GW_DRC0010J_TI_TPS2662` remains a candidate because its four copper extensions have no proven pad-net inheritance. New `GW_DRC0010J_TI_TPS2662_EP11` has real central pad11 and aliases11A/11B/11C/11D;the union matches TI p44. Before binding it,Altium must map **one symbol pin11 to all five pads**,allEF_RTN,and verify that ECO/net readback transfers that net. Aliases are geometry segments,not extra manufacturer pins. Four overlap warnings are intentional only for this common-net construction. Do not use default1:1mapping. Existing symbol stays bound to the original candidate until that check. Alternative:make one native custom pad11 of the exact union. TI windowed paste is retained;thermal vias need explicit assembler treatment. Input connector is nowTB002-500-02BE,pin1positive/pin2GND by project convention;see section15.

Altium documents net inheritance for footprint routing primitives touching a mapped pad. Therefore first test the **existing**footprint in an isolatednativeECO:if allfourextensions acquireEF_RTN,no replacement is needed. This is a transfer-verification hold,not missing manufacturer dimensions or proof that the footprint is defective. For the alternate segmentedfootprint,PCBModel >PinMap >symbol11 >ModelPinDesignator uses `11,11A,11B,11C,11D`;keep allotherpins1:1. Altium21+ supports onepin-to-multiplepads;confirm actualECO/readback. [Official routing-primitive net behavior](https://www.altium.com/documentation/altium-designer/components-libraries/creating-pcb-footprint);[file-library PinMap procedure](https://www.altium.com/documentation/altium-designer/components-libraries/file-based-libraries/schematic).

'''+out[b:]
 out=out.replace('A/B footprint choice and stencil remain provisional.','Both A/B copper/mask/stencil patterns were independently compared with the saved feet2026-11-08. The package lot and assembler process must match the selected variant.')
 out=out.replace('Confirm delivered RNX0012A/B package and stencil before PCB use; neither SW12 nor NC3 is ground.','RNX A/B terminal positions agree. Saved A uses solder-mask-defined copper for1/2/10/11/12;B uses the preferred NSMD pattern. Confirm purchased package and assembler mask/stencil capability;neither SW12 nor NC3 is ground.')
 out=out.replace('provisional translator VCCA','MCU/DI/PHY logic').replace('CAN/translator logic','CAN and the new DO input drivers')
 out=out.replace('Inductor other end ->','Project inductorpin1(marked/shorted winding end) goes toSW;pin2 ->')
 out=re.sub(r'Debug header is the \*\*project-specific six-pin convention\*\*:.*?(?=\n\n)',
  'Debug header J3 is the **actual project-specific six-pin convention**: **1SWDIO,2GND,3SWCLK,4NRST,5GND,6VTref=3.3V sense**. This supersedes the older guide pin order;the existing user wiring is retained. Exact header `61300611121` / `GW_WRPHD_6X1_254_WURTH`;pin1 is the marked end,sequence+X in PCB TOP view. This is an unkeyed1x6 header,not the ARM standard. Wire the adapter to this table;VTref must not inject power. BOOT recovery header `61300211121`:pin1BOOT0,pin2=3.3V;normally OPEN,10k BOOT0-to-GND retained. SW1 currently performs BOOT recovery,not NRST reset;do not populate both a permanent boot shunt and a reset button under the same identity.',out,count=1,flags=re.S)
 out=out.replace('GPIO; **DO drive acceptance pending** | Translator2/3 candidate','GPIO; discrete5V driver selected | Channel1/2 base resistor,section10')
 out=out.replace('Header/button MPNs, mating orientation and exact terminal pairs are unresolved.','Header MPNs/hole patterns and project pin assignments are explicit. The unverified onboardNRST button placeholder isDNP;NRST is accessible at J3.4 and adjacentGND atJ3.5. Replace the existing BOOT SW1 locally with the verifiedBOOT header.')
 out=out.replace('no exact reset/header MPN drawing is available.','exact header drawings are referenced in section15;onboardNRST button is optionalDNP.')
 out=out.replace('Header terminal numbering remains provisional; do not short 3.3V directly to GND.','BOOT header1=BOOT0,2=3.3V,normally open;never short3.3V directly toGND.')
 # Connectors and optional bus-end components are now selected without new bus circuitry.
 out=out.replace('Connector physical pin numbers/ratings are unresolved.','UseTB002-500-03BE:1A,2B,3GND;project numbering/orientation in section15.')
 out=out.replace('Connector roles A/B/COM are selected; **numbered connector assignments await the exact drawing**.','RS connectorTB002-500-03BE: **1A(U6.6),2B(U6.7),3COM=GND(U6.5)**. Label polarity on both PCB and cable.')
 out=out.replace('Connector roles CANH/CANL/COM are selected, but exact physical terminal numbering is pending.','CAN connectorTB002-500-03BE: **1CANH(U7.7),2CANL(U7.6),3COM=GND(U7.2)**.')
 out=out.replace('Finish connector physical numbering. If used at a cable end, select the120Ω termination MPN/jumper.','Connector numbering is defined. Optional end termination isCRCW1206120RFKEA,120ohm1%0.25W,with61300211121 two-pin jumper,normallyOPEN;see section15.')
 out=out.replace('Finish connector physical numbering and optional bus-end120Ω termination/jumper.','Connector/end-termination models and exact connections are defined in section15.')
 out=out.replace('Finish connector physical numbering; keep SUB1/SUB2 floating separately and FIELD_COM isolated.','DI connectorTB002-500-03BE:1FIELD_DI1_PLUS,2FIELD_DI2_PLUS,3FIELD_COM. Keep SUB1/SUB2 floating separately and FIELD_COM isolated.')
 out=out.replace('exact MPN/jumper still unselected','exact MPN/jumper selected in section15').replace('exact MPN, jumper and model unresolved','exact MPN/jumper/model selected in section15')
 out=out.replace('Finish connector physical numbering.','Use the exact connector assignment in section15.')
 newdo=(O/'do_connections.md').read_text(encoding='utf-8').replace('DO1_CMD','DO1').replace('DO2_CMD','DO2')
 out=re.sub(r'## 10\..*?(?=## 11\.)',newdo+'\n\n',out,count=1,flags=re.S)
 # Historical closure notes are preserved in their dedicated reports,not left as
 # contradictory current instructions at the end of the primary guide.
 out=out[:out.index('## 11.')]+'''## 11. Current closure and preserved history

Current decisions are the2026-11-08 sections above and the [closure report](electrical_closure_rev1.md). Earlier TPS/NIS recovery,discrete graphics,BSP physical closure,andEthernet75ohm/1nF reports remain historical evidence. They do not restore translator approval or a missing-BSP-pinout claim. FourETH_RBOB remainCRCW080575R0FKEA/C844859;twoETH_CBOB remainC1206C102KGRACAUTO/C600002. Their two AC return nodes stay separate. No FKEAC substitution or safety-Y certification is inferred. Conditional CFF,optional RS surge,CAN bulk and DI-PE positions are DNP in the selected basic prototype. Full inventory/readback and pending work are linked from the closure report.

'''+(O/'native_actions.md').read_text(encoding='utf-8')
 return out
