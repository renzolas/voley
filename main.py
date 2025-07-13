# main.py
import streamlit as st
from auth import login_view, register_view
from coach import coach_view
from user import user_view

# Estilo CSS global
st.markdown("""
<style>
h1 {color: #2E86C1; font-size: 2.8rem;}
h2 {color: #117A65;}
.stButton>button {border-radius: 8px; padding: 8px 20px;}
.verde {color: green; font-weight: bold;}
.rojo {color: red; font-weight: bold;}
.card {background-color: #F9F9F9; border-radius: 8px; padding: 15px; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# Initialize RAM
for key in ["users","classes","reservations","notifications","dummy_refresh"]:
    if key not in st.session_state:
        st.session_state[key] = {} if key == "notifications" else [] if key != "dummy_refresh" else False
if st.session_state["logged_user"] is None:
    pass
else:
    if "logged_user" not in st.session_state:
        st.session_state["logged_user"] = None

# Title & Sidebar
st.title("🏐 VolleyFit")
st.sidebar.header("📌 Navegación")

if st.session_state["logged_user"] is None:
    choice = st.sidebar.radio("Acción", ["Iniciar sesión", "Registrarse"])
    if choice == "Iniciar sesión":
        login_view()
    else:
        register_view()
else:
    user = st.session_state["logged_user"]
    st.sidebar.success(f"{user['username']} ({user['role']})")
    if st.sidebar.button("🔴 Cerrar sesión"):
        st.session_state["logged_user"] = None
        st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]

    if user["role"] == "coach":
        coach_view()
    else:
        user_view()


