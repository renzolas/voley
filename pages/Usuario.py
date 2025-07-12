import streamlit as st
import datetime
from data.db_simulada import (
    obtener_clases_disponibles_por_deporte,
    inscribir_usuario_en_clase,
    obtener_clases_por_usuario,
    cancelar_reserva
)

def interfaz_usuario():
    st.header(f"Panel de Usuario - {st.session_state.username} 🏃‍♂️")

    st.subheader("Reservar una clase")
    deporte = st.selectbox("Selecciona un deporte", ["voley", "futbol", "gym"])
    clases_disponibles = obtener_clases_disponibles_por_deporte(deporte)

    if not clases_disponibles:
        st.info("No hay clases disponibles para este deporte.")
    else:
        opciones = [
            f"{c['nombre_clase']} - {c['fecha']} - {c['horario']} ({len(c['inscritos'])}/{c['aforo']})"
            for c in clases_disponibles
        ]
        seleccion = st.selectbox("Elige la clase para reservar", opciones)

        if st.button("Reservar clase"):
            idx = opciones.index(seleccion)
            clase_seleccionada = clases_disponibles[idx]

            # Validar reserva con anticipación (4 días)
            fecha_clase = datetime.datetime.strptime(clase_seleccionada["fecha"], "%Y-%m-%d").date()
            hoy = datetime.date.today()
            if (fecha_clase - hoy).days > 4:
                st.error("Solo puedes reservar con un máximo de 4 días de anticipación.")
            else:
                ok, msg = inscribir_usuario_en_clase(st.session_state.username, clase_seleccionada["id"])
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.divider()
    st.subheader("Tus reservas")

    reservas = obtener_clases_por_usuario(st.session_state.username)
    if not reservas:
        st.info("No tienes reservas activas.")
    else:
        for r in reservas:
            st.markdown(f"### {r['nombre_clase']} ({r['deporte'].capitalize()})")
            st.write(f"📅 Fecha: {r['fecha']} | 🕒 Horario: {r['horario']}")
            if st.button(f"Cancelar reserva - {r['nombre_clase']}", key=f"cancel-{r['id']}"):
                ok, msg = cancelar_reserva(st.session_state.username, r["id"])
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
            st.divider()

