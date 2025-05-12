import secrets
def generate_numeric_otp(length):
    otp = ''.join(secrets.choice("0123456789") for _ in range(length))
    return otp