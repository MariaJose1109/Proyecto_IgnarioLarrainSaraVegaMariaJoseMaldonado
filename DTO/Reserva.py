from DAO.CRUDReserva import agregarReserva, cambiarEstadoReserva, mostrarReservaPorId
from DAO.CRUDPaquete import mostrarUno as mostrarPaquete  # Método para obtener un paquete
from DAO.CRUDUsuario import CRUDUsuario  # Método para verificar existencia del usuario
from tabulate import tabulate
import datetime


class Reserva:
    def __init__(self, idUsuario, idPaquete, fechaReserva, estado="confirmada", idReserva=None):
        self.idReserva = idReserva
        self.idUsuario = idUsuario
        self.idPaquete = idPaquete
        self.fechaReserva = fechaReserva
        self.estado = estado

    def __str__(self):
        return (f"Reserva(ID: {self.idReserva}, Usuario: {self.idUsuario}, "
                f"Paquete: {self.idPaquete}, Fecha: {self.fechaReserva}, Estado: {self.estado})")

    # Confirmar una reserva
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

    # Cancelar una reserva
    def cancelarReserva(self):
        try:
            if self.estado == "cancelada":
                print(f"La reserva ya está cancelada.")
                return False
            
            self.estado = "cancelada"
            if cambiarEstadoReserva(self.idReserva, self.estado):
                print(f"Reserva {self.idReserva} cancelada con éxito.")
                return True
            else:
                print("No se pudo cancelar la reserva.")
                return False
        except Exception as e:
            print(f"Error al cancelar la reserva: {e}")
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
