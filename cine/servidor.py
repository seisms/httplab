import socket

# Creación de socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definición de host, quizás se deba cambiar por una dirección ip
host = 'localhost'

# Definición de puerto de comunicación
port = 5555

# Vincular el socket al puerto
sock.bind((host, port))

# Escuchar conexiones entrantes
sock.listen(1)

# Esperar a que llegue una conexión
print('Esperando conexión...')
connection, client = sock.accept()

print(client, 'conectado..')

# Recibir los datos en pequeños bloques y reenviarlos

data = connection.recv(16)
print('Recibido: "%s"' % data)
if data:
    connection.sendall(data)
else:
    print('Sin mensaje', client)

# Cerrar la conexión
connection.close()
