import pymysql
from pymysql.cursors import DictCursor

class Conexion:
    def __init__(self, host, user, password, db):
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=DictCursor  # Configurar resultados como diccionarios
            )
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.db = None  # Prevenir operaciones con una conexión inválida

    def ejecutaQuery(self, sql, params=None):
        """Ejecuta una consulta SQL con parámetros opcionales."""
        if not self.db:
            print("No se puede ejecutar la consulta: conexión no establecida.")
            return None
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor
        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def commit(self):
        """Confirma los cambios realizados en la base de datos."""
        if not self.db:
            print("No se puede realizar commit: conexión no establecida.")
            return
        try:
            self.db.commit()
        except pymysql.MySQLError as e:
            print(f"Error en commit: {e}")

    def rollback(self):
        """Revertir los cambios realizados en la base de datos."""
        if not self.db:
            print("No se puede realizar rollback: conexión no establecida.")
            return
        try:
            self.db.rollback()
            print("Cambios revertidos exitosamente.")
        except pymysql.MySQLError as e:
            print(f"Error en rollback: {e}")

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if not self.db:
            print("No se puede cerrar la conexión: ya está desconectada o no se estableció.")
            return
        try:
            self.db.close()
        except pymysql.MySQLError as e:
            print(f"Error al cerrar la conexión: {e}")
