from datetime import datetime
import streamlit as st
import os
import csv
import pandas as pd

# Carpeta donde se guardan los CSV
DIRECTORIO_CSV = "Filecsv"
os.makedirs(DIRECTORIO_CSV, exist_ok=True)

# Archivo CSV
CSV_FILE = os.path.join(DIRECTORIO_CSV, "tiempos_trabajados.csv")

# Función para calcular tiempo trabajado
def calcular_tiempo_trabajado(hora_inicio, hora_fin):
    formato = "%H:%M"
    inicio = datetime.strptime(hora_inicio, formato)
    fin = datetime.strptime(hora_fin, formato)
    diferencia = fin - inicio
    horas, segundos = divmod(diferencia.seconds, 3600)
    minutos, _ = divmod(segundos, 60)
    return horas, minutos

# Inicializar el estado de sesión
if "hora_inicio" not in st.session_state:
    st.session_state.hora_inicio = "09:00"
if "hora_fin" not in st.session_state:
    st.session_state.hora_fin = "17:00"
if "resultado" not in st.session_state:
    st.session_state.resultado = None

# Función para borrar los valores
def borrar_valores():
    st.session_state.hora_inicio = "09:00"
    st.session_state.hora_fin = "17:00"
    st.session_state.resultado = None

# Cargar el archivo CSS desde la carpeta static
def cargar_css(nombre_archivo):
    ruta_css = os.path.join("static", nombre_archivo)
    with open(ruta_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cargar el archivo CSS
cargar_css("botones.css")

# Guardar datos en CSV
def guardar_en_csv(fecha, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados):
    existe = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(["Fecha", "Hora de inicio", "Hora de fin", "Horas trabajadas", "Minutos trabajados"])
        writer.writerow([fecha, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados])

# Cargar datos CSV en un DataFrame
def cargar_datos():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Fecha", "Hora de inicio", "Hora de fin", "Horas trabajadas", "Minutos trabajados"])

# Guardar cambios en CSV (sobreescribir)
def actualizar_csv(df):
    df.to_csv(CSV_FILE, index=False)

# Borrar una fila
def borrar_fila(indice):
    df = cargar_datos()
    df = df.drop(indice).reset_index(drop=True)
    actualizar_csv(df)

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

# Botón para guardar
if st.button("Guardar Registro"):
    try:
        horas_trabajadas, minutos_trabajados = calcular_tiempo_trabajado(hora_inicio, hora_fin)
        guardar_en_csv(fecha_seleccionada, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados)
        st.success("Registro guardado correctamente en CSV")
    except Exception as e:
        st.error(f"Error: {e}")

# Cargar datos
df = cargar_datos()

# Seleccionar una fila para editar
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
        horas_trabajadas, minutos_trabajados = calcular_tiempo_trabajado(hora_inicio_edit, hora_fin_edit)
        df.loc[seleccion, "Horas trabajadas"] = horas_trabajadas
        df.loc[seleccion, "Minutos trabajados"] = minutos_trabajados
        actualizar_csv(df)
        st.success("Registro actualizado correctamente.")

    # Botón para eliminar
    if st.button("Eliminar"):
        borrar_fila(seleccion)
        st.warning("Registro eliminado.")

# Mostrar tabla de datos
st.subheader("📜 Historial de tiempos trabajados")
st.dataframe(df)
