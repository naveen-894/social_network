import jwt
from cryptography.fernet import Fernet
from social_network.settings import SECRET_KEY, SECRET_CIPHER_KEY
CIPHER = Fernet(SECRET_CIPHER_KEY)

def string_to_bytes(string):
    return bytes(string)

def crypto_encode(value):
    bytes_string = string_to_bytes(value)
    encrypted_text = Fernet(SECRET_CIPHER_KEY).encrypt(bytes_string).decode("utf-8")
    return encrypted_text

def generate_token(payload):
    secret_key = SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    encrypted_token = crypto_encode(token)
    return encrypted_token

def decode_encrypted_token(encrypted_token):
    cipher_suite = Fernet(SECRET_CIPHER_KEY)
    decrypted_data = cipher_suite.decrypt(encrypted_token)
    return decrypted_data.decode("utf-8")

def decode_jwt(jwt_crypto_token):
    try:
        jwt_token = decode_encrypted_token(jwt_crypto_token)
        secret_key = SECRET_KEY
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
        return decoded_token
    except Exception:
        return None
