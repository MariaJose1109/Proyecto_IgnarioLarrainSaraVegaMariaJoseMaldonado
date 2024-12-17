import pymysql
from DAO.Conexion import Conexion

class CRUDUsuario:
    # Datos de conexión
    host = 'localhost'
    user = 'adminagencia'
    password = 'adminagencia'
    db = 'agencia_de_viajes'

    @staticmethod
    def agregarUsuario(usuario):
        try:
            con = Conexion(CRUDUsuario.host, CRUDUsuario.user, CRUDUsuario.password, CRUDUsuario.db)
            sql = """
            INSERT INTO usuario (nombre, correo, password, tipo_usuario, fecha_registro)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (usuario.nombre, usuario.correo, usuario.password, usuario.tipoUsuario, usuario.fechaRegistro)
            con.ejecutaQuery(sql, valores)
            con.commit()
            print("Usuario agregado con éxito.")
            return True
        except Exception as e:
            print(f"Error al agregar el usuario: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.desconectar()

    @staticmethod
    def obtenerUsuario(correo):
        try:
            con = Conexion(CRUDUsuario.host, CRUDUsuario.user, CRUDUsuario.password, CRUDUsuario.db)
            sql = """
            SELECT id_usuario, nombre, correo, password, tipo_usuario, fecha_registro
            FROM usuario
            WHERE correo = %s LIMIT 1
            """
            cursor = con.ejecutaQuery(sql, (correo,))
            usuarioData = cursor.fetchone()
            return usuarioData
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            if con:
                con.desconectar()
    @staticmethod
    def mostrarTodos():
        try:
            con = Conexion(CRUDUsuario.host, CRUDUsuario.user, CRUDUsuario.password, CRUDUsuario.db)
            sql = """
            SELECT id_usuario, nombre, correo, tipo_usuario
            FROM usuario
            """
            cursor = con.ejecutaQuery(sql)
            usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            print(f"Error al obtener la lista de usuarios: {e}")
            return []
        finally:
            if con:
                con.desconectar()