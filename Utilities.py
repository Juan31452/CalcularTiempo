# Utilities.py
import os
import csv
import pandas as pd

class Utilities:
    def __init__(self, directorio_csv="Filecsv", archivo_csv="tiempos_trabajados.csv"):
        self.directorio_csv = directorio_csv
        self.archivo_csv = os.path.join(directorio_csv, archivo_csv)
        os.makedirs(directorio_csv, exist_ok=True)

    def guardar_en_csv(self, fecha, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados):
        existe = os.path.isfile(self.archivo_csv)
        with open(self.archivo_csv, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not existe:
                writer.writerow(["Fecha", "Hora de inicio", "Hora de fin", "Horas trabajadas", "Minutos trabajados"])
            writer.writerow([fecha, hora_inicio, hora_fin, horas_trabajadas, minutos_trabajados])

    def cargar_datos(self):
        if os.path.exists(self.archivo_csv):
            return pd.read_csv(self.archivo_csv)
        return pd.DataFrame(columns=["Fecha", "Hora de inicio", "Hora de fin", "Horas trabajadas", "Minutos trabajados"])

    def actualizar_csv(self, df):
        df.to_csv(self.archivo_csv, index=False)

    def borrar_fila(self, indice):
        df = self.cargar_datos()
        df = df.drop(indice).reset_index(drop=True)
        self.actualizar_csv(df)
