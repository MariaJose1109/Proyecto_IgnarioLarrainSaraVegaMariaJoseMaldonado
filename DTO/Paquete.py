from DAO.CRUDDestino import *  
from DAO.CRUDPaquete import *  
from datetime import datetime, timedelta
import random

class Paquete:
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin, precio_total):
        self.id_paquete = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total
        self.destinos = []

    def __str__(self):
        return (f"Paquete(ID: {self.id_paquete}, Nombre: {self.nombre}, Precio: {self.precio_total}, "
                f"Fechas: {self.fecha_inicio} a {self.fecha_fin}, Destinos: {len(self.destinos)} destinos)")

    @staticmethod
    def generarPaqueteAleatorio():
        try:
            # Obtener destinos de la base de datos
            destinos_disponibles = consultarDestinos()
            if not destinos_disponibles:
                print("No hay destinos disponibles para generar paquetes.")
                return None

            # Seleccionar aleatoriamente entre 2 y 5 destinos
            cantidad_destinos = random.randint(2, 5)
            destinos_seleccionados = random.sample(destinos_disponibles, cantidad_destinos)

            # Generar fechas aleatorias (rango de fechas válido)
            hoy = datetime.now()
            fecha_inicio = hoy + timedelta(days=random.randint(10, 60))  # Fecha entre 10 y 60 días desde hoy
            fecha_fin = fecha_inicio + timedelta(days=random.randint(3, 10))  # Duración del viaje entre 3 y 10 días

            # Calcular precio total sumando costos de destinos
            precio_total = sum(destino["costo"] for destino in destinos_seleccionados)

            # Crear una descripción aleatoria
            descripcion = f"Paquete con {cantidad_destinos} destinos increíbles, para disfrutar desde el {fecha_inicio.date()} hasta el {fecha_fin.date()}."

            # Crear el objeto Paquete
            nombre_paquete = f"Paquete-{random.randint(1000, 9999)}"
            nuevo_paquete = Paquete(
                nombre=nombre_paquete,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio.date(),
                fecha_fin=fecha_fin.date(),
                precio_total=precio_total
            )
            nuevo_paquete.destinos = destinos_seleccionados

            # Insertar el paquete en la base de datos
            if agregarPaqueteConDestino(nuevo_paquete, destinos_seleccionados):
                print(f"Paquete '{nombre_paquete}' generado y registrado exitosamente.")
                return nuevo_paquete
            else:
                print("Error al registrar el paquete en la base de datos.")
                return None

        except Exception as e:
            print(f"Error al generar paquete aleatorio: {e}")
            return None
