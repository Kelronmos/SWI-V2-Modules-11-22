@echo off
setlocal enabledelayedexpansion

echo ==================================
echo SWI LOCAL REBUILD
echo ==================================

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    exit /b 1
)

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git was not found.
    exit /b 1
)

echo Python:
python --version

echo Git:
git --version

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip

if exist requirements.txt (
    python -m pip install -r requirements.txt
)

echo.
echo Running tests...

python -m pytest

if errorlevel 1 (
    echo.
    echo SWI REBUILD/TEST FAILED
    exit /b 1
)

echo.
echo SWI REBUILD/TEST PASSED

endlocal
