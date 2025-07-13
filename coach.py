# coach.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

def coach_view():
    st.header("👨‍🏫 Entrenador")

    with st.expander("📌 Crear nueva clase", expanded=True):
        with st.form("form_crear"):
            title = st.text_input("Título")
            sport = st.selectbox("Deporte", ["voley","futbol","gym"])
            date = st.date_input("Fecha", min_value=datetime.today())
            hour = st.selectbox("Horario", ["08:00-09:00","09:00-10:00","13:00-14:00","17:00-18:00"])
            capacity = st.number_input("Capacidad", min_value=1, max_value=50, value=5)
            periodic = st.checkbox("Clase periódica (3 días)")
            submitted = st.form_submit_button("➕ Agregar")

            if submitted:
                coach = st.session_state["logged_user"]["username"]
                base = {"coach":coach,"sport":sport,"title":title,"hour":hour,
                        "capacity":capacity,"enrolled":0,"periodic":periodic}
                dates = [date + timedelta(days=i) for i in range(3)] if periodic else [date]
                for d in dates:
                    new = base.copy()
                    new["id"] = str(uuid.uuid4())
                    new["date"] = d.strftime("%Y-%m-%d")
                    st.session_state["classes"].append(new)
                st.success("Clase(s) creada(s)")
                st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]

    st.subheader("📋 Tus clases")
    my = [c for c in st.session_state["classes"] if c["coach"]==st.session_state["logged_user"]["username"]]
    if not my:
        st.info("Sin clases creadas aún")
    else:
        for c in sorted(my,key=lambda x:x["date"]):
            with st.container():
                st.markdown(f"<div class='card'><strong>{c['title']}</strong> — {c['sport'].capitalize()}</div>", unsafe_allow_html=True)
                col1,col2 = st.columns([3,1])
                col1.write(f"📅 {c['date']} | 🕐 {c['hour']}")
                col1.write(f"👥 {c['enrolled']} / {c['capacity']}")
                lleno = c["enrolled"]>=c["capacity"]
                col2.markdown(f"<span class='{'rojo' if lleno else 'verde'}'>{'🔴 Lleno' if lleno else '🟢 Disponible'}</span>", unsafe_allow_html=True)
                if col2.button("🗑 Eliminar", key=f"el_{c['id']}"):
                    inscritos = [r["username"] for r in st.session_state["reservations"] if r["class_id"]==c["id"]]
                    for u in inscritos:
                        st.session_state["notifications"].setdefault(u,[]).append(f"Tu clase '{c['title']}' del {c['date']} fue cancelada.")
                    st.session_state["classes"].remove(c)
                    st.session_state["reservations"] = [r for r in st.session_state["reservations"] if r["class_id"]!=c["id"]]
                    st.success("Eliminada.")
                    st.session_state["dummy_refresh"] = not st.session_state["dummy_refresh"]
                    return

    st.divider()
    st.subheader("📊 KPIs")
    total = len(my)
    reservas = sum(c["enrolled"] for c in my)
    col1,col2 = st.columns(2)
    col1.metric("Clases creadas", total)
    col2.metric("Reservas totales", reservas)

    freq = {}
    for r in st.session_state["reservations"]:
        if any(r["class_id"]==c["id"] for c in my):
            freq[r["username"]] = freq.get(r["username"],0)+1
    if freq:
        st.markdown("**Alumnos frecuentes:**")
        for u,n in sorted(freq.items(),key=lambda x:-x[1]):
            st.write(f"- {u}: {n} reservas")

    top = sorted(my, key=lambda x:-x["enrolled"])[:3]
    if top:
        st.markdown("**Clases más populares:**")
        for c in top:
            pct = int(c["enrolled"]/c["capacity"]*100)
            st.write(f"- {c['title']} ({pct}% lleno)")

