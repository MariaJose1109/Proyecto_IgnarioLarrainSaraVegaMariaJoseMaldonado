from DAO.CRUDDestino import *
from DAO.CRUDUsuario import *
from DAO.CRUDPaquete import *
from DAO.CRUDReserva import *
from DTO.PaqueteTuristico import * 
from DTO.Reserva import * 
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
        tipo_usuario = input("Ingrese tipo Usuario (administrador/cliente): ").strip().lower()
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
            print("Los campos de correo y contraseña no pueden estar vacíos. Intente nuevamente.")
            continue
        resultado_login = Usuario.login(correo, password) 
        if resultado_login["autenticado"]:
            print("\n¡Inicio de sesión exitoso!")
            return {
                "tipo_usuario": resultado_login["tipo_usuario"],
                "nombre": resultado_login["nombre"],  # Nombre del usuario (si está disponible)
                "correo": correo                      # Correo para referencia
                    }
        else:
            print("\nCorreo o contraseña incorrectos.")
            retry = input("¿Desea intentarlo de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                print("Cancelando inicio de sesión.")
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
            agregarDestino(nuevo_destino)  # Se pasa el objeto
        elif opcion == "2":
            destinos = consultarDestinos()
            for destino in destinos:
                print(destino)
        elif opcion == "3":
            destino_id = input("Ingrese el ID del destino a actualizar: ").strip()
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            nueva_descripcion = input("Ingrese la nueva descripción: ").strip()
            nueva_actividad = input("Ingrese la nueva actividad: ").strip()
            nuevo_costo = input("Ingrese el nuevo precio: ").strip()
            actualizarDestino(destino_id, nuevo_nombre, nueva_descripcion,nueva_actividad, nuevo_costo)
        elif opcion == "4":
            destino_id = input("Ingrese el ID del destino a eliminar: ").strip()
            eliminarDestino(destino_id)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menuPaquetes(nombre_usuario):
    while True:
        #os.system('cls')
        print("---------------------------")
        print("  MENÚ PAQUETES TURÍSTICOS ")
        print("---------------------------")
        print("1. Registrar Paquete Turístico")
        print("2. Consultar Paquetes Turísticos")
        print("3. Actualizar Paquete Turístico")
        print("4. Eliminar Paquete Turístico")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            nombre_paquete  = input("Ingrese el nombre del paquete: ").strip()
            descripcion = input("Ingrese la descripción: ").strip()
            precio_total = int(input("Ingrese el precio: "))  
            fecha_inicio = input("Ingrese la fecha de inicio (AAAA-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de termino (AAAA-MM-DD): ")
            nuevo_paquete = PaqueteTuristico(nombre_paquete , descripcion, precio_total,fecha_inicio,fecha_fin)
            agregarPaquete(nuevo_paquete)
            break
        elif opcion == "2":
            paquetes = consultarTodosPaquetes()
            print(paquetes)
        elif opcion == "3":
            id_paquete = input("Ingrese el ID del paquete a actualizar: ").strip()
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            nueva_descripcion = input("Ingrese la nueva descripción: ").strip()
            nuevo_precio = int(input("Ingrese el nuevo precio: "))
            actualizarPaquete(id_paquete, nuevo_nombre, nueva_descripcion, nuevo_precio)
        elif opcion == "4":
            id_paquete = input("Ingrese el ID del paquete a eliminar: ").strip()
            eliminarPaquete(id_paquete)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menuReservas(nombre_usuario):
    while True:
        print("---------------------------")
        print("         MENÚ RESERVAS     ")
        print("---------------------------")
        print("1. Consultar Reservas")
        print("2. Registrar Reserva")
        print("3. Cancelar Reserva")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
         # pendiente validar si mostraremos las reservas en estado cancelado
        if opcion == "1":
            reservas = consultarTodosReserva()
            if reservas:
                print("\nLista de reservas:")
                for reserva in reservas:
                    print(f"ID Reserva: {reserva[0]},ID Usuario: {reserva[1]}, ID Paquete: {reserva[2]}, Fecha Reserva: {reserva[3]}, Estado: {reserva[4]}")
            else:
                print("No se encontraron reservas.")
        elif opcion == "2":
            # Registrar una nueva reserva
            try:
                id_usuario = input("Ingrese el ID del usuario: ").strip()
                id_paquete = input("Ingrese el ID del paquete: ").strip()
                fecha_reserva = input("Ingrese la fecha de reserva (YYYY-MM-DD): ").strip()
                estado = "pendiente"  # Por defecto al registrar una nueva reserva
                nueva_reserva = Reserva(id_usuario, id_paquete, fecha_reserva, estado)
                realizarReserva(nueva_reserva)
            except Exception as e:
                print(f"Error al intentar registrar la reserva: {e}")

        elif opcion == "3":
            #cancelar una reserva, solo la cancela, no la elimina de la bd, igual esta la query para borrar
            try:
                id_reserva = input("Ingrese el ID de la reserva a cancelar: ").strip()
                # valida si el estado es "pendiente" queda pendiente que valide tmb el estado confirmada
                if validarEstadoReserva(id_reserva, "pendiente"):
                    cancelarReserva(id_reserva)
                else:
                    print("No se puede cancelar la reserva: la reserva no está en estado 'pendiente'.")
            except Exception as e:
                print(f"Error al intentar cancelar la reserva: {e}")

        elif opcion == "4":
            print("Saliendo del menú de reservas...")
            break
        else:
            print("Opción no válida.")



def main():
    while True:
      #  os.system('cls')
        print("---------------------------")
        print("     1. Login             ")
        print("     2. Registro          ")
        print("     3. Salir             ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            datos_usuario = login()  # Captura toda la información del usuario autenticado
            if datos_usuario:
                tipo_usuario = datos_usuario["tipo_usuario"]
                nombre_usuario = datos_usuario["nombre"]
                correo_usuario = datos_usuario["correo"]
                # Redirige al menú correspondiente según el tipo de usuario
                if tipo_usuario == "administrador":
                    menuAdmin(nombre_usuario)
                elif tipo_usuario == "cliente":
                    menuClientes(nombre_usuario)
                else:
                    print("Tipo de usuario no reconocido.")
            else:
                print("No se pudo iniciar sesión.")
        elif opcion == "2":
            registrarUsuario()
        elif opcion == "3":
            print("Saliendo del programa...")
            exit() 
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


# menu administrador
def menuAdmin(nombre_usuario):
    while True:
        #os.system('cls') 
        print(f"Bienvenido, Administrador: {nombre_usuario}")
        print("---------------------------")
        print("       MENÚ ADMIN         ")
        print("---------------------------")
        print("1. Gestionar Destinos     ")
        print("2. Gestionar Paquetes     ")
        print("3. Gestionar Reservas     ")
        print("4. Salir                  ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menuDestinos()
        elif opcion == "2":
            menuPaquetes(nombre_usuario)
        elif opcion == "3":
            menuReservas(nombre_usuario)
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


#menu cliente
def menuClientes():
    while True:
        os.system('cls')
        print("--------------------------")
        print("       MENÚ CLIENTE       ")
        print("--------------------------")
        print("1. Consultar Destinos")
        print("2. Consultar Paquetes Turísticos")
        print("3. Realizar Reserva")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            destinos = consultarDestinos()
            print(destinos)
        elif opcion == "2":
            paquetes = consultarTodosPaquetes()
            print(paquetes)
        elif opcion == "3":
            realizarReserva()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()