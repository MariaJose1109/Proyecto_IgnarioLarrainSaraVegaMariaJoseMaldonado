from DAO.Conexion import Conexion
from DTO.Destino import Destino
from tabulate import tabulate 

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Agregar destino
def agregarDestino(destino):
    try:
        con = Conexion(host, user, password, db)
        sql = "INSERT INTO destino (nombre, descripcion, actividades, costo) VALUES (%s, %s, %s, %s)"
        con.ejecutaQuery(sql, (destino.nombre, destino.descripcion, destino.actividades, destino.costo))
        con.commit()
        return True
    except Exception:
        con.rollback()
        return False
    finally:
        con.desconectar()

# Mostrar todos los destinos
def mostrarTodos():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id_destino, nombre, descripcion, actividades, costo FROM destino"
        cursor = con.ejecutaQuery(sql)
        datos = cursor.fetchall()
        return datos
    except Exception:
        return []
    finally:
        con.desconectar()

# Mostrar un destino por ID
def mostrarUno(idDestino):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id_destino, nombre, descripcion, actividades, costo FROM destino WHERE id_destino = %s"
        cursor = con.ejecutaQuery(sql, (idDestino,))
        destino = cursor.fetchone()
        return destino
    except Exception:
        return None
    finally:
        con.desconectar()

# Mostrar destinos parciales
def mostrarParcial(cant_reg):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id_destino, nombre, descripcion, actividades, costo FROM destino LIMIT %s"
        cursor = con.ejecutaQuery(sql, (cant_reg,))
        destinos = cursor.fetchall()
        return destinos
    except Exception:
        return []
    finally:
        con.desconectar()

# Actualizar destino
def modificarDestino(idDestino, nuevoNombre, nuevaDescripcion, nuevaActividad, nuevoCosto):
    try:
        con = Conexion(host, user, password, db)
        sql = """
        UPDATE destino 
        SET nombre = %s, descripcion = %s, actividades = %s, costo = %s 
        WHERE id_destino = %s
        """
        con.ejecutaQuery(sql, (nuevoNombre, nuevaDescripcion, nuevaActividad, nuevoCosto, idDestino))
        con.commit()
        return True
    except Exception:
        con.rollback()
        return False
    finally:
        con.desconectar()

# Eliminar destino
def eliminarDestino(idDestino):
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM destino WHERE id_destino = %s"
        con.ejecutaQuery(sql, (idDestino,))
        con.commit()
        return True
    except Exception:
        con.rollback()
        return False
    finally:
        con.desconectar()
