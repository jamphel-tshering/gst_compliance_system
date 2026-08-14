@echo off
cd /d "C:\Users\jamphelt_mongar\gst_compliance_system"
echo Starting GST Compliance System...
echo.
echo Your system will be available at: http://localhost:8888
echo Admin panel: http://localhost:8888/admin/
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 0.0.0.0:8888
pause
