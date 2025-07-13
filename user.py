# user.py
import streamlit as st
from datetime import datetime

def user_view():
    st.header("🙋 Panel del Usuario")
    username = st.session_state["logged_user"]["username"]

    # Mostrar notificaciones
    notis = st.session_state.get("notifications", {}).get(username, [])
    if notis:
        st.warning("🔔 Tienes notificaciones importantes:")
        for n in notis:
            st.markdown(f"- {n}")
        if st.button("Marcar como leídas"):
            st.session_state["notifications"][username] = []

    deporte = st.selectbox("Selecciona el deporte", ["voley", "futbol", "gym"])
    fecha_seleccionada = st.date_input("📅 Ver clases del día", min_value=datetime.today())

    clases_disponibles = [
        c for c in st.session_state["classes"]
        if c["sport"] == deporte and c["date"] == fecha_seleccionada.strftime("%Y-%m-%d")
    ]

    st.subheader("📆 Clases disponibles")
    if not clases_disponibles:
        st.info("No hay clases disponibles para esta fecha.")
        return

    for c in clases_disponibles:
        lleno = c["enrolled"] >= c["capacity"]
        estado = "🔴 Lleno" if lleno else "🟢 Disponible"

        st.markdown(f"""
        ### {c['title']}
        🏷️ {c['sport'].capitalize()}  
        📅 {c['date']} — 🕐 {c['hour']}  
        👥 {c['enrolled']} / {c['capacity']} — **{estado}**
        """)

        if not lleno:
            if st.button("Reservar", key=f"res_{c['id']}"):
                ya_reservado = any(
                    r for r in st.session_state["reservations"]
                    if r["username"] == username and r["class_id"] == c["id"]
                )
                if not ya_reservado:
                    st.session_state["reservations"].append({
                        "username": username,
                        "class_id": c["id"]
                    })
                    c["enrolled"] += 1
                    st.success("Reserva confirmada.")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return
                else:
                    st.warning("Ya estás inscrito en esta clase.")

    st.divider()
    st.subheader("📒 Mis reservas")

    reservas_usuario = [
        r for r in st.session_state["reservations"]
        if r["username"] == username
    ]
    clases_reservadas = [
        c for c in st.session_state["classes"] if any(r["class_id"] == c["id"] for r in reservas_usuario)
    ]

    if not clases_reservadas:
        st.info("No tienes clases reservadas.")
    else:
        for c in clases_reservadas:
            st.markdown(f"""
            **{c['title']}**  
            📅 {c['date']} — 🕐 {c['hour']}  
            👥 {c['enrolled']} / {c['capacity']}
            """)
            if st.button("Cancelar reserva", key=f"cancel_{c['id']}"):
                st.session_state["reservations"] = [
                    r for r in st.session_state["reservations"]
                    if not (r["username"] == username and r["class_id"] == c["id"])
                ]
                c["enrolled"] -= 1
                st.success("Reserva cancelada.")
                st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                return

