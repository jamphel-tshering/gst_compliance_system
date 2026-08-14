import urllib.request
import sys

# Test if the server is responding
try:
    response = urllib.request.urlopen('http://127.0.0.1:8888', timeout=5)
    content = response.read()
    print(f"Server is responding! Status code: {response.status}")
    print(f"Response length: {len(content)} characters")
    print("\nFirst 500 characters of response:")
    print(content[:500].decode('utf-8'))
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
