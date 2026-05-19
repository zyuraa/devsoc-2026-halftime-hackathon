import secrets
import string
import threading


def delete_group_after(group_id, delay_seconds, gyms):
    def delete():
        for gym in gyms:
            gym.groups = [
                group for group in gym.groups
                if str(group.id) != str(group_id)
            ]

    timer = threading.Timer(delay_seconds, delete)
    timer.start()


def generate_secure_userid(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))