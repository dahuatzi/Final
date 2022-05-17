import socket
from Crypto.Cipher import AES
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
import Aleatorios

# Se indica en el server los usuarios y contraseñas
BITACORA = {"danimijares": "737513",
            "profesor": "cripto"}

# Se establecen los datos para tener conexión
host = '127.0.0.1'
puerto = 3000
FORMAT = "utf-8"
SIZE = 1024


def main():

    print("El servidor esta arrancando...")
    servertcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servertcp.bind((host, puerto))
    servertcp.listen(3)
    print("El servidor está escuchando...")

    conn, address = servertcp.accept()
    print(f"La conexión desde: {address}")

    if login(usuario="danimijares", contrasena="737513"):
        with open("mandar/recibido.txt", "rb") as filename:
            file = conn.recv(1024)
            key = Aleatorios.numeros
            cifrador = AES.new(key, AES.MODE_EAX)
            filecifrado, tag = cifrador.encrypt_and_digest(file)
            filename.write(filecifrado)

            print("Archivo Firmado")
            infosigned, llave = firma(filecifrado)

            print("Verificacion de firma")
            infoverify = verificacion(infosigned, llave)

    elif login(usuario="profesor", contrasena="cripto"):
        with open("mandar/recibido.txt", "rb") as filename:
            file = conn.recv(1024)
            key = Aleatorios.numeros
            cifrador = AES.new(key, AES.MODE_EAX)
            filecifrado, tag = cifrador.encrypt_and_digest(file)
            filename.write(filecifrado)

            print("Archivo Firmado")
            infosigned, llave = firma(filecifrado)

            print("Verificacion de firma")
            infoverify = verificacion(infosigned, llave)



    else:
        print("Algo salió mal")

    servertcp.close()


# Función para extraer los valores de la bitacora y ver si coinciden
def login(usuario, contrasena):
    if usuario in BITACORA and contrasena in BITACORA.values():
        return True
    else:
        return False


# Función para guardar las verificaciones que se hagan dentro de un archivo de LOGS
def bitacora(usuario, contrasena):
    with open("LOGS.txt", "a") as logs:
        if login(usuario, contrasena):
            logs.write(f"Usuario: {usuario}")
            ingreso = True
        else:
            logs.write("Usuario o contraseña incorrecto")
            ingreso = False
        logs.close()
    return ingreso


# Función para firmar el archivo cifrado
def firma(filecifrado):
    sign = SigningKey.generate()
    datafirmada = sign.sign(filecifrado)
    return datafirmada, sign


def verificacion(datafirmada, key: SigningKey):
    verify = VerifyKey(key.verify_key.encode())
    v = verify.verify(datafirmada)
    return v
























