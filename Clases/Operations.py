from datetime import datetime
import streamlit as st

class Operations:
    # Función para calcular tiempo trabajado
    def calcular_tiempo_trabajado(self, hora_inicio, hora_fin):
        """Calcula la cantidad de horas y minutos trabajados entre dos horas."""
        formato = "%H:%M"
        inicio = datetime.strptime(hora_inicio, formato)
        fin = datetime.strptime(hora_fin, formato)
        diferencia = fin - inicio
        horas, segundos = divmod(diferencia.seconds, 3600)
        minutos, _ = divmod(segundos, 60)
        return horas, minutos
    
    # Función para borrar los valores
    def borrar_valores(self):
        st.session_state.hora_inicio = "09:00"
        st.session_state.hora_fin = "17:00"
        st.session_state.resultado = None
