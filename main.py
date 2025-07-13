# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# Estilo base
st.set_page_config(page_title="VolleyFit", layout="centered")
st.markdown("""
<style>
    h1 {color: #2E86C1;}
    .verde {color: green;}
    .rojo {color: red;}
    .stButton>button {border-radius: 8px; padding: 8px 20px;}
</style>
""", unsafe_allow_html=True)

# 🧠 Estado en RAM (se crea si no existe)
defaults = {
    "users": [],
    "classes": [],
    "reservations": [],
    "notifications": {},
    "logged_user": None,
    "dummy_refresh": False
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val
        st.rerun()  # ← ⚠️ rerun() para reiniciar flujo con estado seguro

# Título de app
st.title("🏐 VolleyFit")

# 🔐 Login o Registro
if st.session_state["logged_user"] is None:
    choice = st.sidebar.radio("Acceso", ["Iniciar sesión", "Registrarse"])
    if choice == "Iniciar sesión":
        login_view()
    else:
        register_view()
else:
    user = st.session_state["logged_user"]
    st.sidebar.success(f"{user['username']} ({user['role']})")
    
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_user"] = None
        st.experimental_rerun()

    if user["role"] == "coach":
        coach_view()
    else:
        user_view()


