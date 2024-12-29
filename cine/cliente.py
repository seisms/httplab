import socket
import json

precio = 1500
sold_limit = 5
room_size = 50

prompt1 = "\nIngrese la operación a realizar\
        \n\t 1) Comprar asientos.\
        \n\t 2) Consultar fecha de la función.\
        \n Operación: "
prompt_buy = "\nIngrese los asientos que desea comprar, separados por espacio\
            \n Asientos: "


def DecodeMessage(data):
    return json.loads(data.decode('utf-8'))


def PrintReceived(received):
    if (received['state'] == "Exception"):
        print(f"\nFalló la petición HTTP: {received['message']}")
    if (received['state'] == "Bought"):
        print(f"\nEntrada(s) comprada(s) con éxito!\
              \n\t Cantidad: {received['cant']}\
              \n\t Precio: {received['precio']}\
              \n\t Asientos: {received['asientos']}\n")
    if (received['state'] == "Date"):
        print(f"\nEspectáculo: {received['name']}\
              \n\t Fecha: {received['date']}\
              \n\t hora: {received['time']}\n")


def BuildMessage():
    op = ""
    asientos = []
    while (op != "1" and op != "2"):
        op = input(prompt1)
    if op == "1":
        seat_str = input(prompt_buy)
        aux = set(seat_str.split())
        for item in aux:
            asientos.append(int(item))
    message = {
        'operation': 'comprar' if op == "1" else "fecha-hora",
        'data': asientos
    }
    return json.dumps(message)


try:
    stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Definición del servidor
    host = 'localhost'
    port = 5555
    server_address = ((host, port))
    print("Conectando...")
    stream_socket.connect(server_address)
    # Aquí hacemos las peticiones
    while True:
        request = BuildMessage()
        stream_socket.sendall(request.encode('utf-8'))
        data = stream_socket.recv(1024)
        received = DecodeMessage(data)
        PrintReceived(received)

except socket.error as e:
    print(f"\nConexión fallida con error: {e}")
except KeyboardInterrupt as e:
    print(f"\nEjecución interrumpida por el usuario: {e}")
finally:
    print("\nCerrando la conexión.")
    stream_socket.close()
