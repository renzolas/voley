import streamlit as st
from controllers.auth import login, register
from pages import admin, usuario

# Configuración básica
st.set_page_config(page_title="Reservas Deportivas", page_icon="🏐", layout="centered")

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username" not in st.session_state:
    st.session_state.username = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.experimental_rerun()

def main():
    st.title("App de Reservas Deportivas 🏐⚽🏋️‍♂️")

    if not st.session_state.logged_in:
        opcion = st.radio("¿Qué deseas hacer?", ["Login", "Registrarse"], horizontal=True)
        if opcion == "Login":
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.button("Ingresar"):
                success, result = login(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_role = result
                    st.session_state.username = username
                    st.success(f"Bienvenido {username} ({result})")
                    st.experimental_rerun()
                else:
                    st.error(result)
        else:
            username = st.text_input("Nuevo usuario")
            password = st.text_input("Nueva contraseña", type="password")
            confirm = st.text_input("Confirmar contraseña", type="password")
            rol = st.selectbox("Perfil", ["user", "admin"])
            if st.button("Crear cuenta"):
                if password != confirm:
                    st.error("Las contraseñas no coinciden")
                else:
                    success, msg = register(username, password, rol)
                    if success:
                        st.success(msg)
                        st.experimental_rerun()
                    else:
                        st.error(msg)
    else:
        st.sidebar.write(f"Usuario: {st.session_state.username} ({st.session_state.user_role})")
        if st.sidebar.button("Cerrar sesión"):
            logout()

        if st.session_state.user_role == "admin":
            admin.interfaz_admin()
        else:
            usuario.interfaz_usuario()

if __name__ == "__main__":
    main()
