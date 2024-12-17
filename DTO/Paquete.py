from DAO.CRUDPaquete import *
from datetime import datetime

class Paquete:
    def __init__(self, nombre, descripcion, fechaIda, fechaVuelta, costo, idPaquete=None):
        self.idPaquete = idPaquete  # Se asignará después de registrarse en la base de datos
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaIda = fechaIda  # Fecha de inicio
        self.fechaVuelta = fechaVuelta  # Fecha de finalización
        self.costo = costo

    def calcularCosto(self):
        """
        Simula el cálculo del costo en función de los destinos asociados o algún otro criterio.
        Aquí retorna el costo ya registrado.
        """
        return self.costo

    def registrarPaquete(self, destinos_validos):
        """
        Registra el paquete turístico en la base de datos junto con los destinos asociados.
        """
        if agregarPaqueteConDestino(self, destinos_validos):
            print(f"Paquete '{self.nombre}' registrado con éxito.")
            return True
        else:
            print("Error al registrar el paquete.")
            return False

    def actualizarPaquete(self, nuevoNombre, nuevaDescripcion, idDestino, nuevaFechaIda, nuevaFechaVuelta):
        """
        Actualiza los datos del paquete turístico en la base de datos.
        """
        if actualizarPaqueteConDestino(self.idPaquete, nuevoNombre, nuevaDescripcion, idDestino, nuevaFechaIda, nuevaFechaVuelta):
            print(f"Paquete con ID {self.idPaquete} actualizado correctamente.")
            return True
        else:
            print("Error al actualizar el paquete.")
            return False

    def eliminarPaquete(self):
        """
        Elimina el paquete turístico de la base de datos.
        """
        if eliminarPaquete(self.idPaquete):
            print(f"Paquete con ID {self.idPaquete} eliminado correctamente.")
            return True
        else:
            print("Error al eliminar el paquete.")
            return False

    @staticmethod
    def consultarPaquetes():
        """
        Muestra todos los paquetes turísticos disponibles.
        """
        paquetes = DAO.CRUDPaquete.mostrarTodos()
        if paquetes:
            print("\n--- LISTA DE PAQUETES TURÍSTICOS ---\n")
            print(f"{'ID':<5} {'Nombre':<25} {'Descripción':<35} {'Costo':<10} {'Fecha Inicio':<12} {'Fecha Fin':<12}")
            print("-" * 100)
            for paquete in paquetes:
                print(f"{paquete['id_paquete']:<5} "
                      f"{paquete['nombre_paquete']:<25} "
                      f"{paquete['descripcion'][:35]:<35} "
                      f"${paquete['precio_total']:<10} "
                      f"{paquete['fecha_inicio']:<12} "
                      f"{paquete['fecha_fin']:<12}")
            print("-" * 100)
        else:
            print("No hay paquetes turísticos disponibles.")

    @staticmethod
    def consultarUnPaquete(idPaquete):
        """
        Consulta un paquete turístico específico por su ID.
        """
        paquete = DAO.CRUDPaquete.mostrarUno(idPaquete)
        if paquete:
            print("\n--- DETALLE DEL PAQUETE TURÍSTICO ---\n")
            print(f"ID: {paquete['id_paquete']}")
            print(f"Nombre: {paquete['nombre_paquete']}")
            print(f"Descripción: {paquete['descripcion']}")
            print(f"Costo: ${paquete['precio_total']}")
            print(f"Fecha de Inicio: {paquete['fecha_inicio']}")
            print(f"Fecha de Fin: {paquete['fecha_fin']}")
        else:
            print(f"No se encontró un paquete con el ID {idPaquete}.")
