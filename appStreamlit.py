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

# Cargar el archivo CSS
def cargar_css(nombre_archivo):
    with open(nombre_archivo) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Interfaz de la aplicación
st.title("Calculadora de Tiempo Trabajado ⏱️")

# Cargar el archivo CSS
cargar_css("botones.css")

# Función para crear un campo de hora con horas y minutos separados
def campo_hora(label, hora_predeterminada="09:00"):
    col1, col2 = st.columns(2)  # Divide la fila en dos columnas
    with col1:
        horas = st.number_input(f"{label} - Horas", min_value=0, max_value=23, value=int(hora_predeterminada.split(":")[0]), step=1)
    with col2:
        # Minutos con intervalos de 5
        minutos = st.number_input(f"{label} - Minutos", min_value=0, max_value=55, value=int(hora_predeterminada.split(":")[1]), step=5)
    return f"{horas:02d}:{minutos:02d}"  # Devuelve la hora en formato HH:MM

# Campos para la hora de inicio y finalización
hora_inicio = campo_hora("Hora de inicio", "09:00")
hora_fin = campo_hora("Hora de finalización", "17:00")

# Botón para calcular
if st.button("Calcular"):
    try:
        horas_trabajadas, minutos_trabajados = calcular_tiempo_trabajado(hora_inicio, hora_fin)
        st.success(f"**Tiempo trabajado:** {horas_trabajadas} horas y {minutos_trabajados} minutos")
    except Exception as e:
        st.error(f"Error: {e}")