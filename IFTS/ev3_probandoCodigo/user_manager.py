from user import Usuario, Administrador, UsuarioEstandar
from user_info import Perfil
# Importar las funciones de validación desde utils
from validations import validar_contrasena, validar_dni # Se asume que también tienes validar_dni

class UserManager:
    """
    Clase encargada de gestionar la colección de usuarios en memoria.
    Simula las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    y la autenticación de usuarios.
    """
    def __init__(self):
        self._usuarios = {}  # Diccionario para almacenar usuarios por username
        self._next_user_id = 1
        self._next_profile_id = 1 # Para IDs de perfil únicos
        self._inicializar_usuarios_ejemplo()

    def _inicializar_usuarios_ejemplo(self):
        """
        Inicializa algunos usuarios de ejemplo para propósitos de demostración.
        """
        print("Inicializando usuarios de ejemplo...")
        self.registrar_usuario("admin", "Admin123", rol="administrador",
                               nombre_perfil="Super", apellido_perfil="Admin", email_perfil="admin@example.com")
        self.registrar_usuario("usuario1", "UserPass1", rol="estandar",
                               nombre_perfil="Ana", apellido_perfil="Gomez", email_perfil="ana.gomez@example.com")
        self.registrar_usuario("pepe", "Pepe123", rol="estandar",
                               nombre_perfil="Pepe", apellido_perfil="Argento", email_perfil="pepe@example.com")

    def registrar_usuario(self, username: str, password: str, rol: str = "estandar", 
                           nombre_perfil: str = "", apellido_perfil: str = "", email_perfil: str = "") -> Usuario | None:
        """
        Registra un nuevo usuario en el sistema.
        Incluye validación de contraseña y creación de perfil.
        """
        if username in self._usuarios:
            print(f"Error: El nombre de usuario '{username}' ya existe.")
            return None

        es_valida_pw, mensaje_pw = validar_contrasena(password)
        if not es_valida_pw:
            print(f"Error al registrar usuario: {mensaje_pw}")
            return None

        user_id = self._next_user_id
        profile_id = self._next_profile_id

        if rol == "administrador":
            new_user = Administrador(user_id, username, password)
        elif rol == "estandar":
            new_user = UsuarioEstandar(user_id, username, password)
        else:
            print("Error: Rol no válido. Solo 'administrador' o 'estandar'.")
            return None

        # Crear y asignar un perfil al usuario
        new_profile = Perfil(
            id_perfil=profile_id,
            id_usuario=user_id, # Relaciona el perfil con el usuario
            nombre=nombre_perfil,
            apellido=apellido_perfil,
            email=email_perfil,            
        )
        new_user.set_perfil(new_profile) # Asigna el perfil al objeto Usuario

        self._usuarios[username] = new_user
        self._next_user_id += 1
        self._next_profile_id += 1
        print(f"Usuario '{username}' ({rol}) registrado exitosamente.")
        return new_user

    def iniciar_sesion(self, username: str, password: str) -> Usuario | None:
        """
        Intenta iniciar sesión de un usuario.
        Retorna el objeto Usuario si las credenciales son válidas, None en caso contrario.
        """
        usuario = self._usuarios.get(username)
        if usuario and usuario.verificar_password(password):
            print(f"Inicio de sesión exitoso para '{username}'.")
            return usuario
        else:
            print("Error: Nombre de usuario o contraseña incorrectos.")
            return None

    def obtener_usuario_por_username(self, username: str) -> Usuario | None:
        """Retorna un usuario por su nombre de usuario."""
        return self._usuarios.get(username)

    def obtener_todos_los_usuarios(self) -> list[Usuario]:
        """Retorna una lista de todos los usuarios registrados."""
        return list(self._usuarios.values())

    def visualizar_listado_usuarios(self) -> None:
        """
        Muestra un listado de todos los usuarios registrados en el sistema.
        Este método es invocado por el administrador a través del UserManager.
        """
        print("\n--- Listado de Usuarios Registrados ---")
        usuarios = self.obtener_todos_los_usuarios()
        if not usuarios:
            print("No hay usuarios registrados en el sistema.")
            return

        for user in usuarios:
            print(f"ID: {user.get_id_usuario()}, Username: {user.get_username()}, Rol: {user.get_rol()}")
        print("---------------------------------------")

    def cambiar_rol_usuario(self, username_a_modificar: str, nuevo_rol: str, admin_solicitante_id: int) -> bool:
        """
        Cambia el rol de un usuario específico.
        Requiere el ID del administrador que realiza la solicitud para evitar auto-modificación.
        """
        usuario_a_modificar = self.obtener_usuario_por_username(username_a_modificar)
        if not usuario_a_modificar:
            print(f"Error: El usuario '{username_a_modificar}' no fue encontrado.")
            return False

        if nuevo_rol not in ["administrador", "estandar"]:
            print("Error: El rol solo puede ser 'administrador' o 'estandar'.")
            return False

        if usuario_a_modificar.get_id_usuario() == admin_solicitante_id:
            print("Error: No puedes cambiar tu propio rol.")
            return False

        # Asignar el nuevo rol directamente al atributo _rol del objeto Usuario
        # Esto es un acceso directo para simplificar, en un sistema más complejo
        # podrías tener un método 'set_rol' en Usuario si hay lógica adicional.
        usuario_a_modificar._rol = nuevo_rol
        print(f"El rol del usuario '{usuario_a_modificar.get_username()}' ha sido cambiado a '{nuevo_rol}'.")
        return True

    def eliminar_usuario(self, username_a_eliminar: str, admin_solicitante_id: int) -> bool:
        """
        Elimina un usuario del sistema por su username.
        Requiere el ID del administrador que realiza la solicitud para evitar auto-eliminación.
        """
        if username_a_eliminar not in self._usuarios:
            print(f"Error: El usuario '{username_a_eliminar}' no existe.")
            return False

        usuario_a_eliminar_obj = self._usuarios[username_a_eliminar]

        if usuario_a_eliminar_obj.get_id_usuario() == admin_solicitante_id:
            print("Error: No puedes eliminarte a ti mismo.")
            return False

        del self._usuarios[username_a_eliminar]
        print(f"Usuario '{username_a_eliminar}' eliminado exitosamente.")
        return True
