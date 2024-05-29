@echo off
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel% equ 0 (
    py update.py %*
    goto :end
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python update.py %*
    goto :end
)

echo Neither 'py' nor 'python' was found on the system path.
exit /b 1

:end
exit /b 0
