import datetime
import uuid

# Usuarios: username -> {password, role}
usuarios = {
    "admin": {"password": "admin", "role": "admin"},
    "user": {"password": "user", "role": "user"}
}

# Clases deportivas (lista de dicts)
# Cada clase tiene id único, coach, nombre_clase, deporte, fecha (str), horario, aforo, inscritos (list usernames)
clases = []

def registrar_usuario(username, password, role):
    if username in usuarios:
        return False, "Usuario ya existe"
    usuarios[username] = {"password": password, "role": role}
    return True, "Usuario registrado correctamente"

def validar_login(username, password):
    if username in usuarios and usuarios[username]["password"] == password:
        return True, usuarios[username]["role"]
    return False, "Usuario o contraseña incorrectos"

def crear_clase(coach, deporte, nombre_clase, fecha, horario, aforo):
    clase_id = str(uuid.uuid4())
    nueva_clase = {
        "id": clase_id,
        "coach": coach,
        "nombre_clase": nombre_clase,
        "deporte": deporte,
        "fecha": fecha,
        "horario": horario,
        "aforo": aforo,
        "inscritos": [],
        "estado": "disponible"
    }
    clases.append(nueva_clase)

def obtener_clases_de_coach(coach):
    return [c for c in clases if c["coach"] == coach]

def eliminar_clase(clase_id):
    global clases
    clases = [c for c in clases if c["id"] != clase_id]

def inscribir_usuario_en_clase(username, clase_id):
    for c in clases:
        if c["id"] == clase_id:
            if len(c["inscritos"]) < c["aforo"]:
                if username not in c["inscritos"]:
                    c["inscritos"].append(username)
                    if len(c["inscritos"]) >= c["aforo"]:
                        c["estado"] = "llena"
                    return True, "Reserva exitosa"
                else:
                    return False, "Ya estás inscrito en esta clase"
            else:
                return False, "La clase está llena"
    return False, "Clase no encontrada"

def cancelar_reserva(username, clase_id):
    for c in clases:
        if c["id"] == clase_id:
            if username in c["inscritos"]:
                c["inscritos"].remove(username)
                c["estado"] = "disponible"
                return True, "Reserva cancelada"
            else:
                return False, "No estás inscrito en esta clase"
    return False, "Clase no encontrada"

def obtener_clases_disponibles_por_deporte(deporte):
    return [c for c in clases if c["deporte"] == deporte and c["estado"] == "disponible"]

def obtener_clases_por_usuario(username):
    return [c for c in clases if username in c["inscritos"]]

