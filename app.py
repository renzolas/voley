import streamlit as st
import datetime
from controllers.auth import registrar_usuario, validar_login
from data.db_simulada import (
    crear_clase,
    obtener_clases_de_coach,
    eliminar_clase,
    eliminar_usuario_de_clase
)

# Configuración de la app
st.set_page_config(page_title="Reservas Deportivas", page_icon="⚽", layout="centered")

# Ocultar menú lateral de navegación
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Estado inicial de sesión
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
            st.session_state.username = username
            st.success(f"Bienvenido, {username} ({result})")
            st.experimental_rerun()
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
    st.experimental_rerun()

# Función para interfaz admin (entrenador)
def interfaz_admin():
    st.header(f"Panel de Entrenador - {st.session_state.username} 🏋️‍♂️")

    st.subheader("Crear nueva clase")
    nombre_clase = st.text_input("Nombre de la clase")
    deporte = st.selectbox("Deporte", ["voley", "futbol", "gym"])
    fecha = st.date_input("Fecha", min_value=datetime.date.today())
    horario = st.selectbox("Horario", ["13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00"])
    aforo = st.number_input("Máximo de alumnos", min_value=1, max_value=20, step=1)

    if st.button("Agregar clase"):
        if not nombre_clase:
            st.error("Debes ingresar el nombre de la clase.")
        else:
            crear_clase(
                coach=st.session_state.username,
                deporte=deporte,
                nombre_clase=nombre_clase,
                fecha=str(fecha),
                horario=horario,
                aforo=aforo
            )
            st.success("Clase creada con éxito ✅")

    st.divider()
    st.subheader("Tus clases creadas")

    clases = obtener_clases_de_coach(st.session_state.username)
    if not clases:
        st.info("No has creado clases aún.")
    else:
        for clase in clases:
            st.markdown(f"### {clase['nombre_clase']} ({clase['deporte'].capitalize()})")
            st.write(f"📅 Fecha: {clase['fecha']} | 🕒 Horario: {clase['horario']}")
            st.write(f"👥 Aforo: {len(clase['inscritos'])}/{clase['aforo']}")

            estado_color = "🟢 Disponible" if clase["estado"] == "disponible" else "🔴 Llena"
            st.write(f"Estado: {estado_color}")

            if clase["inscritos"]:
                st.markdown("**Alumnos inscritos:**")
                for alumno in clase["inscritos"]:
                    col1, col2 = st.columns([4, 1])
                    col1.write(f"👤 {alumno}")
                    if col2.button("Eliminar", key=f"del-{clase['id']}-{alumno}"):
                        ok, msg = eliminar_usuario_de_clase(clase['coach'], clase['id'], alumno)
                        if ok:
                            st.success(f"{alumno} eliminado de la clase.")
                        else:
                            st.error(msg)
            else:
                st.info("No hay alumnos inscritos.")

            if st.button("❌ Eliminar esta clase", key=f"delete-{clase['id']}"):
                eliminar_clase(clase["id"])
                st.warning("Clase eliminada.")

            st.divider()

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
        st.button("Cerrar Sesión", on_click=logout)

        if st.session_state.user_role == "admin":
            interfaz_admin()
        else:
            st.info("Pantalla para usuarios en desarrollo...")

if __name__ == "__main__":
    main()
