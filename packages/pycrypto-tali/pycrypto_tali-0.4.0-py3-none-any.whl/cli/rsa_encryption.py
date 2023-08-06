import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import random, string

def utf8(s: bytes) -> str:
    return str(s, 'utf-8')

def create_pair_keys(filename : str) -> None:
    # Creacion de par de claves en el  directorio actual 
    # Genera una clave privada y una clave publica 
    # - public_key.pem 
    # - private_key.pem
    private_key = rsa.generate_private_key(
       public_exponent=65537,
       key_size=4096,
       backend=default_backend()
    )
    public_key = private_key.public_key()


    private_pem = private_key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.PKCS8,
       encryption_algorithm=serialization.NoEncryption()
    )

    with open(f'{filename}/private_key.pem', 'wb') as f:
        f.write(private_pem)

    public_pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(f'{filename}/public_key.pem', 'wb') as f:
        f.write(public_pem)

def encrypt_password(public_key: str,password: str,filename_encrypt:str) -> None:
    # Encriptacion de contraseña junto con la clave publica:
    #   - public_key.pem
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted = base64.b64encode(public_key.encrypt(
        password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ))
    with open(f'{filename_encrypt}/file_encrypted.txt', 'wb') as f:
        f.write(encrypted)

def decrypt_password(path_private_key:str,file_encrypted:str) -> str:
    # Desencripta el archivo encriptado por la clave publica
    # Se necesita la clave privada para poder desencriptarlo
    #   - private_key.pem
    #   - file_encrypted.txt
    with open(path_private_key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    with open(f'{file_encrypted}','rb') as f:
        encrypted = f.read()

    decrypted = private_key.decrypt(
        base64.b64decode(encrypted),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )
    decryptedutf = utf8(decrypted)
    return decryptedutf

def generate_password(LEN:int) -> str:
    # Genera una contraseña alfanumerica
    # Default 20 length
    length = LEN
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for i in range(length))