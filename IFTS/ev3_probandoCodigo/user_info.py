

class Perfil:
    """
    Clase que representa el perfil de un usuario con información adicional.
    """
    def __init__(self, id_perfil: int, id_usuario: int, nombre: str = "", apellido: str = "", email: str = ""):
        self._id_perfil = id_perfil # Opcional, podría usar el mismo ID que el usuario
        self._id_usuario = id_usuario # Clave foránea para relacionar con Usuario
        self._nombre = nombre
        self._apellido = apellido
        self._email = email        
        # Puedes añadir más campos aquí, como fecha_nacimiento, bio, etc.

    def get_nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}".strip()

    # Métodos para obtener/establecer otros atributos del perfil
    def get_email(self) -> str:
        return self._email

    def set_email(self, nuevo_email: str): # Agregar validaciones??
        self._email = nuevo_email

    def mostrar_info_adicional(self):
        print(f"Nombre Completo: {self.get_nombre_completo()}")
        print(f"Email: {self._email}")        