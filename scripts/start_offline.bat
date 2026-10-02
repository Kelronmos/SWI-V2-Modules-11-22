@echo off
setlocal
cd /d "%~dp0\.."
python scripts\start_offline.py %*
exit /b %ERRORLEVEL%
