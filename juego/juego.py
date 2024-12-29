import socket
import threading
import random
import time

HOST = 'localhost'
PORT = 10000
MAX_PLAYERS = 3

def host_game(player_name):
    """Modo host del juego."""
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_socket.bind((HOST, PORT))
    players = [player_name]
    player_sockets = {player_name: host_socket}
    player_addresses = {player_name: (HOST, PORT)}
    waiting_queue = []

    print(f"Eres el anfitrión del juego. Esperando jugadores...")

    try:
        while True:
            data, addr = host_socket.recvfrom(1024)
            message = data.decode()

            if message.startswith("JOIN"):
                _, new_player = message.split()
                if len(players) < MAX_PLAYERS:
                    players.append(new_player)
                    player_sockets[new_player] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    player_addresses[new_player] = addr
                    host_socket.sendto("ACCEPTED".encode(), addr)
                    print(f"Jugador {new_player} se unió al juego.")

                    if len(players) == MAX_PLAYERS:
                        print(f"Juego iniciado con jugadores: {players}")
                        threading.Thread(target=start_game, args=(host_socket, players, player_sockets, waiting_queue, player_addresses, player_name)).start()
                else:
                    waiting_queue.append((new_player, addr))
                    host_socket.sendto("WAIT".encode(), addr)
                    print(f"Jugador {new_player} añadido a la cola de espera.")

    except Exception as e:
        print(f"Error en el modo host: {e}")
    finally:
        pass

def start_game(host_socket, players, player_sockets, waiting_queue, player_addresses, player_name):
    """Inicia la lógica del juego y gestiona eliminaciones."""
    while len(players) > 1:
        time.sleep(5) # En segundos
        loser = random.choice(players)
        players.remove(loser)

        # Notifica al jugador eliminado
        addr = player_addresses[loser]
        host_socket.sendto("ELIMINADO".encode(), addr)

        # Elimina al jugador de los diccionarios
        del player_sockets[loser]
        del player_addresses[loser]

        print(f"Jugador eliminado: {loser}")

        # Si el host actual es eliminado, elegir un nuevo host
        if len(players) > 0 and loser == player_name:
            new_host = players[0]  # El primer jugador restante se convierte en el nuevo host
            print(f"El nuevo host es: {new_host}")
            notify_new_host(new_host, players, host_socket, player_addresses)
            player_name = new_host  # Actualizar el nombre del host actual

        # Si hay jugadores en la cola, moverlos al juego
        if len(waiting_queue) > 0:
            new_player, addr = waiting_queue.pop(0)
            players.append(new_player)
            player_sockets[new_player] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            player_addresses[new_player] = addr
            host_socket.sendto("ACCEPTED".encode(), addr)
            print(f"Jugador {new_player} ingresó desde la cola de espera.")

    if len(players) == 1:
        print(f"El ganador del juego es: {players[0]}.")
        

    # El juego terminó, cerrar todas las conexiones
    for sock in player_sockets.values():
        sock.close()
    # host_socket.close()  # No cerrar el socket del host aquí

def notify_new_host(new_host, players, host_socket, player_addresses):
    """Notifica a todos los jugadores sobre el nuevo host."""
    for player in players:
        addr = player_addresses[player]
        host_socket.sendto(f"NUEVO_HOST {new_host}".encode(), addr)

def client_mode(player_name):
    """Modo cliente para unirse a un juego."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_socket.sendto(f"JOIN {player_name}".encode(), (HOST, PORT))
        response, _ = client_socket.recvfrom(1024)
        response = response.decode()

        if response == "ACCEPTED":
            print("Te uniste al juego.")
            play_game(client_socket)
        elif response == "WAIT":
            print("El juego está lleno. Estás en la cola de espera.")
            wait_in_queue(client_socket)
        else:
            print(f"Respuesta desconocida del anfitrión: {response}")
    except Exception as e:
        print(f"Error al conectar al anfitrión: {e}")
    finally:
        client_socket.close()

def play_game(client_socket):
    """Modo de juego para los jugadores."""
    try:
        while True:
            data, _ = client_socket.recvfrom(1024)
            message = data.decode()
            print(f"Mensaje del anfitrión: {message}")

            if message.startswith("ELIMINADO"):
                print("Has sido eliminado del juego.")
                break
            elif message.startswith("NUEVO_HOST"):
                new_host = message.split()[1]
                print(f"El nuevo host es: {new_host}")

    except Exception as e:
        print(f"Error durante el juego: {e}")

def wait_in_queue(client_socket):
    """Modo de espera en la cola de jugadores."""
    try:
        while True:
            data, _ = client_socket.recvfrom(1024) # Por convención, _ se usa para variables que no se usarán
            message = data.decode()

            if message == "ACCEPTED":
                print("Ingresaste al juego desde la cola.")
                play_game(client_socket)
                break
            elif message.startswith("NUEVO_HOST"):
                new_host = message.split()[1]
                print(f"El nuevo host es: {new_host}")
    except Exception as e:
        print(f"Error mientras estabas en la cola: {e}")

if __name__ == "__main__":
    player_name = input("Ingresa tu nombre: ")
    is_host = input("¿Quieres ser el anfitrión del juego? (s/n): ").lower() == 's'

    if is_host:
        host_game(player_name)
    else:
        client_mode(player_name)
