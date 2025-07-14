# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# Inicializar estructuras en RAM
if "users" not in st.session_state:
    st.session_state["users"] = []  # [{username, password, role}]
if "classes" not in st.session_state:
    st.session_state["classes"] = []  # [{id, coach, sport, title, date, hour, capacity, enrolled}]
if "reservations" not in st.session_state:
    st.session_state["reservations"] = []  # [{username, class_id}]
if "logged_user" not in st.session_state:
    st.session_state["logged_user"] = None

st.set_page_config(page_title="VolleyFit App", page_icon="🏐", layout="wide")

st.title("🏐 VolleyFit App - Reservas deportivas")

if st.session_state["logged_user"] is None:
    choice = st.sidebar.selectbox("Selecciona una opción", ["Iniciar sesión", "Registrarse"])
    if choice == "Iniciar sesión":
        login_view()
    else:
        register_view()
else:
    user = st.session_state["logged_user"]
    st.sidebar.success(f"Conectado como: {user['username']} ({user['role']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_user"] = None
        st.rerun()

    # Navegación con pestañas para Coach y Usuario
    if user["role"] == "coach":
        tabs = st.tabs(["Crear Clase", "Mis Clases", "KPIs"])
        with tabs[0]:
            coach_view(tab="create")
        with tabs[1]:
            coach_view(tab="list")
        with tabs[2]:
            coach_view(tab="kpis")

    elif user["role"] == "user":
        tabs = st.tabs(["Clases Disponibles", "Mis Reservas", "Perfil"])
        with tabs[0]:
            user_view(tab="browse")
        with tabs[1]:
            user_view(tab="my_reservations")
        with tabs[2]:
            user_view(tab="profile")


