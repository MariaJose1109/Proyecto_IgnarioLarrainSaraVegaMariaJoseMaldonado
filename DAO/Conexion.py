import pymysql
from pymysql.cursors import DictCursor  # Importamos el cursor para obtener resultados como diccionario

class Conexion:
    def __init__(self, host, user, password, db):
        try:
            self.conexion = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=DictCursor  # Configurar para que las respuestas sean diccionarios / Como ahora son diccionarios, la forma de buscar los atributos es a través del nombre y no la posición
            )
            self.cursor = self.conexion.cursor()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def ejecutar_query(self, sql):
        try:
            self.cursor.execute(sql)  # Ejecutar la consulta SQL
            return self.cursor  # Retornar el cursor
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def desconectar(self):
        try:
            self.conexion.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def commit(self):
        try:
            self.conexion.commit()
        except Exception as e:
            print(f"Error en commit: {e}")

    def rollback(self):
        try:
            self.conexion.rollback()
        except Exception as e:
            print(f"Error en rollback: {e}")
