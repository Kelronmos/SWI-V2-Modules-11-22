@echo off
setlocal enabledelayedexpansion

REM =============================================================================
REM SWI ONLINE TEST REBUILD — V1 + V2  (Windows)
REM =============================================================================
REM Controlled TEST-ONLY bootstrap.
REM Does NOT establish production authorization.
REM =============================================================================

set "SCRIPT_DIR=%~dp0"
set "WORKSPACE=%SCRIPT_DIR%swi-test-workspace"
set "TIMESTAMP=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%T%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

set "V1_URL=https://github.com/Kelronmos/SWI-V1-Module-1-10.git"
set "V2_URL=https://github.com/Kelronmos/SWI-V2-Modules-11-22.git"
set "V1_DIR=%WORKSPACE%\v1"
set "V2_DIR=%WORKSPACE%\v2"
set "ARTIFACT_DIR=%WORKSPACE%\artifacts"
set "REPORT_DIR=%WORKSPACE%\reports"
set "LOG_DIR=%WORKSPACE%\logs"

echo ==============================================
echo SWI ONLINE TEST REBUILD — V1 + V2
echo ==============================================
echo Mode          : TEST ONLY
echo Workspace     : %WORKSPACE%
echo Production authorization : NO
echo ==============================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is required but was not found.
    exit /b 1
)
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is required but was not found.
    exit /b 1
)

echo Git:
git --version
echo Python:
python --version
echo.

mkdir "%V1_DIR%" 2>nul
mkdir "%V2_DIR%" 2>nul
mkdir "%ARTIFACT_DIR%" 2>nul
mkdir "%REPORT_DIR%" 2>nul
mkdir "%LOG_DIR%" 2>nul

REM ---- Acquire V1 ----
echo ---- Acquiring V1 ----
if exist "%V1_DIR%\.git" (
    cd /d "%V1_DIR%"
    git status --porcelain >nul 2>&1
    for /f %%i in ('git status --porcelain 2^>nul') do (
        echo ERROR: V1 working tree has uncommitted changes. Refusing to sync.
        exit /b 1
    )
    git fetch origin
    git pull --ff-only origin main
    if errorlevel 1 (
        echo ERROR: Unable to fast-forward V1. Divergent history. Stopping.
        exit /b 1
    )
) else (
    git clone --branch main %V1_URL% "%V1_DIR%"
    if errorlevel 1 git clone %V1_URL% "%V1_DIR%"
    if errorlevel 1 (
        echo ERROR: V1 clone failed.
        exit /b 1
    )
    cd /d "%V1_DIR%"
)
for /f "tokens=*" %%s in ('git rev-parse HEAD') do set "V1_SHA=%%s"
echo V1 commit: %V1_SHA%
echo %V1_SHA%> "%ARTIFACT_DIR%\V1_COMMIT.txt"
cd /d "%SCRIPT_DIR%"

REM ---- Acquire V2 ----
echo ---- Acquiring V2 ----
if exist "%V2_DIR%\.git" (
    cd /d "%V2_DIR%"
    for /f %%i in ('git status --porcelain 2^>nul') do (
        echo ERROR: V2 working tree has uncommitted changes. Refusing to sync.
        exit /b 1
    )
    git fetch origin
    git pull --ff-only origin main
    if errorlevel 1 (
        echo ERROR: Unable to fast-forward V2. Divergent history. Stopping.
        exit /b 1
    )
) else (
    git clone --branch main %V2_URL% "%V2_DIR%"
    if errorlevel 1 git clone %V2_URL% "%V2_DIR%"
    if errorlevel 1 (
        echo ERROR: V2 clone failed.
        exit /b 1
    )
    cd /d "%V2_DIR%"
)
for /f "tokens=*" %%s in ('git rev-parse HEAD') do set "V2_SHA=%%s"
echo V2 commit: %V2_SHA%
echo %V2_SHA%> "%ARTIFACT_DIR%\V2_COMMIT.txt"
cd /d "%SCRIPT_DIR%"

echo.
echo V1 COMMIT : %V1_SHA%
echo V2 COMMIT : %V2_SHA%
echo.

REM ---- V1 Rebuild ----
echo ==============================================
echo V1 REBUILD + TEST
echo ==============================================
set "V1_REBUILD=FAIL"
set "V1_TEST=FAIL"
set "V1_LOG=%LOG_DIR%\v1_rebuild.log"

cd /d "%V1_DIR%"
if not exist ".venv" python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist requirements.txt python -m pip install -r requirements.txt
python -m pytest -q > "%V1_LOG%" 2>&1
if errorlevel 1 (
    set "V1_REBUILD=PASS"
    set "V1_TEST=FAIL"
) else (
    set "V1_REBUILD=PASS"
    set "V1_TEST=PASS"
)
echo V1 REBUILD : %V1_REBUILD%
echo V1 TEST    : %V1_TEST%
cd /d "%SCRIPT_DIR%"

REM ---- V2 Rebuild ----
echo ==============================================
echo V2 REBUILD + TEST
echo ==============================================
set "V2_REBUILD=FAIL"
set "V2_TEST=FAIL"
set "V2_LOG=%LOG_DIR%\v2_rebuild.log"

cd /d "%V2_DIR%"
if exist tools\rebuild_swi.bat (
    call tools\rebuild_swi.bat > "%V2_LOG%" 2>&1
) else (
    if not exist ".venv" python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    if exist requirements.txt python -m pip install -r requirements.txt
    python -m pytest -q > "%V2_LOG%" 2>&1
)
if errorlevel 1 (
    set "V2_REBUILD=PASS"
    set "V2_TEST=FAIL"
) else (
    set "V2_REBUILD=PASS"
    set "V2_TEST=PASS"
)
echo V2 REBUILD : %V2_REBUILD%
echo V2 TEST    : %V2_TEST%
cd /d "%SCRIPT_DIR%"

echo.
echo ==============================================
echo SWI ONLINE TEST REBUILD — FINAL STATUS
echo ==============================================
echo V1 COMMIT              : %V1_SHA%
echo V2 COMMIT              : %V2_SHA%
echo V1 REBUILD             : %V1_REBUILD%
echo V1 TEST                : %V1_TEST%
echo V2 REBUILD             : %V2_REBUILD%
echo V2 TEST                : %V2_TEST%
echo SYSTEM COMPLETION      : INCOMPLETE
echo PROVEN                 : NO
echo SEALED                 : NO
echo PRODUCTION AUTHORIZED  : NO
echo ==============================================
echo.
echo This process is a controlled test rebuild only.
echo Logs under: %WORKSPACE%
echo.

endlocal
exit /b 0
