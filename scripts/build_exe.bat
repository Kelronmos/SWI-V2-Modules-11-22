@echo off
setlocal
cd /d "%~dp0\.."
if not exist logs mkdir logs
where pyinstaller >nul 2>&1
if errorlevel 1 (
  echo [ERROR] PyInstaller unavailable
  exit /b 30
)
pyinstaller --onefile scripts\start_offline.py --name swi-offline-runner >> logs\build-exe.log 2>&1
if errorlevel 1 (
  echo [ERROR] EXE build failed
  exit /b 20
)
echo [OK] EXE build completed
exit /b 0
