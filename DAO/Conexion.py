import pymysql

class Conexion:
    def __init__(self,host,user,password,db):
        self.db=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        self.cursor=self.db.cursor()
    
    def ejecutar_query(self, sql):
        try:
            cursor = self.db.cursor()  # Crear un cursor nuevo en cada llamada
            cursor.execute(sql)
            return cursor
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def desconectar(self):
        self.db.close()
    
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
    