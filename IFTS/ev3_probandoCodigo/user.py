# Importar las funciones de hashing de contraseñas desde utils
# Asegúrate de que utils.py contenga generar_contrasena_hash y verificar_contrasena_hash (con bcrypt)
from validations import generar_contrasena_hash, verificar_contrasena_hash
# Importar las clases de usuario y perfil
from user_info import Perfil # Importar la clase Perfil

class Usuario:
    """
    Clase base que representa un usuario del sistema.
    Contiene atributos comunes y métodos para manejar la autenticación y perfil.
    """
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str, rol: str):
        self._id_usuario = id_usuario
        self._nombre_usuario = nombre_usuario
        self._contrasena_hash = generar_contrasena_hash(contrasena)
        self._rol = rol
        self._perfil: Perfil | None = None # Explicitly typed for clarity

    # Using @property for common getters
    @property
    def id_usuario(self) -> int:
        return self._id_usuario

    @property
    def nombre_usuario(self) -> str:
        return self._nombre_usuario

    @property
    def rol(self) -> str:
        return self._rol

    def verificar_contrasena(self, contrasena: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return verificar_contrasena_hash(contrasena, self._contrasena_hash)

    def set_perfil(self, perfil_obj: Perfil):
        """Asigna un objeto Perfil a este usuario."""
        if not isinstance(perfil_obj, Perfil):
            raise TypeError("El objeto asignado debe ser una instancia de Perfil.")
        if perfil_obj.id_usuario != self._id_usuario:
            raise ValueError("El perfil no pertenece a este ID de usuario.")
        self._perfil = perfil_obj

    def get_perfil(self) -> Perfil | None:
        """Devuelve el objeto Perfil asociado a este usuario (o None)."""
        return self._perfil

    def mostrar_datos_personales(self):
        """Muestra los datos básicos del usuario y la información del perfil si está disponible."""
        print(f"ID: {self.id_usuario}, nombre_usuario: {self.nombre_usuario}, Rol: {self.rol}")
        if self._perfil:
            self._perfil.mostrar_info_adicional()
        else:
            print("  (Sin información de perfil adicional)")

class Administrador(Usuario):
    """
    Representa un usuario administrador.
    """
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str):
        super().__init__(id_usuario, nombre_usuario, contrasena, "administrador")

    def mostrar_datos_personales(self):
        """Muestra los datos específicos del administrador."""
        print(f"\n--- Datos del Administrador ---")
        super().mostrar_datos_personales() 
        print(f"--------------------------")

class UsuarioEstandar(Usuario):
    """
    Representa un usuario estándar.
    """
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str):
        super().__init__(id_usuario, nombre_usuario, contrasena, "estandar")

    def mostrar_datos_personales(self):
        """Muestra los datos específicos del usuario estándar."""
        print(f"\n--- Mis Datos Personales ---")
        super().mostrar_datos_personales() # Call base class method
        print(f"--------------------------")
