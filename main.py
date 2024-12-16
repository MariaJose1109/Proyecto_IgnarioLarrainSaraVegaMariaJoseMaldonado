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
                "nombre": resultado_login["nombre"], 
                "correo": correo 
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
        print("1. Registrar un nuevo destino")
        print("2. Consultar destinos disponibles")
        print("3. Actualizar destino")
        print("4. Eliminar destino")
        print("5. Salir")
        opcion = input("Por favor, selecciona una opción (1-5): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR UN NUEVO DESTINO ---")
            nombre = input("Ingrese el nombre del destino: ").strip()
            descripcion = input("Ingrese la descripción del destino: ").strip()
            actividades = input("Ingrese las actividades disponibles en el destino: ").strip()
            try:
                costo = int(input("Ingrese el costo aproximado para visitar el destino (en $): ").strip())
                nuevo_destino = Destino(nombre, descripcion, actividades, costo)
                agregarDestino(nuevo_destino)
                print(f"¡Destino {nombre} registrado exitosamente!")
            except ValueError:
                print("Por favor, ingresa un valor numérico válido para el costo.")

        elif opcion == "2":
            print("\n--- CONSULTAR DESTINOS DISPONIBLES ---")
            destinos = consultarDestinos()
            if destinos:
                print("Destinos disponibles:")
                for destino in destinos:
                    print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, Costo: ${destino['costo']}")
            else:
                print("No se encontraron destinos registrados en este momento.")

        elif opcion == "3":
            print("\n--- ACTUALIZAR UN DESTINO EXISTENTE ---")
            destino_id = input("Ingrese el ID del destino que desea actualizar: ").strip()
            nuevo_nombre = input("Ingrese el nuevo nombre del destino: ").strip()
            nueva_descripcion = input("Ingrese la nueva descripción del destino: ").strip()
            nueva_actividad = input("Ingrese la nueva actividad disponible: ").strip()
            try:
                nuevo_costo = int(input("Ingrese el nuevo precio aproximado para el destino (en $): ").strip())
                actualizarDestino(destino_id, nuevo_nombre, nueva_actividad, nueva_descripcion, nuevo_costo) 
                print(f"¡Destino con ID {destino_id} actualizado correctamente!")
            except ValueError:
                print("Por favor, ingresa un valor numérico válido para el costo.")            
        elif opcion == "4":
            print("\n--- ELIMINAR UN DESTINO ---")
            destino_id = input("Ingrese el ID del destino que desea eliminar: ").strip()
            if eliminarDestino(destino_id): 
                print(f"Destino con ID {destino_id} eliminado correctamente.")
            else:
                print(f"No se pudo eliminar el destino con ID {destino_id}.")
        elif opcion == "5":
            print("¡Gracias por usar el sistema de gestión de destinos! Saliendo...")
            break            

        else:
            print("Opción no válida. Por favor, selecciona una opción entre 1 y 5.")

def menuPaquetes(nombre_usuario):
    while True:
        print("---------------------------")
        print("  MENÚ PAQUETES TURÍSTICOS ")
        print("---------------------------")
        print("1. Registrar Paquete Turístico")
        print("2. Consultar Paquetes Turísticos")
        print("3. Actualizar Paquete Turístico")
        print("4. Eliminar Paquete Turístico")
        print("5. Salir")
        opcion = input("Por favor, selecciona una opción (1-5): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR UN NUEVO PAQUETE TURÍSTICO ---")
            # Consultar destinos disponibles
            destinos = consultarDestinos()
            if not destinos:
                print("Lo sentimos, no hay destinos disponibles para crear paquetes turísticos en este momento.")
                continue
            # Mostrar destinos al usuario
            print("Destinos disponibles para incluir en el paquete:")
            for destino in destinos:
                print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, Costo: ${destino['costo']}")
            # Pedir destinos al usuario para crear el paquete
            destinos_seleccionados = input("Ingrese los IDs de los destinos a incluir en el paquete, separados por comas: ").strip()
            try:
                destinos_ids = [int(id.strip()) for id in destinos_seleccionados.split(",") if id.strip().isdigit()]
                destinos_validos = [destino for destino in destinos if destino["id_destino"] in destinos_ids]
                if not destinos_validos:
                    print("No se seleccionaron destinos válidos. Por favor, intente nuevamente.")
                    continue
                # Calcular el costo total del paquete
                costo_total = sum(destino["costo"] for destino in destinos_validos)
                # Solicitar información del paquete
                nombre_paquete = input("Ingrese el nombre del paquete turístico: ").strip()
                descripcion = input("Ingrese la descripción del paquete: ").strip()
                fecha_inicio = input("Ingrese la fecha de inicio del paquete (YYYY-MM-DD): ").strip()
                fecha_fin = input("Ingrese la fecha de fin del paquete (YYYY-MM-DD): ").strip()
                # Crear objeto PaqueteTuristico
                nuevo_paquete = PaqueteTuristico(nombre_paquete, descripcion, costo_total, fecha_inicio, fecha_fin)                
                # Registrar el paquete
                if nuevo_paquete.registrarPaquete(destinos_validos):
                    print(f"¡Paquete registrado con éxito! ID del paquete: {nuevo_paquete.id_paquete}")
                else:
                    print("Hubo un problema al registrar el paquete turístico. Intenta nuevamente.")
            except ValueError as e:
                print(f"Error en la entrada de datos: {e}. Por favor, revisa la información e inténtalo nuevamente.")
        elif opcion == "2":
            print("\n--- CONSULTAR PAQUETES TURÍSTICOS ---")
            PaqueteTuristico.consultarPaquetes()     
        elif opcion == "3":
            try:
                print("\n--- PAQUETES TURÍSTICOS DISPONIBLES ---")
                PaqueteTuristico.consultarPaquetes()
                id_paquete = int(input("Ingrese el ID del paquete que desea actualizar: ").strip())
                nuevo_nombre = input("Ingrese el nuevo nombre del paquete: ").strip()
                nueva_descripcion = input("Ingrese la nueva descripción del paquete: ").strip()
                consultarDestinos()
                id_destino = int(input("Ingrese el ID del destino asociado al paquete: ").strip())
                nueva_fecha_inicio = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ").strip()
                nueva_fecha_fin = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ").strip()
                paquete = PaqueteTuristico(None, None, None, None, None)
                paquete.id_paquete = id_paquete
                if paquete.actualizarPaquete(nuevo_nombre, nueva_descripcion, id_destino, nueva_fecha_inicio, nueva_fecha_fin):
                    print("¡Actualización completada con éxito!")
                else:
                    print("Hubo un problema al intentar actualizar el paquete. Verifique los datos e intente nuevamente.")
            except ValueError as e:
                print(f"Error en la entrada de datos: {e}. Por favor, revisa los valores y vuelve a intentarlo.")
        
        elif opcion == "4":
            PaqueteTuristico.consultarPaquetes()
            id_paquete = input("Ingrese el ID del paquete que desea eliminar: ").strip()
            paquete = PaqueteTuristico(None, None, None, None, None)
            paquete.id_paquete = id_paquete
            if paquete.eliminarPaquete():
                print(f"Paquete con ID {id_paquete} eliminado correctamente. ¡Operación exitosa!")
            else:
                print("Hubo un problema al eliminar el paquete. Asegúrese de que el ID sea correcto.")
        
        elif opcion == "5":
            print("¡Gracias por usar el sistema de gestión de paquetes turísticos! Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, ingresa un número entre 1 y 5.")


def menuReservas(nombre_usuario):
    while True:
        print("---------------------------")
        print("         MENÚ RESERVAS     ")
        print("---------------------------")
        print("1. Consultar todas las reservas")
        print("2. Realizar una nueva reserva")
        print("3. Cancelar una reserva")
        print("4. Confirmar una reserva")
        print("5. Salir")
        opcion = input("Por favor, elija una opción (1-5): ").strip()
        
        if opcion == "1":
            reservas = consultarTodosReserva()
            if reservas:
                print("\nAquí están las reservas registradas:")
                for reserva in reservas:
                    print(f"ID Reserva: {reserva['id_reserva']}, Usuario ID: {reserva['id_usuario']}, Paquete ID: {reserva['id_paquete']}, Fecha de Reserva: {reserva['fecha_reserva']}, Estado: {reserva['estado']}")
            else:
                print("No se encontraron reservas registradas en este momento.")
        
        elif opcion == "2":
            try:
                paquetes = consultarPaquetesDisponibles()
                if paquetes:
                    print("\n--- Paquetes disponibles ---")
                    for paquete in paquetes:
                        print(f"ID Paquete: {paquete['id_paquete']}, Nombre: {paquete['nombre_paquete']}, Descripción: {paquete['descripcion']}, Precio: {paquete['precio_total']}")
                else:
                    print("No hay paquetes turísticos disponibles.")
                    continue 
                id_paquete = int(input("Ingrese el ID del paquete turístico que desea reservar: "))
                clientes = consultarUsuariosTipoCliente()  
                if clientes:
                    print("\n--- Usuarios tipo Cliente ---")
                    for cliente in clientes:
                        print(f"ID Usuario: {cliente['id_usuario']}, Nombre: {cliente['nombre']}")
                else:
                    print("No hay usuarios tipo cliente disponibles.")
                    continue 
                id_usuario = int(input("Ingrese su ID de usuario para realizar la reserva: "))
                fecha_reserva = input("Por favor, ingrese la fecha de reserva (YYYY-MM-DD): ").strip()
                nueva_reserva = Reserva(id_usuario, id_paquete, fecha_reserva)
                if nueva_reserva.realizarReserva():
                    print("¡Tu reserva ha sido registrada con éxito!")
                else:
                    print("Lo siento, no pudimos registrar tu reserva en este momento. Intenta nuevamente.")
            except Exception as e:
                print(f"Hubo un error al intentar registrar la reserva: {e}")
        
        elif opcion == "3":
            try:
                id_reserva = int(input("Por favor, ingresa el ID de la reserva que deseas cancelar: "))
                if cancelarReserva(id_reserva):
                    print("¡Reserva cancelada exitosamente!")
                else:
                    print("No fue posible cancelar la reserva. Verifica que el ID sea correcto o que la reserva esté en estado 'pendiente'.")
            except Exception as e:
                print(f"Hubo un error al intentar cancelar la reserva: {e}")
                
        elif opcion == "4":
            try:
                id_reserva = input("Ingrese el ID de la reserva que desea confirmar: ").strip()
                reserva = Reserva(None, None, None)
                reserva.id_reserva = id_reserva
                if reserva.confirmarReserva():
                    print("¡Reserva confirmada correctamente! ¡Gracias por elegirnos!")
                else:
                    print("No se pudo confirmar la reserva. Asegúrese de que el ID sea válido.")
            except Exception as e:
                print(f"Hubo un error al intentar confirmar la reserva: {e}")
        
        elif opcion == "5":
            print("¡Gracias por usar nuestro sistema! Saliendo del menú de reservas...")
            break
        
        else:
            print("Opción no válida. Por favor, ingrese un número entre 1 y 5.")


def main():
    while True:
        print("---------------------------")
        print("     1. Login             ")
        print("     2. Registro          ")
        print("     3. Salir             ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            correo = input("Ingrese Correo: ")
            password = input("Ingrese Contraseña: ")

            # Llamamos al login y capturamos los datos
            datos_usuario = Usuario.login(correo, password)  
            print("Datos del usuario autenticado:", datos_usuario)
            if datos_usuario and "id_usuario" in datos_usuario:
                # Si los datos son correctos, continua
                id_usuario = datos_usuario["id_usuario"]
                nombre_usuario = datos_usuario["nombre"]
                tipo_usuario = datos_usuario["tipo_usuario"]
                correo_usuario = datos_usuario["correo"]

                print(f"ID de usuario: {id_usuario}")
                print(f"Nombre de usuario: {nombre_usuario}")
                print(f"Tipo de usuario: {tipo_usuario}")

                if tipo_usuario == "administrador":
                    menuAdmin(nombre_usuario, id_usuario)  
                elif tipo_usuario == "cliente":
                    menuClientes(nombre_usuario, id_usuario)  
                else:
                    print("Tipo de usuario no reconocido.")
            else:
                print("Error: 'id_usuario' no se encuentra en los datos del usuario.")
                
        elif opcion == "2":
            registrarUsuario() 
        elif opcion == "3":
            print("Saliendo del programa...")
            exit()
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")



# menu administrador
def menuAdmin(nombre_usuario, id_usuario):
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


def menuClientes(nombre_usuario, id_usuario):  # Ahora también pasamos 'id_usuario'
    while True:
        print("--------------------------")
        print(f"       MENÚ CLIENTE - {nombre_usuario}")
        print("--------------------------")
        print("1. Consultar Paquetes Turísticos")
        print("2. Realizar Reserva")
        print("3. Mostrar Reservas")
        print("4. Cancelar Reserva")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
                PaqueteTuristico.consultarPaquetes() 
        elif opcion == "2":
            try:
                # Mostrar paquetes disponibles
                PaqueteTuristico.consultarPaquetes() 
                id_paquete = int(input("Ingrese el ID del paquete turístico que desea reservar: "))
                fecha_reserva = input("Por favor, ingrese la fecha de reserva (YYYY-MM-DD): ").strip()
                # Crear reserva con el id_usuario logeado
                nueva_reserva = Reserva(id_usuario, id_paquete, fecha_reserva) 
                if nueva_reserva.realizarReserva():
                    print("¡Tu reserva ha sido registrada con éxito!")
                else:
                    print("Lo siento, no pudimos registrar tu reserva en este momento. Intenta nuevamente.")
            except Exception as e:
                print(f"Hubo un error al intentar registrar la reserva: {e}")
        elif opcion == "3":
            try:
                # Mostrar reservas del cliente
                reservas = mostrarReservaPorId(id_usuario)  
                if reservas:
                    print("\n--- Tus reservas ---")
                    for reserva in reservas:
                        print(f"ID Reserva: {reserva['id_reserva']}, Paquete ID: {reserva['id_paquete']}, Fecha: {reserva['fecha_reserva']}, Estado: {reserva['estado']}")
                else:
                    print("No tienes reservas registradas.")
            except Exception as e:
                print(f"Hubo un error al intentar mostrar las reservas: {e}")
        elif opcion == "4":
            try:
                # Mostrar reservas para seleccionar una a cancelar
                reservas = mostrarReservaPorId(id_usuario) 
                if reservas:
                    print("\n--- Tus reservas ---")
                    for reserva in reservas:
                        print(f"ID Reserva: {reserva['id_reserva']}, Paquete ID: {reserva['id_paquete']}, Fecha: {reserva['fecha_reserva']}, Estado: {reserva['estado']}")        
                    id_reserva = int(input("Ingrese el ID de la reserva que desea cancelar: "))
                    # Buscar los detalles de la reserva seleccionada (paquete y fecha)
                    reserva_seleccionada = next((reserva for reserva in reservas if reserva['id_reserva'] == id_reserva), None)
                    if reserva_seleccionada:
                        id_paquete = reserva_seleccionada['id_paquete']
                        fecha_reserva = reserva_seleccionada['fecha_reserva']
                        reserva_a_cancelar = Reserva(id_usuario, id_paquete, fecha_reserva, id_reserva=id_reserva)  # Pasa todos los parámetros
                        if reserva_a_cancelar.cancelarReserva():
                            print("¡Tu reserva ha sido cancelada con éxito!")
                        else:
                            print("No pudimos cancelar tu reserva en este momento.")
                    else:
                        print("No se encontró una reserva con ese ID.")
                else:
                    print("No tienes reservas registradas para cancelar.")
            except Exception as e:
                print(f"Hubo un error al intentar cancelar la reserva: {e}")
        
        elif opcion == "5":
            print("¡Gracias por visitar el menú de clientes! Hasta luego.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main() 
