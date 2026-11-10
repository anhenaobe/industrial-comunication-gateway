"""Validate audit artifacts and source preservation, without writing native CAD."""
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).parent
DOC = ROOT / 'docs/hardware'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))

before = read_json('native_files_hashes_before.json')
archive = read_json('reference_archive_inventory.json')
history = read_json('reference_history_records.json')
expected = dict(before)
expected[archive['archive']] = archive['sha256']
for entry in history:
    assert entry['archive'] not in expected or expected[entry['archive']] == entry['sha256']
    expected[entry['archive']] = entry['sha256']
after = {name: digest(name) for name in expected}
assert expected == after, 'A protected native source or archive changed'

with (DOC / 'pcb_rules_proposal.csv').open(encoding='utf-8-sig', newline='') as handle:
    reader = csv.DictReader(handle)
    fields = reader.fieldnames
    proposal = list(reader)
required = {
    'rule_name', 'altium_rule_type', 'intended_scope_query', 'second_scope_query',
    'net_or_component_class', 'minimum_value', 'preferred_value', 'maximum_value',
    'units', 'priority', 'supporting_source', 'verification_status',
    'required_user_decision', 'parameter', 'connective_check',
    'implementation_method', 'scope_verification', 'target_configuration_status',
}
assert required <= set(fields)
assert len(proposal) == 70
assert len({r['rule_name'] for r in proposal}) == 69
assert len({(r['rule_name'], r['parameter']) for r in proposal}) == 70
assert all(None not in r and all(v is not None and v.strip() for v in r.values()) for r in proposal)
assert {r['verification_status'] for r in proposal} <= {'VALID', 'CONDITIONALLY_VALID', 'BLOCKED'}

priorities = defaultdict(dict)
for row in proposal:
    assert int(row['priority']) > 0
    if row['implementation_method'] != 'NATIVE_RULE':
        continue
    assert row['target_configuration_status'] == 'MISSING - academic PcbDoc absent'
    rank = int(row['priority'])
    previous = priorities[row['altium_rule_type']].get(rank)
    assert previous in (None, row['rule_name']), (row['altium_rule_type'], rank, previous, row['rule_name'])
    priorities[row['altium_rule_type']][rank] = row['rule_name']
    for key in ('intended_scope_query', 'second_scope_query'):
        query = row[key]
        assert query.count("'") % 2 == 0
        depth = 0
        for char in query:
            depth += (char == '(') - (char == ')')
            assert depth >= 0
        assert depth == 0

with (OUT / 'actual_rules.csv').open(encoding='utf-8-sig', newline='') as handle:
    actual = list(csv.DictReader(handle))
assert len(actual) == 43
assert len({r['source'] for r in actual}) == 43
assert all('::Rules6/Data@' in r['source'] for r in actual)
assert Counter(r['classification'] for r in actual) == {
    'VALID': 5, 'INCORRECT': 7, 'CONDITIONALLY_VALID': 27, 'BLOCKED': 4,
}
saved = read_json('saved_board_records.json')[0]['extracted']['Rules6']
assert {r['rule_name'] for r in actual} == {r['fields']['NAME'] for r in saved}
assert next(r for r in actual if r['rule_name'] == 'Clearance_vias')['classification'] == 'INCORRECT'

academic = ROOT / 'hardware/academic_rev1'
assert not list(academic.rglob('*.PcbDoc'))
assert not list(academic.rglob('*.RUL'))
project = (academic / 'Industrial_Gateway_Academic.PrjPcb').read_text()
members = [line.split('=', 1)[1] for line in project.splitlines() if line.startswith('DocumentPath=')]
assert members == [r'libraries\Gateway_Academic.SchLib', r'libraries\Gateway_Academic.PcbLib']

report = (DOC / 'pcb_design_rules_audit.md').read_text(encoding='utf-8')
assert report.count('<!-- ACTUAL_RULES_START -->') == 1
assert report.count('<!-- ACTUAL_RULES_END -->') == 1
assert 'READY TO APPLY: NO' in report
for path in (DOC / 'pcb_design_rules_audit.md', OUT / 'actual_rules_table.md'):
    text = path.read_text(encoding='utf-8')
    assert '\ufffd' not in text
    assert all(line == line.rstrip() for line in text.splitlines()), path

diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert diff.returncode == 0, diff.stdout + diff.stderr
status = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, check=True)
(OUT / 'git_status_after.txt').write_text(status.stdout, encoding='utf-8')
result = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'native_source_preservation_pass': True,
    'protected_native_files_and_archives': len(after),
    'after_sha256': after,
    'academic_pcb_documents': 0,
    'academic_rul_files': 0,
    'academic_project_members': members,
    'proposal_parameter_rows': len(proposal),
    'proposal_named_constraints_or_gates': len({r['rule_name'] for r in proposal}),
    'actual_rule_records': len(actual),
    'actual_reuse_classifications': dict(Counter(r['classification'] for r in actual)),
    'proposal_schema_and_required_values_pass': True,
    'unique_parameter_keys_pass': True,
    'native_rule_priorities_per_type_pass': True,
    'query_quotes_and_parentheses_balanced': True,
    'native_query_parser_validation': 'NOT PERFORMED; handler blocked; classes and target board absent',
    'complete_actual_rule_coverage_and_source_locators_pass': True,
    'report_text_checks_pass': True,
    'git_diff_check_exit_code': diff.returncode,
    'git_diff_check_output': diff.stdout + diff.stderr,
    'no_native_writes_or_drc_executed': True,
}
(OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in result.items() if key != 'after_sha256'}, indent=2))
