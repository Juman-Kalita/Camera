@echo off
echo ========================================
echo Workplace Activity Analytics
echo Easy Installer for Windows
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

echo Step 2: Installing dependencies...
echo This may take 2-3 minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo Step 3: Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Workplace Analytics.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\start.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.Description = "Workplace Activity Analytics System" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs
echo [OK] Desktop shortcut created
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now:
echo 1. Double-click "Workplace Analytics" on your desktop
echo 2. Or run "start.bat" from this folder
echo.
echo The dashboard will open automatically in your browser.
echo.
pause
