from DAO.CRUDReserva import *  # Importación de funciones CRUD para reservas
from DAO.CRUDPaquete import *  # Para validar existencia de paquetes
from DAO.CRUDUsuario import *  # Para validar existencia de usuarios
from tabulate import tabulate  # Para mejorar la presentación en consola


class Reserva:
    def __init__(self, idUsuario, idPaquete, fechaReserva, estado="pendiente", idReserva=None):
        self.idReserva = idReserva
        self.idUsuario = idUsuario
        self.idPaquete = idPaquete
        self.fechaReserva = fechaReserva
        self.estado = estado

    def __str__(self):
        """
        Representación en string de la reserva.
        """
        return (f"Reserva(ID: {self.idReserva}, Usuario: {self.idUsuario}, "
                f"Paquete: {self.idPaquete}, Fecha: {self.fechaReserva}, Estado: {self.estado})")

    # Realizar una reserva
    def realizarReserva(self):
        try:
            if not self.existeUsuario(self.idUsuario):
                print("Error: El usuario no existe.")
                return False
            if not self.existePaquete(self.idPaquete):
                print("Error: El paquete no existe.")
                return False
            if registrarReserva(self):
                print("\nReserva registrada correctamente.")
                return True
            else:
                print("Error al registrar la reserva en la base de datos.")
                return False
        except Exception as e:
            print(f"Error inesperado al realizar la reserva: {e}")
            return False

    # Confirmar una reserva (solo si está pendiente)
    def confirmarReserva(self):
        try:
            if self.estado != "pendiente":
                print(f"No se puede confirmar la reserva. Estado actual: {self.estado}")
                return False
            self.estado = "confirmada"
            if cambiarEstadoReserva(self.idReserva, self.estado):
                print(f"Reserva confirmada con éxito. ID: {self.idReserva}")
                return True
            else:
                print("Error al confirmar la reserva.")
                return False
        except Exception as e:
            print(f"Error inesperado al confirmar la reserva: {e}")
            return False

    # Cancelar una reserva (solo si está pendiente)
    def cancelarReserva(self):
        try:
            if self.estado != "pendiente":
                print(f"No se puede cancelar la reserva. Estado actual: {self.estado}")
                return False
            self.estado = "cancelada"
            if cambiarEstadoReserva(self.idReserva, self.estado):
                print(f"Reserva cancelada con éxito. ID: {self.idReserva}")
                return True
            else:
                print("Error al cancelar la reserva.")
                return False
        except Exception as e:
            print(f"Error inesperado al cancelar la reserva: {e}")
            return False

    # Verificar existencia de usuario
    @staticmethod
    def existeUsuario(idUsuario):
        try:
            return existeUsuario(idUsuario)
        except Exception as e:
            print(f"Error al verificar la existencia del usuario: {e}")
            return False

    # Verificar existencia de paquete
    @staticmethod
    def existePaquete(idPaquete):
        try:
            paquete = consultarUnPaquete(idPaquete)
            return paquete is not None
        except Exception as e:
            print(f"Error al verificar la existencia del paquete: {e}")
            return False

    # Mostrar reservas por usuario
    @staticmethod
    def mostrarReservasPorUsuario(idUsuario):
        try:
            reservas = mostrarReservaPorId(idUsuario)
            if reservas:
                print("\n--- RESERVAS DEL USUARIO ---")
                headers = ["ID Reserva", "ID Paquete", "Fecha de Reserva", "Estado"]
                tabla_reservas = [[
                    reserva['id_reserva'], 
                    reserva['id_paquete'], 
                    reserva['fecha_reserva'], 
                    reserva['estado']
                ] for reserva in reservas]
                print(tabulate(tabla_reservas, headers=headers, tablefmt="fancy_grid"))
            else:
                print(f"No se encontraron reservas para el usuario con ID {idUsuario}.")
        except Exception as e:
            print(f"Error al mostrar reservas por usuario: {e}")
