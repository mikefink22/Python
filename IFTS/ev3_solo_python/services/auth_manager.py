import bcrypt
import itertools  # Para generar IDs únicos


# Importa Perfil, UsuarioEstandar y Administrador. Si Perfil está en models.users, no necesitas importarlo de modelos.usuario directamente
from models.users import UsuarioEstandar, Administrador, Perfil # Asumiendo que Perfil también está en models.users

class GestorAutenticacion:
    def __init__(self):
        self.usuarios = []
        self.usuario_logueado = None
        self._inicializar_admin_por_defecto()

    def _hashear_contrasena(self, contrasena):
        return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    def _verificar_contrasena(self, contrasena_plana, contrasena_hasheada):
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), contrasena_hasheada)

    def _inicializar_admin_por_defecto(self):
        # Es una buena práctica verificar si ya existe un admin en self.usuarios antes de crear uno nuevo
        # Esto es especialmente importante si vas a cargar usuarios desde un archivo
        if not any(isinstance(u, Administrador) for u in self.usuarios):
            admin_id = next(itertools.count(1)) # Genera un ID para el admin por defecto
            admin_contrasena_hasheada = self._hashear_contrasena("admin123") # Usa tu método hashear
            
            perfil_admin_inicial = Perfil(
                dni="12345678A",
                nombre="Admin",
                apellido="Principal",
                email="admin@ejemplo.com",
                telefono="1122334455",
                direccion="Calle Falsa 123",
                fecha_nacimiento="1990-01-01"
            )
            # PASA EL ID AL CONSTRUCTOR DE ADMINISTRADOR
            admin_usuario = Administrador(id_usuario=admin_id, nombre_usuario="admin", 
                                        contrasena_hasheada=admin_contrasena_hasheada, 
                                        perfil_objeto=perfil_admin_inicial)
            self.usuarios.append(admin_usuario)

    def registrar_usuario(self, nombre_usuario, contrasena, rol="estandar", perfil_objeto=None):
        nombre_usuario_normalizado = nombre_usuario.lower()

        if any(usuario.nombre_usuario == nombre_usuario_normalizado for usuario in self.usuarios):
            return False, "El nombre de usuario ya existe."

        contrasena_hasheada = self._hashear_contrasena(contrasena)
        
        # Genera un ID para el nuevo usuario
        nuevo_usuario_id = next(itertools.count(1))  # <-- Nuevo ID aquí

        # Si no se proporciona un objeto de perfil, crea uno vacío
        if perfil_objeto is None:
            nuevo_perfil = Perfil()
        else:
            nuevo_perfil = perfil_objeto 

        if rol == "admin":
            # PASA EL ID AL CONSTRUCTOR DE ADMINISTRADOR
            nuevo_usuario = Administrador(id_usuario=nuevo_usuario_id, nombre_usuario=nombre_usuario_normalizado, 
                                        contrasena_hasheada=contrasena_hasheada, perfil_objeto=nuevo_perfil)
        elif rol == "estandar":
            # PASA EL ID AL CONSTRUCTOR DE USUARIOESTANDAR
            nuevo_usuario = UsuarioEstandar(id_usuario=nuevo_usuario_id, nombre_usuario=nombre_usuario_normalizado, 
                                          contrasena_hasheada=contrasena_hasheada, perfil_objeto=nuevo_perfil)
        else:
            return False, "Rol no válido. Debe ser 'admin' o 'estandar'."

        self.usuarios.append(nuevo_usuario)
        return True, f"Usuario '{nombre_usuario}' con rol '{nuevo_usuario.rol}' registrado exitosamente."

    def iniciar_sesion(self, nombre_usuario_ingresado, contrasena_plana):
        nombre_usuario_normalizado_ingresado = nombre_usuario_ingresado.lower()

        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario_normalizado_ingresado:
                if self._verificar_contrasena(contrasena_plana, usuario.contrasena_hasheada):
                    self.usuario_logueado = usuario
                    return True, f"Inicio de sesión exitoso como '{usuario.rol}'."
                else:
                    return False, "Credenciales incorrectas."
        return False, "Credenciales incorrectas."

    def cerrar_sesion(self):
        if self.usuario_logueado:
            nombre_usuario_actual = self.usuario_logueado.nombre_usuario
            self.usuario_logueado = None
            return True, f"Sesión de '{nombre_usuario_actual}' cerrada."
        return False, "No hay ningún usuario logueado."

    def obtener_usuario_logueado(self):
        return self.usuario_logueado

    def obtener_usuario_por_nombre(self, nombre_usuario):
        nombre_usuario_normalizado = nombre_usuario.lower()
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario_normalizado:
                return usuario
        return None