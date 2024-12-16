from DAO.CRUDReserva import *  # Mantén esta importación si es necesario para las funciones CRUD
from DAO.CRUDPaquete import *
from DAO.CRUDUsuario import *


class Reserva:
    def __init__(self, id_usuario, id_paquete, fecha_reserva, estado="pendiente", id_reserva=None):
        self.id_usuario = id_usuario
        self.id_paquete = id_paquete
        self.fecha_reserva = fecha_reserva
        self.estado = estado
        self.id_reserva = id_reserva

    def realizarReserva(self):
        if not self.existeUsuario(self.id_usuario):
            print("Error: El usuario no existe.")
            return False
        if not self.existePaquete(self.id_paquete):
            print("Error: El paquete no existe.")
            return False
        if realizarReserva(self):
            print(f"Reserva realizada correctamente para el usuario {self.id_usuario} y paquete {self.id_paquete}.")
            return True
        else:
            print("Error al registrar la reserva en la base de datos.")
            return False

    def existeUsuario(self, id_usuario):
        return existeUsuario(id_usuario)

    def existePaquete(self, id_paquete):
        return consultarUnPaquete(id_paquete)


    def confirmarReserva(self):
        # Verificar si la reserva está pendiente antes de confirmar
        if self.estado != "pendiente":
            print(f"No se puede confirmar: la reserva no está en estado 'pendiente'. Estado actual: {self.estado}")
            return False
        else:
            self.estado = "confirmada"
            if cambiarEstadoReserva(self.id_reserva, self.estado):
                print(f"Reserva confirmada correctamente: Usuario ID {self.id_usuario}, Paquete ID {self.id_paquete}, Estado {self.estado}")
                return True
            else:
                print(f"Error al confirmar la reserva en la base de datos.")
                return False
