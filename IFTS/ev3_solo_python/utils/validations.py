def validar_contrasena(contrasena):
    """
    Valida que la contraseña tenga al menos 6 caracteres, letras y números
    usando funciones de cadena y any().
    """
    if len(contrasena) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."

    tiene_letras = any(c.isalpha() for c in contrasena)
    if not tiene_letras:
        return False, "La contraseña debe contener al menos una letra."

    tiene_numeros = any(c.isdigit() for c in contrasena)
    if not tiene_numeros:
        return False, "La contraseña debe contener al menos un número."

    return True, "Contraseña válida."

def validar_dni(dni):
    """
    Valida el formato de un DNI argentino.
    Debe contener solo dígitos y tener entre 7 y 8 caracteres.
    """
    if not dni.isdigit():
        return False, "El DNI debe contener solo números."
    if not (7 <= len(dni) <= 8):
        return False, "El DNI debe tener entre 7 y 8 dígitos."
    return True, "DNI válido."