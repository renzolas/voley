import streamlit as st
from controllers.auth import registrar_usuario, validar_login

# Configuración de la app
st.set_page_config(page_title="Reservas Deportivas", page_icon="⚽", layout="centered")

# Oculta la navegación lateral automática de otras páginas
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Estado inicial
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Login'
if 'username' not in st.session_state:
    st.session_state.username = None

# Función de login
def login():
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        success, result = validar_login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_role = result  # 'admin' o 'user'
            st.session_state.username = username  # ✅ Guarda el nombre de usuario
            st.success(f"Bienvenido, {username} ({result})")
        else:
            st.error(result)

# Función de registro
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

# Cerrar sesión
def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.success("Sesión cerrada correctamente")

# Función principal
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
        st.sidebar.button("Cerrar Sesión", on_click=logout)

        if st.session_state.user_role == "admin":
            st.success("Has ingresado como Entrenador")
            st.write("Ve al menú lateral izquierdo → selecciona: `1_Admin`")
        elif st.session_state.user_role == "user":
            st.success("Has ingresado como Usuario")
            st.write("Ve al menú lateral izquierdo → selecciona: `2_Usuario`")

if __name__ == "__main__":
    main()



