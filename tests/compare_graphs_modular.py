"""
Versión del compare_graphs.py que usa el código modularizado.
Demuestra que la modularización mantiene compatibilidad completa.
"""
import numpy as np
import matplotlib.pyplot as plt

# Importar los datos de las tres simulaciones
from heat_graph import tiempos as tiempos1, temperaturas as temperaturas1
from heat_loss_graph_modular import tiempos as tiempos2, temperaturas as temperaturas2  # Usar versión modular
from heat_loss_with_ice_graph import tiempos as tiempos3, temperaturas as temperaturas3

# Crear un gráfico comparativo
plt.figure(figsize=(12, 8))

# Convertir tiempos a minutos para el eje X para cada conjunto de datos
tiempos1_min = np.array(tiempos1) / 60.0
tiempos2_min = np.array(tiempos2) / 60.0
tiempos3_min = np.array(tiempos3) / 60.0

# Gráfico 1
plt.plot(tiempos1_min, temperaturas1, label="Sin pérdidas de calor", linestyle='-', color='blue')

# Gráfico 2 (usando versión modular)
plt.plot(tiempos2_min, temperaturas2, label="Con pérdidas de calor (Modular)", linestyle='--', color='orange')

# Gráfico 3
plt.plot(tiempos3_min, temperaturas3, label="Con pérdidas de calor y hielo", linestyle='-.', color='green')

# Configuración del gráfico
plt.title('Comparación de Curvas de Temperatura (Con Código Modular)')
plt.xlabel('Tiempo (min)')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.legend()

# Ajustar los ticks del eje X para que sean más legibles en minutos
max_tiempo_min_comparativo = max(max(tiempos1_min if tiempos1_min.size > 0 else [0]), 
                                 max(tiempos2_min if tiempos2_min.size > 0 else [0]), 
                                 max(tiempos3_min if tiempos3_min.size > 0 else [0]))

tick_spacing_comparativo = 2 if max_tiempo_min_comparativo > 40 else 1
if max_tiempo_min_comparativo == 0:
    plt.xticks([0])
else:
    upper_limit_comparativo = np.ceil(max_tiempo_min_comparativo / tick_spacing_comparativo) * tick_spacing_comparativo + tick_spacing_comparativo / 2
    plt.xticks(np.arange(0, upper_limit_comparativo, tick_spacing_comparativo))

plt.xlim(0, max_tiempo_min_comparativo * 1.05)

if __name__ == "__main__":
    plt.show()
