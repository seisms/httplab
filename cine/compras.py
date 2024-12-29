sold_limit = 5
room_size = 50
precio = 1500


class Espectaculo:
    def __init__(self, nom, date, time):
        self.sala = [Asiento(x) for x in range(room_size)]
        self.name = nom
        self.date = date
        self.time = time

    def Comprar(self, sold):
        if (len(sold) > sold_limit):
            raise ComprarException(f"No puedes comprar más de {sold_limit} entradas")
        self.CheckSeat(sold)
        for i in sold:
            self.sala[i].ocupado = True
        entr = Entrada(len(sold), sold)
        return entr

    def CheckSeat(self, sold):
        for seat in sold:
            if (seat > room_size - 1):
                raise ComprarException(f"No existe el asiento {seat}")
            if (self.sala[seat].ocupado is True):
                raise ComprarException(f"El asiento {seat} ya fué comprado para el espectaculo {self.name}")


class Asiento:
    def __init__(self, numero):
        self.ocupado = False
        self.numero = numero


class Entrada:
    def __init__(self, cant, asientos):
        self.cant = cant
        self.precio = cant * precio
        self.asientos = asientos


class ComprarException(Exception):
    pass
