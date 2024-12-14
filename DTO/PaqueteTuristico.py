from DAO.CRUDPaquete import * 

class PaqueteTuristico:
    def __init__(self, nombre_paquete, descripcion,precio_total, fecha_inicio,fecha_fin):
        self.nombre_paquete = nombre_paquete
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total

