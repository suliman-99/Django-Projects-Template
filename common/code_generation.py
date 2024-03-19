import secrets


def generate_code(length: int):
    mx = 10**length
    mn = 10**(length-1)
    return str(secrets.randbelow(mx-mn)+mn)
