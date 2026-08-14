import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.test import Client
from django.urls import reverse

# Test the main dashboard
client = Client()

# Try to access main dashboard
print("Testing main dashboard...")
response = client.get('/admin/dashboard/')
print(f"Status code: {response.status_code}")
print(f"Content type: {response.get('Content-Type')}")
print(f"Redirect location: {response.get('Location', 'None')}")

# Test compliance dashboard
print("\nTesting compliance dashboard...")
response = client.get('/admin/compliance/')
print(f"Status code: {response.status_code}")
print(f"Content type: {response.get('Content-Type')}")
print(f"Redirect location: {response.get('Location', 'None')}")

# Test taxpayers
print("\nTesting taxpayers...")
response = client.get('/taxpayers/')
print(f"Status code: {response.status_code}")
print(f"Content type: {response.get('Content-Type')}")
