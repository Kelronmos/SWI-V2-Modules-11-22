@echo off
setlocal EnableExtensions EnableDelayedExpansion
title SWI Universal Test / Demonstration Runner

REM ============================================================
REM SWI UNIVERSAL TEST / DEMONSTRATION RUNNER (Windows)
REM ============================================================
REM TEST ONLY — does not establish production authorization
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo SWI UNIVERSAL TEST / DEMONSTRATION RUNNER
echo ============================================================
echo MODE                  : TEST + SIMULATION + EVIDENCE
echo REAL-WORLD ACTION     : NONE
echo PRODUCTION AUTHORIZED : NO
echo ============================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found in PATH.
    echo Install Python 3.10+ and ensure "python" works in Command Prompt.
    echo.
    echo PRODUCTION AUTHORIZED: NO
    echo PROVEN               : NO
    echo SEALED               : NO
    echo.
    pause
    exit /b 1
)

echo Python:
python --version
echo.

echo Launching runner...
echo.
python -m runner.main %*
set EXITCODE=%ERRORLEVEL%

echo.
echo ============================================================
echo SWI RUN COMPLETE
echo ============================================================
echo Reports are under: swi-test-workspace\reports
echo.
echo PRODUCTION AUTHORIZED: NO
echo PROVEN               : NO
echo SEALED               : NO
echo ============================================================
echo.
echo Press any key to close...
pause >nul
exit /b %EXITCODE%
