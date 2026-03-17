@echo off
:: ============================================================
::  Project Reforged Patch Manager — EXE Builder
::  Run this once to build ProjectReforged_PatchManager.exe
::
::  Requirements:
::    - Python 3.8+ installed and on PATH
::      Download from https://www.python.org/downloads/
::      Make sure "Add Python to PATH" is checked during install.
:: ============================================================

echo.
echo  Project Reforged Patch Manager — EXE Builder
echo  =============================================
echo.

:: Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Please install Python 3.8+ from https://www.python.org/
    echo          Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo  [1/3] Installing / updating PyInstaller...
python -m pip install --upgrade pyinstaller --quiet
if errorlevel 1 (
    echo  [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)

echo  [2/3] Building EXE (this may take 30-60 seconds)...
python -m PyInstaller ProjectReforged_PatchManager.spec --noconfirm
if errorlevel 1 (
    echo  [ERROR] Build failed. Check the output above for details.
    pause
    exit /b 1
)

echo  [3/3] Done!
echo.
echo  Your EXE is ready at:
echo    dist\ProjectReforged_PatchManager.exe
echo.
echo  You can move that .exe anywhere you like.
echo  It will store patch_versions.json and patch_manager_config.json
echo  in the same folder as the .exe.
echo.
pause