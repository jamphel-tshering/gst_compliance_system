@echo off
REM GST COMPLIANCE SYSTEM - PRODUCTION STARTUP
REM Simple deployment - same configuration as final test

echo ==========================================
echo GST Compliance System - Production Mode
echo Domain: mongargst.drc.gov.bt
echo ==========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.production to .env
    pause
    exit /b 1
)

echo Starting Django Production Server...
echo Server will run on: http://127.0.0.1:8001/
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python manage.py runserver 127.0.0.1:8001

pause