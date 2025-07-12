import streamlit as st
import datetime

st.header("Panel de Entrenador - TEST")

nombre_clase = st.text_input("Nombre de la clase")
deporte = st.selectbox("Deporte", ["voley", "futbol", "gym"])
fecha = st.date_input("Fecha", min_value=datetime.date.today())
horario = st.selectbox("Horario", ["13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00"])
aforo = st.number_input("Máximo de alumnos", min_value=1, max_value=20, step=1)

periodicidad = st.selectbox(
    "¿Repetir esta clase semanalmente?",
    [
        "No",
        "Repetir por 1 semana",
        "Repetir por 2 semanas",
        "Repetir por 3 semanas",
        "Repetir por todo el mes"
    ]
)

mapa_periodos = {
    "No": 1,
    "Repetir por 1 semana": 2,
    "Repetir por 2 semanas": 3,
    "Repetir por 3 semanas": 4,
    "Repetir por todo el mes": 5
}
semanas = mapa_periodos[periodicidad]

if st.button("Agregar clase"):
    for i in range(semanas):
        nueva_fecha = fecha + datetime.timedelta(weeks=i)
        st.write(f"Clase creada para {nueva_fecha}")
    st.success("Clases creadas correctamente ✅")

