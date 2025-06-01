import matplotlib.pyplot as plt
import numpy as np

# Parámetros
masa = 1.0  # kg
c = 4186    # J/kg·°C
delta_T = 80  # °C (de 20 a 100)
Q_total = masa * c * delta_T  # Energía total
potencia = 360  # W
tiempo_total = Q_total / potencia  # segundos

# Datos para el gráfico
tiempos = [i for i in range(int(tiempo_total) + 1)]
temperaturas = [20 + (potencia * i) / (masa * c) for i in tiempos]

if __name__ == "__main__":
    # Código para ejecutar el gráfico
    plt.figure(figsize=(10,6))
    
    # Convertir tiempos a minutos para el eje X
    tiempos_min_plot = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min_plot, temperaturas, label="Temperatura del agua")
    plt.axhline(100, color='r', linestyle='--', label="100 °C")
    plt.title('Curva de Temperatura sin Pérdidas de Calor')
    plt.xlabel('Tiempo (min)') # Etiqueta del eje X actualizada
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.legend()
    
    # Ajustar los ticks del eje X para que sean más legibles en minutos
    max_tiempo_min = max(tiempos_min_plot) if tiempos_min_plot.size > 0 else 0
    # Generar ticks cada 2 minutos si el total es > 10 min, sino cada 1 minuto.
    tick_spacing = 2 if max_tiempo_min > 40 else 1
    if max_tiempo_min == 0: 
        plt.xticks([0])
    else:
        upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
        plt.xticks(np.arange(0, upper_limit, tick_spacing))
        
    plt.show()
