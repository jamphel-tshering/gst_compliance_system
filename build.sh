# Render.com Deployment Configuration
# Python
python-3.12.10
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Start application
gunicorn gst_compliance_system.wsgi:application