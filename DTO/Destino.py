from DAO.CRUDDestino import *
class Destino:
    def __init__(self, nombre, descripcion, actividades, costo, destino_id=None):
        self.destino_id = destino_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo

