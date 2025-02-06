# app.py
from datetime import datetime
import streamlit as st
import os
from Operations import Operations  # Asegúrate de que la clase Operations esté definida en este archivo
from Utilities import Utilities  # Importamos la clase Utilities

# Inicializamos las clases
ops = Operations()
utils = Utilities()

# Inicializar el estado de sesión
if "hora_inicio" not in st.session_state:
    st.session_state.hora_inicio = "09:00"
if "hora_fin" not in st.session_state:
    st.session_state.hora_fin = "17:00"
if "resultado" not in st.session_state:
    st.session_state.resultado = None

# Cargar el archivo CSS desde la carpeta static
def cargar_css(nombre_archivo):
    ruta_css = os.path.join("static", nombre_archivo)
    with open(ruta_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cargar el archivo CSS
cargar_css("botones.css")

# Interfaz
st.title("Calculadora de Tiempo Trabajado ⏱️")

# 📅 Seleccionar fecha con calendario
fecha_seleccionada = st.date_input("📅 Selecciona la fecha:", datetime.today())

# ✅ Campos de hora con botones + y - 
col1, col2 = st.columns(2)
with col1:
    horas_inicio = st.number_input("⏰ Hora de inicio", min_value=0, max_value=23, value=9, step=1)
with col2:
    minutos_inicio = st.number_input("⏳ Minutos de inicio", min_value=0, max_value=55, value=0, step=5)

col3, col4 = st.columns(2)
with col3:
    horas_fin = st.number_input("🏁 Hora de fin", min_value=0, max_value=23, value=17, step=1)
with col4:
    minutos_fin = st.number_input("⌛ Minutos de fin", min_value=0, max_value=55, value=0, step=5)

# Formatear las horas en formato "HH:MM"
hora_inicio = f"{horas_inicio:02d}:{minutos_inicio:02d}"
hora_fin = f"{horas_fin:02d}:{minutos_fin:02d}"

# Mostrar las opciones para guardar, modificar o eliminar
operation = st.selectbox("Elige una operación:", ["Guardar Registro", "Modificar Registro", "Eliminar Registro"])

# ==========================
# Opción para guardar un nuevo registro
if operation == "Guardar Registro":
    if st.button("Guardar Registro"):
        try:
            horas_trabajadas, minutos_trabajados = ops.calcular_tiempo_trabajado(hora_inicio, hora_fin)
            utils.guardar_en_csv(fecha_seleccionada, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados)
            st.success("Registro guardado correctamente en CSV")
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================
# Opción para modificar un registro
elif operation == "Modificar Registro":
    df = utils.cargar_datos()
    if not df.empty:
        seleccion = st.radio("✏️ Selecciona un registro para modificar:", df.index, format_func=lambda x: f"{df.loc[x, 'Fecha']} | {df.loc[x, 'Hora de inicio']} - {df.loc[x, 'Hora de fin']}")

        # Cargar valores en los campos
        fecha_edit = st.date_input("📅 Editar Fecha:", datetime.strptime(df.loc[seleccion, "Fecha"], "%Y-%m-%d"))

        col5, col6 = st.columns(2)
        with col5:
            horas_inicio_edit = st.number_input("⏰ Editar Hora de inicio", min_value=0, max_value=23, value=int(df.loc[seleccion, "Hora de inicio"].split(":")[0]), step=1)
        with col6:
            minutos_inicio_edit = st.number_input("⏳ Editar Minutos de inicio", min_value=0, max_value=55, value=int(df.loc[seleccion, "Hora de inicio"].split(":")[1]), step=5)

        col7, col8 = st.columns(2)
        with col7:
            horas_fin_edit = st.number_input("🏁 Editar Hora de fin", min_value=0, max_value=23, value=int(df.loc[seleccion, "Hora de fin"].split(":")[0]), step=1)
        with col8:
            minutos_fin_edit = st.number_input("⌛ Editar Minutos de fin", min_value=0, max_value=55, value=int(df.loc[seleccion, "Hora de fin"].split(":")[1]), step=5)

        hora_inicio_edit = f"{horas_inicio_edit:02d}:{minutos_inicio_edit:02d}"
        hora_fin_edit = f"{horas_fin_edit:02d}:{minutos_fin_edit:02d}"

        # Botón para actualizar
        if st.button("Actualizar"):
            df.loc[seleccion, "Fecha"] = fecha_edit.strftime("%Y-%m-%d")  # Convertir fecha a texto
            df.loc[seleccion, "Hora de inicio"] = hora_inicio_edit
            df.loc[seleccion, "Hora de fin"] = hora_fin_edit
            horas_trabajadas, minutos_trabajados = ops.calcular_tiempo_trabajado(hora_inicio_edit, hora_fin_edit)
            df.loc[seleccion, "Horas trabajadas"] = horas_trabajadas
            df.loc[seleccion, "Minutos trabajados"] = minutos_trabajados
            utils.actualizar_csv(df)
            st.success("Registro actualizado correctamente.")
    else:
        st.warning("No hay registros para modificar.")

# ==========================
# Opción para eliminar un registro
elif operation == "Eliminar Registro":
    df = utils.cargar_datos()
    if not df.empty:
        seleccion = st.radio("🔴 Selecciona un registro para eliminar:", df.index, format_func=lambda x: f"{df.loc[x, 'Fecha']} | {df.loc[x, 'Hora de inicio']} - {df.loc[x, 'Hora de fin']}")
        
        # Botón para eliminar
        if st.button("Eliminar"):
            utils.borrar_fila(seleccion)
            st.warning("Registro eliminado.")
    else:
        st.warning("No hay registros para eliminar.")

# Mostrar tabla de datos
st.subheader("📜 Historial de tiempos trabajados")
df = utils.cargar_datos()  # Asegurarse de cargar los datos más actualizados
st.dataframe(df)
