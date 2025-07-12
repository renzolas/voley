# data/db_simulada.py

import uuid

# Estructura de clases creadas por los entrenadores
# Cada clase tiene: id, coach, deporte, nombre, fecha, horario, aforo, inscritos, estado
clases = []

# Estructura de reservas hechas por usuarios
# Cada reserva tiene: id, usuario, id_clase
reservas = []


def crear_clase(coach, deporte, nombre_clase, fecha, horario, aforo):
    clase_id = str(uuid.uuid4())
    nueva_clase = {
        "id": clase_id,
        "coach": coach,
        "deporte": deporte,
        "nombre_clase": nombre_clase,
        "fecha": fecha,
        "horario": horario,
        "aforo": aforo,
        "inscritos": [],
        "estado": "disponible"
    }
    clases.append(nueva_clase)
    return clase_id


def obtener_clases_disponibles(deporte=None):
    disponibles = [c for c in clases if c["estado"] == "disponible"]
    if deporte:
        disponibles = [c for c in disponibles if c["deporte"] == deporte]
    return disponibles


def inscribir_usuario_a_clase(usuario, clase_id):
    for clase in clases:
        if clase["id"] == clase_id:
            if usuario in clase["inscritos"]:
                return False, "Ya estás inscrito en esta clase."
            if len(clase["inscritos"]) >= clase["aforo"]:
                clase["estado"] = "lleno"
                return False, "La clase ya está llena."
            clase["inscritos"].append(usuario)
            if len(clase["inscritos"]) == clase["aforo"]:
                clase["estado"] = "lleno"
            return True, "Te has inscrito correctamente."
    return False, "Clase no encontrada."


def obtener_reservas_de_usuario(usuario):
    return [c for c in clases if usuario in c["inscritos"]]


def cancelar_reserva(usuario, clase_id):
    for clase in clases:
        if clase["id"] == clase_id:
            if usuario in clase["inscritos"]:
                clase["inscritos"].remove(usuario)
                if clase["estado"] == "lleno":
                    clase["estado"] = "disponible"
                return True, "Reserva cancelada."
            else:
                return False, "No estabas inscrito en esta clase."
    return False, "Clase no encontrada."


def eliminar_clase(clase_id):
    global clases
    clases = [c for c in clases if c["id"] != clase_id]


def obtener_clases_de_coach(coach):
    return [c for c in clases if c["coach"] == coach]


def eliminar_usuario_de_clase(coach, clase_id, usuario):
    for clase in clases:
        if clase["id"] == clase_id and clase["coach"] == coach:
            if usuario in clase["inscritos"]:
                clase["inscritos"].remove(usuario)
                if clase["estado"] == "lleno":
                    clase["estado"] = "disponible"
                return True, "Usuario eliminado de la clase."
    return False, "No autorizado o datos incorrectos."

