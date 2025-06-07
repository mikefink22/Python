# database.py

import mysql.connector
from mysql.connector import Error
import hashlib

# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    'host': 'localhost',
    'database': 'proyecto_usuarios_db',
    'user': 'root',
    'password': 'root'
}

# --- Funciones de Conexión e Inicialización ---

def get_db_connection():
    """Establece y retorna una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def initialize_db():
    """
    Inicializa la base de datos MySQL creando las tablas 'usuarios' y 'perfiles' si no existen.
    También inserta un usuario administrador por defecto si la tabla 'usuarios' está vacía.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos para inicializarla.")
            return

        cursor = conn.cursor()

        # Script SQL para crear la tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(255) NOT NULL UNIQUE,
                contrasena_hash VARCHAR(255) NOT NULL,
                rol VARCHAR(50) NOT NULL,
                CHECK (rol IN ('administrador', 'estandar'))
            );
        ''')

        # Script SQL para crear la tabla de perfiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles (
                id_perfil INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL UNIQUE,          -- Clave foránea a usuarios.id_usuario
                nombre_completo VARCHAR(255) NULL,
                apellido VARCHAR(255) NULL,
                email VARCHAR(255) UNIQUE NULL,
                fecha_nacimiento DATE NULL,
                direccion VARCHAR(255) NULL,
                telefono VARCHAR(50) NULL,
                
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                    ON DELETE CASCADE -- Si se elimina un usuario, su perfil también se elimina
            );
        ''')

        # Verificar si ya existe un administrador para no duplicarlo
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'administrador'")
        if cursor.fetchone()[0] == 0:
            default_admin_pass_hash = hashlib.sha256("admin123".encode()).hexdigest()
            # Primero insertamos en usuarios
            cursor.execute('''
                INSERT INTO usuarios (nombre_usuario, contrasena_hash, rol)
                VALUES (%s, %s, %s)
            ''', ('admin', default_admin_pass_hash, 'administrador'))
            
            # Obtener el ID del usuario recién insertado para el perfil
            admin_id = cursor.lastrowid 

            # Luego insertamos en perfiles
            cursor.execute('''
                INSERT INTO perfiles (id_usuario, nombre_completo, apellido, email)
                VALUES (%s, %s, %s, %s)
            ''', (admin_id, 'Administrador Principal', 'Sistema', 'admin@ejemplo.com'))

            print("Administrador por defecto 'admin' creado con contraseña 'admin123' y perfil básico.")

        conn.commit()
        print(f"Base de datos MySQL '{DB_CONFIG['database']}' inicializada correctamente con tablas de usuarios y perfiles.")

    except Error as e:
        print(f"Error durante la inicialización de MySQL: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- Funciones CRUD para la tabla 'usuarios' (estas casi no cambian, solo se agregan las de perfil) ---

def crear_usuario(nombre_usuario, contrasena_hash, rol):
    """Inserta un nuevo usuario en la tabla 'usuarios'."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return None # Devolvemos el ID o None
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nombre_usuario, contrasena_hash, rol)
            VALUES (%s, %s, %s)
        ''', (nombre_usuario, contrasena_hash, rol))
        conn.commit()
        return cursor.lastrowid # Retorna el ID del nuevo usuario
    except Error as e:
        if e.errno == 1062:
            print(f"Error: El nombre de usuario '{nombre_usuario}' ya existe.")
        else:
            print(f"Error al crear usuario: {e}")
        if conn: conn.rollback()
        return None

def obtener_usuario_por_nombre(nombre_usuario):
    """Busca un usuario por su nombre de usuario. Retorna una tupla (id, nombre, hash, rol) o None."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, nombre_usuario, contrasena_hash, rol FROM usuarios WHERE nombre_usuario = %s', (nombre_usuario,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener usuario: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def obtener_usuario_por_id(id_usuario):
    """Busca un usuario por su ID. Retorna una tupla (id, nombre, hash, rol) o None."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, nombre_usuario, contrasena_hash, rol FROM usuarios WHERE id_usuario = %s', (id_usuario,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def obtener_todos_los_usuarios():
    """Retorna una lista de tuplas con todos los usuarios registrados (solo datos de autenticación)."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, nombre_usuario, contrasena_hash, rol FROM usuarios')
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todos los usuarios: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def actualizar_rol_usuario(id_usuario, nuevo_rol):
    """Actualiza el rol de un usuario específico."""
    if nuevo_rol not in ['administrador', 'estandar']:
        print("Rol no válido. Debe ser 'administrador' o 'estandar'.")
        return False
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET rol = %s WHERE id_usuario = %s', (nuevo_rol, id_usuario))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar rol del usuario: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def eliminar_usuario(id_usuario):
    """
    Elimina un usuario de la base de datos por su ID.
    Debido a ON DELETE CASCADE, su perfil asociado también será eliminado.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al eliminar usuario: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- NUEVAS Funciones CRUD para la tabla 'perfiles' ---

def crear_perfil(id_usuario, nombre_completo=None, apellido=None, email=None, fecha_nacimiento=None, direccion=None, telefono=None):
    """Inserta un nuevo perfil en la tabla 'perfiles' asociado a un id_usuario."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO perfiles (id_usuario, nombre_completo, apellido, email, fecha_nacimiento, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (id_usuario, nombre_completo, apellido, email, fecha_nacimiento, direccion, telefono))
        conn.commit()
        return True
    except Error as e:
        if e.errno == 1062: # Duplicate entry for id_usuario in perfiles
            print(f"Error: Ya existe un perfil para el usuario ID {id_usuario}.")
        else:
            print(f"Error al crear perfil para usuario ID {id_usuario}: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def obtener_perfil_por_usuario_id(id_usuario):
    """Busca un perfil por el ID de usuario. Retorna una tupla con los datos del perfil o None."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id_perfil, id_usuario, nombre_completo, apellido, email, fecha_nacimiento, direccion, telefono
            FROM perfiles
            WHERE id_usuario = %s
        ''', (id_usuario,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener perfil para usuario ID {id_usuario}: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def actualizar_perfil(id_usuario, nombre_completo=None, apellido=None, email=None, fecha_nacimiento=None, direccion=None, telefono=None):
    """Actualiza los datos de perfil para un usuario dado su id_usuario."""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        
        # Construimos la consulta UPDATE dinámicamente para solo actualizar los campos que no son None
        updates = []
        params = []
        if nombre_completo is not None:
            updates.append("nombre_completo = %s")
            params.append(nombre_completo)
        if apellido is not None:
            updates.append("apellido = %s")
            params.append(apellido)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if fecha_nacimiento is not None:
            updates.append("fecha_nacimiento = %s")
            params.append(fecha_nacimiento)
        if direccion is not None:
            updates.append("direccion = %s")
            params.append(direccion)
        if telefono is not None:
            updates.append("telefono = %s")
            params.append(telefono)

        if not updates: # No hay nada que actualizar
            print("No se proporcionaron datos para actualizar el perfil.")
            return False

        query = f"UPDATE perfiles SET {', '.join(updates)} WHERE id_usuario = %s"
        params.append(id_usuario)

        cursor.execute(query, tuple(params))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar perfil para usuario ID {id_usuario}: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Ejemplo de uso (para pruebas, no debería estar en el archivo final)
if __name__ == "__main__":
    print("Inicializando la base de datos...")
    initialize_db()
    # Aquí puedes agregar pruebas para crear_perfil, obtener_perfil_por_usuario_id, etc.
    print("\nPrueba de conexión terminada.")