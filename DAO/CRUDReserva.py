from DAO.Conexion import Conexion

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Registrar reserva
def registrarReserva(reserva):
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
def obtenerReserva():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM reserva"
        cursor = con.ejecutaQuery(sql)
        reservas = cursor.fetchall()
        con.desconectar()
        
        if reservas:
            print("Reservas encontradas:")
            for reserva in reservas:
                print(reserva)
        else:
            print("No hay reservas registradas.")
        return reservas
    except Exception as e:
        print(f"Error al consultar las reservas: {e}")
        return []

# Consultar reservas por ID de usuario
def obtenerReserva(idUsuario):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM reserva WHERE id_usuario = %s"
        cursor = con.ejecutaQuery(sql, (idUsuario,))
        reservas = cursor.fetchall()
        con.desconectar()

        if reservas:
            print(f"Reservas del usuario {idUsuario}:")
            for reserva in reservas:
                print(reserva)
        else:
            print(f"No se encontraron reservas para el usuario {idUsuario}.")
        return reservas
    except Exception as e:
        print(f"Error al consultar las reservas del usuario: {e}")
        return []

# Eliminar reserva
def eliminarReserva(idReserva):
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM reserva WHERE id_reserva = %s"
        con.ejecutaQuery(sql, (idReserva,))
        con.commit()
        print("Reserva eliminada con éxito.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar la reserva: {e}")
        return False
    finally:
        con.desconectar()

# Cancelar reserva (cambia el estado a 'cancelada')
def cancelarReserva(idReserva):
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

# Cambiar estado de una reserva
def cambiarEstadoReserva(idReserva, nuevoEstado):
    try:
        if nuevoEstado not in ['pendiente', 'confirmada', 'cancelada']:
            raise ValueError(f"Estado inválido: {nuevoEstado}")

        con = Conexion(host, user, password, db)
        sql = "UPDATE reserva SET estado = %s WHERE id_reserva = %s"
        cursor = con.ejecutaQuery(sql, (nuevoEstado, idReserva))
        if cursor.rowcount > 0:
            con.commit()
            print(f"El estado de la reserva {idReserva} ha sido actualizado a '{nuevoEstado}'.")
            return True
        else:
            print(f"No se encontró la reserva {idReserva} para actualizar.")
            return False
    except Exception as e:
        con.rollback()
        print(f"Error al cambiar el estado de la reserva: {e}")
        return False
    finally:
        con.desconectar()
