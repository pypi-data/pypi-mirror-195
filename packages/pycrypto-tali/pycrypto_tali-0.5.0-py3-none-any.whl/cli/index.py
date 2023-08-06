import typer
from cli.rsa_encryption import generate_password,create_pair_keys,encrypt_password,decrypt_password
from typing import Optional
import os

app = typer.Typer()


@app.command()
def generate(lenght: Optional[int] = typer.Argument(20, help='Cantidad de caracteres para la contraseña')):
    """ 
    Crea una contraseña con 20 caracteres alfanumericos
    """
    password = generate_password(lenght)
    password = typer.style(password, fg=typer.colors.GREEN)
    print('\nPassword :', password)

@app.command()
def create(filepath:str = typer.Argument(os.getcwd())):
    """
    Crea una clave publica y una privada en el directorio actual.
    """
    create_pair_keys(filepath)
    print('\nLas claves fueron creadas en la carpeta actual: \n - public_key.pem \n - private_key.pem')

@app.command()
def encrypt(password: str = typer.Option(..., prompt='\n Password a encriptar ')):
    """
    Encripta una contraseña con la clave publica generada 'public_key.pem' y crea un archivo encriptado 'file_encrypted.txt'
    """
    file_public = os.getcwd() + '/public_key.pem'
    encrypt_password(file_public,password.encode('ascii'),os.getcwd())
    print('\n El archivo encriptado se encuentra en la carpeta actual: \n\t - ',typer.style('file_encryted.txt',fg=typer.colors.BLUE))

@app.command()
def decrypt():
    """
    Desencripta un archivo encriptado 'file_encrypted.txt' junto con la clave privada 'private_key.pem' y devolver la contraseña encriptada.
    """
    password = decrypt_password(os.getcwd()+'/private_key.pem',os.getcwd()+'/file_encrypted.txt')
    print('\nLa password encriptada: ',typer.style(password, fg=typer.colors.GREEN))

def main():
    app()