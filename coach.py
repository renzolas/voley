# coach.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

# Estilos CSS para tarjetas compactas y diseño
def local_css():
    st.markdown("""
    <style>
    .card {
        background: #f0f2f6;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgb(0 0 0 / 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.95rem;
        transition: box-shadow 0.3s ease;
    }
    .card:hover {
        box-shadow: 0 4px 10px rgb(0 0 0 / 0.2);
    }
    .icon {
        font-size: 2.5rem;
        margin-right: 12px;
        user-select: none;
    }
    .info {
        flex-grow: 1;
        padding-right: 15px;
    }
    .buttons {
        display: flex;
        gap: 8px;
    }
    .status-available {
        color: green;
        font-weight: bold;
    }
    .status-full {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_icon(sport):
    icons = {
        "voley": "🏐",
        "futbol": "⚽",
        "gym": "🏋️"
    }
    return icons.get(sport, "❓")

def coach_view(tab="create"):
    local_css()
    coach = st.session_state["logged_user"]["username"]

    if tab == "create":
        st.header("👨‍🏫 Crear nueva clase")
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
            st.experimental_rerun()

    elif tab == "list":
        st.header("📋 Tus clases")
        my_classes = [c for c in st.session_state["classes"] if c["coach"] == coach]

        if not my_classes:
            st.info("Aún no has creado clases.")
        else:
            for c in sorted(my_classes, key=lambda x: x["date"]):
                icono = get_icon(c["sport"])
                lleno = c["enrolled"] >= c["capacity"]
                estado_texto = "Disponible" if not lleno else "Lleno"
                estado_clase = "status-available" if not lleno else "status-full"

                st.markdown(f"""
                <div class='card'>
                    <div class='icon'>{icono}</div>
                    <div class='info'>
                        <b>{c['title']}</b><br>
                        🏷️ {c['sport'].capitalize()}<br>
                        📅 {c['date']} — 🕐 {c['hour']}<br>
                        👥 {c['enrolled']} / {c['capacity']} — <span class='{estado_clase}'>{estado_texto}</span>
                    </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])
                with col2:
                    if st.button(f"Eliminar", key=f"eliminar_{c['id']}"):
                        st.session_state["classes"].remove(c)
                        st.session_state["reservations"] = [
                            r for r in st.session_state["reservations"] if r["class_id"] != c["id"]
                        ]
                        st.success("Clase eliminada.")
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "kpis":
        st.header("📊 Estadísticas y KPIs")
        my_classes = [c for c in st.session_state["classes"] if c["coach"] == coach]
        total_clases = len(my_classes)
        total_reservas = sum(c["enrolled"] for c in my_classes)

        st.markdown(f"""
        - 🧾 **Total de clases creadas:** {total_clases}  
        - 🧍‍♂️ **Total de reservas recibidas:** {total_reservas}
        """)

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


