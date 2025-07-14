# user.py
import streamlit as st
from datetime import datetime

def local_css():
    st.markdown("""
    <style>
    .card {
        background: #fefefe;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.9rem;
        transition: box-shadow 0.25s ease;
    }
    .card:hover {
        box-shadow: 0 6px 15px rgb(0 0 0 / 0.2);
    }
    .icon {
        font-size: 2.4rem;
        margin-right: 12px;
        user-select: none;
    }
    .info {
        flex-grow: 1;
        padding-right: 15px;
    }
    .buttons {
        display: flex;
        gap: 8px;
    }
    .status-available {
        color: green;
        font-weight: bold;
    }
    .status-full {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_icon(sport):
    icons = {
        "voley": "🏐",
        "futbol": "⚽",
        "gym": "🏋️"
    }
    return icons.get(sport, "❓")

def user_view(tab="browse"):
    local_css()

    if tab == "browse":
        st.header("🏐 Clases disponibles")

        # Filtro: deporte
        deporte_filter = st.selectbox("Filtrar por deporte", ["Todos", "voley", "futbol", "gym"])

        # Filtro: fechas próximas 7 días
        hoy = datetime.today()
        fecha_limite = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
        clases_filtradas = [
            c for c in st.session_state["classes"]
            if (deporte_filter == "Todos" or c["sport"] == deporte_filter)
            and datetime.strptime(c["date"], "%Y-%m-%d") >= fecha_limite
        ]

        if not clases_filtradas:
            st.info("No hay clases disponibles con esos filtros.")
            return

        for c in sorted(clases_filtradas, key=lambda x: (x["date"], x["hour"])):
            icono = get_icon(c["sport"])
            lleno = c["enrolled"] >= c["capacity"]
            estado_texto = "Disponible" if not lleno else "Lleno"
            estado_clase = "status-available" if not lleno else "status-full"

            st.markdown(f"""
            <div class='card'>
                <div class='icon'>{icono}</div>
                <div class='info'>
                    <b>{c['title']}</b><br>
                    🏷️ {c['sport'].capitalize()}<br>
                    📅 {c['date']} — 🕐 {c['hour']}<br>
                    👥 {c['enrolled']} / {c['capacity']} — <span class='{estado_clase}'>{estado_texto}</span>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with col2:
                if st.button("Reservar", key=f"reservar_{c['id']}") and not lleno:
                    # Registrar reserva
                    user = st.session_state["logged_user"]["username"]
                    st.session_state["reservations"].append({
                        "username": user,
                        "class_id": c["id"]
                    })
                    # Aumentar inscritos
                    c["enrolled"] += 1
                    st.success("Reserva realizada con éxito!")
                    st.experimental_rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "my_reservations":
        st.header("📋 Mis reservas")
        user = st.session_state["logged_user"]["username"]
        mis_reservas = [r for r in st.session_state["reservations"] if r["username"] == user]

        if not mis_reservas:
            st.info("Aún no tienes reservas.")
            return

        for r in mis_reservas:
            clase = next((c for c in st.session_state["classes"] if c["id"] == r["class_id"]), None)
            if not clase:
                continue

            icono = get_icon(clase["sport"])

            st.markdown(f"""
            <div class='card'>
                <div class='icon'>{icono}</div>
                <div class='info'>
                    <b>{clase['title']}</b><br>
                    🏷️ {clase['sport'].capitalize()}<br>
                    📅 {clase['date']} — 🕐 {clase['hour']}
                </div>
            """ , unsafe_allow_html=True)

            col1, col2 = st.columns([1,1])
            with col2:
                if st.button("Cancelar Reserva", key=f"cancelar_{r['class_id']}"):
                    st.session_state["reservations"].remove(r)
                    clase["enrolled"] -= 1
                    st.success("Reserva cancelada.")
                    st.experimental_rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "profile":
        st.header("👤 Perfil de usuario")
        user = st.session_state["logged_user"]
        st.markdown(f"""
        - **Usuario:** {user['username']}
        - **Rol:** {user['role']}
        """)



