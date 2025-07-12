from data.db_simulada import registrar_usuario, validar_login

def login(username, password):
    return validar_login(username, password)

def register(username, password, role):
    return registrar_usuario(username, password, role)

