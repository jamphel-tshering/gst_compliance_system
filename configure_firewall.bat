@echo off
echo Configuring Windows Firewall for GST Compliance System...
echo.

netsh advfirewall firewall add rule name="Django Server Port 8888" dir=in action=allow protocol=TCP localport=8888
if %errorlevel% equ 0 (
    echo Success! Firewall rule added for port 8888
) else (
    echo Failed to add firewall rule. Please run as Administrator.
)

echo.
echo Your system should now be accessible from other devices on your network.
echo Access URL: http://192.168.0.102:8888
echo.
pause
