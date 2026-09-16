@echo off
setlocal

echo ==================================
echo SWI LOCAL NODE INFORMATION
echo ==================================

echo.
echo Computer:
hostname

echo.
echo OS:
ver

echo.
echo Architecture:
echo %PROCESSOR_ARCHITECTURE%

echo.
echo Processor:
echo %PROCESSOR_IDENTIFIER%

echo.
echo Python:
where python
python --version 2>nul

echo.
echo Git:
where git
git --version 2>nul

echo.
echo Timestamp:
echo %DATE% %TIME%

echo.
echo ==================================
echo LOCAL ONLY - NOT AN AUTHORIZATION
echo ==================================

endlocal
