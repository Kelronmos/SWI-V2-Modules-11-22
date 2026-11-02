@echo off
setlocal EnableExtensions DisableDelayedExpansion

REM ============================================================
REM SWI Universal Test Runner (Windows)
REM Self-repair launcher with explicit user consent and validation.
REM ============================================================

set "ROOT=%~dp0"
cd /d "%ROOT%"

echo.
echo ============================================================
echo SWI UNIVERSAL TEST RUNNER
echo ============================================================
echo ROOT                 : %ROOT%
echo MODE                 : SELF-REPAIR + TEST + EVIDENCE
echo PRODUCTION AUTHORIZED: NO
echo PROVEN               : NO
echo SEALED               : NO
echo ============================================================
echo.

if not exist "%ROOT%packages.json" (
    echo ERROR: packages.json was not found at "%ROOT%packages.json".
    echo This launcher must be run from the repository root or its parent directory.
    echo PRODUCTION AUTHORIZED: NO
    echo PROVEN               : NO
    echo SEALED               : NO
    exit /b 12
)

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.10+ and then restart this terminal before running SWI.
    echo PRODUCTION AUTHORIZED: NO
    echo PROVEN               : NO
    echo SEALED               : NO
    exit /b 10
) else (
    echo [OK] Python detected
    python --version
)

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git was not found.
    echo Install Git and then restart this terminal before running SWI.
    echo PRODUCTION AUTHORIZED: NO
    echo PROVEN               : NO
    echo SEALED               : NO
    exit /b 11
) else (
    echo [OK] Git detected
    git --version
)

set "NEEDS_NODE=0"
for /f "delims=" %%I in ('set "SWI_ROOT=%ROOT%" ^&^& python -c "import json,os; from pathlib import Path; p=Path(os.environ['SWI_ROOT'])/'packages.json'; d=json.loads(p.read_text(encoding='utf-8')); repos=d.get('repositories', {}); print(1 if any('node' in str(item).lower() for repo in repos.values() for item in repo.get('toolchain', [])) else 0)"') do set "NEEDS_NODE=%%I"

if "%NEEDS_NODE%"=="1" (
    where node >nul 2>&1
    if errorlevel 1 (
        echo.
        echo Missing tool detected: Node.js is required by the manifest.
        echo The launcher will not silently install software.
        choice /C YN /M "Install Node.js now?"
        if errorlevel 2 (
            echo Installation cancelled by user.
            echo PRODUCTION AUTHORIZED: NO
            echo PROVEN               : NO
            echo SEALED               : NO
            exit /b 23
        )
        echo Installing Node.js via winget...
        winget install --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
        if errorlevel 1 (
            echo ERROR: Node.js installation failed or was denied.
            echo Install Node.js and restart this terminal before running SWI.
            echo PRODUCTION AUTHORIZED: NO
            echo PROVEN               : NO
            echo SEALED               : NO
            exit /b 23
        )
    )
    echo [OK] Node.js detected
    node --version
)

echo.
echo Manifest validation...
set "SWI_ROOT=%ROOT%"
python -c "import json,os,sys; from pathlib import Path; p=Path(os.environ['SWI_ROOT'])/'packages.json'; d=json.loads(p.read_text(encoding='utf-8')); schema=d.get('schema',''); repos=d.get('repositories', {}); assert str(schema).startswith('swi.online.test.rebuild.packages.'), 'Unsupported schema: %s' % schema; assert isinstance(repos, dict) and repos, 'No repositories declared'; print(f'Manifest validated: {len(repos)} repositories')" 
if errorlevel 1 (
    echo ERROR: Manifest validation failed.
    echo PRODUCTION AUTHORIZED: NO
    echo PROVEN               : NO
    echo SEALED               : NO
    exit /b 15
)

echo.
echo Launching verified Python runner...
python -m runner.main %*
set "EXITCODE=%ERRORLEVEL%"

echo.
echo ============================================================
echo SWI RUN COMPLETE
echo ============================================================
echo Reports are under: %ROOT%swi-test-workspace\reports
echo.
echo PRODUCTION AUTHORIZED: NO
echo PROVEN               : NO
echo SEALED               : NO
echo ============================================================
echo.
exit /b %EXITCODE%
