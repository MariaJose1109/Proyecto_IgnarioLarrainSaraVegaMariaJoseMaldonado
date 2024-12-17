import DAO.CRUDUsuario
import DAO.CRUDReserva
import DAO.CRUDDestino
import DAO.CRUDPaquete
from DTO.Paquete import * 
from DTO.Reserva import * 
from DTO.Usuario import * 
from DTO.Destino import Destino
import os
import json
from tabulate import tabulate


def registrarUsuario():
    os.system('cls')
    print("---------------------------")
    print("     REGISTRAR USUARIO     ")
    print("---------------------------")
    while True:
        nombre = input("Ingrese Usuario: ").strip()
        correo = input("Ingrese Correo: ").strip()
        password = input("Ingrese Contraseña: ").strip()
        tipoUsuario = input("Ingrese tipo Usuario (administrador/cliente): ").strip().lower()
        if not nombre or not password or not correo or not tipoUsuario:
            print("Usuario, contraseña, correo y/o tipo Usuario no pueden estar vacíos.")
            continue  
        if tipoUsuario not in ["administrador", "cliente"]:
            print("El tipo de usuario debe ser 'administrador' o 'cliente'.")
            continue 
        nuevoUsuario = Usuario.registrarUsuario(nombre, correo, password, tipoUsuario)
        if nuevoUsuario:
            print(f"Usuario {nombre} registrado con éxito.")
            return nuevoUsuario  
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
        print("2. Mostrar todos los destinos")
        print("3. Mostrar un destino")
        print("4. Mostrar destinos parciales")
        print("5. Actualizar destino")
        print("6. Eliminar destino")
        print("7. Salir")
        opcion = input("Por favor, selecciona una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR UN NUEVO DESTINO ---")
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            actividades = input("Actividades: ").strip()
            try:
                costo = int(input("Costo: ").strip())
                destino = Destino(None, nombre, descripcion, actividades, costo)
                if agregarDestino(destino):
                    print("Destino registrado con éxito.")
            except ValueError:
                print("Error: El costo debe ser numérico.")

        elif opcion == "2":
            print("\n--- MOSTRAR TODOS LOS DESTINOS ---")
            destinos = DAO.CRUDDestino.mostrarTodos()
            if destinos:
                for destino in destinos:
                    print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, "
                        f"Descripción: {destino['descripcion']}, Actividades: {destino['actividades']}, Costo: ${destino['costo']}")
            else:
                print("No hay destinos disponibles.")

        elif opcion == "3":
            print("\n--- MOSTRAR UN DESTINO ---")
            id_destino = input("Ingrese el ID del destino: ").strip()
            destino = mostrarUno(id_destino)
            if destino:
                print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, "
                      f"Descripción: {destino['descripcion']}, Actividades: {destino['actividades']}, Costo: ${destino['costo']}")
            else:
                print("Destino no encontrado.")

        elif opcion == "4":
            print("\n--- MOSTRAR DESTINOS PARCIALES ---")
            try:
                cantidad = int(input("Cantidad de destinos a mostrar: ").strip())
                destinos = mostrarParcial(cantidad)
                for destino in destinos:
                    print(f"ID: {destino['id_destino']}, Nombre: {destino['nombre']}, Costo: ${destino['costo']}")
            except ValueError:
                print("Error: La cantidad debe ser numérica.")

        elif opcion == "5":
            print("\n--- ACTUALIZAR DESTINO ---")
            id_destino = input("ID del destino a actualizar: ").strip()
            nuevo_nombre = input("Nuevo nombre: ").strip()
            nueva_descripcion = input("Nueva descripción: ").strip()
            nuevas_actividades = input("Nuevas actividades: ").strip()
            try:
                nuevo_costo = int(input("Nuevo costo: ").strip())
                if modificarDestino(id_destino, nuevo_nombre, nueva_descripcion, nuevas_actividades, nuevo_costo):
                    print("Destino actualizado correctamente.")
            except ValueError:
                print("Error: El costo debe ser numérico.")

        elif opcion == "6":
            print("\n--- ELIMINAR DESTINO ---")
            id_destino = input("ID del destino a eliminar: ").strip()
            if eliminarDestino(id_destino):
                print("Destino eliminado con éxito.")
            else:
                print("No se pudo eliminar el destino.")

        elif opcion == "7":
            print("Saliendo del menú de destinos...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def menuPaquetes(nombre):
    while True:
        print("\n============================")
        print("    MENÚ PAQUETES TURÍSTICOS   ")
        print("============================")
        print("1. Mostrar todos los paquetes")
        print("2. Mostrar un paquete específico")
        print("3. Mostrar paquetes parciales")
        print("4. Agregar paquete")
        print("5. Eliminar paquete")
        print("6. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            # Mostrar todos los paquetes turísticos
            print("\n--- MOSTRAR TODOS LOS PAQUETES ---")
            paquetes = mostrarTodos()
            if paquetes:
                for paquete in paquetes:
                    print(f"ID: {paquete['id_paquete']}, Nombre: {paquete['nombre_paquete']}, Precio: ${paquete['precio_total']}")
            else:
                print("No hay paquetes turísticos registrados.")

        elif opcion == "2":
            # Mostrar un paquete específico
            print("\n--- MOSTRAR UN PAQUETE ---")
            idPaquete = input("Ingrese el ID del paquete: ").strip()
            paquete = mostrarUno(idPaquete)
            if paquete:
                print(f"ID: {paquete['id_paquete']}, Nombre: {paquete['nombre_paquete']}, Precio: ${paquete['precio_total']}")
            else:
                print("No se encontró un paquete con ese ID.")

        elif opcion == "3":
            # Mostrar paquetes parciales
            print("\n--- MOSTRAR PAQUETES PARCIALES ---")
            try:
                cantidad = int(input("¿Cuántos paquetes desea mostrar?: ").strip())
                paquetes = mostrarParcial(cantidad)
                if paquetes:
                    for paquete in paquetes:
                        print(f"ID: {paquete['id_paquete']}, Nombre: {paquete['nombre_paquete']}, Precio: ${paquete['precio_total']}")
                else:
                    print("No se encontraron paquetes turísticos para mostrar.")
            except ValueError:
                print("Debe ingresar un número válido.")

        elif opcion == "4":
            # Agregar un paquete
            print("\n--- AGREGAR UN PAQUETE ---")
            nombre = input("Nombre del paquete: ").strip()
            descripcion = input("Descripción: ").strip()
            try:
                precio = float(input("Precio total: ").strip())
                fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
                fecha_fin = input("Fecha de fin (YYYY-MM-DD): ").strip()
                paquete = Paquete(None, nombre, descripcion, None, fecha_inicio, fecha_fin)
                if agregarPaquete(paquete):
                    print("Paquete agregado con éxito.")
            except ValueError:
                print("Error: El precio debe ser un valor numérico.")

        elif opcion == "5":
            # Eliminar un paquete
            print("\n--- ELIMINAR UN PAQUETE ---")
            idPaquete = input("Ingrese el ID del paquete a eliminar: ").strip()
            if eliminarPaquete(idPaquete):
                print("Paquete eliminado correctamente.")
            else:
                print("Error al eliminar el paquete. Verifique el ID.")

        elif opcion == "6":
            print("\nRegresando al menú principal...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

# Función para generar paquetes aleatorios
def menuGenerarPaquetesAleatorios():
    print("\n--- GENERAR PAQUETES ALEATORIOS ---")
    try:
        cantidad = int(input("¿Cuántos paquetes aleatorios desea generar? (1-10): ").strip())
        if 1 <= cantidad <= 10:
            print("\nGenerando paquetes aleatorios...\n")
            for i in range(1, cantidad + 1):
                paquete = Paquete.generarPaqueteAleatorio()
                print(f"Paquete #{i}: {paquete}")
        else:
            print("Por favor, ingrese un número entre 1 y 10.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un número válido.")

def menuReservas(nombre):
    while True:
        print("---------------------------")
        print("         MENÚ RESERVAS     ")
        print("---------------------------")
        print("1. Mostrar todas las reservas")
        print("2. Mostrar una reserva")
        print("3. Mostrar reservas parciales")
        print("4. Realizar una nueva reserva")
        print("5. Cancelar una reserva")
        print("6. Confirmar una reserva")
        print("7. Salir")
        opcion = input("Por favor, elija una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- MOSTRAR TODAS LAS RESERVAS ---")
            reservas = consultarTodosReserva()
            for reserva in reservas:
                print(f"ID: {reserva['id_reserva']}, Usuario ID: {reserva['id_usuario']}, Estado: {reserva['estado']}")
        elif opcion == "2":
            print("\n--- MOSTRAR UNA RESERVA ---")
            idReserva = input("Ingrese el ID de la reserva: ").strip()
            reserva = consultarReservaPorId(idReserva)
            if reserva:
                print(f"ID: {reserva['id_reserva']}, Usuario ID: {reserva['id_usuario']}, Estado: {reserva['estado']}")
            else:
                print("Reserva no encontrada.")
        elif opcion == "3":
            print("\n--- MOSTRAR RESERVAS PARCIALES ---")
            estado = input("Ingrese el estado de la reserva (pendiente, confirmada, etc.): ").strip()
            reservas = consultarReservasParciales(estado)
            for reserva in reservas:
                print(f"ID: {reserva['id_reserva']}, Estado: {reserva['estado']}")
        elif opcion == "7":
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def main():
    while True:
        print("\n---------------------------")
        print("     1. Login             ")
        print("     2. Registro          ")
        print("     3. Salir             ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            correo = input("\nIngrese su correo: ").strip()
            password = input("Ingrese su contraseña: ").strip()

            datos_usuario = Usuario.login(correo, password)
            if datos_usuario["autenticado"]:
                print(f"\n¡Bienvenido, {datos_usuario['nombre']}!\n")
                if datos_usuario["tipo_usuario"] == "administrador":
                    menuAdmin(datos_usuario["nombre"], datos_usuario["id_usuario"])
                elif datos_usuario["tipo_usuario"] == "cliente":
                    menuClientes(datos_usuario["nombre"], datos_usuario["id_usuario"])
            else:
                input("Presione Enter para intentar nuevamente...")

        elif opcion == "2":
            registrarUsuario()
        elif opcion == "3":
            print("\nGracias por usar el sistema. ¡Hasta pronto!\n")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.\n")

# menu administrador
def menuAdmin(nombre, idUsuario):
    while True:
        #os.system('cls') 
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
            menuPaquetes(nombre)
        elif opcion == "3":
            menuReservas(nombre)
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def menuClientes(nombre, idUsuario):  # Ahora también pasamos 'id_usuario'
    while True:
        print("--------------------------")
        print(f"       MENÚ CLIENTE")
        print("--------------------------")
        print("1. Consultar Paquetes Turísticos")
        print("2. Realizar Reserva")
        print("3. Mostrar Reservas")
        print("4. Cancelar Reserva")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
                Paquete.consultarPaquetes() 
        elif opcion == "2":
            try:
                # Mostrar paquetes disponibles
                Paquete.consultarPaquetes() 
                idPaquete = int(input("Ingrese el ID del paquete turístico que desea reservar: "))
                fechaReserva = input("Por favor, ingrese la fecha de reserva (YYYY-MM-DD): ").strip()
                # Crear reserva con el id_usuario logeado
                nuevaReserva = Reserva(idUsuario, idPaquete, fechaReserva) 
                if nuevaReserva.realizarReserva():
                    print("¡Tu reserva ha sido registrada con éxito!")
                else:
                    print("Lo siento, no pudimos registrar tu reserva en este momento. Intenta nuevamente.")
            except Exception as e:
                print(f"Hubo un error al intentar registrar la reserva: {e}")
        elif opcion == "3":
            try:
                # Mostrar reservas del cliente
                reservas = mostrarReservaPorId(idUsuario)  
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
                reservas = mostrarReservaPorId(idUsuario) 
                if reservas:
                    print("\n--- Tus reservas ---")
                    for reserva in reservas:
                        print(f"ID Reserva: {reserva['id_reserva']}, Paquete ID: {reserva['id_paquete']}, Fecha: {reserva['fecha_reserva']}, Estado: {reserva['estado']}")        
                    idReserva = int(input("Ingrese el ID de la reserva que desea cancelar: "))
                    # Buscar los detalles de la reserva seleccionada (paquete y fecha)
                    reservaSeleccionada = next((reserva for reserva in reservas if reserva['id_reserva'] == idReserva), None)
                    if reservaSeleccionada:
                        idPaquete = reservaSeleccionada['id_paquete']
                        fechaReserva = reservaSeleccionada['fecha_reserva']
                        reservaACancelar = Reserva(idUsuario, idPaquete, fechaReserva, idReserva=idReserva)  # Pasa todos los parámetros
                        if reservaACancelar.cancelarReserva():
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
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main() 
