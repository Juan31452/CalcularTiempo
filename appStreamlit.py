from datetime import datetime
import streamlit as st
import os
from RegisterController import RegisterController  # Importamos la nueva clase
from Clases.Operations import Operations

# Inicializamos la clases
controller = RegisterController()
Ops = Operations()

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

col1, col2 = st.columns(2)

with col1:
    operation = st.radio(
        "Seleccione una opción:", 
        ["Guardar Registro", "Modificar Registro", "Eliminar Registro", "Solo Calcular", "Ver Lista"], 
        index=0
    )

# Interfaz
st.title("Calculadora de Tiempo Trabajado ⏱️")
# ==========================

# Opción para guardar un nuevo registro
if operation == "Guardar Registro":

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

    if st.button("Guardar Registro"):
        resultado = controller.guardar_registro(fecha_seleccionada, hora_inicio, hora_fin)
        st.success(resultado)

# ==========================
# Opción para modificar un registro
elif operation == "Modificar Registro":
    df = controller.utils.cargar_datos()
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
            resultado = controller.modificar_registro(seleccion, fecha_edit, hora_inicio_edit, hora_fin_edit)
            st.success(resultado)
    else:
        st.warning("No hay registros para modificar.")

# ==========================
# Opción para eliminar un registro
elif operation == "Eliminar Registro":
    df = controller.utils.cargar_datos()
    if not df.empty:
        seleccion = st.radio("🔴 Selecciona un registro para eliminar:", df.index, format_func=lambda x: f"{df.loc[x, 'Fecha']} | {df.loc[x, 'Hora de inicio']} - {df.loc[x, 'Hora de fin']}")

        # Botón para eliminar
        if st.button("Eliminar"):
            resultado = controller.eliminar_registro(seleccion)
            st.warning(resultado)
    else:
        st.warning("No hay registros para eliminar.")


elif operation == "Solo Calcular":

    
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

    if st.button("Calcular"):
        try:
         horas_trabajadas, minutos_trabajados = Ops.calcular_tiempo_trabajado(hora_inicio, hora_fin)
         st.success(f"**Tiempo trabajado:** {horas_trabajadas} horas y {minutos_trabajados} minutos")
        except Exception as e:
         st.error(f"Error: {e}")


elif operation == "Ver Lista":

 # Mostrar tabla de datos
 st.subheader("📜 Historial de tiempos trabajados")
 df = controller.utils.cargar_datos()  # Asegurarse de cargar los datos más actualizados
 st.dataframe(df)
