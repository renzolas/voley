# coach.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

def coach_view():
    st.header("👨‍🏫 Panel del Entrenador")

    st.subheader("📌 Crear nueva clase")
    title = st.text_input("Título de la clase (ej: Voley Avanzado)")
    sport = st.selectbox("Deporte", ["voley", "futbol", "gym"])
    date = st.date_input("Fecha de la clase", min_value=datetime.today())
    hour = st.selectbox("Horario disponible", [
        "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00",
        "11:00 - 12:00", "13:00 - 14:00", "14:00 - 15:00",
        "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
    ])
    capacity = st.number_input("Máximo de alumnos", min_value=1, max_value=50, step=1)
    periodic = st.checkbox("¿Clase periódica? (mismo horario en los próximos 3 días)")

    if st.button("Agregar clase"):
        coach = st.session_state["logged_user"]["username"]
        base_class = {
            "coach": coach,
            "sport": sport,
            "title": title,
            "hour": hour,
            "capacity": capacity,
            "enrolled": 0,
            "periodic": periodic,
        }

        if periodic:
            for i in range(3):
                new_class = base_class.copy()
                new_class["date"] = (date + timedelta(days=i)).strftime("%Y-%m-%d")
                new_class["id"] = str(uuid.uuid4())
                st.session_state["classes"].append(new_class)
        else:
            base_class["date"] = date.strftime("%Y-%m-%d")
            base_class["id"] = str(uuid.uuid4())
            st.session_state["classes"].append(base_class)

        st.success("Clase(s) creada(s) correctamente.")
        st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]

    st.divider()
    st.subheader("📋 Tus clases")

    coach = st.session_state["logged_user"]["username"]
    my_classes = [c for c in st.session_state["classes"] if c["coach"] == coach]

    if not my_classes:
        st.info("Aún no has creado clases.")
    else:
        for c in sorted(my_classes, key=lambda x: x["date"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **{c['title']}**  
                🏷️ {c['sport'].capitalize()}  
                📅 {c['date']} — 🕐 {c['hour']}  
                👥 {c['enrolled']} / {c['capacity']}
                """)
            with col2:
                lleno = c["enrolled"] >= c["capacity"]
                estado = "🔴 Lleno" if lleno else "🟢 Disponible"
                st.markdown(f"**Estado:** {estado}")

                if st.button(f"Eliminar", key=f"eliminar_{c['id']}"):
                    alumnos_inscritos = [
                        r["username"] for r in st.session_state["reservations"]
                        if r["class_id"] == c["id"]
                    ]
                    for alumno in alumnos_inscritos:
                        if alumno not in st.session_state["notifications"]:
                            st.session_state["notifications"][alumno] = []
                        st.session_state["notifications"][alumno].append(
                            f"❌ Tu clase '{c['title']}' del {c['date']} fue cancelada."
                        )

                    st.session_state["classes"].remove(c)
                    st.session_state["reservations"] = [
                        r for r in st.session_state["reservations"] if r["class_id"] != c["id"]
                    ]
                    st.success("Clase eliminada.")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return

            alumnos = [r["username"] for r in st.session_state["reservations"] if r["class_id"] == c["id"]]
            if alumnos:
                with st.expander("👥 Ver y eliminar alumnos"):
                    for alumno in alumnos:
                        col_a1, col_a2 = st.columns([3, 1])
                        with col_a1:
                            st.write(f"- {alumno}")
                        with col_a2:
                            if st.button("Eliminar", key=f"del_{alumno}_{c['id']}"):
                                st.session_state["reservations"] = [
                                    r for r in st.session_state["reservations"]
                                    if not (r["class_id"] == c["id"] and r["username"] == alumno)
                                ]
                                c["enrolled"] -= 1
                                st.success(f"{alumno} eliminado de la clase.")
                                st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                                return

    st.divider()
    st.subheader("📊 Estadísticas y KPIs")

    total_clases = len(my_classes)
    total_reservas = sum(c["enrolled"] for c in my_classes)

    col1, col2 = st.columns(2)
    col1.metric("🧾 Clases creadas", total_clases)
    col2.metric("👥 Total reservas", total_reservas)

    mis_ids = [c["id"] for c in my_classes]
    alumno_frecuencia = {}
    for r in st.session_state["reservations"]:
        if r["class_id"] in mis_ids:
            alumno_frecuencia[r["username"]] = alumno_frecuencia.get(r["username"], 0) + 1

    if alumno_frecuencia:
        st.markdown("📌 **Alumnos más frecuentes:**")
        for alumno, freq in sorted(alumno_frecuencia.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"- {alumno} — {freq} reservas")

    llenadas = sorted(my_classes, key=lambda c: c["enrolled"], reverse=True)[:3]
    if llenadas:
        st.markdown("🔥 **Clases más populares:**")
        for c in llenadas:
            porcentaje = (c["enrolled"] / c["capacity"]) * 100
            st.markdown(f"- {c['title']} ({c['date']}) — {porcentaje:.0f}% lleno")

