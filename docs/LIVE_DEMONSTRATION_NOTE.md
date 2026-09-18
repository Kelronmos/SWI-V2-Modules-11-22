# Live Demonstration Note (V2)

**Paired doctrine (canonical):**  
[SWI-V1 `docs/LIVE_DEMONSTRATION_DOCTRINE.md`](https://github.com/Kelronmos/SWI-V1-Module-1-10/blob/main/docs/LIVE_DEMONSTRATION_DOCTRINE.md)

## What we are building

Learning materials and architecture volumes describe intent.  
**This repository** demonstrates the V2 continuation boundary in code:

```text
V1 serialized foundation evidence
        → M11 admission (schema + integrity + status)
        → AdmittedInput
        → kernel / post-admission paths as implemented
```

Plus: authority boundary helper (Lane A), travel CI, controlled M12 gates.

## Live demo (minimum)

```bash
git clone https://github.com/Kelronmos/SWI-V2-Modules-11-22.git
cd SWI-V2-Modules-11-22
pip install -r requirements.txt
python -m pytest -q
```

Cross-repo travel: workflow `two_checkout_travel.yml` (produce on V1-only job,
admit on V2-only job).

## Remember

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
TESTED ≠ CI-VERIFIED ≠ SEALED
```

Volume 2 themes (SAD-DFU, mesh, etc.) are not live demos until implemented
and tested here or in a declared repo under the same chain.
