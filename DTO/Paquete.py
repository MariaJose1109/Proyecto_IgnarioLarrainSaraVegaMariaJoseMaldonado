from DAO.CRUDDestino import mostrarTodos as mostrarTodosDestinos
from DAO.CRUDPaquete import agregarPaqueteConDestino
from datetime import datetime, timedelta
import random

class Paquete:
    def __init__(self, nombre_paquete, descripcion, fecha_inicio, fecha_fin, precio_total):
        self.id_paquete = None
        self.nombre_paquete = nombre_paquete
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total
        self.destinos = []

    def __str__(self):
        return (f"Paquete(ID: {self.id_paquete}, Nombre: {self.nombre_paquete}, Precio: {self.precio_total}, "
                f"Fechas: {self.fecha_inicio} a {self.fecha_fin}, Destinos: {len(self.destinos)} destinos)")

    @staticmethod
    def generarPaqueteAleatorio():
        """
        Genera un objeto Paquete y una lista de destinos seleccionados aleatoriamente.
        No inserta el paquete en la base de datos. Esa responsabilidad recae en la capa superior.

        Retorna:
            - paquete (Paquete): El objeto paquete generado, o None si no se pudieron generar destinos.
            - destinos_seleccionados (list): Lista de destinos seleccionados para este paquete, o None si no se pudo.
        """
        try:
            destinos_disponibles = mostrarTodosDestinos()  # Obtener destinos existentes
            if not destinos_disponibles:
                print("No hay destinos disponibles para generar paquetes.")
                return None, None

            # Asegurar que haya al menos 1 destino
            cantidad_destinos_disponibles = len(destinos_disponibles)
            cantidad_destinos = min(random.randint(2, 5), cantidad_destinos_disponibles)  # No puede ser mayor a la cantidad disponible

            # Seleccionar aleatoriamente los destinos disponibles
            destinos_seleccionados = random.sample(destinos_disponibles, cantidad_destinos)

            # Generar fechas aleatorias (fecha de inicio y fin válidas)
            hoy = datetime.now()
            fecha_inicio = hoy + timedelta(days=random.randint(10, 60))  # Inicio entre 10 y 60 días desde hoy
            fecha_fin = fecha_inicio + timedelta(days=random.randint(3, 10))  # Fin entre 3 y 10 días después del inicio

            # Calcular precio total sumando el costo de los destinos
            precio_total = sum(destino["costo"] for destino in destinos_seleccionados)

            # Nombres y ubicaciones base para nombres atractivos
            nombres_base = [
                "Aventura Extrema", "Ruta del Sol", "Explorador Urbano", "Escapada Romántica", 
                "Maravillas Naturales", "Viaje Cultural", "Reto de la Selva", "Descubre el Mundo", 
                "Relax Total", "Gastronomía y Tradición", "Explorando el Paraíso", "Aventura en la Montaña"
            ]

            ubicaciones_base = [
                "en la playa", "en la montaña", "en el campo", "en la ciudad", "en el desierto", 
                "en la selva", "en el bosque", "en la isla", "en la ruta", "en el valle"
            ]

            # Generar nombre atractivo para el paquete
            nombre_paquete = f"{random.choice(nombres_base)} {random.choice(ubicaciones_base)}"

            # Crear descripción aleatoria
            descripcion = (f"Paquete con {cantidad_destinos} destinos increíbles, "
                        f"para disfrutar desde el {fecha_inicio.date()} hasta el {fecha_fin.date()}.")

            # Crear el objeto Paquete con fechas válidas
            nuevo_paquete = Paquete(
                nombre_paquete=nombre_paquete,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio.date(),
                fecha_fin=fecha_fin.date(),
                precio_total=precio_total
            )
            nuevo_paquete.destinos = destinos_seleccionados

            # Devolver el paquete y los destinos seleccionados
            return nuevo_paquete, destinos_seleccionados

        except Exception as e:
            print(f"Error al generar paquete aleatorio: {e}")
            return None, None

    @staticmethod
    def generarYRegistrarPaqueteAleatorio():
        """
        Genera un paquete aleatorio y lo inserta automáticamente en la base de datos,
        junto con sus destinos.
        
        Retorna:
            - paquete (Paquete): El objeto paquete generado y registrado, o None si no se pudo.
        """
        paquete, destinos = Paquete.generarPaqueteAleatorio()
        if paquete and destinos:
            # Insertar el paquete en la base de datos
            if agregarPaqueteConDestino(paquete, destinos):
                print(f"Paquete '{paquete.nombre_paquete}' generado y registrado exitosamente.")
                return paquete
            else:
                print("Error al registrar el paquete en la base de datos.")
                return None
        else:
            print("No se pudo generar un paquete aleatorio.")
            return None
