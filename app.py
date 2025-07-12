import streamlit as st

# Configuración de la app
st.set_page_config(page_title="Reservas Deportivas", page_icon="⚽", layout="centered")

# Oculta navegación automática de Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Estado de sesión inicial
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Login'

# Función para login
def login():
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        # Validación temporal para testeo
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.user_role = "admin"
            st.success("Bienvenido, Coach/Admin")
        elif username == "user" and password == "user123":
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.success("Bienvenido, Alumno")
        else:
            st.error("Credenciales inválidas")

# Función para registro
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
            # Aquí guardaríamos en base de datos (simulado)
            st.success("¡Cuenta creada con éxito! Por favor inicia sesión")
            st.session_state.auth_mode = 'Login'
        else:
            st.error(msg)

# Función para cerrar sesión
def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.success("Sesión cerrada correctamente")

# Contenido principal
def main():
    st.title("App de Reservas Deportivas 🏐⚽🏋️‍♂️")

    if not st.session_state.logged_in:
        # Selector entre Login y Registro
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
            st.write("Desde el menú lateral selecciona: `1_Admin` para gestionar tus clases.")
        elif st.session_state.user_role == "user":
            st.success("Has ingresado como Usuario")
            st.write("Desde el menú lateral selecciona: `2_Usuario` para ver y reservar clases.")

if __name__ == "__main__":
    main()


