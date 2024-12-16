from DAO.Conexion import Conexion
from datetime import datetime
from DTO.Destino import Destino

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'viajes_aventura_bd'

def agregarDestino(destino):
    try:
        con = Conexion(host, user, password, db)
        sql = "insert into destino set nombre='{}', descripcion='{}', actividades='{}', costo={}".format(
            destino.nombre, destino.descripcion, destino.actividades, destino.costo
        )
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Destino registrado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al registrar el destino: {e}")
        return False

#mostrar todos
def consultarDestinos():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM destino"
        cursor = con.ejecutar_query(sql)
        destinos = cursor.fetchall()  # Obtendrás una lista de diccionarios
        print(destinos)
        con.desconectar()
        return destinos
    except Exception as e:
        print(f"Error al consultar los destinos: {e}")
        return []

#mostrar parcial

#mostrar uno
def consultarUnDestinos(id_destino):
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from destino where id_destino = {}".format(id_destino)
        cursor = con.ejecutar_query(sql)
        destinos = cursor.fetchall()
        con.desconectar()
        return destinos
    except Exception as e:
        print(f"Error al consultar los destinos: {e}")
        return []


def actualizarDestino(destino_id, nuevo_nombre,nueva_actividad, nueva_descripcion, nuevo_costo):
    try:
        con = Conexion(host, user, password, db)
        sql = "UPDATE destino SET nombre = '{}', descripcion = '{}', actividades ='{}', costo = {} WHERE id_destino = {}".format(
            nuevo_nombre, nueva_descripcion,nueva_actividad, nuevo_costo, destino_id )
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Destino actualizado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al actualizar el destino: {e}")
        return False

def eliminarDestino(id_destino ):
    try:
        con = Conexion(host, user, password, db)
        sql = "delete from destino where id_destino = {}".format(id_destino)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Destino eliminado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al eliminar el destino: {e}")
        return False
