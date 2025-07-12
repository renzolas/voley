import streamlit as st

# Estado simple para simular sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def login():
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        # Aquí iría la validación real con datos de auth.py
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.user_role = "admin"
            st.success("Login como Admin exitoso")
        elif username == "user" and password == "user123":
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.success("Login como Usuario exitoso")
        else:
            st.error("Usuario o contraseña incorrectos")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.success("Sesión cerrada")

def main():
    if not st.session_state.logged_in:
        login()
    else:
        st.sidebar.button("Cerrar Sesión", on_click=logout)
        if st.session_state.user_role == "admin":
            st.title("Panel Admin")
            st.write("Aquí va el panel de entrenador.")
            # Luego linkeamos a pages/1_Admin.py o importamos funciones
        elif st.session_state.user_role == "user":
            st.title("Panel Usuario")
            st.write("Aquí va el panel de usuario.")
            # Link a pages/2_Usuario.py o funciones

if __name__ == "__main__":
    main()

