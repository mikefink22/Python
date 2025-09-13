# main.py
from validations import limpiar_pantalla
from user_manager import UserManager

def main():
    limpiar_pantalla()
    print("--- Bienvenido al Sistema Planificador ---")

    user_manager = UserManager()

    print("\n--- Probando el registro y login de un usuario ---")

    # 1. Registrar un nuevo usuario
    print("\nRegistrando 'usuario_prueba'...")
    usuario_creado = user_manager.registrar_usuario(
        username="usuario_prueba",
        password="Password123",
        rol="estandar",
        nombre_perfil="Juan",
        apellido_perfil="Perez",
        email_perfil="juan.perez@example.com"
    )

    if usuario_creado:
        print(f"Usuario '{usuario_creado.get_username()}' registrado exitosamente.")
        usuario_creado.mostrar_datos_personales()

        # 2. Intentar iniciar sesión con el usuario recién creado
        print(f"\nIntentando iniciar sesión como '{usuario_creado.get_username()}'...")
        user_logueado = user_manager.iniciar_sesion("usuario_prueba", "Password123")

        if user_logueado:
            print(f"¡Inicio de sesión exitoso para '{user_logueado.get_username()}'!")
        else:
            print("Fallo el inicio de sesión. Algo salió mal.")
    else:
        print("El registro de 'usuario_prueba' falló.")

    print("\n--- Fin de la prueba ---")

if __name__ == "__main__":
    main()