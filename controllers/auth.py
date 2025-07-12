# controllers/auth.py

# Simulador de base de datos de usuarios (en memoria)
usuarios_db = {
    "admin": {"password": "admin123", "rol": "admin"},
    "user": {"password": "user123", "rol": "user"}
}

def registrar_usuario(username, password, rol="user"):
    """
    Registra un nuevo usuario si no existe ya.
    :param username: Nombre de usuario
    :param password: Contraseña
    :param rol: 'admin' o 'user'
    :return: (bool, mensaje)
    """
    if username in usuarios_db:
        return False, "El usuario ya existe."
    
    usuarios_db[username] = {
        "password": password,
        "rol": rol
    }
    return True, "Usuario registrado correctamente."

def validar_login(username, password):
    """
    Valida usuario y contraseña.
    :param username: Nombre de usuario
    :param password: Contraseña
    :return: (bool, rol o mensaje de error)
    """
    if username in usuarios_db:
        if usuarios_db[username]["password"] == password:
            return True, usuarios_db[username]["rol"]
        else:
            return False, "Contraseña incorrecta."
    return False, "Usuario no encontrado."

