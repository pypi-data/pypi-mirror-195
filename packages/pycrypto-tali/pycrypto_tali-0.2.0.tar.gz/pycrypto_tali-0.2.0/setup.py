# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==39', 'pyperclip==1.8.2', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pct = cli.index:main']}

setup_kwargs = {
    'name': 'pycrypto-tali',
    'version': '0.2.0',
    'description': 'CLI Mensajeria encriptada',
    'long_description': '# python_crypto\n## Secure Delivery of Credentials\n\n### Attacking\n\nActualmente el robo de credenciales es muy frecuente, ya que los atacantes logran tener acceso al correo o los servicios de mensajería, obteniendo en texto plano nuestra credencial.\nPrincipalmente los mayores ataques se dan a las cuentas Cloud como es el caso de AWS, Azure o GCP.\nEl administrador root de la cuenta, cuando genera un nuevo usuario, este mismo debe proveer la credencial, utilizando canales de comunicación poco seguros, debido a esto los atacantes logran obtener la credencial y hacer uso de los servicio y recursos Cloud para sus beneficios.\n\n<img src="assets/UNID-5.jpg" width="750" height="400"/>\n\n### Asymmetric Encryption\n\nLa criptografía asimétrica es uno de los tipos de criptografía informática y una de las técnicas de criptografía más potentes diseñadas en base al uso de una fórmula matemática muy compleja para crear un par de claves: la clave privada y la clave pública. A través de estas claves se establece un canal de comunicación seguro entre las partes, en el que tanto el emisor como el receptor deben usar criptografía asimétrica con un mismo algoritmo definido, que les permitirá crear un juego de claves único e irrepetible para cada uno.\n\nEn ese proceso de comunicación, el emisor y el receptor comparten entre ellos sus claves públicas; estas claves cifrarán posteriormente los mensajes que intercambien entre ellos. Y las claves privadas descifrarán esos mensajes para poder ver su contenido. Este proceso hace imposible que un tercero puede interferir en la comunicación y ver el contenido los mensajes.\n\n<img src="assets/ae.png" width="400" height="250"/>\n\n\n## Aplication SDC\n\nLa App SDC o Secure delivery of credentials, ofrece una solución al problema de un envió seguro, generando un cifrado de encriptación RSA, creando una llave publica y una privada para el cifrado. Como tambien un des encriptación de la credencial.\n\nEs totalmente portable para Windows.\n\n### Paso 1\n\nPrimero el usuario debe generar sus propias credenciales a traves de la app.exe almacenada en el repositorio de Github, compartiendo la clave publica con el Administrador Root, ya que esta llave solo cifra el texto.\n\n**El usuario NO DEBE COMPARTI, NI ALMACENAR EN DRIVE su clave privada, de lo contrario se podria acceder al documento cifrado**\n\n<img src="assets/UNID-1.jpg" width="750" height="400"/>\n\n### Paso 2\n\nUna vez obtenida la clave pública por el Administrador Root, puede crear un nuevo usuario en la nube, para este ejemplo utilizaremos AWS Cloud, a través de la App SDC logra encriptar la contraseña generada por AWS, y realizar el envió seguro del archivo cifrado al nuevo usuario.\n\n<img src="assets/UNID-2.jpg" width="520" height="600"/>\n\n### Paso 3\n\nAl obtener el archivo cifrado el nuevo usuario se dispone a des encriptar el archivo cifrado junto con la clave privada por la App SDC, teniendo como resultado la contraseña de AWS generada de forma segura.\n\n<img src="assets/UNID-3.jpg" width="520" height="600"/>\n\n### Paso 4\n\nAWS Cloud ofrece un segundo nivel de seguridad, al colocar la contraseña administrada se debe volver a cambiar por una que el usuario genere. La App SDC permite generar una credencial de 20 caracteres alfanuméricos de forma random. Logrando que este tipo de credenciales fortalezcan el acceso seguro.\n\n<img src="assets/UNID-4.jpg" width="520" height="600"/>\n\n## MFA\n\nOtro nivel de seguridad sugerido es el MFA o Autenticación Multifactor, el cual genera 6 números random cada 30 segundos, los cuales deben ser ingresados una vez introducido la contraseña de AWS Account. Logrando una validación en tiempo real para un acceso seguro.\n\nEn el caso de teléfonos android se puede descargar la aplicación "Google Authenticator" y los pasos de habilitación en la cuenta cloud.\n\n<img src="assets/mfa.jpg"  width="750" height="400"/>\n\n[Documentacion AWS Cloud MFA Instalacion](https://docs.aws.amazon.com/es_es/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html)\n\n[Documentacion Azure Cloud MFA Instalacion](https://learn.microsoft.com/es-es/azure/active-directory/authentication/howto-mfaserver-deploy)\n\n[Documentacion GCP Cloud MFA Instalacion](https://cloud.google.com/identity/solutions/enforce-mfa?hl=es)\n',
    'author': 'Kevin Barroso',
    'author_email': 'kevin.barroso@taligent.com.ar',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
