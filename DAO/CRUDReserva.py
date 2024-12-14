from DAO.Conexion import Conexion

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'agencia_de_viajes'


def realizarReserva(reserva):
    try:
        con = Conexion(host, user, password, db)
       # Validar existencia de id_usuario
       # cursor = con.cursor()
       # cursor.execute("select count(*) from usuario where id_usuario ={}".format(reserva.id_usuario))
       # if cursor.fetchone()[0] == 0:
       #     print("Error: El id_usuario no existe.")
       #     return False
       # # Validar existencia de id_usuario
       # cursor.execute("select count(*) from paquete_turistico where id_paquete ={}", (reserva.id_paquete))
       # if cursor.fetchone()[0] == 0:
       #     print("Error: El id_paquete no existe.")
       #     return False
        # Validar el estado
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

#mostrar parcial
def mostrarReservaParcial(cant_reg):
    try:
        con=Conexion(host,user,password,db)
        sql="select * from reserva"
        cursor=con.ejecutar_query(sql)
        reserva=cursor.fetchmany(size=cant_reg)
        con.desconectar()
        return reserva
    except Exception as e:
        print(f"Error al consultar las reservas: {e}")
        input("Presione Enter para Continuar")

#mostrar uno
def consultarUnPaquete(id_reserva):
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from reserva where id_reserva  = {}".format(id_reserva)
        cursor = con.ejecutar_query(sql)
        paquete_turistico = cursor.fetchall()
        con.desconectar()
        return paquete_turistico
    except Exception as e:
        print(f"Error al consultar las Reserva: {e}")
        input("Presione Enter para Continuar")



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
    
#esta solo cambia el estaod de la reserva a 'cancelado'
def cancelarReserva(id_reserva):
    try:
        con = Conexion(host, user, password, db)
        
        # Cambiar el estado de la reserva a 'cancelado'
        sql = "UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = {}".format(id_reserva)
        
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Reserva cancelada con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al cancelar la reserva: {e}")
        return False


def validarEstadoReserva(id_reserva, estado_requerido):
    try:
        con = Conexion(host, user, password, db)
        cursor = con.ejecutar_query(f"SELECT estado FROM reserva WHERE id_reserva = {id_reserva}")
        resultado = cursor.fetchone()
        con.desconectar()

        if resultado and resultado[0] == estado_requerido:
            return True
        else:
            print(f"El estado actual de la reserva no es '{estado_requerido}'.")
            return False
    except Exception as e:
        print(f"Error al validar el estado de la reserva: {e}")
        return False
