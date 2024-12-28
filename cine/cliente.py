import socket
import compras as c

precio = 1500
sold_limit = 5
room_size = 50


try:
    stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Definición del servidor
    host = 'localhost'

    port = 5555

    server_address = ((host, port))
    print("Conectando...")

    stream_socket.connect(server_address)

    message = 'Hola, servidor, soy el cliente'
    stream_socket.sendall(message.encode('utf-8'))

    data = stream_socket.recv(10)

    print(data)
    print('Socket cerrado')
except socket.error as e:
    print(f"Conexión fallida con error: {e}")
stream_socket.close()
