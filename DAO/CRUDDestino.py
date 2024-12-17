from DAO.Conexion import Conexion
from DTO.Destino import Destino

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
        print("Destino registrado con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al registrar el destino: {e}")
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
        if datos:
            print("Destinos encontrados:")
            for destino in datos:
                print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, Descripción: {destino['descripcion']}, Actividades: {destino['actividades']}, Costo: ${destino['costo']}")
        else:
            print("No hay destinos registrados.")
        return datos
    except Exception as e:
        print(f"Error al consultar los destinos: {e}")
        return []
    finally:
        con.desconectar()

# Mostrar un destino por ID
def mostrarUno(idDestino):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM destino WHERE id_destino = %s"
        cursor = con.ejecutaQuery(sql, (idDestino,))
        destino = cursor.fetchone()
        if destino:
            print("Destino encontrado:", destino)
        else:
            print(f"No se encontró ningún destino con el ID: {idDestino}")
        return destino
    except Exception as e:
        print(f"Error al consultar el destino: {e}")
        return None
    finally:
        con.desconectar()

# Mostrar destinos parciales
def mostrarParcial(cant_reg):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM destino LIMIT %s"
        cursor = con.ejecutaQuery(sql, (cant_reg,))
        destinos = cursor.fetchall()
        if destinos:
            print(f"Mostrando {len(destinos)} destinos:")
            for destino in destinos:
                print(destino)
        else:
            print("No hay destinos disponibles para mostrar.")
        return destinos
    except Exception as e:
        print(f"Error al consultar destinos parciales: {e}")
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
        con.ejecutaQuery(sql, (idDestino, nuevoNombre, nuevaDescripcion, nuevaActividad, nuevoCosto))
        con.commit()
        print("Destino actualizado con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al actualizar el destino: {e}")
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
        print("Destino eliminado con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar el destino: {e}")
        return False
    finally:
        con.desconectar()
