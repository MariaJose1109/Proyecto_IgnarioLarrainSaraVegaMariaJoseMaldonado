from DAO.CRUDUsuario import *
import bcrypt


class Usuario:
    def __init__(self, nombre, correo, password, tipo_usuario):
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.tipo_usuario = tipo_usuario
        self.fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    @staticmethod
    def login(correo, password):
        usuario_data = obtenerUsuario(correo)
        if usuario_data:
            stored_password = usuario_data[3]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Inicio de sesión exitoso.")
                return {"autenticado": True, "tipo_usuario": usuario_data[4], "nombre": usuario_data[1] } # retorna autenticado para el login. tambien captura el tipo de usuario 
            else:
                print("Contraseña incorrecta.")
        else:
            print("Usuario no encontrado.")
        return {"autenticado": False, "tipo_usuario": None}
    
    @staticmethod
    def registrarUsuario(nombre, correo, password, tipo_usuario):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nuevo_usuario = Usuario(nombre, correo, hashed_password, tipo_usuario)
        if agregarUsuario(nuevo_usuario):
            print(f"Usuario {nombre} registrado con éxito.")
            return nuevo_usuario
        else:
            print(f"Error al registrar el usuario {nombre}.")
            return None