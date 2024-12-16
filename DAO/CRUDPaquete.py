from DAO.Conexion import Conexion
from datetime import datetime

host = 'localhost'
user = 'admin1'
password = 'admin'
db = 'viajes_aventura_bd'


def agregarPaqueteConDestino(paquete, destinos_validos):
    try:
        con = Conexion(host, user, password, db)  # Conexión a la base de datos
        # Insertar el paquete turístico
        sql = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES ('{}', '{}', {}, '{}', '{}')
        """.format(paquete.nombre_paquete, paquete.descripcion, paquete.precio_total, paquete.fecha_inicio, paquete.fecha_fin)
        cursor = con.ejecutar_query(sql)
        con.commit()
        # Capturar el ID recién generado para el paquete
        id_paquete_creado = cursor.lastrowid
        # Verifica que el ID del paquete se haya generado correctamente
        if not id_paquete_creado:
            raise Exception("No se pudo generar un ID válido para el paquete.")
        # Insertar los destinos asociados al paquete en la tabla detalle_paquete
        for destino in destinos_validos:
            sql_destino = "INSERT INTO detalle_paquete (id_paquete, id_destino) VALUES ({}, {})".format(id_paquete_creado, destino['id_destino'])
            con.ejecutar_query(sql_destino)
        con.commit()
        con.desconectar()
        
        # Asignar el ID generado al objeto paquete
        paquete.id_paquete = id_paquete_creado
        return True
    except Exception as e:
        print(f"Error al registrar el paquete turístico: {e}")
        return False



def agregarPaqueteConDestinoPaquete(id_paquete, id_destino):
    try:
        con = Conexion(host, user, password, db)
        sql = "INSERT INTO detalle_paquete (id_paquete, id_destino) VALUES ({}, {})".format(id_paquete, id_destino)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print(f"Destino {id_destino} añadido correctamente al paquete {id_paquete}.")
        return True
    except Exception as e:
        print(f"Error al asociar el destino: {e}")
        return False

def actualizarPaqueteConDestino(id_paquete, nuevo_nombre, nueva_descripcion, id_destino, nueva_fecha_inicio, nueva_fecha_fin):
    try:
        con = Conexion(host, user, password, db)
        
        sql = "update paquete_turistico set nombre_paquete = '{}', descripcion = '{}', precio_total = (select costo from destino where id_destino = {}), fecha_inicio = '{}', fecha_fin = '{}' WHERE id_paquete = {}".format(
            nuevo_nombre, nueva_descripcion, id_destino, nueva_fecha_inicio, nueva_fecha_fin, id_paquete)
        con.ejecutar_query(sql)  # Ejecutar la consulta
        con.commit()  # Confirmar los cambios
        con.desconectar()  # Desconectar la base de datos
        print("Paquete turístico actualizado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()  # Revertir los cambios si algo falla
        print(f"Error al actualizar el paquete turístico: {e}")
        return False


#mostrar todos


def consultarTodosPaquetes():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM paquete_turistico"
        cursor = con.ejecutar_query(sql)
        paquete_turistico = cursor.fetchall()  # Esto devuelve una lista de diccionarios
        con.desconectar()

        # Convertir las fechas a datetime en los diccionarios
        for paquete in paquete_turistico:
            # Asegurarse de que las fechas se manejen correctamente
            if isinstance(paquete['fecha_inicio'], str) and paquete['fecha_inicio'] != '0000-00-00':
                try:
                    paquete['fecha_inicio'] = datetime.strptime(paquete['fecha_inicio'], "%Y-%m-%d")
                except ValueError:
                    paquete['fecha_inicio'] = "Fecha no válida"
            
            if isinstance(paquete['fecha_fin'], str) and paquete['fecha_fin'] != '0000-00-00':
                try:
                    paquete['fecha_fin'] = datetime.strptime(paquete['fecha_fin'], "%Y-%m-%d")
                except ValueError:
                    paquete['fecha_fin'] = "Fecha no válida"

        return paquete_turistico

    except Exception as e:
        print(f"Error al consultar el Paquete Turístico: {e}")
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



def eliminarPaquete(id_paquete):
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM paquete_turistico WHERE id_paquete = {}".format(id_paquete)
        con.ejecutar_query(sql)
        con.commit()
        con.desconectar()
        print("Paquete turístico eliminado con éxito.")
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al eliminar el paquete turístico: {e}")
        return False

