# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# Configuración de página
st.set_page_config(page_title="VolleyFit App", layout="centered")

# 💅 Estilo visual CSS embebido
st.markdown("""
    <style>
    .stApp {
        background-color: #f6f6f9;
        font-family: "Segoe UI", sans-serif;
    }

    h1, h2, h3 {
        color: #2c3e50;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div.stButton > button {
        background-color: #1abc9c;
        color: white;
        padding: 0.6em 1.5em;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        font-size: 1rem;
    }

    div.stButton > button:hover {
        background-color: #16a085;
        transition: 0.3s;
    }

    input, select, textarea {
        border-radius: 6px !important;
    }

    .card {
        background-color: white;
        padding: 16px;
        margin-bottom: 10px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .kpi {
        background: #ffffff;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        font-weight: bold;
    }

    details summary {
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 🔁 Inicializar estados de sesión
if "users" not in st.session_state:
    st.session_state["users"] = []

if "classes" not in st.session_state:
    st.session_state["classes"] = []

if "reservations" not in st.session_state:
    st.session_state["reservations"] = []

if "logged_user" not in st.session_state:
    st.session_state["logged_user"] = None

if "notifications" not in st.session_state:
    st.session_state["notifications"] = {}  # username: [msg1, msg2]

# 🚀 Interfaz principal
st.title("🏐 VolleyFit App — Reservas deportivas")

if st.session_state["logged_user"] is None:
    with st.sidebar:
        st.markdown("## Bienvenido 👋")
        nav = st.radio("Menú principal", ["Iniciar sesión", "Registrarse"], index=0)

    if nav == "Iniciar sesión":
        login_view()
    else:
        register_view()
else:
    user = st.session_state["logged_user"]

    with st.sidebar:
        st.markdown(f"👤 **{user['username']}** ({user['role']})")
        nav = st.radio("🏠 Navegación", ["Inicio", "Cerrar sesión"], index=0)

    if nav == "Cerrar sesión":
        st.session_state["logged_user"] = None
        st.rerun()
    else:
        # 🔔 Mostrar notificaciones si hay
        notif = st.session_state["notifications"].get(user["username"], [])
        if notif:
            with st.expander("🔔 Notificaciones importantes", expanded=True):
                for msg in notif:
                    st.warning(msg)
            st.session_state["notifications"][user["username"]] = []

        # Entrar al panel correspondiente
        if user["role"] == "coach":
            coach_view()
        elif user["role"] == "user":
            user_view()


