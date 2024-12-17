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
                cursorclass=DictCursor
            )
            self.cursor = self.db.cursor()
        except pymysql.MySQLError:
            self.db = None  # Conexión inválida

    def ejecutaQuery(self, sql, params=None):
        """Ejecuta una consulta SQL con parámetros opcionales. Retorna el cursor o None si hay error."""
        if not self.db:
            return None
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor
        except pymysql.MySQLError:
            return None

    def commit(self):
        """Confirma los cambios realizados en la base de datos. Retorna True si se realiza con éxito, de lo contrario None."""
        if not self.db:
            return None
        try:
            self.db.commit()
            return True
        except pymysql.MySQLError:
            return None

    def rollback(self):
        """Revierte los cambios realizados en la base de datos. Retorna True si se realiza con éxito, de lo contrario None."""
        if not self.db:
            return None
        try:
            self.db.rollback()
            return True
        except pymysql.MySQLError:
            return None

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if not self.db:
            return
        try:
            self.db.close()
        except pymysql.MySQLError:
            pass
        finally:
            self.db = None
