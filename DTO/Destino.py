class Destino:
    def __init__(self, nombre, descripcion, actividades, costo, idDestino=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo
        self.idDestino = idDestino  # Consistencia con el diagrama de clases

    def __str__(self):
              return f"Destino(ID: {self.idDestino}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Actividades: {self.actividades}, Costo: {self.costo})"

    def to_dict(self):
           return {
            "id_destino": self.idDestino,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "actividades": self.actividades,
            "costo": self.costo
        }
