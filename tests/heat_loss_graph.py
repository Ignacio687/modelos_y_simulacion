import numpy as np
import matplotlib.pyplot as plt

# Constantes
masa = 1.0  # kg de agua
calor_especifico = 4186  # J/(kg°C)
potencia = 360  # Watts
T_amb = 20  # Temperatura ambiente en °C
dt = 1  # intervalo de tiempo en segundos
tiempo_total = 2500  # segundos

# Coeficiente de transmisión térmica U
# Materiales: acero (k=16 W/mK), poliuretano (k=0.03 W/mK), ambos de 1 mm de espesor
R_acero = 0.001 / 16
R_poliuretano = 0.001 / 0.03
R_total = R_acero + R_poliuretano
U = 1 / R_total  # Coeficiente de transmisión térmica

# Geometría del cilindro
radio = 0.05  # metros
altura = 0.13  # metros
area_lateral = 2 * np.pi * radio * altura
area_superior = np.pi * radio**2
area_total = area_lateral + area_superior  # m²

# Inicialización
T = 20  # Temperatura inicial en °C
tiempos = [0]
temperaturas = [T]

# Simulación segundo a segundo
for t in range(1, tiempo_total + 1):
    perdida = U * area_total * (T - T_amb)  # Watts perdidos instantáneamente
    energia_neta = potencia - perdida  # Watts útiles
    if energia_neta < 0:
        energia_neta = 0
    dT = (energia_neta * dt) / (masa * calor_especifico)
    T += dT
    tiempos.append(t)
    temperaturas.append(T) # type: ignore
    if T >= 100:
        break  # Alcanzamos 100°C

if __name__ == "__main__":
    # Código para ejecutar el gráfico
    plt.figure(figsize=(10,6))
    
    # Convertir tiempos a minutos para el eje X
    tiempos_min_plot = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min_plot, temperaturas, label="Temperatura del agua")
    plt.axhline(100, color='r', linestyle='--', label="100 °C")
    plt.title('Curva de Temperatura con Pérdidas de Calor Reales')
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
