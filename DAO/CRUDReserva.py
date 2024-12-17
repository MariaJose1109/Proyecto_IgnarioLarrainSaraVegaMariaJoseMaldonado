from DAO.Conexion import Conexion

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
    try:
        con = Conexion(host, user, password, db)
        if reserva.estado not in ['pendiente', 'confirmada', 'cancelada']:
            raise ValueError(f"Estado inválido: {reserva.estado}")

        sql = """
        INSERT INTO reserva (id_usuario, id_paquete, fecha_reserva, estado)
        VALUES (%s, %s, %s, %s)
        """
        con.ejecutaQuery(sql, (reserva.idUsuario, reserva.idPaquete, reserva.fechaReserva, reserva.estado))
        con.commit()
        print("Reserva registrada con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al realizar la reserva: {e}")
        return False
    finally:
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
        reservas = cursor.fetchall()
        return reservas
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
        reserva = cursor.fetchone()
        return reserva
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
        reservas = cursor.fetchall()
        return reservas
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

# Cancelar reserva (actualiza el estado a 'cancelada')
def cancelarReserva(idReserva):
    """
    Cambia el estado de la reserva a 'cancelada' si está 'pendiente'.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = "UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s AND estado = 'pendiente'"
        cursor = con.ejecutaQuery(sql, (idReserva,))
        if cursor.rowcount > 0:
            con.commit()
            print(f"Reserva {idReserva} cancelada con éxito.")
            return True
        else:
            print(f"No se puede cancelar la reserva {idReserva}: no está en estado 'pendiente' o no existe.")
            return False
    except Exception as e:
        con.rollback()
        print(f"Error al cancelar la reserva: {e}")
        return False
    finally:
        con.desconectar()

# Confirmar reserva (actualiza el estado a 'confirmada')
def confirmarReserva(idReserva):
    """
    Cambia el estado de la reserva a 'confirmada'.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = "UPDATE reserva SET estado = 'confirmada' WHERE id_reserva = %s"
        cursor = con.ejecutaQuery(sql, (idReserva,))
        if cursor.rowcount > 0:
            con.commit()
            print(f"Reserva {idReserva} confirmada con éxito.")
            return True
        else:
            print(f"No se pudo confirmar la reserva {idReserva}: no existe.")
            return False
    except Exception as e:
        con.rollback()
        print(f"Error al confirmar la reserva: {e}")
        return False
    finally:
        con.desconectar()
