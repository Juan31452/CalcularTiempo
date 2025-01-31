from datetime import datetime
import streamlit as st

# Función para calcular el tiempo trabajado
def calcular_tiempo_trabajado(hora_inicio, hora_fin):
    formato = "%H:%M"
    inicio = datetime.strptime(hora_inicio, formato)
    fin = datetime.strptime(hora_fin, formato)
    diferencia = fin - inicio
    horas, segundos = divmod(diferencia.seconds, 3600)
    minutos, _ = divmod(segundos, 60)
    return horas, minutos

# Interfaz de la aplicación
st.title("Calculadora de Tiempo Trabajado ⏱️")

# Crear listas desplegables para seleccionar la hora
horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)]  # Horas de 00:00 a 23:45 en intervalos de 15 minutos

hora_inicio = st.selectbox("Hora de inicio:", horas, index=horas.index("09:00"))  # Valor predeterminado: 09:00
hora_fin = st.selectbox("Hora de finalización:", horas, index=horas.index("17:00"))  # Valor predeterminado: 17:00

# Botón para calcular
if st.button("Calcular"):
    try:
        horas_trabajadas, minutos_trabajados = calcular_tiempo_trabajado(hora_inicio, hora_fin)
        st.success(f"**Tiempo trabajado:** {horas_trabajadas} horas y {minutos_trabajados} minutos")
    except Exception as e:
        st.error(f"Error: {e}")