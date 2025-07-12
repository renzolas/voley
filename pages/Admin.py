# pages/1_Admin.py

import streamlit as st
import datetime
from data.db_simulada import crear_clase, obtener_clases_de_coach, eliminar_clase, eliminar_usuario_de_clase

# Solo mostrar si es admin
if st.session_state.get("user_role") != "admin":
    st.warning("Acceso solo para entrenadores.")
    st.stop()

st.title("Panel del Entrenador 🏋️‍♂️")

st.header("Crear nueva clase")
nombre_clase = st.text_input("Nombre de la clase (Ej: Clase de Vóley)")
deporte = st.selectbox("Deporte", ["voley", "futbol", "gym"])
fecha = st.date_input("Selecciona una fecha", min_value=datetime.date.today())
horario = st.selectbox("Horario disponible", ["13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00"])
aforo = st.number_input("Cantidad máxima de alumnos", min_value=1, max_value=20, step=1)

if st.button("Agregar clase"):
    if not nombre_clase:
        st.error("Debes poner un nombre a la clase.")
    else:
        crear_clase(
            coach=st.session_state.get("username", "admin"),
            deporte=deporte,
            nombre_clase=nombre_clase,
            fecha=str(fecha),
            horario=horario,
            aforo=aforo
        )
        st.success("Clase creada exitosamente ✅")

st.divider()
st.subheader("Tus clases creadas")

clases = obtener_clases_de_coach(st.session_state.get("username", "admin"))

if not clases:
    st.info("No has creado clases aún.")
else:
    for clase in clases:
        st.markdown(f"### {clase['nombre_clase']} ({clase['deporte'].capitalize()})")
        st.write(f"🗓️ Fecha: {clase['fecha']} | ⏰ Horario: {clase['horario']}")
        st.write(f"👥 Aforo: {len(clase['inscritos'])}/{clase['aforo']}")

        estado_color = "🟢 Disponible" if clase["estado"] == "disponible" else "🔴 Llena"
        st.write(f"Estado: {estado_color}")

        if clase["inscritos"]:
            st.markdown("**Alumnos inscritos:**")
            for alumno in clase["inscritos"]:
                col1, col2 = st.columns([4, 1])
                col1.write(f"👤 {alumno}")
                if col2.button("Eliminar", key=f"del-{clase['id']}-{alumno}"):
                    ok, msg = eliminar_usuario_de_clase(clase['coach'], clase['id'], alumno)
                    if ok:
                        st.success(f"{alumno} eliminado de la clase")
                    else:
                        st.error(msg)
        else:
            st.info("No hay alumnos inscritos.")

        # Botón para eliminar la clase
        if st.button("❌ Eliminar esta clase", key=f"delete-{clase['id']}"):
            eliminar_clase(clase["id"])
            st.warning("Clase eliminada.")
        st.divider()

# KPIs (muy básicos por ahora)
st.header("📊 KPIs")
total_clases = len(clases)
total_inscritos = sum([len(c["inscritos"]) for c in clases])
alumnos_frecuentes = {}

for clase in clases:
    for alumno in clase["inscritos"]:
        alumnos_frecuentes[alumno] = alumnos_frecuentes.get(alumno, 0) + 1

st.write(f"🔢 Total de clases creadas: {total_clases}")
st.write(f"👥 Total de alumnos inscritos: {total_inscritos}")

if alumnos_frecuentes:
    top = sorted(alumnos_frecuentes.items(), key=lambda x: x[1], reverse=True)
    st.write("🏅 Alumnos más frecuentes:")
    for alumno, count in top:
        st.write(f"- {alumno} (inscrito en {count} clases)")

