import secrets
import string

def generate_password(length=12, include_special=True):
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password
