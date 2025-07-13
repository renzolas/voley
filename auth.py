# auth.py
import streamlit as st

def register_view():
    st.subheader("Crear cuenta")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    role = st.selectbox("Tipo de cuenta", ["user", "coach"])

    if st.button("Registrarse"):
        if any(u["username"] == username for u in st.session_state["users"]):
            st.error("El nombre de usuario ya existe.")
        elif username and password:
            st.session_state["users"].append({
                "username": username,
                "password": password,
                "role": role
            })
            st.success("¡Cuenta creada! Ahora inicia sesión.")
        else:
            st.warning("Completa todos los campos.")

def login_view():
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        user = next(
            (u for u in st.session_state["users"]
             if u["username"] == username and u["password"] == password),
            None
        )
        # Cuando se hace login exitoso
        if user:
            st.session_state["logged_user"] = user
            st.session_state["rerun_requested"] = True  # MARCAR rerun (ya no lo ejecutamos aquí)

        else:
            st.error("Usuario o contraseña incorrectos.")


