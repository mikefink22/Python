from services.auth_manager import GestorAutenticacion
from models.users import Perfil
import bcrypt # se usa en crear_usuario

class GestorUsuarios:
    def __init__(self, gestor_autenticacion: GestorAutenticacion):
        self.gestor_autenticacion = gestor_autenticacion

    # --- NUEVO MÉTODO AUXILIAR PARA UNICIDAD DE DNI ---
    def _dni_ya_existe(self, dni_a_verificar, id_perfil_a_excluir=None):
        """
        Verifica si un DNI ya está registrado por otro usuario.
        Si se proporciona id_perfil_a_excluir, ignora el DNI de ese perfil.
        """
        for usuario in self.gestor_autenticacion.usuarios:
            # Asegurarse de que el usuario tenga un perfil y un DNI no vacío
            if usuario.perfil and usuario.perfil.dni:
                # Compara el DNI en minúsculas por si hubiera inconsistencias de capitalización (aunque con dígitos no es un problema)
                # O si quisieras una normalización más robusta en el futuro (ej. quitar puntos si los permitieras)
                if usuario.perfil.dni == dni_a_verificar:
                    # Si estamos excluyendo un perfil (ej. al actualizar), y es el mismo usuario,
                    # entonces no lo contamos como un duplicado.
                    if id_perfil_a_excluir and usuario.perfil.id_perfil == id_perfil_a_excluir:
                        continue # Es el mismo usuario, ignóralo para la comprobación de duplicados
                    return True # DNI encontrado en otro usuario
        return False
    # --- FIN NUEVO MÉTODO AUXILIAR ---


    def crear_usuario(self, nombre_usuario, contrasena, datos_perfil, rol):
        usuario_logueado = self.gestor_autenticacion.obtener_usuario_logueado()
        if not usuario_logueado or usuario_logueado.rol != 'admin':
            return False, "Acceso denegado. Solo los administradores pueden crear usuarios."

        # Validar unicidad del DNI
        dni = datos_perfil.get('dni', "")
        if dni and self._dni_ya_existe(dni): # Solo verifica si el DNI fue proporcionado
            return False, f"Error: El DNI '{dni}' ya está registrado por otro usuario."

        try:
            # Los campos obligatorios se manejan en la UI, aquí los obtenemos con .get()
            dni = datos_perfil.get('dni', "")
            nombre = datos_perfil.get('nombre', "")
            apellido = datos_perfil.get('apellido', "")
            email = datos_perfil.get('email', "")
            telefono = datos_perfil.get('telefono', "")
            direccion = datos_perfil.get('direccion', "")
            fecha_nacimiento = datos_perfil.get('fecha_nacimiento', "")

            nuevo_perfil = Perfil(
                dni=dni, nombre=nombre, apellido=apellido, email=email,
                telefono=telefono, direccion=direccion, fecha_nacimiento=fecha_nacimiento
            )
        except Exception as e:
            return False, f"Error al crear perfil: {e}"

        # Llamar a registrar_usuario de GestorAutenticacion con el perfil ya creado
        exito, mensaje = self.gestor_autenticacion.registrar_usuario(
            nombre_usuario, contrasena, rol, perfil_objeto=nuevo_perfil
        )
        return exito, mensaje

    def leer_usuarios(self):
        # Esta función originalmente leía todos los usuarios en memoria del GestorAutenticacion,
        # pero cuando se llama desde 'Ver Mi Perfil' para un usuario estándar,
        # solo se debería devolver su propio perfil.
        # Para evitar reescribir demasiado, el `principal.py` ya filtra por `usuario_logueado`
        # cuando es un usuario estándar, así que aquí devolvemos la lista completa.
        usuarios_data = []
        for usuario in self.gestor_autenticacion.usuarios:
            usuarios_data.append(usuario.a_diccionario())
        return True, usuarios_data

    def actualizar_contrasena_usuario(self, nombre_usuario, nueva_contrasena):
        usuario_logueado = self.gestor_autenticacion.obtener_usuario_logueado()
        if not usuario_logueado:
            return False, "Debe iniciar sesión para actualizar la contraseña."

        usuario_a_actualizar = self.gestor_autenticacion.obtener_usuario_por_nombre(nombre_usuario)
        if not usuario_a_actualizar:
            return False, "Usuario no encontrado."

        # Verificar permisos:
        # Un admin puede actualizar la contraseña de cualquier usuario.
        # Un usuario estándar solo puede actualizar su propia contraseña.
        if usuario_logueado.rol == 'estandar' and usuario_logueado.nombre_usuario != usuario_a_actualizar.nombre_usuario:
            return False, "Acceso denegado. No tiene permisos para actualizar la contraseña de otro usuario."

        # Hashear la nueva contraseña
        nueva_contrasena_hasheada = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
        usuario_a_actualizar.contrasena_hasheada = nueva_contrasena_hasheada
        return True, f"Contraseña del usuario '{usuario_a_actualizar.nombre_usuario}' actualizada exitosamente."

    def actualizar_perfil_usuario(self, nombre_usuario, nuevos_datos_perfil):
        usuario_logueado = self.gestor_autenticacion.obtener_usuario_logueado()
        if not usuario_logueado:
            return False, "Debe iniciar sesión para actualizar el perfil."

        usuario_a_actualizar = self.gestor_autenticacion.obtener_usuario_por_nombre(nombre_usuario)
        if not usuario_a_actualizar:
            return False, "Usuario no encontrado."

        # Verificar permisos:
        # Un admin puede actualizar el perfil de cualquier usuario.
        # Un usuario estándar solo puede actualizar su propio perfil.
        if usuario_logueado.rol == 'estandar' and usuario_logueado.nombre_usuario != usuario_a_actualizar.nombre_usuario:
            return False, "Acceso denegado. No tiene permisos para actualizar el perfil de otro usuario."

        if not usuario_a_actualizar.perfil:
            # Si por alguna razón el usuario no tiene perfil (no debería pasar con el flujo actual)
            usuario_a_actualizar.perfil = Perfil()

        # --- VALIDACIÓN DE UNICIDAD DEL DNI AL ACTUALIZAR ---
        if 'dni' in nuevos_datos_perfil and nuevos_datos_perfil['dni']:
            nuevo_dni = nuevos_datos_perfil['dni']
            # Excluye el ID del perfil del usuario que estamos actualizando
            if self._dni_ya_existe(nuevo_dni, usuario_a_actualizar.perfil.id_perfil):
                return False, f"Error: El DNI '{nuevo_dni}' ya está registrado por otro usuario."
        # --- FIN VALIDACIÓN DE UNICIDAD DEL DNI ---

        # Actualizar los campos del perfil
        for key, value in nuevos_datos_perfil.items():
            # Solo actualiza si el valor no está vacío (permite dejar opcionales sin modificar)
            # Y se asegura de que el atributo exista en el objeto Perfil
            if hasattr(usuario_a_actualizar.perfil, key):
                setattr(usuario_a_actualizar.perfil, key, value)

        return True, f"Perfil del usuario '{usuario_a_actualizar.nombre_usuario}' actualizado exitosamente."

    def eliminar_usuario(self, nombre_usuario):
        usuario_logueado = self.gestor_autenticacion.obtener_usuario_logueado()
        if not usuario_logueado or usuario_logueado.rol != 'admin':
            return False, "Acceso denegado. Solo los administradores pueden eliminar usuarios."

        # No permitir que un admin se elimine a sí mismo si es el único admin
        if usuario_logueado.nombre_usuario == nombre_usuario:
            admins_activos = [u for u in self.gestor_autenticacion.usuarios if u.rol == 'admin']
            if len(admins_activos) == 1 and admins_activos[0].nombre_usuario == nombre_usuario:
                return False, "No puedes eliminar el único usuario administrador del sistema."

        usuario_a_eliminar = None
        # Iterar sobre la lista de usuarios del gestor de autenticación y eliminarlo
        for i, usuario in enumerate(self.gestor_autenticacion.usuarios):
            if usuario.nombre_usuario == nombre_usuario.lower(): # Siempre comparar normalizado
                usuario_a_eliminar = usuario
                del self.gestor_autenticacion.usuarios[i]
                # Si el usuario logueado actualmente es el que se elimina, cerrar su sesión
                if self.gestor_autenticacion.obtener_usuario_logueado() and \
                   self.gestor_autenticacion.obtener_usuario_logueado().nombre_usuario == usuario.nombre_usuario:
                    self.gestor_autenticacion.cerrar_sesion()
                return True, f"Usuario '{nombre_usuario}' eliminado exitosamente."
        return False, "Usuario no encontrado."
    
    def actualizar_rol_usuario(self, nombre_usuario, nuevo_rol):
        usuario_logueado = self.gestor_autenticacion.obtener_usuario_logueado()
        if not usuario_logueado or usuario_logueado.rol != 'admin':
            return False, "Acceso denegado. Solo los administradores pueden cambiar roles."

        if nuevo_rol not in ['admin', 'estandar']:
            return False, "Rol no válido. Debe ser 'admin' o 'estandar'."

        usuario_a_actualizar = self.gestor_autenticacion.obtener_usuario_por_nombre(nombre_usuario)
        if not usuario_a_actualizar:
            return False, f"Usuario '{nombre_usuario}' no encontrado."

        # No permitir que un admin se cambie a sí mismo a estándar si es el único admin
        if usuario_a_actualizar.nombre_usuario == usuario_logueado.nombre_usuario and nuevo_rol == 'estandar':
            admins_activos = [u for u in self.gestor_autenticacion.usuarios if u.rol == 'admin']
            if len(admins_activos) == 1 and admins_activos[0].nombre_usuario == usuario_a_actualizar.nombre_usuario:
                return False, "No puedes degradar al único usuario administrador del sistema a estándar."
        
        # Si el usuario es el que actualmente está logueado y va a cambiar su rol,
        # su objeto de sesión debe actualizarse para reflejar el nuevo rol.
        if usuario_a_actualizar.nombre_usuario == usuario_logueado.nombre_usuario:
            usuario_logueado.rol = nuevo_rol
            # No es estrictamente necesario llamar a set_usuario_logueado nuevamente,
            # ya que el objeto es el mismo, pero lo dejo como recordatorio de la actualización.
            # self.gestor_autenticacion.set_usuario_logueado(usuario_logueado) 

        usuario_a_actualizar.rol = nuevo_rol
        return True, f"Rol del usuario '{nombre_usuario}' actualizado a '{nuevo_rol}' exitosamente."