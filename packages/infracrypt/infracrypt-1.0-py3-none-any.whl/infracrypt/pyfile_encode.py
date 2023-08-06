"""Encode flask responses in python file."""
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import requests

def check_response_type(response) -> str:
    """Return the type of the response"""
    if isinstance(response, str):
        return 'string'
    if isinstance(response, dict):
        return 'json'
    if isinstance(response, int):
        return 'integer'
    if isinstance(response, list):
        return 'list'
    return 'unknown'

# need to find get the part after return
# then check the type of the response
# then encode the response

def get_encryption_key() -> str:
    """Get the encryption key from the server"""
    text = requests.get("http://192.168.4.1/", timeout=30).text
    return "".join(text.split())

def encrypt_single_response(response: str) -> dict:
    """Encrypt a single response"""
    key = get_encryption_key()
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(response.encode('utf-8'))
    return {
        'response': b64encode(ciphertext).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        'key': key
    }

def decrypt_single_response(response: dict) -> str:
    """Decrypt a single response"""
    salt = b64decode(response['salt'])
    private_key = hashlib.scrypt(
        response['key'].encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=b64decode(response['nonce']))
    plaintext = cipher.decrypt_and_verify(
        b64decode(response['response']),
        b64decode(response['tag'])
    )
    return plaintext.decode('utf-8')

def encrypt_responses(responses: list) -> list:
    """Encrypt a list of responses"""
    return [
        encrypt_single_response(response)
        for response in responses
        if check_response_type(response) != 'unknown'
    ]
