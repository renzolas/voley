# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# Inicializar estructuras en memoria RAM
if "users" not in st.session_state:
    st.session_state["users"] = []  # [{username, password, role}]
if "classes" not in st.session_state:
    st.session_state["classes"] = []  # [{id, coach, sport, title, date, hour, capacity, enrolled}]
if "reservations" not in st.session_state:
    st.session_state["reservations"] = []  # [{username, class_id}]
if "notifications" not in st.session_state:
    st.session_state["notifications"] = {}  # {username: [mensajes]}
if "logged_user" not in st.session_state:
    st.session_state["logged_user"] = None
if "dummy_refresh" not in st.session_state:
    st.session_state["dummy_refresh"] = False  # Forzar refresco controlado

# Título
st.title("🏐 VolleyFit App - Reservas deportivas")

# Autenticación
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

    if user["role"] == "coach":
        coach_view()
    elif user["role"] == "user":
        user_view()


