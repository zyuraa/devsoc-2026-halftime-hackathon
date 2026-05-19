import secrets
import string

def generate_secure_userid(length=16):
    # Characters used to generate the ID
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))