# coach.py
import streamlit as st
from utils import get_available_hours, get_status_badge
import uuid

def coach_view():
    st.subheader("📅 Crear nueva clase")
    sports = ["Voley", "Fútbol", "Gimnasio"]
    title = st.text_input("Nombre de la clase")
    sport = st.selectbox("Deporte", sports)
    date = st.date_input("Fecha de la clase")
    hour = st.selectbox("Horario", get_available_hours())
    capacity = st.number_input("Capacidad máxima (aforo)", min_value=1, max_value=20, value=5)

    if st.button("Agregar clase"):
        new_class = {
            "id": str(uuid.uuid4()),
            "coach": st.session_state["logged_user"]["username"],
            "sport": sport,
            "title": title,
            "date": str(date),
            "hour": hour,
            "capacity": capacity,
            "enrolled": []
        }
        st.session_state["classes"].append(new_class)
        st.success("Clase agregada.")

    st.subheader("🧾 Clases creadas")
    my_classes = [c for c in st.session_state["classes"] if c["coach"] == st.session_state["logged_user"]["username"]]

    for c in my_classes:
        badge = get_status_badge(len(c["enrolled"]), c["capacity"])
        st.markdown(f"**{c['title']}** ({c['sport']}) - {c['date']} {c['hour']} {badge}")
        st.text(f"Inscritos: {len(c['enrolled'])}/{c['capacity']}")

        if st.button(f"Eliminar clase {c['id']}", key=c['id']):
            # Avisar a usuarios (simplemente eliminar reservas relacionadas)
            st.session_state["reservations"] = [r for r in st.session_state["reservations"] if r["class_id"] != c["id"]]
            st.session_state["classes"].remove(c)
            st.success("Clase eliminada.")
            st.experimental_rerun()


