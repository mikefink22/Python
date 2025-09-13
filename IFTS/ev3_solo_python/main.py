import os # Importar os para limpiar la pantalla
from services.auth_manager import GestorAutenticacion
from services.user_manager import GestorUsuarios
from utils.validations import validar_contrasena, validar_dni # Importante importar esto

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    gestor_autenticacion = GestorAutenticacion()
    gestor_usuarios = GestorUsuarios(gestor_autenticacion)

    while True:
        limpiar_pantalla()
        usuario_logueado = gestor_autenticacion.obtener_usuario_logueado()

        if usuario_logueado:
            print(f"Bienvenido, {usuario_logueado.nombre_usuario} ({usuario_logueado.rol})")
            if usuario_logueado.rol == 'admin':
                mostrar_menu_administrador()
                opcion = input("Seleccione una opción: ").strip()
                manejar_opcion_administrador(opcion, gestor_autenticacion, gestor_usuarios)
            else: # usuario estandar
                mostrar_menu_usuario_estandar()
                opcion = input("Seleccione una opción: ").strip()
                manejar_opcion_usuario_estandar(opcion, gestor_autenticacion, gestor_usuarios)
        else:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()
            manejar_opcion_menu_principal(opcion, gestor_autenticacion)

        input("\nPresione Enter para continuar...")

def mostrar_menu_principal():
    print("\n--- Menú Principal ---")
    print("1. Iniciar Sesión")
    print("2. Registrar Usuario")
    print("3. Salir")

def mostrar_menu_administrador():
    print("\n--- Menú de Administrador ---")
    print("1. Ver Todos los Usuarios y Perfiles")
    print("2. Crear Nuevo Usuario")
    print("3. Actualizar Contraseña de Usuario")
    print("4. Actualizar Perfil de Usuario")
    print("5. Eliminar Usuario")
    print("6. Actualizar Rol de Usuario") # <-- Nueva opción
    print("7. Cerrar Sesión")
    print("8. Salir del Programa") # 

def mostrar_menu_usuario_estandar():
    print("\n--- Menú de Usuario Estándar ---")
    print("1. Ver Mi Perfil")
    print("2. Actualizar Mi Contraseña")
    print("3. Actualizar Mi Perfil")
    print("4. Cerrar Sesión")
    print("5. Salir del Programa")

# --- INICIO DE LA MODIFICACIÓN ---
def solicitar_datos_perfil(solo_obligatorios=False):
    limpiar_pantalla
    print("\n--- Ingrese Datos del Perfil ---")

    # Campos obligatorios - Ahora con bucles para asegurar que no estén vacíos
    while True:
        dni = input("DNI (Obligatorio): ").strip()
        if not dni:
            print("Error: El DNI es un campo obligatorio y no puede estar vacío.")
            continue # Vuelve a pedir si está vacío

        es_valido_dni, mensaje_dni = validar_dni(dni) # <-- Llama a la nueva función de validación
        if es_valido_dni:
            break # Sale del bucle si el DNI es válido
        else:
            print(f"Error: {mensaje_dni}") # Muestra el error de formato
            continue # Vuelve a pedir si el formato es inválido
    while True:
        nombre = input("Nombre (Obligatorio): ").strip()
        if nombre:
            break
        print("Error: El Nombre es un campo obligatorio y no puede estar vacío.")

    while True:
        apellido = input("Apellido (Obligatorio): ").strip()
        if apellido:
            break
        print("Error: El Apellido es un campo obligatorio y no puede estar vacío.")


    datos = {
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
    }

    if not solo_obligatorios:
        email = input("Email (Opcional): ").strip()
        telefono = input("Teléfono (Opcional): ").strip()
        direccion = input("Dirección (Opcional): ").strip()
        fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD) (Opcional): ").strip()

        # Solo agregar si no están vacíos (para opcionales)
        if email: datos['email'] = email
        if telefono: datos['telefono'] = telefono
        if direccion: datos['direccion'] = direccion
        if fecha_nacimiento: datos['fecha_nacimiento'] = fecha_nacimiento

    return datos
# --- FIN DE LA MODIFICACIÓN ---

def solicitar_y_validar_contrasena(max_intentos=5):
    intentos = 0
    while intentos < max_intentos:
        print(f"(Intento {intentos + 1}/{max_intentos}) o escriba 'salir' para cancelar.")
        contrasena = input("Ingrese contraseña: ").strip()

        if contrasena.lower() == 'salir':
            print("Operación de contraseña cancelada.")
            return None

        es_valida, mensaje = validar_contrasena(contrasena)
        if not es_valida:
            print(f"Error: {mensaje}")
            intentos += 1
            continue

        confirmar_contrasena = input("Confirme contraseña: ").strip()
        if contrasena != confirmar_contrasena:
            print("Error: Las contraseñas no coinciden. Intente de nuevo.")
            intentos += 1
            continue

        return contrasena

    print(f"Se excedió el número máximo de {max_intentos} intentos. Operación cancelada.")
    return None

def manejar_opcion_menu_principal(opcion, gestor_autenticacion):
    if opcion == '1':
        nombre_usuario = input("Ingrese nombre de usuario: ").strip()
        contrasena = input("Ingrese contraseña: ").strip()
        exito, mensaje = gestor_autenticacion.iniciar_sesion(nombre_usuario, contrasena)
        print(mensaje)
    elif opcion == '2':
        print("\n--- Registrar Nuevo Usuario ---")
        nombre_usuario = input("Ingrese nombre de usuario para registrar: ").strip()

        contrasena = solicitar_y_validar_contrasena()
        if contrasena is None:
            print("Registro de usuario cancelado.")
            return

        exito, mensaje = gestor_autenticacion.registrar_usuario(
            nombre_usuario, contrasena, rol="estandar"
        )
        print(mensaje)

        if exito:
            print("\nIniciando sesión con el nuevo usuario...")
            exito_login, mensaje_login = gestor_autenticacion.iniciar_sesion(nombre_usuario, contrasena)
            if exito_login:
                print(f"Sesión iniciada. Por favor, complete su perfil ahora.")
            else:
                print(f"Error al iniciar sesión automáticamente: {mensaje_login}")
    elif opcion == '3':
        print("Saliendo del programa. ¡Hasta luego!")
        exit()
    else:
        print("Opción no válida. Intente de nuevo.")

def manejar_opcion_administrador(opcion, gestor_autenticacion, gestor_usuarios):
    if opcion == '1':
        exito, usuarios_data = gestor_usuarios.leer_usuarios()
        if exito:
            if usuarios_data:
                print("\n--- Lista de Usuarios y Perfiles ---")
                for usuario in usuarios_data:
                    print(f"Usuario: {usuario['nombre_usuario']}, Rol: {usuario['rol']}")
                    if usuario['perfil']:
                        print("  Perfil:")
                        for key, value in usuario['perfil'].items():
                            if value:
                                print(f"    {key.replace('_', ' ').capitalize()}: {value}")
                    else:
                        print("  Perfil: No asignado")
                    print("-" * 30)
            else:
                print("No hay usuarios registrados.")
        else:
            print(f"Error: {usuarios_data}")
    elif opcion == '2':
        print("\n--- Crear Nuevo Usuario (Admin) ---")
        nombre_usuario = input("Ingrese nombre de usuario para el nuevo usuario: ").strip()

        contrasena = solicitar_y_validar_contrasena()
        if contrasena is None:
            print("Creación de usuario cancelada.")
            return

        rol = input("Ingrese rol (admin/estandar): ").strip().lower()
        if rol not in ['admin', 'estandar']:
            print("Rol no válido. Debe ser 'admin' o 'estandar'.")
            return

        print("\n--- Ingrese Datos del Perfil para el Nuevo Usuario ---")
        datos_perfil = solicitar_datos_perfil() # Esta llamada ahora fuerza los obligatorios

        exito, mensaje = gestor_usuarios.crear_usuario(nombre_usuario, contrasena, datos_perfil, rol)
        print(mensaje)
    elif opcion == '3':
        nombre_usuario = input("Ingrese el nombre de usuario cuya contraseña desea actualizar: ").strip()
        print(f"Actualizando contraseña para {nombre_usuario}...")

        nueva_contrasena = solicitar_y_validar_contrasena()
        if nueva_contrasena is None:
            print("Actualización de contraseña cancelada.")
            return

        exito, mensaje = gestor_usuarios.actualizar_contrasena_usuario(nombre_usuario, nueva_contrasena)
        print(mensaje)
    elif opcion == '4':
        nombre_usuario = input("Ingrese el nombre de usuario cuyo perfil desea actualizar: ").strip()
        # Nota: La función solicitar_datos_perfil ahora fuerza los obligatorios.
        # Si el usuario quiere dejar un obligatorio vacío, tendrá que reingresarlo.
        # Esto es correcto si estamos esperando una "actualización completa" de obligatorios.
        print("Ingrese los datos del perfil a actualizar (los campos obligatorios deben ser llenados):")
        nuevos_datos_perfil = solicitar_datos_perfil() # Esta llamada ahora fuerza los obligatorios
        
        exito, mensaje = gestor_usuarios.actualizar_perfil_usuario(nombre_usuario, nuevos_datos_perfil)
        print(mensaje)
    elif opcion == '5':
        nombre_usuario = input("Ingrese el nombre de usuario a eliminar: ").strip()
        exito, mensaje = gestor_usuarios.eliminar_usuario(nombre_usuario)
        print(mensaje)
    elif opcion == '6': # <-- Nueva opción para actualizar rol
        print("\n--- Actualizar Rol de Usuario ---")
        nombre_usuario = input("Ingrese el nombre de usuario cuyo rol desea actualizar: ").strip()
        nuevo_rol = input("Ingrese el nuevo rol (admin/estandar): ").strip().lower()

        exito, mensaje = gestor_usuarios.actualizar_rol_usuario(nombre_usuario, nuevo_rol) # <-- Llamada a la nueva función
        print(mensaje)
    elif opcion == '7': # <-- Se ajusta el número para Cerrar Sesión
        exito, mensaje = gestor_autenticacion.cerrar_sesion()
        print(mensaje)
    elif opcion == '8': # <-- Se ajusta el número para Salir del Programa
        print("Saliendo del programa. ¡Hasta luego!")
        exit()
    else:
        print("Opción no válida. Intente de nuevo.")

def manejar_opcion_usuario_estandar(opcion, gestor_autenticacion, gestor_usuarios):
    usuario_logueado = gestor_autenticacion.obtener_usuario_logueado() # Esto es correcto

    # Asegúrate de que haya un usuario logueado para cualquier operación
    if not usuario_logueado:
        print("Error: No hay usuario logueado para realizar esta acción.")
        return

    if opcion == '1': # Ver Mi Perfil
        # NO DEBES USAR gestor_usuarios.leer_usuarios() AQUÍ.
        # Ya tienes el usuario_logueado correcto.
        print("\n--- Mi Perfil ---")
        print(f"Usuario: {usuario_logueado.nombre_usuario}")
        print(f"Rol: {usuario_logueado.rol}")

        # Accede directamente al perfil del usuario logueado
        # Ya nos aseguramos en modelos/usuario.py que .perfil siempre es un objeto Perfil
        perfil_data = usuario_logueado.perfil.a_diccionario() 

        if perfil_data: # Esto sigue siendo útil si un perfil se guardó históricamente con None
            print("  Datos Personales:")
            # Itera sobre los elementos del diccionario del perfil
            for key, value in perfil_data.items():
                if value: # Solo imprime si el valor no está vacío
                    print(f"    {key.replace('_', ' ').capitalize()}: {value}")
            # Puedes añadir aquí un else para el caso donde el perfil está vacío pero no es None
            # (ej. recién registrado y no ha llenado nada)
        elif not any(perfil_data.values()): # Si todos los valores del perfil están vacíos
                 print("  Perfil: Vacío. Por favor, actualice su perfil.")
        else:
            # Esta línea debería ser poco probable con las últimas modificaciones
            print("  Perfil: No asignado (Error al cargar perfil o inconsistencia de datos)")

    elif opcion == '2':
        # ... (el resto de tu código para actualizar contraseña)
        print(f"Actualizando contraseña para {usuario_logueado.nombre_usuario}...")
        nueva_contrasena = solicitar_y_validar_contrasena()
        if nueva_contrasena is None:
            print("Actualización de contraseña cancelada.")
            return
        exito, mensaje = gestor_usuarios.actualizar_contrasena_usuario(usuario_logueado.nombre_usuario, nueva_contrasena)
        print(mensaje)
    elif opcion == '3': # Actualizar Mi Perfil (Usuario Estándar)
        print("Ingrese los datos de su perfil a actualizar (los campos obligatorios deben ser llenados):")
        nuevos_datos_perfil = solicitar_datos_perfil()
        exito, mensaje = gestor_usuarios.actualizar_perfil_usuario(usuario_logueado.nombre_usuario, nuevos_datos_perfil)
        print(mensaje)
    elif opcion == '4':
        exito, mensaje = gestor_autenticacion.cerrar_sesion()
        print(mensaje)
    elif opcion == '5':
        print("Saliendo del programa. ¡Hasta luego!")
        exit()
    else:
        print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()