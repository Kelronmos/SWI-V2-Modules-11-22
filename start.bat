@echo off
setlocal EnableExtensions EnableDelayedExpansion
title SWI Online Test Rebuild - V1 + V2

REM ============================================================
REM SWI ONLINE TEST REBUILD - V1 + V2 (Windows 11)
REM ============================================================
REM TEST ONLY
REM PRODUCTION AUTHORIZED: NO
REM ============================================================

set "SCRIPT_DIR=%~dp0"
set "WORKSPACE=%SCRIPT_DIR%swi-test-workspace"

set "V1_URL=https://github.com/Kelronmos/SWI-V1-Module-1-10.git"
set "V2_URL=https://github.com/Kelronmos/SWI-V2-Modules-11-22.git"

set "V1_DIR=%WORKSPACE%\v1"
set "V2_DIR=%WORKSPACE%\v2"
set "ARTIFACT_DIR=%WORKSPACE%\artifacts"
set "REPORT_DIR=%WORKSPACE%\reports"
set "LOG_DIR=%WORKSPACE%\logs"

set "FINAL_EXIT=0"
set "FAIL_STAGE=NONE"

cd /d "%SCRIPT_DIR%"
if errorlevel 1 goto :fatal

echo.
echo ============================================================
echo SWI ONLINE TEST REBUILD - V1 + V2
echo ============================================================
echo Windows launcher : start.bat
echo Script directory : %SCRIPT_DIR%
echo Workspace        : %WORKSPACE%
echo Mode             : TEST ONLY
echo Production auth  : NO
echo ============================================================
echo.

echo [1/8] Checking Windows prerequisites...

where git >nul 2>&1
if errorlevel 1 (
    set "FAIL_STAGE=Git prerequisite"
    echo ERROR: Git was not found in PATH.
    echo Install Git for Windows.
    goto :fatal
)

where python >nul 2>&1
if errorlevel 1 (
    set "FAIL_STAGE=Python prerequisite"
    echo ERROR: Python was not found in PATH.
    echo Install Python 3 and make sure python works in Command Prompt.
    goto :fatal
)

echo Git:
git --version

echo Python:
python --version

echo.
echo [2/8] Creating workspace...

for %%D in ("%V1_DIR%" "%V2_DIR%" "%ARTIFACT_DIR%" "%REPORT_DIR%" "%LOG_DIR%") do (
    if not exist "%%~D" mkdir "%%~D"
    if errorlevel 1 (
        set "FAIL_STAGE=Workspace creation"
        echo ERROR: Could not create %%~D
        goto :fatal
    )
)

echo Workspace ready.
echo.

echo [3/8] Acquiring V1...

if exist "%V1_DIR%\.git" (

    echo Existing V1 checkout found.
    cd /d "%V1_DIR%"

    for /f "delims=" %%i in ('git status --porcelain 2^>nul') do (
        echo ERROR: V1 working tree has uncommitted changes.
        echo Refusing to synchronize dirty checkout.
        echo.
        echo Safe recovery:
        echo Delete ONLY:
        echo %V1_DIR%
        set "FAIL_STAGE=V1 dirty checkout"
        goto :fatal
    )

    git fetch origin

    if errorlevel 1 (
        set "FAIL_STAGE=V1 git fetch"
        goto :fatal
    )

    git pull --ff-only origin main

    if errorlevel 1 (
        set "FAIL_STAGE=V1 git pull"
        goto :fatal
    )

) else (

    echo Cloning V1...
    git clone --branch main "%V1_URL%" "%V1_DIR%"

    if errorlevel 1 (
        set "FAIL_STAGE=V1 clone"
        goto :fatal
    )
)

cd /d "%V1_DIR%"

for /f "tokens=* delims=" %%s in ('git rev-parse HEAD 2^>nul') do set "V1_SHA=%%s"

if not defined V1_SHA (
    set "FAIL_STAGE=V1 commit identification"
    goto :fatal
)

echo V1 commit: %V1_SHA%

> "%ARTIFACT_DIR%\V1_COMMIT.txt" echo %V1_SHA%

cd /d "%SCRIPT_DIR%"

echo.
echo [4/8] Acquiring V2...

if exist "%V2_DIR%\.git" (

    echo Existing V2 checkout found.
    cd /d "%V2_DIR%"

    for /f "delims=" %%i in ('git status --porcelain 2^>nul') do (
        echo ERROR: V2 working tree has uncommitted changes.
        echo Refusing to synchronize dirty checkout.
        echo.
        echo Safe recovery:
        echo Delete ONLY:
        echo %V2_DIR%
        set "FAIL_STAGE=V2 dirty checkout"
        goto :fatal
    )

    git fetch origin

    if errorlevel 1 (
        set "FAIL_STAGE=V2 git fetch"
        goto :fatal
    )

    git pull --ff-only origin main

    if errorlevel 1 (
        set "FAIL_STAGE=V2 git pull"
        goto :fatal
    )

) else (

    echo Cloning V2...
    git clone --branch main "%V2_URL%" "%V2_DIR%"

    if errorlevel 1 (
        set "FAIL_STAGE=V2 clone"
        goto :fatal
    )
)

cd /d "%V2_DIR%"

for /f "tokens=* delims=" %%s in ('git rev-parse HEAD 2^>nul') do set "V2_SHA=%%s"

if not defined V2_SHA (
    set "FAIL_STAGE=V2 commit identification"
    goto :fatal
)

echo V2 commit: %V2_SHA%

> "%ARTIFACT_DIR%\V2_COMMIT.txt" echo %V2_SHA%

cd /d "%SCRIPT_DIR%"

echo.
echo V1 COMMIT : %V1_SHA%
echo V2 COMMIT : %V2_SHA%
echo.

echo [5/8] V1 rebuild + test...

set "V1_REBUILD=FAIL"
set "V1_TEST=FAIL"
set "V1_LOG=%LOG_DIR%\v1_rebuild.log"

cd /d "%V1_DIR%"

if not exist ".venv\Scripts\python.exe" (
    echo Creating V1 virtual environment...
    python -m venv .venv > "%V1_LOG%" 2>&1

    if errorlevel 1 (
        set "FAIL_STAGE=V1 virtual environment"
        goto :fatal
    )
)

call ".venv\Scripts\activate.bat"

if errorlevel 1 (
    set "FAIL_STAGE=V1 virtual environment activation"
    goto :fatal
)

echo Installing V1 dependencies...

python -m pip install --upgrade pip >> "%V1_LOG%" 2>&1

if errorlevel 1 (
    set "FAIL_STAGE=V1 pip upgrade"
    goto :fatal
)

if exist requirements.txt (
    python -m pip install -r requirements.txt >> "%V1_LOG%" 2>&1

    if errorlevel 1 (
        set "FAIL_STAGE=V1 dependency installation"
        goto :fatal
    )
)

echo Running V1 tests...

python -m pytest -q >> "%V1_LOG%" 2>&1

if errorlevel 1 (
    set "V1_REBUILD=PASS"
    set "V1_TEST=FAIL"
) else (
    set "V1_REBUILD=PASS"
    set "V1_TEST=PASS"
)

echo V1 REBUILD: %V1_REBUILD%
echo V1 TEST   : %V1_TEST%
echo V1 LOG    : %V1_LOG%

cd /d "%SCRIPT_DIR%"

echo.
echo [6/8] V2 rebuild + test...

set "V2_REBUILD=FAIL"
set "V2_TEST=FAIL"
set "V2_LOG=%LOG_DIR%\v2_rebuild.log"

cd /d "%V2_DIR%"

if exist "tools\rebuild_swi.bat" (

    echo Running V2 native rebuild script...

    call "tools\rebuild_swi.bat" > "%V2_LOG%" 2>&1

    if errorlevel 1 (
        set "FAIL_STAGE=V2 rebuild"
        goto :final_status
    )

    set "V2_REBUILD=PASS"
    set "V2_TEST=PASS"

) else (

    echo No tools\rebuild_swi.bat found.
    echo Falling back to pytest.

    if not exist ".venv\Scripts\python.exe" (
        python -m venv .venv > "%V2_LOG%" 2>&1

        if errorlevel 1 (
            set "FAIL_STAGE=V2 virtual environment"
            goto :fatal
        )
    )

    call ".venv\Scripts\activate.bat"

    python -m pip install --upgrade pip >> "%V2_LOG%" 2>&1

    if errorlevel 1 (
        set "FAIL_STAGE=V2 pip upgrade"
        goto :fatal
    )

    if exist requirements.txt (
        python -m pip install -r requirements.txt >> "%V2_LOG%" 2>&1

        if errorlevel 1 (
            set "FAIL_STAGE=V2 dependency installation"
            goto :fatal
        )
    )

    python -m pytest -q >> "%V2_LOG%" 2>&1

    if errorlevel 1 (
        set "V2_REBUILD=PASS"
        set "V2_TEST=FAIL"
    ) else (
        set "V2_REBUILD=PASS"
        set "V2_TEST=PASS"
    )
)

cd /d "%SCRIPT_DIR%"

echo.
echo [7/8] Writing final status...

if /i not "%V1_TEST%"=="PASS" set "FINAL_EXIT=1"
if /i not "%V2_TEST%"=="PASS" set "FINAL_EXIT=1"

(
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
) > "%REPORT_DIR%\FINAL_STATUS.txt"

echo.
echo ============================================================
echo FINAL STATUS
echo ============================================================
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
echo ============================================================
echo.

if "%FINAL_EXIT%"=="0" (
    echo RESULT: Test stages completed without test failure.
) else (
    echo RESULT: One or more test stages failed.
    echo Review the logs before drawing conclusions.
)

goto :finish

:fatal

set "FINAL_EXIT=1"

echo.
echo ============================================================
echo SWI BOOTSTRAP STOPPED
echo ============================================================
echo FAILED STAGE: %FAIL_STAGE%
echo WORKSPACE   : %WORKSPACE%
echo.
echo This is an execution/acquisition/environment stop.
echo It is NOT evidence that SWI is proven or disproven.
echo.
echo PRODUCTION AUTHORIZED: NO
echo PROVEN                : NO
echo SEALED                : NO
echo ============================================================
echo.

:finish

echo.
echo Logs:
echo %LOG_DIR%
echo.
echo The window will remain open.
echo Press any key to close...
pause >nul

endlocal
exit /b %FINAL_EXIT%
