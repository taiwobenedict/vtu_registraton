import hashlib
import random
import string
from django.http import HttpRequest
from Crypto.Cipher import AES
import binascii

def encrypt_key(hex_key: str, data: str) -> str:
    key = binascii.unhexlify(hex_key)
    cipher = AES.new(key, AES.MODE_ECB)
    if len(data) > 16:
        data = data[:16]
    elif len(data) < 16:
        data = data.ljust(16)
    ciphertext = cipher.encrypt(data.encode())
    return binascii.hexlify(ciphertext).decode()




def generate_activation_key():
    characters = string.hexdigits.lower()
    key = "".join(random.choice(characters) for _ in range(32))
    return key


def generate_secret_key(activation_key, domain_name):
    combined_string = activation_key + domain_name
    hash_object = hashlib.sha256(combined_string.encode())
    secret_key = hash_object.hexdigest()
    return secret_key

def get_full_url(request: HttpRequest) -> str:
    """
    Returns the full URL (protocol + domain) of the current request.
    """
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    return f"{protocol}://{domain}"
