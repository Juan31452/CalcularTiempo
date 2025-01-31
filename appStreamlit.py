from datetime import datetime
import streamlit as st

st.title("Calculadora de Tiempo Trabajado ⏱️")

hora_inicio = st.text_input("Hora de inicio (HH:MM):", placeholder="Ej: 09:00")
hora_fin = st.text_input("Hora de finalización (HH:MM):", placeholder="Ej: 17:30")

if st.button("Calcular"):
    try:
        formato = "%H:%M"
        inicio = datetime.strptime(hora_inicio, formato)
        fin = datetime.strptime(hora_fin, formato)
        diferencia = fin - inicio
        horas, segundos = divmod(diferencia.seconds, 3600)
        minutos, _ = divmod(segundos, 60)
        st.success(f"**Tiempo trabajado:** {horas} horas y {minutos} minutos")
    except:
        st.error("Formato inválido. Usa HH:MM (ej: 09:00).")