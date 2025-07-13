# coach.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

def coach_view():
    st.header("👨‍🏫 Panel del Entrenador")

    st.subheader("📌 Crear nueva clase")
    title = st.text_input("Título de la clase (ej: Voley Avanzado)")
    sport = st.selectbox("Deporte", ["voley", "futbol", "gym"])
    date = st.date_input("Fecha de la clase", min_value=datetime.today())
    hour = st.selectbox("Horario disponible", [
        "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00",
        "11:00 - 12:00", "13:00 - 14:00", "14:00 - 15:00",
        "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
    ])
    capacity = st.number_input("Máximo de alumnos", min_value=1, max_value=50, step=1)
    periodic = st.checkbox("¿Clase periódica? (mismo horario en los próximos 3 días)")

    if st.button("Agregar clase"):
        coach = st.session_state["logged_user"]["username"]
        base_class = {
            "coach": coach,
            "sport": sport,
            "title": title,
            "hour": hour,
            "capacity": capacity,
            "enrolled": 0,
            "periodic": periodic,
        }

        if periodic:
            for i in range(3):  # Crea clases para hoy y 2 días más
                new_class = base_class.copy()
                new_class["date"] = (date + timedelta(days=i)).strftime("%Y-%m-%d")
                new_class["id"] = str(uuid.uuid4())
                st.session_state["classes"].append(new_class)
        else:
            base_class["date"] = date.strftime("%Y-%m-%d")
            base_class["id"] = str(uuid.uuid4())
            st.session_state["classes"].append(base_class)

        st.success("Clase(s) creada(s) correctamente.")
        st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]

    st.divider()
    st.subheader("📋 Tus clases")

    coach = st.session_state["logged_user"]["username"]
    my_classes = [c for c in st.session_state["classes"] if c["coach"] == coach]

    if not my_classes:
        st.info("Aún no has creado clases.")
    else:
        for c in sorted(my_classes, key=lambda x: x["date"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **{c['title']}**  
                🏷️ {c['sport'].capitalize()}  
                📅 {c['date']} — 🕐 {c['hour']}  
                👥 {c['enrolled']} / {c['capacity']}
                """)
            with col2:
                lleno = c["enrolled"] >= c["capacity"]
                estado = "🔴 Lleno" if lleno else "🟢 Disponible"
                st.markdown(f"**Estado:** {estado}")

                if st.button(f"Eliminar", key=f"eliminar_{c['id']}"):
                    st.session_state["classes"].remove(c)
                    st.session_state["reservations"] = [
                        r for r in st.session_state["reservations"] if r["class_id"] != c["id"]
                    ]
                    st.success("Clase eliminada.")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return  # cortar ejecución tras eliminar
