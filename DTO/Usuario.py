from DAO.CRUDUsuario import CRUDUsuario
import bcrypt
from datetime import datetime


class Usuario:
    def __init__(self, nombre, correo, password, tipoUsuario):
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.tipoUsuario = tipoUsuario
        self.fechaRegistro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def login(correo, password):
        try:
            usuario_data = CRUDUsuario.obtenerUsuario(correo)
            if not usuario_data:
                print("\nError: Correo no registrado. Intente nuevamente.\n")
                return {"autenticado": False, "tipo_usuario": None}

            # Comparar contraseña hasheada
            stored_password = usuario_data.get("password")
            if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("\n¡Inicio de sesión exitoso!\n")
                return {
                    "autenticado": True,
                    "id_usuario": usuario_data.get("id_usuario"),
                    "nombre": usuario_data.get("nombre"),
                    "tipo_usuario": usuario_data.get("tipo_usuario")
                }
            else:
                print("\nError: Contraseña incorrecta. Intente nuevamente.\n")
                return {"autenticado": False, "tipo_usuario": None}
        except Exception as e:
            print("\nOcurrió un error inesperado durante el inicio de sesión. Intente más tarde.\n")
            print(f"Detalles del error: {e}")
            return {"autenticado": False, "tipo_usuario": None}

    @staticmethod
    def registrarUsuario(nombre, correo, password, tipoUsuario):
        # Verificar si el correo ya está registrado
        if CRUDUsuario.obtenerUsuario(correo):
            print("\nError: El correo ya está registrado.\n")
            return None

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Crear instancia del nuevo usuario
        nuevoUsuario = Usuario(nombre, correo, hashed_password, tipoUsuario)

        # Insertar el usuario en la base de datos
        if CRUDUsuario.agregarUsuario(nuevoUsuario):
            print(f"\nUsuario '{nombre}' registrado con éxito.\n")
            return nuevoUsuario
        else:
            print(f"\nError al registrar el usuario '{nombre}'.\n")
            return None
