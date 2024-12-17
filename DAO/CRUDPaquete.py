from DAO.Conexion import Conexion
from datetime import datetime

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Agregar paquete turístico
def agregarPaquete(paquete):
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = con.ejecutaQuery(sql, (paquete.nombre, paquete.descripcion, paquete.costo, paquete.fechaIda, paquete.fechaVuelta))
        con.commit()
        paquete.idPaquete = cursor.lastrowid  # Capturar el ID recién insertado
        print("Paquete turístico agregado con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al agregar el paquete turístico: {e}")
        return False
    finally:
        con.desconectar()

# Eliminar paquete turístico
def eliminarPaquete(idPaquete):
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM paquete_turistico WHERE id_paquete = %s"
        con.ejecutaQuery(sql, (idPaquete,))
        con.commit()
        print("Paquete turístico eliminado con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar el paquete turístico: {e}")
        return False
    finally:
        con.desconectar()

# Mostrar un paquete por ID
def mostrarUno(idPaquete):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM paquete_turistico WHERE id_paquete = %s"
        cursor = con.ejecutaQuery(sql, (idPaquete,))
        paquete = cursor.fetchone()
        con.desconectar()

        if paquete:
            print("Paquete encontrado:", paquete)
        else:
            print(f"No se encontró ningún paquete con el ID: {idPaquete}")
        return paquete
    except Exception as e:
        print(f"Error al consultar el paquete turístico: {e}")
        return None
    finally:
        con.desconectar()

# Mostrar paquetes parciales
def mostrarParcial(cant_reg):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM paquete_turistico LIMIT %s"
        cursor = con.ejecutaQuery(sql, (cant_reg,))
        paquetes = cursor.fetchall()
        con.desconectar()

        if paquetes:
            print(f"Mostrando {len(paquetes)} paquetes turísticos:")
            for paquete in paquetes:
                print(paquete)
        else:
            print("No hay paquetes turísticos para mostrar.")
        return paquetes
    except Exception as e:
        print(f"Error al consultar paquetes parciales: {e}")
        return []
    finally:
        con.desconectar()

# Mostrar todos los paquetes turísticos
def mostrarTodos():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM paquete_turistico"
        cursor = con.ejecutaQuery(sql)
        paquetes = cursor.fetchall()
        con.desconectar()

        if paquetes:
            print("Lista de paquetes turísticos:")
            for paquete in paquetes:
                print(paquete)
        else:
            print("No hay paquetes turísticos registrados.")
        return paquetes
    except Exception as e:
        print(f"Error al consultar todos los paquetes turísticos: {e}")
        return []
    finally:
        con.desconectar()
