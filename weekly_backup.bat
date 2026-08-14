@echo off
echo Starting weekly GST Compliance System backup...
cd /d "C:\Users\jamphelt_mongar\gst_compliance_system"
python backup_database.py
echo Weekly backup completed.
pause
