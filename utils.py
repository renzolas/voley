# utils.py
import streamlit as st

def get_available_hours():
    return [
        "08:00 - 09:00",
        "09:00 - 10:00",
        "10:00 - 11:00",
        "13:00 - 14:00",
        "14:00 - 15:00",
        "17:00 - 18:00",
        "18:00 - 19:00"
    ]

def get_status_badge(current, max_):
    if current >= max_:
        return "🔴 *Lleno*"
    else:
        return "🟢 *Disponible*"

