# user.py
import streamlit as st
from utils import get_status_badge

def user_view():
    st.subheader("📌 Selecciona deporte")
    deportes = ["Voley", "Fútbol", "Gimnasio"]
    deporte = st.selectbox("Deporte", deportes)

    st.subheader("📋 Clases disponibles")
    available = [c for c in st.session_state["classes"]
                 if c["sport"] == deporte and len(c["enrolled"]) < c["capacity"]]

    for c in available:
        badge = get_status_badge(len(c["enrolled"]), c["capacity"])
        st.markdown(f"**{c['title']}** con {c['coach']} - {c['date']} {c['hour']} {badge}")
        st.text(f"Inscritos: {len(c['enrolled'])}/{c['capacity']}")
        if st.button(f"Reservar {c['id']}", key=c['id']):
            if st.session_state["logged_user"]["username"] in c["enrolled"]:
                st.warning("Ya estás inscrito en esta clase.")
            else:
                c["enrolled"].append(st.session_state["logged_user"]["username"])
                st.session_state["reservations"].append({
                    "username": st.session_state["logged_user"]["username"],
                    "class_id": c["id"]
                })
                st.success("Reservado correctamente.")
                st.experimental_rerun()

    st.subheader("🧾 Tus reservas")
    my_res = [r for r in st.session_state["reservations"]
              if r["username"] == st.session_state["logged_user"]["username"]]

    for r in my_res:
        c = next((cl for cl in st.session_state["classes"] if cl["id"] == r["class_id"]), None)
        if c:
            st.markdown(f"➡️ {c['title']} con {c['coach']} - {c['date']} {c['hour']}")
            if st.button(f"Cancelar {r['class_id']}", key=r['class_id']):
                c["enrolled"].remove(r["username"])
                st.session_state["reservations"].remove(r)
                st.success("Reserva cancelada.")
                st.experimental_rerun()

