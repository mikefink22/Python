import itertools # Para generar IDs únicos
import bcrypt # Asegúrate de que bcrypt esté importado

class Perfil:
    _next_id_counter = itertools.count(1)

    def __init__(self, id_perfil=None, dni="", nombre="", apellido="", email="",
                 telefono="", direccion="", fecha_nacimiento=""):
        # Genera un ID único para el perfil si no se proporciona
        self.id_perfil = id_perfil if id_perfil is not None else next(Perfil._next_id_counter)
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento

    def a_diccionario(self):
        """Convierte el objeto Perfil a un diccionario."""
        return {
            "id_perfil": self.id_perfil,
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_nacimiento": self.fecha_nacimiento
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un objeto Perfil desde un diccionario."""
        if datos is None: # Si el perfil no existe en el diccionario, devuelve un Perfil vacío
            return cls()
        return cls(
            id_perfil=datos.get('id_perfil'),
            dni=datos.get('dni', ""),
            nombre=datos.get('nombre', ""),
            apellido=datos.get('apellido', ""),
            email=datos.get('email', ""),
            telefono=datos.get('telefono', ""),
            direccion=datos.get('direccion', ""),
            fecha_nacimiento=datos.get('fecha_nacimiento', "")
        )

    def __repr__(self):
        return (f"Perfil(id_perfil='{self.id_perfil}', dni='{self.dni}', nombre='{self.nombre}', "
                f"apellido='{self.apellido}', email='{self.email}')")


class Usuario:
    def __init__(self, id_usuario=None, nombre_usuario="", contrasena_hasheada="", rol="estandar", perfil_objeto=None):
        # Genera un ID único para el usuario si no se proporciona
        self.id_usuario = id_usuario if id_usuario is not None else str(next(itertools.count(1))) # Genera un ID único usando itertools
        self.nombre_usuario = nombre_usuario
        self.contrasena_hasheada = contrasena_hasheada # Almacena el hash, NO la contraseña en texto plano
        self._rol = rol # Almacena el rol internamente (usado por @property)
        # Asegura que perfil sea siempre un objeto Perfil, incluso si se pasa None
        self.perfil = perfil_objeto if perfil_objeto is not None else Perfil()

    @property # Getter para la propiedad 'rol'
    def rol(self):
        return self._rol

    @rol.setter # Setter para la propiedad 'rol' - ¡Esto permite modificarlo!
    def rol(self, value):
        # Pequeña validación al intentar cambiar el rol
        if value not in ['admin', 'estandar']:
            raise ValueError("Rol no válido. Debe ser 'admin' o 'estandar'.")
        self._rol = value

    def verificar_contrasena(self, contrasena):
        """Verifica si la contraseña proporcionada coincide con la hasheada."""
        return bcrypt.checkpw(contrasena.encode('utf-8'), self.contrasena_hasheada)

    def a_diccionario(self):
        """Convierte el objeto Usuario a un diccionario para almacenamiento/visualización."""
        return {
            "id_usuario": self.id_usuario, # Incluir el ID del usuario
            "nombre_usuario": self.nombre_usuario,
            # Decodificar el hash a string para guardar/mostrar (bcrypt lo almacena en bytes)
            "contrasena_hasheada": self.contrasena_hasheada.decode('utf-8'),
            "rol": self.rol, # Accede a la propiedad 'rol' (que devuelve _rol)
            "perfil": self.perfil.a_diccionario() # Convierte el perfil a diccionario
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un objeto Usuario (o subclase) desde un diccionario."""
        perfil_datos = datos.get('perfil')
        # Usa el método desde_diccionario de Perfil para crear el objeto Perfil
        perfil_objeto = Perfil.desde_diccionario(perfil_datos) 
        
        # Asegúrate de decodificar la contraseña hasheada al cargarla si está en string
        contrasena_hasheada_bytes = datos['contrasena_hasheada'].encode('utf-8')
        
        # Determina el tipo de usuario y lo crea
        if datos['rol'] == 'admin':
            return Administrador(
                id_usuario=datos.get('id_usuario'), # Pasa el ID al constructor
                nombre_usuario=datos.get('nombre_usuario'),
                contrasena_hasheada=contrasena_hasheada_bytes,
                perfil_objeto=perfil_objeto # Pasa el objeto Perfil
            )
        else: # Por defecto, si no es admin o es cualquier otro, es UsuarioEstandar
            return UsuarioEstandar(
                id_usuario=datos.get('id_usuario'), # Pasa el ID al constructor
                nombre_usuario=datos.get('nombre_usuario'),
                contrasena_hasheada=contrasena_hasheada_bytes,
                perfil_objeto=perfil_objeto # Pasa el objeto Perfil
            )

    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.id_usuario[:8]}...', nombre='{self.nombre_usuario}', rol='{self.rol}')"


class UsuarioEstandar(Usuario):
    def __init__(self, id_usuario=None, nombre_usuario="", contrasena_hasheada="", perfil_objeto=None):
        # Llama al constructor de Usuario, pasando el rol 'estandar'
        super().__init__(id_usuario, nombre_usuario, contrasena_hasheada, 'estandar', perfil_objeto)

class Administrador(Usuario):
    def __init__(self, id_usuario=None, nombre_usuario="", contrasena_hasheada="", perfil_objeto=None):
        # Llama al constructor de Usuario, pasando el rol 'admin'
        super().__init__(id_usuario, nombre_usuario, contrasena_hasheada, 'admin', perfil_objeto)     