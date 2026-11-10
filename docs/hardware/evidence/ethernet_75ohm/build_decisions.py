import json
from pathlib import Path
O=Path(__file__).parent;src='Vishay20035 Rev18-Jun-2018 p3 ordering/p9 body and REFLOW lands; exact C844859 catalog identity2026-11-07'
mpn='CRCW080575R0FKEA';fp='GW_CRCW0805_VISHAY_20035_REFLOW'
patch=dict(recommended_mpn=mpn,quantity=4,nominal_value='75 Ohm',tolerance='1%',power_rating='0.125 W at70C; derating applies',
 package='0805 resistor',rated_voltage_or_current='150 V limiting element; actual75Ohm continuous voltage limited bysqrt(P*R)',
 cad_route='PROJECT_LOCAL_VERIFIED',electrical_value_source=src,
 observations='Retained original75Ohm0805 selection; C844859 verified exact FKEA, not C1511836 FKEAC. Four positions: magnetics15/10 separately to nodeA; RJ45(4+5)/(7+8) separately to nodeB. Each node has its own1nF HV capacitor to chassis; no DC logic-ground bridge.')
decision=dict(patches={'ETH_RBOB':patch},record_fields={'ETH_RBOB':dict(design_approval='RETAINED_ORIGINAL_SELECTION',validation_scope='ACADEMIC_BASIC_ETHERNET_TERMINATION; NO_SURGE_CLAIM',test_status='NOT_ELECTRICALLY_TESTED')})
asset=dict(asset_id=mpn,item_kind='PASSIVE',component_ids=['ETH_RBOB'],mpn=mpn,symbol=mpn,footprint=fp,source=src,
 cad_status='CAD_VERIFIED',symbol_status='CAD_VERIFIED',footprint_status='CAD_VERIFIED',package_requirement=fp,
 limitations='Nonpolar project1/2 mapping; exact manufacturer reflow copper/body. Mask+.05mm and1:1paste are explicit process selections, not manufacturer prescribed. No hardware/surge/board qualification.',
 lcsc_code='C844859',datasheet_url='https://www.vishay.com/docs/20035/dcrcwe3.pdf',local_datasheet='hardware/academic_rev1/libraries/sources/ethernet_75ohm/C844859.pdf',
 availability_category='JLC Extended; C844859; public JSON-LD observed2026-11-07',stock_status='Catalog reports in_stock; exact assembly quantity unknown; recheck before order')
(O/'bom_decisions.json').write_text(json.dumps(decision,indent=2)+'\n');(O/'cad_assets.json').write_text(json.dumps([asset],indent=2)+'\n')
