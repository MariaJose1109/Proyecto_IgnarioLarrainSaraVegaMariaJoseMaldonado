from DAO.Conexion import Conexion

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'viajes_aventura_bd'


def realizarReserva(reserva):
    try:
        con = Conexion(host, user, password, db)
        if reserva.estado not in ['pendiente', 'confirmada', 'cancelada']:
            raise ValueError(f"Estado inválido: {reserva.estado}")
        sql = "insert into reserva set id_usuario={}, id_paquete={}, fecha_reserva='{}', estado='{}'".format(
            reserva.id_usuario, reserva.id_paquete, reserva.fecha_reserva, reserva.estado.replace("'", "''")
        )
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Reserva registrada con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al realizar la reserva: {e}")
        return False
#mostrar todos
def consultarTodosReserva():
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from reserva"
        cursor = con.ejecutar_query(sql)
        reserva = cursor.fetchall()
        con.desconectar()
        return reserva
    except Exception as e:
        print(f"Error al consultar las reserva: {e}")
        input("Presione Enter para Continuar")

def mostrarReservaPorId(id_usuario):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM reserva WHERE id_usuario = {}".format(id_usuario)
        cursor = con.ejecutar_query(sql)

        # Asumiendo que 'cursor' es un iterable que contiene las filas de la consulta
        if cursor:  # Si hay resultados
            reservas = cursor.fetchall()  # Obtener todas las filas
            if reservas:  # Si hay reservas
                print("\n--- Tus reservas ---")
                for reserva in reservas:
                    print(f"ID Reserva: {reserva['id_reserva']}, Paquete ID: {reserva['id_paquete']}, Fecha: {reserva['fecha_reserva']}, Estado: {reserva['estado']}")
                return reservas  # Devolver la lista de reservas
            else:
                print("No tienes reservas registradas.")
                return None
        else:
            print("Error: No se pudo obtener el cursor.")
            return None

    except Exception as e:
        print(f"Error al consultar las reservas: {e}")
        return None  # En caso de error, devolvemos None



def eliminarReserva(id_reserva):
    try:
        con = Conexion(host, user, password, db)
        sql = "delete from reserva where id_reserva = {}".format(id_reserva)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Reseerva eliminar con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al eliminar la reserva: {e}")
        return False
    
# manejo de estados de reserva
#esta solo cambia el estaod de la reserva a 'cancelado'
def verificarEstadoReserva(id_reserva):
    try:
        con = Conexion(host, user, password, db)
        cursor = con.ejecutar_query(f"SELECT estado FROM reserva WHERE id_reserva = {id_reserva}")
        resultado = cursor.fetchone()
        con.desconectar()

        if resultado:
            estado_actual = resultado[0].strip().lower()  # Accede al estado
            return estado_actual
        else:
            print(f"No se encontró una reserva con el ID {id_reserva}.")
            return None
    except Exception as e:
        print(f"Error al verificar el estado de la reserva: {e}")
        return None

# Función de cancelar reserva
# Función de cancelar reserva
def cancelarReserva(id_reserva):
    try:
        con = Conexion(host, user, password, db)
        
        # Ejecutar la consulta para obtener el estado de la reserva
        resultado = con.ejecutar_query(f"SELECT estado FROM reserva WHERE id_reserva = {id_reserva}")
        estado_reserva = resultado.fetchone()  # Esto devuelve un diccionario
        if not estado_reserva:
            print(f"La reserva con ID {id_reserva} no existe en la base de datos.")
            return False
        estado_actual = estado_reserva['estado'].strip().lower()  # Accedemos al estado con la clave 'estado'
        print(f"Estado actual de la reserva con ID {id_reserva}: {estado_actual}")  # Imprimir estado para depuración
        if estado_actual != "pendiente":
            print(f"No se puede cancelar: la reserva no está en estado 'pendiente' (estado actual: {estado_actual}).")
            return False
        sql = f"UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = {id_reserva}"
        print(f"Ejecutando consulta SQL: {sql}")  # Imprimir la consulta SQL
        cursor = con.ejecutar_query(sql)
        if cursor.rowcount > 0:
            print(f"Reserva con ID {id_reserva} cancelada con éxito.")
            con.commit()
            return True
        else:
            print(f"No se encontró una reserva con ID {id_reserva} para cancelar.")
            return False
        
    except Exception as e:
        print(f"Error al cancelar la reserva: {e}")
        return False
    finally:
        con.desconectar()



def cambiarEstadoReserva(id_reserva, nuevo_estado):
    try:
        con = Conexion(host, user, password, db)
        sql = f"UPDATE reserva SET estado = '{nuevo_estado}' WHERE id_reserva = {id_reserva}"
        cursor = con.ejecutar_query(sql)  # Asegúrate de que esto devuelve un cursor y no una cadena

        # Comprobamos el número de filas afectadas
        if cursor.rowcount > 0:
            print(f"El estado de la reserva {id_reserva} ha sido actualizado a '{nuevo_estado}'.")
            con.commit()
            return True
        else:
            print(f"No se encontró ninguna reserva con ID {id_reserva} para actualizar.")
            con.rollback()
        con.desconectar()
    except Exception as e:
        print(f"Error al cambiar el estado de la reserva: {e}")

def consultarPaquetesDisponibles():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id_paquete, nombre_paquete, descripcion, precio_total FROM paquete_turistico"
        cursor = con.ejecutar_query(sql)
        paquetes = cursor.fetchall()
        con.desconectar()
        return paquetes
    except Exception as e:
        print(f"Error al consultar los paquetes disponibles: {e}")
        return []

# Función para consultar usuarios de tipo "cliente"
def consultarUsuariosTipoCliente():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id_usuario, nombre FROM usuario WHERE tipo_usuario = 'cliente'"
        cursor = con.ejecutar_query(sql)
        usuarios = cursor.fetchall()  # Debería ser una lista de diccionarios o tuplas
        con.desconectar()
        return usuarios
    except Exception as e:
        print(f"Error al consultar los usuarios tipo cliente: {e}")
        return []
