from urllib.parse import urlparse
import hashlib
import random
import string
from django.http import HttpRequest
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

def encrypt_key(hex_key: str, data: str) -> str:
    key = binascii.unhexlify(hex_key)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return binascii.hexlify(ciphertext).decode()

def decrypt_key(hex_key: str, encrypted_data: str) -> str:
    key = binascii.unhexlify(hex_key)
    encrypted_data = binascii.unhexlify(encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data, AES.block_size).decode()

def extract_domain(url: str) -> str:
    if not url.startswith(('http://', 'https://','www')):
        url = 'http://' + url
    parsed_url = urlparse(url)
    return parsed_url.netloc



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
