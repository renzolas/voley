import streamlit as st
from controllers.auth import registrar_usuario, validar_login

st.set_page_config(page_title="Reservas Deportivas", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Login'
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        success, result = validar_login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_role = result
            st.session_state.username = username
            st.success(f"Bienvenido, {username} ({result})")
            st.rerun()
        else:
            st.error(result)

def register():
    st.subheader("Registrarse")
    username = st.text_input("Nuevo usuario")
    password = st.text_input("Nueva contraseña", type="password")
    confirm = st.text_input("Confirmar contraseña", type="password")
    rol = st.selectbox("Selecciona tu perfil", ["user", "admin"], index=0)

    if st.button("Crear cuenta"):
        if password != confirm:
            st.error("Las contraseñas no coinciden")
        else:
            success, msg = registrar_usuario(username, password, rol)
            if success:
                st.success(msg)
                st.session_state.auth_mode = 'Login'
            else:
                st.error(msg)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()

def main():
    st.title("App de Reservas Deportivas 🏐⚽🏋️‍♂️")

    if not st.session_state.logged_in:
        auth_option = st.radio("Selecciona una opción:", ["Login", "Registrarse"], horizontal=True)
        st.session_state.auth_mode = auth_option

        if st.session_state.auth_mode == 'Login':
            login()
        else:
            register()
    else:
        st.button("Cerrar Sesión", on_click=logout)

        if st.session_state.user_role == "admin":
            st.success("Has ingresado como entrenador. Ve al menú lateral izquierdo y selecciona tu panel.")
        elif st.session_state.user_role == "user":
            st.success("Has ingresado como alumno. Ve al menú lateral izquierdo para ver tus reservas.")

if __name__ == "__main__":
    main()

