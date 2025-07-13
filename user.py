# user.py
import streamlit as st
from datetime import datetime

def user_view():
    st.header("🙋 Panel del Usuario")

    username = st.session_state["logged_user"]["username"]

    # 🔔 Notificaciones
    if st.session_state["notifications"].get(username):
        with st.expander("📬 Tienes notificaciones"):
            for note in st.session_state["notifications"][username]:
                st.warning(note)
            if st.button("Marcar como leídas"):
                st.session_state["notifications"][username] = []
                st.experimental_rerun()

    st.divider()

    # 🎯 Filtros de búsqueda
    st.subheader("🎯 Buscar clases")
    col1, col2 = st.columns(2)
    with col1:
        selected_sport = st.selectbox("Selecciona un deporte", ["voley", "futbol", "gym"])
    with col2:
        selected_date = st.date_input("Selecciona una fecha", min_value=datetime.today())

    # 🎯 Filtrado de clases
    filtered_classes = [
        c for c in st.session_state["classes"]
        if c["sport"] == selected_sport and c["date"] == selected_date.strftime("%Y-%m-%d")
    ]

    st.markdown("### 📋 Clases disponibles")
    if not filtered_classes:
        st.info("No hay clases disponibles para este deporte y fecha.")
    else:
        for c in filtered_classes:
            lleno = c["enrolled"] >= c["capacity"]
            estado = "🔴 Lleno" if lleno else "🟢 Disponible"

            with st.container():
                st.markdown(f"""
                    <div style="background-color:#f0f0f5; padding:15px; border-radius:8px; margin-bottom:10px">
                        <strong>{c['title']}</strong> — {c['hour']}  
                        <br>📅 {c['date']} | 👥 {c['enrolled']} / {c['capacity']}  
                        <br>Estado: <span style='color:{"red" if lleno else "green"}'>{estado}</span>
                """, unsafe_allow_html=True)

                if not lleno:
                    btn_key = f"btn_reserve_{c['id']}"
                    if st.button("✅ Reservar esta clase", key=btn_key):
                        ya_reservado = any(r for r in st.session_state["reservations"]
                                           if r["username"] == username and r["class_id"] == c["id"])
                        if ya_reservado:
                            st.warning("Ya reservaste esta clase.")
                        else:
                            st.session_state["reservations"].append({
                                "username": username,
                                "class_id": c["id"]
                            })
                            c["enrolled"] += 1
                            st.success("¡Reservaste tu clase!")
                            st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📌 Mis Reservas")

    user_reservas = [
        r for r in st.session_state["reservations"]
        if r["username"] == username
    ]

    if not user_reservas:
        st.info("No tienes clases reservadas.")
    else:
        for r in user_reservas:
            clase = next((c for c in st.session_state["classes"] if c["id"] == r["class_id"]), None)
            if clase:
                with st.container():
                    st.markdown(f"""
                        <div style="background-color:#fff0f0; padding:12px; border-radius:8px; margin-bottom:10px">
                            <strong>{clase['title']}</strong> — {clase['sport'].capitalize()}  
                            <br>📅 {clase['date']} | 🕐 {clase['hour']}  
                            <br>👥 {clase['enrolled']} / {clase['capacity']}
                    """, unsafe_allow_html=True)

                    if st.button("❌ Cancelar reserva", key=f"cancel_{clase['id']}"):
                        st.session_state["reservations"] = [
                            rr for rr in st.session_state["reservations"] if rr != r
                        ]
                        clase["enrolled"] -= 1
                        st.success("Has cancelado tu reserva.")
                        st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

