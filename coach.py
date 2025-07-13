# coach.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

def coach_view():
    st.header("👨‍🏫 Panel del Entrenador")

    st.markdown("### ➕ Crear nueva clase")
    with st.form("form_clase"):
        title = st.text_input("🏷️ Título de la clase (ej: Voley Avanzado)")
        sport = st.selectbox("⚽ Deporte", ["voley", "futbol", "gym"])
        date = st.date_input("📅 Fecha", min_value=datetime.today())
        hour = st.selectbox("🕒 Horario", [
            "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00",
            "11:00 - 12:00", "13:00 - 14:00", "14:00 - 15:00",
            "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
        ])
        capacity = st.number_input("👥 Máximo de alumnos", min_value=1, max_value=50, step=1)
        periodic = st.checkbox("🔁 ¿Clase periódica? (próximos 3 días)")
        submit = st.form_submit_button("✅ Crear clase")

    if submit:
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
            for i in range(3):  # crea clases por 3 días consecutivos
                new_class = base_class.copy()
                new_class["date"] = (date + timedelta(days=i)).strftime("%Y-%m-%d")
                new_class["id"] = str(uuid.uuid4())
                st.session_state["classes"].append(new_class)
        else:
            base_class["date"] = date.strftime("%Y-%m-%d")
            base_class["id"] = str(uuid.uuid4())
            st.session_state["classes"].append(base_class)

        st.success("✅ Clase(s) creada(s) correctamente.")
        st.experimental_rerun()

    st.divider()
    st.markdown("### 📋 Tus clases creadas")

    coach = st.session_state["logged_user"]["username"]
    my_classes = [c for c in st.session_state["classes"] if c["coach"] == coach]

    if not my_classes:
        st.info("Todavía no has creado ninguna clase.")
    else:
        for c in sorted(my_classes, key=lambda x: x["date"]):
            lleno = c["enrolled"] >= c["capacity"]
            estado = "🔴 Lleno" if lleno else "🟢 Disponible"
            color = "#ffcccc" if lleno else "#ccffcc"

            with st.container():
                st.markdown(f"""
                <div style='background-color:{color}; padding: 15px; border-radius: 8px; margin-bottom:10px'>
                <strong>{c['title']}</strong> — {c['sport'].capitalize()}  
                📅 {c['date']} | 🕐 {c['hour']}  
                👥 {c['enrolled']} / {c['capacity']}  
                <br><strong>Estado:</strong> <span style='color:{"red" if lleno else "green"}'>{estado}</span>
                </div>
                """, unsafe_allow_html=True)

                if st.button("❌ Eliminar clase", key=f"del_{c['id']}"):
                    st.session_state["classes"].remove(c)

                    # Eliminar reservas asociadas
                    st.session_state["reservations"] = [
                        r for r in st.session_state["reservations"]
                        if r["class_id"] != c["id"]
                    ]

                    # Notificar usuarios afectados
                    for username in list(st.session_state["notifications"].keys()):
                        st.session_state["notifications"][username] = st.session_state["notifications"].get(username, [])

                    for r in st.session_state["reservations"]:
                        if r["class_id"] == c["id"]:
                            st.session_state["notifications"][r["username"]].append(
                                f"⚠️ Tu clase '{c['title']}' del {c['date']} ha sido cancelada."
                            )

                    st.success("Clase eliminada y usuarios notificados.")
                    st.experimental_rerun()

    st.divider()
    st.markdown("### 📊 Estadísticas y KPIs")

    total_clases = len(my_classes)
    total_reservas = sum(c["enrolled"] for c in my_classes)

    kpi1, kpi2 = st.columns(2)
    kpi1.metric("📚 Clases creadas", total_clases)
    kpi2.metric("📥 Total de reservas", total_reservas)

    # Alumnos frecuentes
    ids_mias = [c["id"] for c in my_classes]
    alumnos = {}
    for r in st.session_state["reservations"]:
        if r["class_id"] in ids_mias:
            alumnos[r["username"]] = alumnos.get(r["username"], 0) + 1

    if alumnos:
        st.markdown("### 🙋 Alumnos más frecuentes")
        for alumno, count in sorted(alumnos.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"- **{alumno}** — {count} reservas")

    # Clases más populares
    top_clases = sorted(my_classes, key=lambda x: x["enrolled"], reverse=True)[:3]
    if top_clases:
        st.markdown("### 🔥 Clases más llenas")
        for tc in top_clases:
            pct = (tc["enrolled"] / tc["capacity"]) * 100
            st.markdown(f"- **{tc['title']}** ({tc['date']}) — {pct:.0f}% de ocupación")

