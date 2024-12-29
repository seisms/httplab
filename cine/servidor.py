import socket
import random
import compras as c
from datetime import date, time
import json

spectacle_names = ["El maravilloso acto de Fooman",
                   "Barman Vs. El Cocodrilo Come-Hombres", "Tres Luciernagas", "Mambrú se fue a la Guerra"]


def RandName():
    return spectacle_names[random.randint(0, len(spectacle_names)-1)]


def RandDate():
    year = random.randint(2025, 2035)
    month = random.randint(1, 12)
    day = random.randint(1, 12)
    return date(year, month, day)


def RandHour():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return time(hour, minute, second)


def DecodeMessage(data):
    return json.loads(data.decode('utf-8'))


def GetSetFromMessage(ms):
    return set(ms['data'])


def BuildResponse_Comprar(entrada):
    response = {
        'state': 'Bought',
        'cant': entrada.cant,
        'precio': entrada.precio,
        'asientos': list(entrada.asientos)
    }
    return json.dumps(response)


def BuildResponse_FechaHora(espectaculo):
    response = {
        'state': 'Date',
        'name': espectaculo.name,
        'date': espectaculo.date.isoformat(),
        'time': espectaculo.time.isoformat()
    }
    return json.dumps(response)


def BuildResponse_Exception(e):
    jresp = {
        'state': 'Exception',
        'message': str(e)
    }
    response = json.dumps(jresp)
    return response


def Connection(connection, esp):
    try:
        bought = 0
        while True:
            # Recibir los datos en pequeños bloques y reenviarlos
            data = connection.recv(1024)
            if not data:
                print("No se recibieron datos.")
                break
            message = DecodeMessage(data)
            print(message)
            if (message['operation'].lower() == "comprar"):
                try:
                    asientos = GetSetFromMessage(message)
                    entrada = esp.Comprar(asientos)
                    bought += len(asientos)
                    if bought > 5:
                        raise c.ComprarException(f"No puedes comprar más de {
                                               c.sold_limit} entradas")
                    response = BuildResponse_Comprar(entrada)
                    print(response)
                    connection.sendall(response.encode('utf-8'))
                except c.ComprarException as e:
                    response = BuildResponse_Exception(e)
                    connection.sendall(response.encode('utf-8'))
            elif (message['operation'].lower() == "fecha-hora"):
                response = BuildResponse_FechaHora(esp)
                print(response)
                connection.sendall(response.encode('utf-8'))

    except socket.error as e:
        print(f"Falló la conexión: {e}")
        BuildResponse_Exception(e)
        connection.sendall(response.encode('utf-8'))
    finally:
        print("Cerrando conexión")
        connection.close()


def main():
    esp = c.Espectaculo(RandName(),
                        RandDate(), RandHour())

    # Creación de socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Definición de host, quizás se deba cambiar por una dirección ip
    host = 'localhost'

    # Definición de puerto de comunicación
    port = 5555

    # Vincular el socket al puerto
    sock.bind((host, port))

    # Escuchar conexiones entrantes
    sock.listen(1)
    try:
        while True:
            connection, client = sock.accept()
            print(client, 'conectado..')
            Connection(connection, esp)
    except KeyboardInterrupt:
        print("Servidor interrumpido por entrada del usuario")
    finally:
        print("Servidor muerto. Cerrando socket.")
        sock.close()


if __name__ == "__main__":
    main()
