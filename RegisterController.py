from Clases.Operations import Operations
from Clases.Utilities import Utilities
from datetime import datetime

class RegisterController:
    def __init__(self):
        self.ops = Operations()
        self.utils = Utilities()

    # Guardar un nuevo registro
    def guardar_registro(self, fecha, hora_inicio, hora_fin):
        try:
            horas_trabajadas, minutos_trabajados = self.ops.calcular_tiempo_trabajado(hora_inicio, hora_fin)
            self.utils.guardar_en_csv(fecha, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados)
            return "Registro guardado correctamente en CSV"
        except Exception as e:
            return f"Error: {e}"

    # Modificar un registro
    def modificar_registro(self, seleccion, fecha_edit, hora_inicio_edit, hora_fin_edit):
        try:
            df = self.utils.cargar_datos()
            df.loc[seleccion, "Fecha"] = fecha_edit.strftime("%Y-%m-%d")  # Convertir fecha a texto
            df.loc[seleccion, "Hora de inicio"] = hora_inicio_edit
            df.loc[seleccion, "Hora de fin"] = hora_fin_edit
            horas_trabajadas, minutos_trabajados = self.ops.calcular_tiempo_trabajado(hora_inicio_edit, hora_fin_edit)
            df.loc[seleccion, "Horas trabajadas"] = horas_trabajadas
            df.loc[seleccion, "Minutos trabajados"] = minutos_trabajados
            self.utils.actualizar_csv(df)
            return "Registro actualizado correctamente."
        except Exception as e:
            return f"Error al actualizar registro: {e}"

    # Eliminar un registro
    def eliminar_registro(self, seleccion):
        try:
            self.utils.borrar_fila(seleccion)
            return "Registro eliminado."
        except Exception as e:
            return f"Error al eliminar registro: {e}"
