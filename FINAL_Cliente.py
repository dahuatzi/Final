import socket
from nacl.signing import SigningKey

# Datos para poder establecer nuestra conexión con el servidor
host = '127.0.0.1'
puerto = 3000
FORMAT = "utf-8"
SIZE = 1024


# Función para ingresar usuario y contraseña
def login():
    print("Ingrese los siguientes datos: \n")
    usuario = str(input("Usuario: "))
    contrasena = str(input("Contraseña: "))
    datos = [usuario, contrasena]
    return datos


# Si la información ingresada en el login es correcta:
if __name__ == "__main__":
    logininfo = login()

# Establecera conexión por medio de socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))
    archivo = "recibido.txt"

# Se realizá la firma y las verificaciones de las llaves con el archivo "recibido.txt"
    with open(archivo, "wb") as filename:
        send = filename.read(SIZE)
        kbyte = SigningKey.generate()
        firma = kbyte.sign(send)
        verificacion = kbyte.verify_key
        verificacionhex = verificacion.encode()

# Se envian las verificaciones y la data se desencripta
        cliente.send(verificacionhex)
        cliente.send(firma.signature)
        cliente.sendall(send)
        data = cliente.recv(SIZE)
        print(data.decode())
        print("Se envió exitosamente")
        cliente.close()
