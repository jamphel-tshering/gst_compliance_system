@echo off
echo ==========================================
echo GST COMPLIANCE SYSTEM - INSTANT LIVE ACCESS
echo ==========================================
echo.
echo This will help you get the system live immediately
echo.

REM Check if ngrok exists
if not exist "C:\Users\jamphelt_mongar\Desktop\ngrok\ngrok.exe" (
    echo ngrok not found on desktop!
    echo.
    echo Please follow these steps:
    echo 1. Go to https://ngrok.com/
    echo 2. Sign up for free account
    echo 3. Download ngrok for Windows
    echo 4. Extract it to your Desktop
    echo 5. Run this file again
    echo.
    pause
    exit /b 1
)

echo ngrok found! Starting tunnel...
echo.

REM Kill any existing ngrok processes
taskkill /F /IM ngrok.exe >nul 2>&1

REM Start ngrok tunnel
cd "C:\Users\jamphelt_mongar\Desktop\ngrok"
start ngrok http 8001

echo.
echo ==========================================
echo NGROK TUNNEL STARTED!
echo ==========================================
echo.
echo ngrok window will open automatically
echo It will show you a URL like: https://random-name.ngrok-free.app
echo.
echo Use that URL to access your system from anywhere!
echo.
echo Press any key to stop the tunnel when done...
pause

REM Stop ngrok when user presses key
taskkill /F /IM ngrok.exe >nul 2>&1
echo.
echo Tunnel stopped.