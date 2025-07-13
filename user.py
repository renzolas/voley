# user.py
import streamlit as st
from datetime import datetime

def user_view():
    st.header("🙋 Usuario")
    u = st.session_state["logged_user"]["username"]

    noti = st.session_state["notifications"].get(u,[])
    if noti:
        for n in noti: st.warning(n)
        if st.button("🧹 Marcar leídas"):
            st.session_state["notifications"][u] = []

    deporte = st.selectbox("Deporte",["voley","futbol","gym"])
    fecha = st.date_input("Fecha", min_value=datetime.today())
    disponibles = [c for c in st.session_state["classes"] if c["sport"]==deporte and c["date"]==fecha.strftime("%Y-%m-%d")]

    st.subheader("Clases disponibles")
    if not disponibles:
        st.info("No hay clases para esa fecha")
    else:
        for c in disponibles:
            lleno = c["enrolled"]>=c["capacity"]
            st.markdown(f"**{c['title']}** - {c['hour']} — 👥 {c['enrolled']}/{c['capacity']} — "+("🔴 Lleno" if lleno else "🟢 Disponible"))
            if not lleno:
                if st.button("Reservar", key=f"res_{c['id']}"):
                    already = any(r for r in st.session_state["reservations"] if r["username"]==u and r["class_id"]==c["id"])
                    if not already:
                        st.session_state["reservations"].append({"username":u,"class_id":c["id"]})
                        c["enrolled"]+=1
                        st.balloons()
                        st.success("¡Listo!")
                        st.session_state["dummy_refresh"]=not st.session_state["dummy_refresh"]
                        return
                    else:
                        st.warning("Ya reservaste")

    st.divider()
    st.subheader("Mis reservas")
    mine = [r for r in st.session_state["reservations"] if r["username"]==u]
    if not mine:
        st.info("No tienes reservas")
    else:
        for r in mine:
            c = next(c for c in st.session_state["classes"] if c["id"]==r["class_id"])
            st.markdown(f"**{c['title']}** — {c['date']} {c['hour']}")
            if st.button("Cancelar", key=f"can_{c['id']}"):
                st.session_state["reservations"] = [rr for rr in st.session_state["reservations"] if rr!=r]
                c["enrolled"]-=1
                st.success("Cancelada")
                st.session_state["dummy_refresh"]=not st.session_state["dummy_refresh"]
                return

