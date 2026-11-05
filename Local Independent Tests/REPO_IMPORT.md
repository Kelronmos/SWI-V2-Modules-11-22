# Repository import instructions

Target repository: `Kelronmos/SWI-V2-Modules-11-22`

Recommended isolated destination:

`research/camera-telemetry-authority/`

Copy the complete contents of this package into that directory. Do not replace `swi_v2/execution_integrity.py` and do not merge into `main` as a production authorization gate. Submit as a research-only branch/PR for review after repository write access is available.

Suggested validation from the destination directory:

```bash
python -m pip install -r requirements.txt
python run_tests.py
sha256sum -c evidence/SHA256SUMS
```

The SHA256SUMS manifest is generated relative to the package root and includes source, tests, runner, JSON run record and Markdown report.
