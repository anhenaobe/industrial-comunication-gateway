"""Generate reviewable CAD preparation tables; never generates a circuit or PCB.

Run with Python 3 from any directory. Uses only the standard library.
The source pin table was transcribed from DS13313 Rev5, table 7, LQFP100.
These are proposed reservations, not a Zephyr DTS or approved netlist.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_csv(name):
    with (HERE / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name, headers, rows):
    with (HERE / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


pins = read_csv("mcu_pin_reference.csv")
assert sorted(int(r["physical_pin"]) for r in pins) == list(range(1, 101))
by_name = {r["pin_name"]: int(r["physical_pin"]) for r in pins if r["pin_name"].startswith("P")}
for power, expected in [("VDD", {11, 27, 50, 75, 100}), ("VSS", {10, 26, 49, 74, 99}), ("VCAP", {48, 73})]:
    assert {int(r["physical_pin"]) for r in pins if r["pin_name"] == power} == expected

reservations = [
    ("Ethernet", "PA1", "ETH_RMII_REF_CLK", "AF11", "input", "PHY clock topology not closed"),
    ("Ethernet", "PA2", "ETH_MDIO", "AF11", "bidirectional", "management bus"),
    ("Ethernet", "PC1", "ETH_MDC", "AF11", "output", "management bus"),
    ("Ethernet", "PA7", "ETH_RMII_CRS_DV", "AF11", "input", "reserve for RMII"),
    ("Ethernet", "PC4", "ETH_RMII_RXD0", "AF11", "input", "reserve for RMII"),
    ("Ethernet", "PC5", "ETH_RMII_RXD1", "AF11", "input", "reserve for RMII"),
    ("Ethernet", "PB11", "ETH_RMII_TX_EN", "AF11", "output", "excludes USART3_RX on PB11"),
    ("Ethernet", "PB12", "ETH_RMII_TXD0", "AF11", "output", "excludes FDCAN2_RX on PB12"),
    ("Ethernet", "PB13", "ETH_RMII_TXD1", "AF11", "output", "excludes FDCAN2_TX on PB13"),
    ("Ethernet", "PD12", "PHY_RESET_N", "GPIO", "output", "hold reset until supply and clock valid"),
    ("Ethernet", "PD13", "PHY_IRQ_N", "GPIO", "input", "optional; pin function depends on PHY mode"),
    ("RS485", "PD8", "RS485_TX", "AF7 USART3_TX", "output", "THVD1420 D pin4"),
    ("RS485", "PD9", "RS485_RX", "AF7 USART3_RX", "input", "THVD1420 R pin1"),
    ("RS485", "PD10", "RS485_DIR", "GPIO", "output", "DE and /RE joined; default low means receive"),
    ("CAN", "PB8", "CAN_RX", "AF9 FDCAN1_RX", "input", "ATA6561 RXD pin4; not FDCAN2"),
    ("CAN", "PB9", "CAN_TX", "AF9 FDCAN1_TX", "output", "ATA6561 TXD pin1"),
    ("CAN", "PD11", "CAN_STBY", "GPIO", "output", "default standby high; pull network not finalized"),
    ("DI", "PE0", "DI1_LOGIC", "GPIO", "input", "ISO1212 OUT1 pin4; no 24V on GPIO"),
    ("DI", "PE1", "DI2_LOGIC", "GPIO", "input", "ISO1212 OUT2 pin5; no 24V on GPIO"),
    ("DO", "PE2", "DO1_CMD", "GPIO", "output", "default OFF; level-stage guarantee still open"),
    ("DO", "PE3", "DO2_CMD", "GPIO", "output", "default OFF; level-stage guarantee still open"),
    ("Power", "PD14", "EFUSE_FAULT_N", "GPIO", "input", "optional open-drain pull-up to 3.3V"),
    ("Power", "PD15", "PG_3V3", "GPIO", "input", "optional; no 24V on GPIO"),
    ("Power", "PC6", "PG_5V", "GPIO", "input", "optional pull-up to 3.3V; USART6_TX excluded"),
    ("Debug", "PA13", "SWDIO", "SYS", "bidirectional", "dedicated SWD"),
    ("Debug", "PA14", "SWCLK", "SYS", "input", "dedicated SWD"),
    ("Debug", "PB3", "SWO", "AF0", "output", "optional; keep until debug connector frozen"),
    ("Console", "PA9", "CONSOLE_TX", "AF7 USART1_TX", "output", "3.3V external USB-UART; no on-board bridge required"),
    ("Console", "PA10", "CONSOLE_RX", "AF7 USART1_RX", "input", "3.3V external USB-UART"),
    ("Clock", "PH0", "HSE_IN", "OSC", "input", "crystal/oscillator selection still open"),
    ("Clock", "PH1", "HSE_OUT", "OSC", "output", "crystal/oscillator selection still open"),
    ("Indicator", "PB0", "STATUS_LED", "GPIO", "output", "optional; resistor/current not finalized"),
]
assert len({r[1] for r in reservations}) == len(reservations)
assert len({r[2] for r in reservations}) == len(reservations)
assert all(r[1] in by_name for r in reservations)
write_csv("pin_reservations.csv", ["block", "port", "net", "function", "direction", "notes", "physical_pin", "status", "evidence"],
          [(*r, by_name[r[1]], "PROPOSED_NOT_ROUTED", "DS13313 Rev5 tables7-8") for r in reservations])

# Requirements and reference values; unresolved selections are deliberately explicit.
# Quantities are for this academic scope only, not Rev.A and not a procurement BOM.
passives = [
    ("MCU", "C_VDD", 5, "100nF", "X7R; suitable effective capacitance at3.3V", "TBD", "new MPN; reject teacher Y5V as automatic substitute", "AN5419 table2; five VDD pins in DS13313", "VALUE_REFERENCE_MPN_OPEN"),
    ("MCU", "C_VDD_BULK", 1, "4.7uF", "ceramic; effective capacitance and voltage rating TBD", "TBD", "new", "AN5419 table2", "VALUE_REFERENCE_MPN_OPEN"),
    ("MCU", "C_VCAP", 2, "2.2uF", "+/-20% effective; ESR<100mOhm; LDO mode", "GRM188R71A225KE15D candidate", "new; primary datasheet download failed; bias/ESR not qualified", "DS13313 table14; Murata exact product reference", "CANDIDATE_NOT_FROZEN"),
    ("MCU", "C_VDDA_1", 1, "1uF", "ceramic", "CL10A105KB8NNNC candidate", "teacher symbol/footprint present; effective C not qualified", "AN5419 table2; library_inventory.csv", "VALUE_REFERENCE_MPN_OPEN"),
    ("MCU", "C_VDDA_2", 1, "100nF", "ceramic", "TBD", "new", "AN5419 table2", "VALUE_REFERENCE_MPN_OPEN"),
    ("MCU", "C_VBAT", 2, "1uF + 100nF", "VBAT tied to3.3V without battery", "TBD", "count is two capacitors, not two pairs", "AN5419 table2", "VALUE_REFERENCE_MPN_OPEN"),
    ("MCU", "VREF_network", "TBD", "TBD", "VREF+ to analog supply or supported reference; no conflicting VREFBUF", "TBD", "not frozen", "DS13313 + AN5419 table2", "OPEN"),
    ("MCU", "HSE_NRST_BOOT_SWD", "TBD", "TBD", "clock, CL, reset and BOOT network; debug connector", "TBD", "not frozen", "AN5419; DS13313", "OPEN"),
    ("Ethernet", "R_RBIAS", 1, "6.49kOhm", "1%", "CRCW04026K49FKED reference", "new exact MPN from EVM", "DP83826I pin10; DP83826EVM R48", "VALUE_REFERENCE_CAD_OPEN"),
    ("Ethernet", "decoupling_straps_clock_MDI", "TBD", "TBD", "full exact network must be selected from reference and mode", "TBD", "reference schematic downloaded; not copied blindly", "DP83826I sections8.4/9; EVM main schematic", "OPEN"),
    ("RS485", "C_RS", 1, "100nF", "ceramic near VCC8/GND5", "TBD", "new X7R MPN", "THVD1420 supply recommendations", "VALUE_REFERENCE_MPN_OPEN"),
    ("RS485", "R_RS_TERM", 1, "120Ohm", "select power/derating; jumper at end of bus", "TBD", "teacher120Ohm0.1W not approved for all conditions", "THVD1420 application transmission-line termination", "VALUE_REFERENCE_RATING_OPEN"),
    ("RS485", "R_DIR_PULL", 1, "TBD", "pull-down; DE and /RE default receive", "TBD", "teacher10k available but leakage/drive check pending", "THVD1420 control truth table", "OPEN"),
    ("RS485", "bus_protection_bias", "TBD", "TBD", "external bias only if justified; protection by fault/surge target", "TBD", "not frozen", "THVD1420 fail-safe and transient sections", "OPEN"),
    ("CAN", "C_CAN_VCC", 1, "100nF", "ceramic near VCC3/GND2", "TBD", "new X7R MPN", "Microchip DS50002649A fig4-1", "VALUE_REFERENCE_MPN_OPEN"),
    ("CAN", "C_CAN_VIO", 1, "100nF", "ceramic near VIO5/GND2", "TBD", "new X7R MPN", "Microchip DS50002649A fig4-1", "VALUE_REFERENCE_MPN_OPEN"),
    ("CAN", "C_CAN_BULK", "TBD", "TBD", "depends on local5V supply; 22uF is reference example, not mandatory", "TBD", "do not add blindly to buck Cout", "Microchip DS50002649A fig4-1 note1", "OPEN"),
    ("CAN", "R_CAN_TERM", 1, "120Ohm", "simple removable termination; power/derating TBD", "TBD", "no split termination selected", "Microchip DS50002649A section3.5", "VALUE_REFERENCE_RATING_OPEN"),
    ("CAN", "control_pulls_and_TVS", "TBD", "TBD", "TXD recessive and STBY high at reset; compatible bus protection", "TBD", "not frozen", "DS20005991B; DS50002649A", "OPEN"),
    ("DI", "R_DI_SENSE", 2, "562Ohm", "1%; 0.1W at70C; 0603", "RC0603FR-07562RL", "new; manufacturer specsheet downloaded; footprint qualification pending", "ISO1212 section8.2.1.2.1; Yageo exact specsheet", "VALUE_AND_MPN_REFERENCE_CAD_OPEN"),
    ("DI", "R_DI_THR", 2, "1kOhm", "MELF >=0.25W with surge/pulse checks", "TBD", "teacher1k0603_0.1W rejected for this role", "ISO1212 section8.2.1.2.1 and table8-1 Type3", "VALUE_REFERENCE_PACKAGE_OPEN"),
    ("DI", "C_DI_IN", 2, "10nF", "100V X7R10%; 0603 candidate", "C0603C103K1RACTU", "new; exact KEMET specsheet downloaded; pulse/derating and layout open", "ISO1212 table8-1 Type3; KEMET specsheet", "VALUE_AND_MPN_REFERENCE_CAD_OPEN"),
    ("DI", "C_DI_VCC1", 1, "100nF", "ceramic on logic side", "TBD", "new X7R MPN", "ISO1212 section8.2.1.1", "VALUE_REFERENCE_MPN_OPEN"),
    ("DI", "PE_filter_optional", "TBD", "TBD", "no PE capacitor until isolation/ground strategy set", "TBD", "500pF is maximum effective guidance in referenced surge setup, not automatic BOM", "ISO1212 fig8-9", "OPEN"),
    ("DO", "C_TRANSLATOR", 2, "100nF each", "one bypass per VCCA/VCCB", "TBD", "new X7R MPN", "SN74LVC2T45 supply recommendations", "VALUE_REFERENCE_MPN_OPEN"),
    ("DO", "control_pulls_series_load_clamp", "TBD", "TBD", "OFF on reset/power loss; verify VIN>=4.5V for BSP protection", "TBD", "do not freeze series resistors or inductive-load limits", "BSP75N p4; SN74LVC2T45 table5.5", "BLOCKED_VOH_AND_LOAD"),
    ("Power", "D_REVERSE", 1, "60V3A Schottky candidate", "SMPC; thermal and surge coordination required", "SS3P6L-M3/86A", "CAD copied from neighbor; not verified dimensionally", "Vishay88987; single-input proposal", "CANDIDATE_NOT_FROZEN"),
    ("Power", "R_EFUSE_LIM", 1, "43.2kOhm", "E96; tolerance and worst-case trip review pending", "TBD", "baseline reference retained; not a guaranteed1.4A threshold", "master6.4; NIS3071 fig5 MT3/MT4", "VALUE_BASELINE_PARTIAL"),
    ("Power", "EFUSE_caps_dvdt_EN_FAULT", "TBD", "TBD", "inrush, input/output overshoot, default EN and FAULT", "TBD", "no C_DVDD pin exists on selectedNIS3071", "NIS3071 table1 and application", "OPEN"),
    ("Buck3V3", "L3", 1, "6.8uH guide", "Isat/Irms/DCR/losses not selected", "TBD", "do not reuse historicalLMR66420 or AR22uH", "LMR36015FB table10-1", "GUIDE_NOT_FROZEN"),
    ("Buck5V", "L5", 1, "10uH guide", "Isat/Irms/DCR/losses not selected", "TBD", "teacher10uH parts not automatically qualified", "LMR36015FB table10-1", "GUIDE_NOT_FROZEN"),
    ("Bucks", "C_IN", "2 sets", "4.7uF +2x220nF per IC guide", "check effective C; rated for input/clamp and derating", "TBD", "no copy of47nF bypass or310nF effective Cin from AR BOM", "LMR36015 section10.2.1.2.6", "GUIDE_NOT_FROZEN"),
    ("Bucks", "C_OUT", "2 sets", "3x15uF per IC guide", "minimum/effective C, ESR and loop by rail", "TBD", "not an approved common BOM", "LMR36015 table10-1", "GUIDE_NOT_FROZEN"),
    ("Buck3V3", "R_FB3", 2, "100k +43.2kOhm guide", "1V feedback reference; tolerances not closed", "TBD", "not eFuse R_LIM", "LMR36015 table10-1", "GUIDE_NOT_FROZEN"),
    ("Buck5V", "R_FB5", 2, "100k +24.9kOhm guide", "1V feedback reference; tolerances not closed", "TBD", "AR resistors are candidates only", "LMR36015 table10-1", "GUIDE_NOT_FROZEN"),
    ("Bucks", "C_FF", 2, "20pF guide", "loop check by rail", "TBD", "not teacher33pF substitute", "LMR36015 table10-1", "GUIDE_NOT_FROZEN"),
    ("Bucks", "C_BOOT", 2, "100nF >=16V", "BOOT-SW", "TBD", "new; AR10V part not automatically approved", "LMR36015 section10.2.1.2.7", "VALUE_REFERENCE_MPN_OPEN"),
    ("Bucks", "C_VCC", 2, "1uF16V", "VCC-GND internal bias only", "TBD", "teacher1uF50V possible after capacitance qualification", "LMR36015 section10.2.1.2.8", "VALUE_REFERENCE_MPN_OPEN"),
    ("Bucks", "EN_PG_input_protection", "TBD", "TBD", "no floatingEN; PG pull-up domain3.3V if used", "TBD", "supply sequencing and UVLO still open", "LMR36015 pin table and application", "OPEN"),
]
write_csv("passive_worklist.csv", ["block", "group", "qty_academic", "value", "requirements", "mpn", "reuse", "evidence", "status"], passives)

cad = [
    ("STM32H723VET6", 1, "LQFP10014x14mm0.5mm", "missing", "missing", "ST CAD resources; DS13313 fig64-65", "all100pins now indexed; geometry/import pending"),
    ("DP83826IRHBR", 1, "RHB32_5x5mm_EP", "missing", "missing", "TI UltraLibrarian RHB32; EVM reference downloaded", "mode/straps/clock/MDI network not frozen"),
    ("THVD1420DR", 1, "SOIC8_D", "missing", "missing", "TI CAD D8; SLLSF78B", "prefer largeSOIC; protect bus"),
    ("ATA6561-GAQW", 1, "SOIC8", "missing", "missing", "Microchip DS20005991B; evaluation guide downloaded", "confirm suffix and noVDFN substitution"),
    ("ISO1212DBQR", 1, "SSOP16_DBQ", "missing", "missing", "TI CAD DBQ16; SLLSEY7G", "SUB1/SUB2 floating copper islands; notGND"),
    ("BSP75NTA", 2, "SOT223_TypeDN", "missing", "missing", "Diodes DS33016", "tab=source; never assume regulatorSOT223 pinout"),
    ("SN74LVC2T45DCTR candidate", 1, "SSOP8_DCT", "missing", "missing", "TI CAD DCT8; SCES516N", "VOH guarantee at BSP input load open; noOE pin"),
    ("LMR36015FBRNXR proposed", 2, "RNX12_2x3mm_HotRod", "missing", "missing", "TI CAD RNX12; SNVSB49D", "sharedICCAD; two distinctpassiveBOMs still needed"),
    ("NIS3071MT4TWG", 1, "WQFN16_CASE510CM", "missing", "missing", "onsemi NIS3071D Rev3", "padGND and unusedchannels must be present"),
    ("TDS3011P.C candidate", 1, "DFN6_1.6x1.6mm", "missing", "missing", "Semtech TDS3011P", "singleinput coordination still open"),
    ("SS3P6L-M3/86A candidate", 1, "SMPC_TO277A", "local_unverified", "local_unverified", "libraries/SS3P6L-M386A.*; Vishay88987", "PN association checked; pin/pad/thermal qualification pending"),
    ("HX1188FNLT reference", 1, "SMT12.7x9.09mm", "missing", "missing", "DP83826EVM T2; Pulse product finder", "not yet selected; pinout and manufacturer sheet pending"),
    ("SS-7188S-A-NF reference", 1, "RJ45_TH", "missing", "missing", "DP83826EVM J17", "not yet selected; no invented compatibleMagJack"),
    ("ECS-250-12-33Q-JES-TR reference", 1, "crystal3.2x2.5mm", "missing", "missing", "DP83826EVM XTAL1", "CL and clock topology not frozen"),
    ("RC0603FR-07562RL", 2, "0603", "missing_exactMPN", "generic_present_unverified", "Yageo specsheet; Professor_shared.PcbLib0603_res", "verify dimensions before binding"),
    ("C0603C103K1RACTU", 2, "0603", "missing_exactMPN", "generic_present_unverified", "KEMET specsheet; Professor_shared.PcbLib0603_cap", "not equivalent to copiedCL10B10325V"),
    ("RTHR1kMELF>=0.25W", 2, "MELF_TBD", "missing", "missing", "ISO1212 section8.2.1.2.1", "exactMPN and pulse qualification open"),
    ("Teacher pasives and headers", "perworklist", "0603/0805/TH", "local_unverified", "local_unverified", "libraries/Professor_shared.*", "CAD presence only; ratings and geometry still require check"),
]
write_csv("cad_queue.csv", ["mpn_or_requirement", "qty", "package", "symbol", "footprint", "evidence", "blocking_notes"], cad)

# Pin-level interface definitions from the named data sheets, without speculative field networks.
interfaces = []
for ref, pin, name, net, note in [
    ("U_RS",1,"R","RS485_RX","toMCU_PD9"), ("U_RS",2,"/RE","RS485_DIR","sharedDE;/RE; default low=receive"),
    ("U_RS",3,"DE","RS485_DIR","sharedDE;/RE"), ("U_RS",4,"D","RS485_TX","fromMCU_PD8"),
    ("U_RS",5,"GND","GND","logicandbusreference_nonisolated"), ("U_RS",6,"A","RS485_A","protectionnetworkOPEN"),
    ("U_RS",7,"B","RS485_B","protectionnetworkOPEN"), ("U_RS",8,"VCC","3V3","local100nF"),
    ("U_CAN",1,"TXD","CAN_TX","fromMCU_PB9"), ("U_CAN",2,"GND","GND","logicandbusreference_nonisolated"),
    ("U_CAN",3,"VCC","5V","local100nF"), ("U_CAN",4,"RXD","CAN_RX","toMCU_PB8"),
    ("U_CAN",5,"VIO","3V3","local100nF;ATA6561notATA6560"), ("U_CAN",6,"CANL","CAN_L","protectionandterminationOPEN"),
    ("U_CAN",7,"CANH","CAN_H","protectionandterminationOPEN"), ("U_CAN",8,"STBY","CAN_STBY","defaultstandbyhigh;pullOPEN"),
    ("U_DI",1,"GND1","GND","logicground"), ("U_DI",2,"VCC1","3V3","local100nF"),
    ("U_DI",3,"EN","3V3","tiehighperdatasheet"), ("U_DI",4,"OUT1","DI1_LOGIC","toMCU_PE0"),
    ("U_DI",5,"OUT2","DI2_LOGIC","toMCU_PE1"), ("U_DI",6,"NC","NC","leaveunconnected"),
    ("U_DI",7,"NC","NC","leaveunconnected"), ("U_DI",8,"GND1","GND","logicground"),
    ("U_DI",9,"FGND2","DI2_FGND","field;neverautomaticallyshorttologicGND"),
    ("U_DI",10,"IN2","DI2_IN_IC","RSENSEbetweenSENSEandIN;fig8-2visuallychecked"),
    ("U_DI",11,"SENSE2","DI2_SENSE_IC","RTHRfromfield;CINfromSENSEtoFGND;fig8-2"),
    ("U_DI",12,"SUB2","DI2_SUB_ISLAND","floating2x2mm;notFGND/GND/SUB1"),
    ("U_DI",13,"SUB1","DI1_SUB_ISLAND","floating2x2mm;notFGND/GND/SUB2"),
    ("U_DI",14,"FGND1","DI1_FGND","field;neverautomaticallyshorttologicGND"),
    ("U_DI",15,"IN1","DI1_IN_IC","RSENSEbetweenSENSEandIN;fig8-2visuallychecked"),
    ("U_DI",16,"SENSE1","DI1_SENSE_IC","RTHRfromfield;CINfromSENSEtoFGND;fig8-2"),
]:
    source = {"U_RS":"THVD1420 table4-1", "U_CAN":"DS20005991B SOIC8 pinout", "U_DI":"ISO1212 table4-2"}[ref]
    interfaces.append((ref,pin,name,net,note,source,"PIN_MAPPING_CHECKED_CIRCUIT_NOT_RELEASED"))
write_csv("interface_pin_checks.csv", ["reference", "pin", "pin_name", "proposed_net", "notes", "source", "status"], interfaces)

for ref, count in [("U_RS",8),("U_CAN",8),("U_DI",16)]:
    assert {r[1] for r in interfaces if r[0]==ref} == set(range(1,count+1))
assert len({(r[0],r[1]) for r in interfaces}) == len(interfaces)

connections = []
for ch in (1, 2):
    connections.extend([
        (f"R_DI{ch}_THR", "1kOhm", f"DI{ch}_FIELD_PLUS", f"DI{ch}_SENSE_IC", "MELF>=0.25W; exactMPN and pulse rating open", "ISO1212 fig8-2/table8-1 Type3"),
        (f"R_DI{ch}_SENSE", "562Ohm1%", f"DI{ch}_SENSE_IC", f"DI{ch}_IN_IC", "RC0603FR-07562RL; CAD mapping still open", "ISO1212 fig8-2"),
        (f"C_DI{ch}_IN", "10nF100V_X7R", f"DI{ch}_SENSE_IC", f"DI{ch}_FGND", "C0603C103K1RACTU candidate; field surge test not performed", "ISO1212 fig8-2/table8-1"),
    ])
connections.extend([
    ("C_DI_LOGIC", "100nF", "3V3", "GND", "place atU_DI pins2/1,8; MPN open", "ISO1212 section8.2.1.1"),
    ("C_CAN_VIO", "100nF", "3V3", "GND", "place atU_CAN pins5/2; MPN open", "DS50002649A fig4-1"),
    ("C_CAN_VCC", "100nF", "5V", "GND", "place atU_CAN pins3/2; MPN open", "DS50002649A fig4-1"),
])
write_csv("reference_connections.csv", ["component_group", "reference_value", "node1", "node2", "limitations", "source"], connections)

# Recalculate academic loads from the original conditioned engineering budget.
# This does not convert those assignments into measured or guaranteed maximum loads.
i3 = (534.303 - 50.0 - 1.9) / 1000
i5 = 72.403 / 1000
electrical = dict(
    supply_budget=dict(i3v3_A=i3, i5v_A=i5, p3v3_W=3.3*i3, p5v_W=5*i5,
                       note="Subtract one assigned50mA RS485 and one1.9mA ISO1212 from master; two DO and CAN retained; conversion losses unknown"),
    di=dict(channels=2, Rsense_ohm=562, Rthr_ohm=1000, Cin_F=10e-9,
            assumed_budget_current_per_channel_A=2.75e-3,
            Rthr_continuous_power_W=(2.75e-3)**2*1000,
            Rsense_continuous_power_upper_bound_W=(2.75e-3)**2*562,
            note="DC screening only; RTHR still MELF>=0.25W per TI surge recommendation; does not validate pulse/EMC"),
    bucks=[],
    source="LMR36015 SNVSB49D sections8.5/8.6/10.2.1.2; master6.7",
    not_verified=["loop stability", "efficiency", "thermal performance", "start-up/inrush", "actual inductor", "effective capacitors", "full DO drive margin", "input surge/continuous OV"],
)
for vout, l_nom, load, rfbb in [(3.3,6.8e-6,0.7,43200),(5.0,10e-6,0.1,24900)]:
    l_min=l_nom*0.8
    delta=vout*(1-vout/30)/(l_min*0.85e6)
    ton=vout/(30*1.15e6)
    electrical["bucks"].append(dict(target_V=vout,nominal_L_H=l_nom,assumed_L_tolerance=0.20,
        assumed_frequency_min_Hz=0.85e6,assumed_frequency_max_Hz=1.15e6,
        deltaIpp_at_30V_Lmin_fmin_A=delta,peak_at_design_load_A=load+delta/2,
        valley_at_design_load_A=load-delta/2,inductor_rms_at_design_load_A=math.sqrt(load*load+delta*delta/12),
        ideal_on_time_at_30V_fmax_s=ton,minimum_on_time_reference_s=83e-9,
        recommended_Isat_floor_before_temperature_derating_A=2.8,
        feedback_Rtop_ohm=100000,feedback_Rbottom_ohm=rfbb,
        feedback_nominal_V=1+100000/rfbb,
        feedback_static_min_V=0.985*(1+100000*0.99/(rfbb*1.01)),
        feedback_static_max_V=1.015*(1+100000*1.01/(rfbb*0.99)),
        note="Guide values screened; resistor1%/reference1.5% endpoints only; ignores ripple/transients; current-limit table is open-loop tested, not a closed-loop overshoot bound"))
(HERE/"electrical_screening.json").write_text(json.dumps(electrical,indent=2)+"\n",encoding="utf-8")

library_manifest = json.loads((HERE/"libraries/library_manifest.json").read_text())
for entry in library_manifest:
    path=HERE/"libraries"/entry["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry["sha256"],path
sources=json.loads((HERE/"libraries/sources/acquisition_manifest.json").read_text())
for entry in sources:
    if "sha256" in entry:
        path=HERE/"libraries/sources"/entry["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry["sha256"],path

summary = dict(physical_mcu_pins=100,proposed_gpio_reservations=len(reservations),
               passive_requirement_groups=len(passives),cad_queue_entries=len(cad),
               interface_pins_checked=len(interfaces),library_files_hash_checked=len(library_manifest),
               source_files_hash_checked=sum("sha256" in e for e in sources),
               reference_connections=len(connections),
               actual_project_created=False,schematic_blocks_drawn=0,pcb_started=False,
               complete_electrical_blocks_released=0,
               validation="CSV consistency, physical-pin uniqueness, interface pin coverage, file hashes; NOT ERC/DRC or circuit validation")
(HERE/"preparation_checks.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
