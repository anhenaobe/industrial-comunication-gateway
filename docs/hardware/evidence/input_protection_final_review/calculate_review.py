"""Review calculations; engineering assumptions are inputs, not manufacturer guarantees."""
import json
from pathlib import Path
p=Path(__file__).parent
rails={'3V3':{'voltage_V':3.3,'allocation_A':.7},'5V':{'voltage_V':5.,'allocation_A':.1}}
power=sum(r['voltage_V']*r['allocation_A'] for r in rails.values())
# Screening assumptions deliberately labelled; source/capacitance bounds remain absent.
efficiency=.75;v_source=18;series_drop_allowance=.60;efuse_bias_allowance=.0012
r_hot=.155
i=power/(efficiency*(v_source-series_drop_allowance))+efuse_bias_allowance
for _ in range(10):i=power/(efficiency*(v_source-series_drop_allowance-i*r_hot))+efuse_bias_allowance
out=dict(rails=rails,output_power_W=power,external_DO_load_current_excluded_A=1.,
    screening_assumptions={'buck_efficiency':efficiency,'source_min_V':v_source,
        'series_drop_allowance_V':series_drop_allowance,'efuse_bias_allowance_A':efuse_bias_allowance,
        'hot_channel_resistance_ohm':r_hot,'guaranteed_application_bounds':False},
    screening_electronics_input_A=i,efuse_hot_conduction_W=i*i*r_hot,
    diode_drop_loss_W=i*series_drop_allowance,
    bare_rail_input_A=power/(efficiency*v_source),
    minimum_required_downstream_ceramic_uF=2*(4.7+2*.220),
    default_ramp_example_not_bound={'ramp_s':.0015,'V':30,
        'charging_A_at_minimum_required_C':2*(4.7+2*.220)*1e-6*30/.0015,
        'total_A':i+2*(4.7+2*.220)*1e-6*30/.0015},
    candidate_RLIM_ohm=62000,typical_ITH_A_approx=1.,typical_ICB_A_approx=2.,
    threshold_tolerance_bound_at_62k='not specified by table3; typical curves only',
    worked_example_only={'Cmax_F':100e-6,'Icap_budget_A':.3,'max_voltage_V':30,
        'minimum_ramp_s':100e-6*30/.3,'Cdvdt_at_24V25C_pF_approx':65,
        'approved':False},
    final_Cmax_F=None,final_Cdvdt_F=None,final_source_fault_A=None,
    fault_pullup_current_A=3.3/15000,fault_pullup_resistor_W=3.3**2/15000,
    TDS3311_max_clamp_headroom_to_60V_V=60-42,
    TDS3311_working_margin_at30V_V=33-30,
    nominal_30V_plus5pct_V=30*1.05)
(p/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
