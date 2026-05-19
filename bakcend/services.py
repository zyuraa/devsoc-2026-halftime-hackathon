import secrets
import string
import threading

def delete_group_after(group_id, delay_seconds):
    def delete():
        global groups
        groups = [g for g in groups if g.id != group_id]
    
    timer = threading.Timer(delay_seconds, delete)
    timer.start()

def generate_secure_userid(length=16):
    # Characters used to generate the ID
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))