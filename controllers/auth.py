# controllers/auth.py

# Simulador de base de datos de usuarios
# clave: nombre_usuario, valor: diccionario con contraseña y tipo de rol
usuarios_db = {
    "admin": {"password": "admin123", "rol": "admin"},
    "user": {"password": "user123", "rol": "user"}
}

def registrar_usuario(username, password, rol="user"):
    if username in usuarios_db:
        return False, "El usuario ya existe."
    usuarios_db[username] = {"password": password, "rol": rol}
    return True, "Usuario registrado correctamente."

def validar_login(username, password):
    if username in usuarios_db:
        if usuarios_db[username]["password"] == password:
            return True, usuarios_db[username]["rol"]
        else:
            return False, "Contraseña incorrecta."
    return False, "Usuario no encontrado."

