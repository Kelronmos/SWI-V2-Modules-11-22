# SWI Desktop Application Requirement

**Status:** SPECIFIED · NOT_IMPLEMENTED as verified platform packages  
**PROVEN:** NO · **SEALED:** NO · **PRODUCTION_AUTHORIZED:** NO  

## Launch modes

1. **Desktop application** — native window (e.g. Tauri shell + Python backend); no browser chrome required.
2. **Browser application** — Chrome / Edge / Firefox against local API.
3. **Portable application** — run from folder/USB subject to platform dependencies.

## Preferred architecture

```
Desktop shell (Tauri or equivalent)
        ↓ local API only
Python SWI governing backend (same spine as browser)
        ↓
Evidence / logs (local)
```

**Hard rule:** The desktop shell must **not** contain a second authorization engine.  
It must call the **same** governing spine as the browser path.

Do **not** package an unverified or placeholder spine (`spine_inspector` 44-byte stub, incomplete EI) as a working implementation.

## Platform deliverables (claim only after OS-native test)

| Platform | Deliverable | Claim without test |
|----------|-------------|-------------------|
| Windows | SWI.exe, SWI-Setup.exe, portable zip | FORBIDDEN |
| Linux | AppImage where supported, launcher | FORBIDDEN |
| macOS | SWI.app, DMG where supported | FORBIDDEN |
| Android | Termux-compatible browser path initially | honest classification |

## Desktop features (required when implemented)

1. Custom SWI icon  
2. Splash screen  
3. Native application window  
4. Automatic local service startup  
5. Automatic local service shutdown on exit  
6. Version display  
7. Update manager + rollback  
8. Offline operation  
9. Local logs and evidence  
10. Dashboard without external browser  
11. Safe updates  
12. No unnecessary administrator privileges  

## Priority

Windows desktop first, then Linux, then macOS.

## Current workspace observation

- Launchers / demo scripts: present (`start.sh`, `run_demo.sh`, Beagle launchers).
- Browser dashboard artifacts: present in Beagle / Workbench trees.
- Verified SWI.exe / AppImage / SWI.app packages: **NOT_ESTABLISHED** in this environment.
