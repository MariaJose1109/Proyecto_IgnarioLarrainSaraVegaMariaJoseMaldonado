from DAO.Conexion import Conexion
from datetime import datetime
from DAO.CRUDUsuario import obtenerRolUsuario
from DTO.Destino import Destino

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'agencia_de_viajes'

def agregarDestino(destino, nombre):
    rol = obtenerRolUsuario(nombre)
    if rol != "administrador":
        print("Permiso denegado: Solo los administradores pueden agregar destinos.")
        return False
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
        sql = "select * from destino"
        cursor = con.ejecutar_query(sql)
        destinos = cursor.fetchall()
        con.desconectar()
        return destinos
    except Exception as e:
        print(f"Error al consultar los destinos: {e}")
        return []

#mostrar parcial
#mostrar uno

def actualizarDestino(destino,nombre):
    rol = obtenerRolUsuario(nombre)
    if rol != "administrador":
       print("Permiso denegado: Solo los administradores pueden agregar destinos.")
       return False
    try:
        con = Conexion(host, user, password, db)
        sql= "update destino set nombre ='{}', descripcion='{}', actividades='{}', costo={} where id_destino = {}".format(destino[1],destino[2],destino[3],destino[4],destino[0])
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

def eliminarDestino(id_destino,nombre ):
    rol = obtenerRolUsuario(nombre)
    if rol != "administrador":
       print("Permiso denegado: Solo los administradores pueden agregar destinos.")
       return False
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
