from DAO.CRUDDestino import *
from DAO.CRUDUsuario import *
from DTO.Usuario import * 
from DTO.Destino import Destino
import os
import json


def registrarUsuario():
    os.system('cls')
    print("---------------------------")
    print("     REGISTRAR USUARIO     ")
    print("---------------------------")
    while True:
        nombre = input("Ingrese Usuario: ").strip()
        correo = input("Ingrese Correo: ").strip()
        password = input("Ingrese Contraseña: ").strip()
        tipo_usuario = input("Ingrese tipo Usuario (administrador/cliente): ").strip()
        if not nombre or not password or not correo or not tipo_usuario:
            print("Usuario, contraseña, correo y/o tipo Usuario no pueden estar vacíos.")
            continue  
        if tipo_usuario not in ["administrador", "cliente"]:
            print("El tipo de usuario debe ser 'administrador' o 'cliente'.")
            continue 
        nuevo_usuario = Usuario.registrarUsuario(nombre, correo, password, tipo_usuario)
        if nuevo_usuario:
            print(f"Usuario {nombre} registrado con éxito.")
            return nuevo_usuario  
        else:
            retry = input("¿Intentar de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                return None  
    
        
#Función para el inicio de sesión 
def login():
    print("---------------------------")
    print("          LOGIN            ")
    print("---------------------------")
    
    while True:
        correo = input("Ingrese Correo: ").strip()
        password = input("Ingrese Contraseña: ").strip()
        if not correo or not password:
            print("Datos de inicio de sesión no pueden estar vacíos.")
        else:
            resultado_login = Usuario.login(correo, password)  # Intenta iniciar sesión
            if resultado_login["autenticado"]:
                print("\n¡Inicio de sesión exitoso!")
                return resultado_login["tipo_usuario"]  # Retorna el tipo de usuario
            else:
                print("\nCorreo o contraseña incorrectos.")
                retry = input("¿Intentar de nuevo? [SI/NO]: ").strip().lower()
                if retry != "si":
                    print("Saliendo del proceso de inicio de sesión.")
                    return None
                
#menu destinos
def menuDestinos():
    while True:
        print("--------------------------")
        print("       MENÚ DESTINOS      ")
        print("--------------------------")
        print("1. Registrar Destino")
        print("2. Consultar Destinos")
        print("3. Actualizar Destino")
        print("4. Eliminar Destino")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            nombre = input("Ingrese el nombre del destino: ").strip()
            descripcion = input("Ingrese la descripción: ").strip()
            actividades = input("Ingrese las actividades: ").strip()
            costo = int(input("Ingrese el costo: "))
            # se crea el objeto destino
            nuevo_destino = Destino(nombre, descripcion, actividades, costo)
            agregarDestino(nuevo_destino, "administrador")  # Se pasa el objeto y el rol de administrador
        elif opcion == "2":
            destinos = consultarDestinos()
            for destino in destinos:
                print(destino)
        elif opcion == "3":
            destino_id = input("Ingrese el ID del destino a actualizar: ").strip()
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            nueva_descripcion = input("Ingrese la nueva descripción: ").strip()
            nuevo_precio = input("Ingrese el nuevo precio: ").strip()
            actualizarDestino(destino_id, nuevo_nombre, nueva_descripcion, nuevo_precio)
        elif opcion == "4":
            destino_id = input("Ingrese el ID del destino a eliminar: ").strip()
            eliminarDestino(destino_id)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")


def main():
    while True:
        os.system('cls')
        print("---------------------------")
        print("     1. Login             ")
        print("     2. Registro          ")
        print("     3. Salir            ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            tipo_usuario = login()
            if tipo_usuario:
                if tipo_usuario == "administrador":
                    menuAdmin()
                elif tipo_usuario == "cliente":
                    menuClientes()
                else:
                    print("Tipo de usuario no reconocido.")
                break
            else:
                print("Error al autenticar usuario.")
        elif opcion == "2":
            registrarUsuario()
        elif opcion == "3":
            print("Saliendo del programa...")
            exit()
        else:
            print("Opción no válida.")

# menu administrador
def menuAdmin():
    while True:
        os.system('cls')
        print("--------------------------")
        print("       MENÚ ADMIN         ")
        print("--------------------------")
        print("1. Gestionar Destinos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menuDestinos()
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

#menu cliente
def menuClientes():
    while True:
        os.system('cls')
        print("--------------------------")
        print("       MENÚ CLIENTE      ")
        print("--------------------------")
        print("1. Consultar Destinos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            destinos = consultarDestinos()
            for destino in destinos:
                print(destino)
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()