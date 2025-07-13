# auth.py
import streamlit as st

def login_view():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔐 Iniciar sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        for user in st.session_state["users"]:
            if user["username"] == username and user["password"] == password:
                st.session_state["logged_user"] = user
                st.success(f"Bienvenido {username} 👋")
                st.experimental_rerun()
                return
        st.error("Usuario o contraseña incorrectos.")

    st.markdown("</div>", unsafe_allow_html=True)


def register_view():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Registro de nuevo usuario")

    username = st.text_input("Elige un nombre de usuario")
    password = st.text_input("Crea una contraseña", type="password")
    role = st.selectbox("Tipo de cuenta", ["user", "coach"])

    if st.button("Registrarse"):
        if not username or not password:
            st.error("Todos los campos son obligatorios.")
            return

        if any(u["username"] == username for u in st.session_state["users"]):
            st.error("Ese nombre de usuario ya está en uso.")
            return

        new_user = {
            "username": username,
            "password": password,
            "role": role
        }
        st.session_state["users"].append(new_user)
        st.session_state["logged_user"] = new_user
        st.success(f"Cuenta creada con éxito, {username} 👏")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


