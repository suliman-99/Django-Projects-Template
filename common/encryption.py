import base64
import hashlib
import secrets
from cryptography.fernet import Fernet


def generate_fernet_key():
    # Generate a 256-bit (32-byte) random key
    fernet_key = hashlib.sha256(base64.urlsafe_b64encode(secrets.token_bytes(32))).digest()
    print(base64.urlsafe_b64encode(fernet_key).decode())
    return fernet_key


def encrypt(data: str, key: str) -> str:
    key = key.encode()
    data = data.encode()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    encrypted_data = encrypted_data.decode()
    return encrypted_data


def decrypt(encrypted_data: str, key: str) -> str:
    key = key.encode()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_data = decrypted_data.decode()
    return decrypted_data


if __name__ == '__main__':
    key = 'L4eZ-2YU3g1yetyaCuv1Y7QQ1OoKL4J9flRYAYp-OH0='
    data = 'Important Sensitive Data'
    print('------------------------------------------------------------------------------')
    print(type(data))
    print(data)
    print('------------------------------------------------------------------------------')
    encrypted_data = encrypt(data, key)
    print(type(encrypted_data))
    print(encrypted_data)
    print('------------------------------------------------------------------------------')
    decrypted_data = decrypt(encrypted_data, key)
    print(type(decrypted_data))
    print(decrypted_data)
    print('------------------------------------------------------------------------------')
