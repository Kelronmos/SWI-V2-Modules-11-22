@echo off
setlocal
cd /d "%~dp0\.."
python scripts\build_offline.py --test %*
exit /b %ERRORLEVEL%
