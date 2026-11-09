# SWI Device Binding Demonstrator

**Research only.** Demonstrates device capability observation and evidence binding.

```text
Android Device → Observation Adapter → Capability Registry → Evidence Binder
                 → (existing) SWI Governing Spine → Report
```

```text
PROVEN=NO · SEALED=NO · PRODUCTION_AUTHORIZED=NO
```

## Offline tests

```bash
cd research/device-binding-demonstrator
PYTHONPATH=. python3 -m pytest -q tests/
```

## Termux

```bash
bash termux/swi-device-bind.sh
```

Reports: `$HOME/storage/shared/SWI-Security-Audits/SWI-DEVICE-BIND/<timestamp>/`  
(or `$HOME/SWI-DEVICE-BIND/` if shared storage unmounted)

Physical camera, biometric, and audio tests require Termux:API and user permissions. Until then they stay BLOCKED / NOT_IMPLEMENTED / NOT_RUN.
