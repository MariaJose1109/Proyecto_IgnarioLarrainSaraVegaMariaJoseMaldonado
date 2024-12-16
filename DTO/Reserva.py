from DAO.CRUDReserva import *

class Reserva:
    def __init__(self, id_usuario, id_paquete, fecha_reserva, estado="pendiente", id_reserva=None):
        self.id_usuario = id_usuario
        self.id_paquete = id_paquete
        self.fecha_reserva = fecha_reserva
        self.estado = estado
        self.id_reserva = id_reserva

    def realizarReserva(self):
        try:
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
        except Exception as e:
            print(f"Error inesperado al realizar la reserva: {e}")
            return False

    def existeUsuario(self, id_usuario):
        try:
            usuarios = consultarUsuariosTipoCliente()
            return any(usuario['id_usuario'] == id_usuario for usuario in usuarios)
        except Exception as e:
            print(f"Error al verificar el usuario: {e}")
            return False

    def existePaquete(self, id_paquete):
        try:
            paquetes = consultarPaquetesDisponibles()
            return any(paquete['id_paquete'] == id_paquete for paquete in paquetes)
        except Exception as e:
            print(f"Error al verificar el paquete: {e}")
            return False

    def cancelarReserva(self):
        if cambiarEstadoReserva(self.id_reserva, "cancelada"):
            self.estado = "cancelada"
            print(f"Reserva cancelada correctamente: Usuario ID {self.id_usuario}, Paquete ID {self.id_paquete}, Estado {self.estado}")
            return True
        else:
            print("No fue posible cancelar la reserva.")
            return False

def confirmarReserva(self):
    if self.estado != "pendiente":
        print(f"No se puede confirmar: la reserva no está en estado 'pendiente'. Estado actual: {self.estado}")
        return False
    else:
        self.estado = "confirmada"
        # Realiza la actualización en la base de datos
        try:
            if cambiarEstadoReserva(self.id_reserva, self.estado):
                print(f"Reserva confirmada correctamente: Usuario ID {self.id_usuario}, Paquete ID {self.id_paquete}, Estado {self.estado}")
                return True
            else:
                print(f"Error al confirmar la reserva en la base de datos.")
                return False
        except Exception as e:
            print(f"Error inesperado al confirmar la reserva: {e}")
            return False
