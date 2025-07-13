# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# --- Inicializar estructuras en RAM ---
if "users" not in st.session_state:
    st.session_state["users"] = []
if "classes" not in st.session_state:
    st.session_state["classes"] = []
if "reservations" not in st.session_state:
    st.session_state["reservations"] = []
if "logged_user" not in st.session_state:
    st.session_state["logged_user"] = None
if "rerun_requested" not in st.session_state:
    st.session_state["rerun_requested"] = False

# --- Manejo seguro de rerun al inicio del ciclo ---
def safe_rerun():
    if st.session_state.get("rerun_requested", False):
        st.session_state["rerun_requested"] = False
        st.experimental_rerun()

safe_rerun()  # Solo se llama si fue marcado previamente

# --- Interfaz principal ---
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
        st.session_state["rerun_requested"] = True  # usamos la nueva bandera
        safe_rerun()

    if user["role"] == "coach":
        coach_view()
    elif user["role"] == "user":
        user_view()

