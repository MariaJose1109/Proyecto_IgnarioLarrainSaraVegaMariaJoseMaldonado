from DAO.Conexion import Conexion
from datetime import datetime

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Registrar reserva
def agregarReserva(reserva):
    """
    Inserta una nueva reserva en la base de datos.
    """
    con = None
    try:
        # Validar formato de fecha
        if not isinstance(reserva.fechaReserva, str):
            raise ValueError("La fecha debe ser una cadena en formato DD-MM-YYYY.")
        
        # Convertir fecha al formato YYYY-MM-DD
        fecha_reserva = datetime.strptime(reserva.fechaReserva, "%d-%m-%Y").strftime("%Y-%m-%d")

        # Validar estado de la reserva
        if reserva.estado not in ['pendiente', 'confirmada', 'cancelada']:
            raise ValueError(f"Estado inválido: {reserva.estado}")

        # Establecer conexión y ejecutar la consulta
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO reserva (id_usuario, id_paquete, fecha_reserva, estado)
        VALUES (%s, %s, %s, %s)
        """
        con.ejecutaQuery(sql, (reserva.idUsuario, reserva.idPaquete, fecha_reserva, reserva.estado))
        con.commit()
        print("Reserva registrada con éxito.")
        return True

    except ValueError as ve:
        print(f"Error: {ve}")
        return False
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al realizar la reserva: {e}")
        return False
    finally:
        if con:
            con.desconectar()
# Consultar todas las reservas
def mostrarTodos():
    """
    Obtiene todas las reservas registradas en la base de datos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT r.id_reserva, r.id_usuario, u.nombre AS nombre_usuario,
               r.id_paquete, p.nombre_paquete, r.fecha_reserva, r.estado
        FROM reserva r
        INNER JOIN usuario u ON r.id_usuario = u.id_usuario
        INNER JOIN paquete_turistico p ON r.id_paquete = p.id_paquete
        """
        cursor = con.ejecutaQuery(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al consultar las reservas: {e}")
        return []
    finally:
        con.desconectar()

# Consultar una reserva por ID
def mostrarUno(idReserva):
    """
    Obtiene una reserva específica por ID.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT r.id_reserva, r.id_usuario, u.nombre AS nombre_usuario,
               r.id_paquete, p.nombre_paquete, r.fecha_reserva, r.estado
        FROM reserva r
        INNER JOIN usuario u ON r.id_usuario = u.id_usuario
        INNER JOIN paquete_turistico p ON r.id_paquete = p.id_paquete
        WHERE r.id_reserva = %s
        """
        cursor = con.ejecutaQuery(sql, (idReserva,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al consultar la reserva: {e}")
        return None
    finally:
        con.desconectar()

# Consultar reservas parciales por estado
def mostrarParcial(estado):
    """
    Obtiene reservas filtradas por estado (pendiente, confirmada, cancelada).
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT r.id_reserva, r.id_usuario, u.nombre AS nombre_usuario,
               r.id_paquete, p.nombre_paquete, r.fecha_reserva, r.estado
        FROM reserva r
        INNER JOIN usuario u ON r.id_usuario = u.id_usuario
        INNER JOIN paquete_turistico p ON r.id_paquete = p.id_paquete
        WHERE r.estado = %s
        """
        cursor = con.ejecutaQuery(sql, (estado,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al consultar reservas parciales: {e}")
        return []
    finally:
        con.desconectar()

# Eliminar una reserva
def eliminarReserva(idReserva):
    """
    Elimina una reserva específica de la base de datos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM reserva WHERE id_reserva = %s"
        con.ejecutaQuery(sql, (idReserva,))
        con.commit()
        print(f"Reserva {idReserva} eliminada con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar la reserva: {e}")
        return False
    finally:
        con.desconectar()

# Cambiar el estado de una reserva
def cambiarEstadoReserva(idReserva, nuevoEstado):
    """
    Actualiza el estado de una reserva específica.
    """
    con = None
    try:
        con = Conexion(host, user, password, db)

        # Verificar si la reserva existe y su estado actual
        verificar_sql = "SELECT estado FROM reserva WHERE id_reserva = %s"
        cursor = con.ejecutaQuery(verificar_sql, (idReserva,))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"No se encontró la reserva {idReserva}.")
            return False

        estado_actual = resultado['estado']
        if estado_actual == "cancelada":
            print(f"La reserva {idReserva} ya está cancelada y no puede modificarse.")
            return False

        if estado_actual == nuevoEstado:
            print(f"La reserva {idReserva} ya está en estado '{nuevoEstado}'.")
            return False

        # Actualizar el estado de la reserva
        actualizar_sql = "UPDATE reserva SET estado = %s WHERE id_reserva = %s"
        con.ejecutaQuery(actualizar_sql, (nuevoEstado, idReserva))
        con.commit()

        print(f"Reserva {idReserva} actualizada a estado '{nuevoEstado}'.")
        return True

    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al actualizar la reserva: {e}")
        return False

    finally:
        if con:
            con.desconectar()

# Consultar reservas por ID de usuario
def mostrarReservaPorId(id_usuario):
    """
    Obtiene todas las reservas de un usuario específico.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT r.id_reserva, r.id_paquete, 
               IF(r.fecha_reserva = '0000-00-00', 'Fecha no válida', r.fecha_reserva) AS fecha_reserva, 
               r.estado
        FROM reserva r
        WHERE r.id_usuario = %s
        """
        cursor = con.ejecutaQuery(sql, (id_usuario,))
        reservas = cursor.fetchall()
        return reservas
    except Exception as e:
        print(f"Error al consultar las reservas del usuario {id_usuario}: {e}")
        return []
    finally:
        if con:
            con.desconectar()