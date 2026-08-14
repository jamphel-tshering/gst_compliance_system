"""
Generate a secure SECRET_KEY for Django production
Run this script: python generate_secret_key.py
"""
import secrets
import string

def generate_django_secret_key():
    """Generate a cryptographically secure secret key for Django"""
    # Generate a 50-character random string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    return secret_key

if __name__ == "__main__":
    print("🔐 Generating secure SECRET_KEY for Django production...")
    secret_key = generate_django_secret_key()
    print(f"\nYour SECRET_KEY: {secret_key}")
    print("\nAdd this to your .env file:")
    print(f"SECRET_KEY={secret_key}")
    print("\n⚠️  Keep this key secret and never commit it to version control!")