# user.py
import streamlit as st
from datetime import datetime, timedelta

def user_view():
    st.header("👟 Reservas deportivas")

    deportes = {
        "voley": "🏐",
        "futbol": "⚽",
        "gym": "🏋️"
    }

    st.markdown("### 📌 Selecciona un deporte")
    deporte = st.selectbox("Elige tu deporte favorito", list(deportes.keys()))

    st.markdown("### 📅 Ver clases disponibles por día")
    selected_day = st.date_input("Selecciona una fecha", min_value=datetime.today())

    clases_disponibles = [
        c for c in st.session_state["classes"]
        if c["sport"] == deporte and c["date"] == selected_day.strftime("%Y-%m-%d")
    ]

    if not clases_disponibles:
        st.info("No hay clases disponibles para este día.")
    else:
        st.markdown("### 📋 Clases disponibles")
        for clase in clases_disponibles:
            coach = clase["coach"]
            icono = deportes[clase["sport"]]
            estado = "🟢 Disponible" if clase["enrolled"] < clase["capacity"] else "🔴 Lleno"

            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                **{icono} {clase['title']}**  
                📅 {clase['date']} — 🕒 {clase['hour']}  
                🧑‍🏫 Coach: `{coach}`  
                👥 {clase['enrolled']} / {clase['capacity']}  
                **Estado:** {estado}
                """)
            with col2:
                if clase["enrolled"] < clase["capacity"]:
                    if st.button("Reservar", key=f"reservar_{clase['id']}"):
                        ya_reservado = any(
                            r for r in st.session_state["reservations"]
                            if r["username"] == st.session_state["logged_user"]["username"] and r["class_id"] == clase["id"]
                        )
                        if ya_reservado:
                            st.warning("Ya estás registrado en esta clase.")
                        else:
                            st.session_state["reservations"].append({
                                "username": st.session_state["logged_user"]["username"],
                                "class_id": clase["id"]
                            })
                            clase["enrolled"] += 1
                            st.success("✅ Clase reservada exitosamente.")
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📦 Tus reservas")

    mis_reservas = [
        r for r in st.session_state["reservations"]
        if r["username"] == st.session_state["logged_user"]["username"]
    ]
    clases_dict = {c["id"]: c for c in st.session_state["classes"]}

    if not mis_reservas:
        st.info("No tienes reservas activas.")
    else:
        for reserva in mis_reservas:
            clase = clases_dict.get(reserva["class_id"])
            if not clase:
                continue

            icono = deportes.get(clase["sport"], "📚")
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                **{icono} {clase['title']}**  
                📅 {clase['date']} — 🕒 {clase['hour']}  
                🧑‍🏫 Coach: `{clase['coach']}`  
                👥 {clase['enrolled']} / {clase['capacity']}
                """)
            with col2:
                if st.button("Cancelar", key=f"cancelar_{clase['id']}"):
                    st.session_state["reservations"] = [
                        r for r in st.session_state["reservations"]
                        if not (r["username"] == st.session_state["logged_user"]["username"] and r["class_id"] == clase["id"])
                    ]
                    clase["enrolled"] -= 1
                    st.success("❌ Reserva cancelada.")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


