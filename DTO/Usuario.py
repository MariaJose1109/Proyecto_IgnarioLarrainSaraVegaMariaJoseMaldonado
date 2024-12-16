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
    @staticmethod
    def login(correo, password):
        usuario_data = obtenerUsuario(correo)
        if usuario_data:  # Si se ha encontrado el usuario
            print("Datos del usuario autenticado:", usuario_data)  # Para depuración
            stored_password = usuario_data['password']  # Accede al valor de la clave 'password'
            
            # Compara la contraseña hasheada con la ingresada por el usuario
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Inicio de sesión exitoso.")
                datos_usuario = {
                    "autenticado": True,
                    "tipo_usuario": usuario_data['tipo_usuario'],  # Tipo de usuario
                    "id_usuario": usuario_data['id_usuario'],  # ID del usuario
                    "nombre": usuario_data['nombre'],  # Nombre del usuario
                    "correo": usuario_data['correo']  # Agregar el correo al diccionario
                }
                print("Datos retornados por login:", datos_usuario)  # Verifica el diccionario retornado
                return datos_usuario
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