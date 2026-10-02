@echo off
setlocal
cd /d "%~dp0\.."
if not exist logs mkdir logs
start /b "" cmd /c "python scripts\start_offline.py > logs\background-start.log 2>&1"
echo Background start requested. See logs\background-start.log
