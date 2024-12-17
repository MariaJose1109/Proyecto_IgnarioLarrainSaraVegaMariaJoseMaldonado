from DAO.Conexion import Conexion
from datetime import datetime

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Agregar paquete turístico
def agregarPaquete(paquete):
    """
    Inserta un paquete en la base de datos.
    paquete: Objeto con atributos nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = con.ejecutaQuery(sql, (
            paquete.nombre_paquete,
            paquete.descripcion,
            paquete.precio_total,
            paquete.fecha_inicio,
            paquete.fecha_fin
        ))
        con.commit()
        # Capturar el ID del paquete recién insertado
        paquete.id_paquete = cursor.lastrowid
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al agregar el paquete: {e}")
        return False
    finally:
        con.desconectar()

# Agregar paquete con destinos relacionados
def agregarPaqueteConDestino(paquete, destinos):
    """
    Inserta un paquete turístico y agrega los destinos relacionados en detalle_paquete.
    - paquete: Objeto con atributos nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin.
    - destinos: Lista de diccionarios con id_destino.
    """
    con = None
    try:
        con = Conexion(host, user, password, db)

        # 1. Insertar el paquete turístico
        sql_paquete = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = con.ejecutaQuery(sql_paquete, (
            paquete.nombre_paquete,
            paquete.descripcion,
            paquete.precio_total,
            paquete.fecha_inicio,
            paquete.fecha_fin
        ))
        paquete.id_paquete = cursor.lastrowid  # Capturar el ID del paquete

        # 2. Insertar los destinos relacionados
        sql_detalle = "INSERT INTO detalle_paquete (id_paquete, id_destino) VALUES (%s, %s)"
        for destino in destinos:
            con.ejecutaQuery(sql_detalle, (paquete.id_paquete, destino['id_destino']))

        con.commit()
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al agregar paquete con destinos: {e}")
        return False
    finally:
        if con:
            con.desconectar()

# Eliminar paquete turístico
def eliminarPaquete(idPaquete):
    """
    Elimina un paquete turístico por su ID.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM paquete_turistico WHERE id_paquete = %s"
        con.ejecutaQuery(sql, (idPaquete,))
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar el paquete: {e}")
        return False
    finally:
        con.desconectar()

# Mostrar un paquete por ID
def mostrarUno(idPaquete):
    """
    Consulta y retorna un paquete turístico por su ID.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico 
        WHERE id_paquete = %s
        """
        cursor = con.ejecutaQuery(sql, (idPaquete,))
        paquete = cursor.fetchone()
        return paquete
    except Exception as e:
        print(f"Error al consultar paquete: {e}")
        return None
    finally:
        con.desconectar()

# Mostrar paquetes parciales
def mostrarParcial(cant_reg):
    """
    Consulta y retorna una cantidad limitada de paquetes turísticos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico 
        LIMIT %s
        """
        cursor = con.ejecutaQuery(sql, (cant_reg,))
        paquetes = cursor.fetchall()
        return paquetes
    except Exception as e:
        print(f"Error al consultar paquetes parciales: {e}")
        return []
    finally:
        con.desconectar()

# Mostrar todos los paquetes turísticos
def mostrarTodos():
    """
    Consulta y retorna todos los paquetes turísticos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico
        """
        cursor = con.ejecutaQuery(sql)
        paquetes = cursor.fetchall()
        return paquetes
    except Exception as e:
        print(f"Error al consultar todos los paquetes: {e}")
        return []
    finally:
        con.desconectar()

