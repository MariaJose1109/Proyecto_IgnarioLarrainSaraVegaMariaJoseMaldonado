from DAO.Conexion import Conexion


host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'agencia_de_viajes'


def agregarPaquete(paquete):
    try:
        con = Conexion(host, user, password, db)
        sql = "insert into paquete_turistico set nombre_paquete ='{}', descripcion='{}', precio_total ={}, fecha_inicio='{}',fecha_fin='{}'".format(
            paquete.nombre_paquete , paquete.descripcion, paquete.precio_total,paquete.fecha_inicio, paquete.fecha_fin)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Paquete Turístico registrado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al registrar el Paquete Turístico: {e}")
        return False


def actualizarPaquete(paquete,nombre):
    rol = obtenerRolUsuario(nombre)
    if rol != "administrador":
       print("Permiso denegado: Solo los administradores pueden agregar destinos.")
       return False
    try:
        con = Conexion(host, user, password, db)
        sql= "update paquete_turistico set nombre ='{}', descripcion='{}', precio_total ={}, destinos='{}', fecha_ida='{}',fecha_vuelta='{}".format(paquete[1],paquete[2],paquete[3],paquete[4],paquete[5],paquete[6],paquete[0])
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

#mostrar todos
def consultarTodosPaquetes():
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from paquete_turistico"
        cursor = con.ejecutar_query(sql)
        paquete_turistico = cursor.fetchall()
        con.desconectar()
        return paquete_turistico
    except Exception as e:
        print(f"Error al consultar el Paquete Turistico : {e}")
        input("Presione Enter para Continuar")

#mostrar parcial
def mostrarPaqueteParcial(cant_reg):
    try:
        con=Conexion(host,user,password,db)
        sql="select * from paquete_turistico"
        cursor=con.ejecutar_query(sql)
        paquete_turistico=cursor.fetchmany(size=cant_reg)
        con.desconectar()
        return paquete_turistico
    except Exception as e:
        print(f"Error al consultar el Paquete Turistico: {e}")
        input("Presione Enter para Continuar")

#mostrar uno
def consultarUnPaquete(id_paquete ):
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from paquete_turistico where id_paquete = {}".format(id_paquete )
        cursor = con.ejecutar_query(sql)
        paquete_turistico = cursor.fetchall()
        con.desconectar()
        return paquete_turistico
    except Exception as e:
        print(f"Error al consultar los Paquete Turistico: {e}")
        input("Presione Enter para Continuar")



def eliminarPaquete(id_paquete ):
    try:
        con = Conexion(host, user, password, db)
        sql = "delete from paquete_turistico where id_paquete = {}".format(id_paquete)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Paquete Turistico eliminado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al eliminar el Paquete Turistico: {e}")
        return False
