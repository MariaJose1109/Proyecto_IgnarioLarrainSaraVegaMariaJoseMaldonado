from DAO.Conexion import Conexion
from datetime import datetime

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'agencia_de_viajes'


def agregarUsuario(usuario):
    con = None
    try:
        con = Conexion(host, user, password, db)
        sql = "insert into usuario set nombre='{}', correo='{}', password='{}', tipo_usuario='{}', fecha_registro='{}'".format( usuario.nombre, usuario.correo, usuario.password, usuario.tipo_usuario, usuario.fecha_registro)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al Agregar un Usuario: {e}")
        return False


#mostrar todos
def obtenerUsuario(correo):
    try:
        con = Conexion(host, user, password, db)
        sql = "select * from usuario where correo = '{}'".format(correo)
        cursor = con.ejecutar_query(sql)
        datos = cursor.fetchone()  # Obtén solo un registro
        con.desconectar()
        return datos
    except Exception as e:
        print(f"Error al Obtener al Usuario: {e}")
        return None

#mostrar parcial
#mostrar uno

## ya lo obtiene el login 
def obtenerRolUsuario(nombre):
    try:
        con = Conexion(host, user, password, db)
        sql = "select tipo_usuario from usuario where nombre = '{}'".format(nombre)
        cursor = con.ejecutar_query(sql) 
        rol = cursor.fetchone()  # solo devuelve el rol
        con.desconectar()
        if rol:
            return rol[0]  # retorna el tipo de usuario (administrador o cliente)
        else:
            print("Usuario no encontrado.")
            return None
    except Exception as e:
        print(f"Error al obtener el rol del usuario: {e}")
        return None

