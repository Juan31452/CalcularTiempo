from datetime import datetime

def calcular_tiempo_trabajado(hora_inicio, hora_fin):
    # Formato de hora esperado: "HH:MM"
    formato = "%H:%M"
    
    # Convertir las cadenas de texto a objetos datetime
    inicio = datetime.strptime(hora_inicio, formato)
    fin = datetime.strptime(hora_fin, formato)
    
    # Calcular la diferencia de tiempo
    diferencia = fin - inicio
    
    # Convertir la diferencia a horas y minutos
    horas, segundos = divmod(diferencia.seconds, 3600)
    minutos, _ = divmod(segundos, 60)
    
    return horas, minutos

def main():
    print("Calculadora de Tiempo Trabajado")
    
    # Solicitar la hora de inicio y finalización
    hora_inicio = input("Ingresa la hora de inicio (HH:MM): ")
    hora_fin = input("Ingresa la hora de finalización (HH:MM): ")
    
    # Calcular el tiempo trabajado
    horas, minutos = calcular_tiempo_trabajado(hora_inicio, hora_fin)
    
    # Mostrar el resultado
    print(f"Tiempo trabajado: {horas} horas y {minutos} minutos")

if __name__ == "__main__":
    main()