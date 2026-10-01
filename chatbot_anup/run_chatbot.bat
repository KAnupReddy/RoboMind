@echo off
setlocal enabledelayedexpansion
title RoboMind - AI Robotics Chatbot (Mistral AI)
color 0A

echo ============================================================
echo    RoboMind - AI Integration in Robotics Chatbot
echo    Powered by Mistral AI
echo ============================================================
echo.

:: -------------------------------------------------------
::  PUT YOUR MISTRAL API KEY HERE
::  Get a free key at: https://console.mistral.ai/
:: -------------------------------------------------------
set MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY_HERE

:: -------------------------------------------------------
::  PORTABLE PYTHON SETTINGS (auto-downloaded if needed)
:: -------------------------------------------------------
set SCRIPT_DIR=%~dp0
set PORTABLE_DIR=%SCRIPT_DIR%_python_runtime
set PORTABLE_PYTHON=%PORTABLE_DIR%\python.exe
set PYTHON_VERSION=3.12.9
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
set GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py

:: -------------------------------------------------------
::  STEP 1: Find a working Python (system or portable)
:: -------------------------------------------------------
set PYTHON_CMD=

:: Try system Python (python, python3, py)
for %%P in (python python3 py) do (
    if "!PYTHON_CMD!"=="" (
        where %%P >nul 2>&1
        if !errorlevel!==0 (
            %%P -c "import sys; exit(0 if sys.version_info>=(3,8) else 1)" >nul 2>&1
            if !errorlevel!==0 (
                set PYTHON_CMD=%%P
            )
        )
    )
)

:: Use already-downloaded portable Python
if "!PYTHON_CMD!"=="" (
    if exist "!PORTABLE_PYTHON!" (
        set PYTHON_CMD=!PORTABLE_PYTHON!
        echo [OK] Using cached portable Python runtime.
    )
)

:: -------------------------------------------------------
::  STEP 2: Download portable Python if nothing found
:: -------------------------------------------------------
if "!PYTHON_CMD!"=="" (
    echo [INFO] Python not found on this PC.
    echo [INFO] Downloading portable Python %PYTHON_VERSION% — one-time setup...
    echo.

    :: Detect CPU architecture
    if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
    ) else if "%PROCESSOR_ARCHITEW6432%"=="AMD64" (
        set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
    ) else (
        set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-win32.zip
    )

    mkdir "!PORTABLE_DIR!" >nul 2>&1

    :: Download Python embeddable zip via PowerShell
    echo Downloading Python runtime...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;" ^
        "Invoke-WebRequest -Uri '!PYTHON_URL!' -OutFile '!PORTABLE_DIR!\python_embed.zip' -UseBasicParsing"
    if !errorlevel! neq 0 (
        echo [ERROR] Download failed. Check internet connection and try again.
        rmdir /s /q "!PORTABLE_DIR!" >nul 2>&1
        pause
        exit /b 1
    )

    :: Extract the zip
    echo Extracting Python...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "Expand-Archive -Path '!PORTABLE_DIR!\python_embed.zip' -DestinationPath '!PORTABLE_DIR!' -Force"
    del "!PORTABLE_DIR!\python_embed.zip" >nul 2>&1

    :: Enable site-packages so pip works (uncomment 'import site' in ._pth file)
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "Get-ChildItem '!PORTABLE_DIR!\' -Filter '*._pth' | ForEach-Object {" ^
        "  (Get-Content $_.FullName) -replace '#import site','import site' | Set-Content $_.FullName" ^
        "}"

    :: Download get-pip.py and install pip
    echo Installing pip...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;" ^
        "Invoke-WebRequest -Uri '!GET_PIP_URL!' -OutFile '!PORTABLE_DIR!\get-pip.py' -UseBasicParsing"
    "!PORTABLE_DIR!\python.exe" "!PORTABLE_DIR!\get-pip.py" --no-warn-script-location --quiet
    del "!PORTABLE_DIR!\get-pip.py" >nul 2>&1

    if not exist "!PORTABLE_PYTHON!" (
        echo [ERROR] Python setup failed. Please install Python manually from:
        echo         https://www.python.org/downloads/
        rmdir /s /q "!PORTABLE_DIR!" >nul 2>&1
        pause
        exit /b 1
    )

    set PYTHON_CMD=!PORTABLE_PYTHON!
    echo [OK] Portable Python ready.
    echo.
)

echo Python: !PYTHON_CMD!
!PYTHON_CMD! --version
echo.

:: -------------------------------------------------------
::  STEP 3: Install / upgrade dependencies to correct versions
:: -------------------------------------------------------
echo Checking dependencies...
!PYTHON_CMD! -m pip install "mistralai>=1.0.0" "flask>=3.0.0" --upgrade --quiet --no-warn-script-location
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies. Check internet connection.
    pause
    exit /b 1
)
echo [OK] Dependencies ready.

echo [OK] All dependencies ready.
echo.

:: -------------------------------------------------------
::  STEP 4: Launch the web chatbot (opens browser automatically)
:: -------------------------------------------------------
echo [OK] Starting RoboMind at http://localhost:5000
echo [OK] Browser will open automatically...
echo [OK] Press Ctrl+C to stop the server.
echo.
!PYTHON_CMD! "%SCRIPT_DIR%app.py"

echo.
echo ============================================================
echo    Session ended. Goodbye!
echo ============================================================
pause
