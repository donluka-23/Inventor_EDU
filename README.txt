INVENTOR EDU — ENGINEERING FOUNDATION / CLEAN RESTART
Generated: 2026-11-21
Source commit: 6f153126f7b71c4c8e67a4716e6443f3573b9479
Purpose: retain the actual Python engineering code, fixtures and test data.
This snapshot intentionally has NO old React/Vite UI, NO MD reports, NO AGENTS.md,
NO rejected ESP32 board illustration, and NO fake simulator.

Structure:
  inventor_edu/         Immutable source-code copy from the recorded commit (headless)
  tests/                Core/headless tests, except tests bound to removed HTML preview
  examples/             Headless engineering examples only
  data/                 Versioned GPIO and pilot facts/catalogs
  governance/           Original OSS_REGISTER.csv is retained for provenance
  project/              Actual project state, product blueprint, and milestone data (JSON)
  knowledge/            Reuse and technical stack decisions (JSON)
  agents/               Short executable prompts and session state
  apps/workbench/       Location for a completely new interactive UI implementation

Install CPython 3.12 on Windows or equivalent, then:
  python -m venv .venv
  .venv\Scripts\activate
  python -m pip install -r requirements-core001a-test.txt
  python -m unittest discover -s tests -p "test_*.py"

CAUTION: Tests were NOT executed during GitHub-to-clean-tree export.
A code-preserving copy is not proof that every requirement is production ready.
Two old UI-preview-dependent tests and the embedded HTML learning preview were
excluded. The transfer_assessment.py and learning_session.py engines remain.

How to work:
  1. Open project/state.json and project/vision.json.
  2. Follow agents/prompts/build_workbench.txt to implement UI prototype first.
  3. Keep visible prototype interactions real. Mark unfed engineering results unavailable.
  4. Use agents/prompts/connect_engine.txt to integrate a verified source-backed loop.
  5. Update agents/session.json after actual execution; no long report necessary.

No existing GitHub branches were deleted or rewritten by this export.
Older Git history still contains prior research if a FULL clone is used.
For a source-only clean snapshot, download this branch as a ZIP or make a shallow clone.
