from DAO.Conexion import Conexion
from datetime import datetime

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'viajes_aventura_bd'


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


#mostrar uno
def obtenerUsuario(correo):
    try:
        con = Conexion('localhost', 'admin1', 'admin', 'viajes_aventura_bd')
        # Modifica la consulta para asegurar que solo obtienes un usuario
        sql = f"SELECT id_usuario, nombre, tipo_usuario, correo, password FROM usuario WHERE correo = '{correo}' LIMIT 1"
        cursor = con.ejecutar_query(sql)
        usuario_data = cursor.fetchone()  # Esto debería devolver un solo diccionario (el primer resultado)
        con.desconectar()
        return usuario_data  # Devuelve el diccionario del usuario encontrado
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None


def existeUsuario(id_usuario):
    try:
        print(f"Verificando existencia del usuario con ID: {id_usuario}")
        con = Conexion(host, user, password, db)
        if con is None:
            print("Error al conectar a la base de datos.")
            return False
        sql = "SELECT id_usuario FROM usuarios WHERE id_usuario = {}".format(id_usuario)
        cursor = con.ejecutar_query(sql)
        usuario = cursor.fetchone()
        con.desconectar()
        return usuario is not None
    except Exception as e:
        print(f"Error al verificar la existencia del usuario: {e}")
        return False
