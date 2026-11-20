#!/usr/bin/env python3
"""Read-only structural check. Not a proof that the app exists or Codex read docs."""
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md','README.md','docs/PRODUCT.md','docs/FIRST_PROMISE.md',
    'docs/REFERENCE_ARCHITECTURE.md','docs/MODEL_SELECTION.md',
    'docs/VERIFICATION_POLICY.md','docs/OSS_POLICY.md',
    'docs/DECISIONS.md','docs/STATUS.md','docs/DEMO.md',
    'docs/DECISION_AUTHORITY.md','docs/SESSION_PROTOCOL.md',
    'tasks/NEXT.md','tasks/BOOT-001.md','tasks/EXECPLAN_RULES.md',
    'tasks/EXECPLAN_TEMPLATE.md','tasks/P1-001_MODEL_FIT.md',
    'tasks/WORK_LOG.md','reports/REPORT_TEMPLATE.md','reports/README.md',
    'governance/OSS_REGISTER.csv',
]
errors = [f'Missing {p}' for p in REQUIRED if not (ROOT / p).is_file()]
if not errors:
    for p in REQUIRED:
        if not (ROOT / p).read_text(encoding='utf-8').strip():
            errors.append(f'Empty {p}')
try:
    with (ROOT/'governance/OSS_REGISTER.csv').open(newline='',encoding='utf-8') as f:
        records=list(csv.DictReader(f))
    if not records or not {'artifact_id','decision','license_status'} <= set(records[0]):
        errors.append('OSS_REGISTER.csv missing required columns/rows')
    if any(r['decision'] not in {'CANDIDATE','REVIEW','APPROVED','REJECTED','REPLACE'} for r in records):
        errors.append('Invalid OSS decision')
except Exception as exc:
    errors.append(f'CSV error: {exc}')
if errors:
    for item in errors: print('FAIL:',item)
    sys.exit(1)
print('PASS: starter documentation and OSS ledger are present; application/engineering correctness NOT assessed.')
