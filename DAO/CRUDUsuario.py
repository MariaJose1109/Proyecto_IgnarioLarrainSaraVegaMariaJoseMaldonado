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
    def existeUsuario(id_usuario):
        """
        Verifica si un usuario existe en la base de datos por su ID.
        """
        try:
            con = Conexion(CRUDUsuario.host, CRUDUsuario.user, CRUDUsuario.password, CRUDUsuario.db)
            sql = "SELECT 1 FROM usuario WHERE id_usuario = %s LIMIT 1"
            cursor = con.ejecutaQuery(sql, (id_usuario,))
            resultado = cursor.fetchone()
            return resultado is not None
        except Exception as e:
            print(f"Error al verificar la existencia del usuario: {e}")
            return False
        finally:
            if con:
                con.desconectar()
            