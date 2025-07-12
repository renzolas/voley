import streamlit as st
import datetime
from data.db_simulada import (
    crear_clase,
    obtener_clases_de_coach,
    eliminar_clase,
    eliminar_usuario_de_clase
)

def interfaz_admin():
    st.header(f"Panel de Entrenador - {st.session_state.username} 🏋️‍♂️")

    st.subheader("Crear nueva clase")
    nombre_clase = st.text_input("Nombre de la clase")
    deporte = st.selectbox("Deporte", ["voley", "futbol", "gym"])
    fecha = st.date_input("Fecha", min_value=datetime.date.today())
    horario = st.selectbox("Horario", ["13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00"])
    aforo = st.number_input("Máximo de alumnos", min_value=1, max_value=20, step=1)

    # ✅ Nueva opción de periodicidad
    periodicidad = st.selectbox(
        "¿Repetir esta clase semanalmente?",
        [
            "No",
            "Repetir por 1 semana",
            "Repetir por 2 semanas",
            "Repetir por 3 semanas",
            "Repetir por todo el mes"
        ]
    )

    # Mapear texto a número de repeticiones
    mapa_periodos = {
        "No": 1,
        "Repetir por 1 semana": 2,
        "Repetir por 2 semanas": 3,
        "Repetir por 3 semanas": 4,
        "Repetir por todo el mes": 5
    }
    semanas = mapa_periodos[periodicidad]

    if st.button("Agregar clase"):
        if not nombre_clase:
            st.error("Debes ingresar el nombre de la clase.")
        else:
            for i in range(semanas):
                nueva_fecha = fecha + datetime.timedelta(weeks=i)
                crear_clase(
                    coach=st.session_state.username,
                    deporte=deporte,
                    nombre_clase=nombre_clase,
                    fecha=str(nueva_fecha),
                    horario=horario,
                    aforo=aforo
                )
            if semanas > 1:
                st.success(f"Clase creada y repetida por {semanas - 1} semanas ✅")
            else:
                st.success("Clase creada ✅")

    st.divider()
    st.subheader("Tus clases creadas")

    clases = obtener_clases_de_coach(st.session_state.username)
    if not clases:
        st.info("No has creado clases aún.")
    else:
        for clase in clases:
            st.markdown(f"### {clase['nombre_clase']} ({clase['deporte'].capitalize()})")
            st.write(f"📅 Fecha: {clase['fecha']} | 🕒 Horario: {clase['horario']}")
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
                            st.success(f"{alumno} eliminado de la clase.")
                        else:
                            st.error(msg)
            else:
                st.info("No hay alumnos inscritos.")

            if st.button("❌ Eliminar esta clase", key=f"delete-{clase['id']}"):
                eliminar_clase(clase["id"])
                st.warning("Clase eliminada.")

            st.divider()

# 🚀 Ejecución automática si el usuario es admin
if __name__ == "__main__" or st.session_state.get("user_role") == "admin":
    if st.session_state.get("logged_in", False):
        interfaz_admin()
    else:
        st.warning("Inicia sesión como entrenador para acceder a esta vista.")


