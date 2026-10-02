@echo off
call "%~dp0build_offline.bat" %*
exit /b %ERRORLEVEL%
