from DAO.CRUDPaquete import *
from datetime import datetime
class PaqueteTuristico:
    def __init__(self, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin):
        self.id_paquete = None  # Se asignará después de registrarse en la base de datos
        self.nombre_paquete = nombre_paquete
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total

    def registrarPaquete(self, destinos_validos):
       if agregarPaqueteConDestino(self, destinos_validos):
           return True
       else:
           return False

    def actualizarPaquete(self, nuevo_nombre, nueva_descripcion, id_destino, nueva_fecha_inicio, nueva_fecha_fin):
        if actualizarPaqueteConDestino(self.id_paquete, nuevo_nombre, nueva_descripcion, id_destino, nueva_fecha_inicio, nueva_fecha_fin):
            print(f"Paquete con ID {self.id_paquete} actualizado correctamente.")
            return True
        else:
            print("Hubo un problema con la actualización del paquete.")
            return False

    def eliminarPaquete(self):
        # Eliminar el paquete turístico
        if eliminarPaquete(self.id_paquete):
            print(f"Paquete con ID {self.id_paquete} eliminado correctamente.")
            return True
        else:
            print("Hubo un problema al eliminar el paquete.")
            return False

    @staticmethod
    def consultarPaquetes():
        paquetes = consultarTodosPaquetes()  # Recuperamos los paquetes con las fechas convertidas
        if paquetes:  # Verifica si la lista no está vacía
            print("\n--- LISTA DE PAQUETES TURÍSTICOS ---\n")
            print(f"{'ID':<5} {'Nombre':<25} {'Descripción':<35} {'Precio':<10} {'Inicio':<12} {'Fin':<12}")
            print("-" * 100)
            for paquete in paquetes:
                fecha_inicio = paquete['fecha_inicio']
                fecha_fin = paquete['fecha_fin']
                print(f"{paquete['id_paquete']:<5} "
                      f"{paquete['nombre_paquete']:<25} "
                      f"{paquete['descripcion'][:35]:<35} "
                      f"${paquete['precio_total']:<10} "
                      f"{fecha_inicio:<12} "
                      f"{fecha_fin:<12}")
    
            print("\n" + "-" * 100)
            input("Presione Enter para continuar...")
        else:
            print("No hay paquetes turísticos disponibles.")
            input("Presione Enter para continuar...")
    


    @staticmethod
    def consultarUnPaquete(id_paquete):
        # Consultar un paquete turístico específico
        paquete = consultarUnPaquete(id_paquete)
        if paquete:
            print(f"Paquete turístico con ID {id_paquete}:")
            print(paquete)
        else:
            print("No se encontró el paquete con ese ID.")
