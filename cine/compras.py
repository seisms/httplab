sold_limit = 5
room_size = 50
precio = 1500


class Asiento:
    def __init__(self, numero):
        self.ocupado = False
        self.numero = numero


class Entrada:
    def __init__(self, cant, asientos):
        self.cant = cant
        self.precio = cant * precio
        self.asientos = asientos


sala = [Asiento(x) for x in range(room_size)]


class ComprarException(Exception):
    pass


def Check_seat(seat):
    if (seat > room_size):
        raise ComprarException(f"No existe el asiento {seat}")
    if (sala[seat].ocupado is True):
        raise ComprarException(f"El asiento {seat} ya fué comprado")


def Comprar(sold, sala):
    if (len(sold) > sold_limit):
        raise ComprarException(f"No puedes comprar mas de {sold_limit} entradas")
    for i in sold:
        Check_seat(i)
        sala[i].ocupado = True
    entr = Entrada(len(sold), sold)
    return entr
