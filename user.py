# user.py
import streamlit as st
from datetime import datetime, timedelta

def user_view():
    st.header("🎯 Panel del Usuario")

    # Paso 1: Elegir deporte
    st.subheader("1️⃣ Selecciona un deporte")
    deporte = st.selectbox("Deporte", ["voley", "futbol", "gym"])

    # Paso 2: Mostrar coaches con clases disponibles de ese deporte
    clases_disponibles = [
        c for c in st.session_state["classes"]
        if c["sport"] == deporte and c["enrolled"] < c["capacity"]
    ]
    coaches = list({c["coach"] for c in clases_disponibles})

    if not coaches:
        st.info("No hay coaches disponibles para este deporte.")
        return

    st.subheader("2️⃣ Elige un coach")
    coach = st.selectbox("Coach disponible", coaches)

    # Paso 3: Mostrar clases del coach seleccionado
    clases_coach = [
        c for c in clases_disponibles if c["coach"] == coach
    ]

    if not clases_coach:
        st.info("Este coach no tiene clases activas disponibles.")
        return

    st.subheader(f"3️⃣ Clases disponibles de {coach.capitalize()}")

    usuario = st.session_state["logged_user"]["username"]
    for c in sorted(clases_coach, key=lambda x: x["date"]):
        reservado = any(r["username"] == usuario and r["class_id"] == c["id"]
                        for r in st.session_state["reservations"])
        lleno = c["enrolled"] >= c["capacity"]
        estado = "🔴 Lleno" if lleno else "🟢 Disponible"

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            **{c['title']}**  
            📅 {c['date']} — 🕐 {c['hour']}  
            👥 {c['enrolled']} / {c['capacity']}  
            **Estado:** {estado}
            """)
        with col2:
            if reservado:
                st.info("Ya estás inscrito.")
            elif not lleno:
                if st.button("Reservar", key=f"reservar_{c['id']}"):
                    st.session_state["reservations"].append({
                        "username": usuario,
                        "class_id": c["id"]
                    })
                    c["enrolled"] += 1
                    st.success("¡Reserva confirmada!")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return

    st.divider()

    # Paso 4: Mostrar mis reservas
    st.subheader("📌 Tus reservas")
    mis_reservas = [
        r for r in st.session_state["reservations"] if r["username"] == usuario
    ]
    if not mis_reservas:
        st.info("Aún no tienes reservas activas.")
        return

    for r in mis_reservas:
        clase = next((c for c in st.session_state["classes"] if c["id"] == r["class_id"]), None)
        if clase:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **{clase['title']}**  
                📅 {clase['date']} — 🕐 {clase['hour']}  
                👥 {clase['enrolled']} / {clase['capacity']}
                """)
            with col2:
                if st.button("Cancelar", key=f"cancelar_{r['class_id']}"):
                    st.session_state["reservations"].remove(r)
                    clase["enrolled"] -= 1
                    st.success("Reserva cancelada.")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return

    # Paso 5: Ver calendario de próximas clases
    st.divider()
    st.subheader("📅 Calendario de próximos 4 días")
    dias = [datetime.today() + timedelta(days=i) for i in range(4)]
    for dia in dias:
        dia_str = dia.strftime("%Y-%m-%d")
        clases_dia = [
            c for c in st.session_state["classes"]
            if c["coach"] == coach and c["date"] == dia_str
        ]
        if clases_dia:
            st.markdown(f"### {dia.strftime('%A %d/%m')}")
            for c in clases_dia:
                lleno = c["enrolled"] >= c["capacity"]
                estado = "🔴 Lleno" if lleno else "🟢 Disponible"
                st.markdown(f"- {c['title']} — 🕐 {c['hour']} ({estado})")

