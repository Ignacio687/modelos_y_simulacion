import numpy as np
import matplotlib.pyplot as plt

# Importar los datos y configuraciones de ambos gráficos
from heat_graph import tiempos as tiempos1, temperaturas as temperaturas1
from heat_loss_graph import tiempos as tiempos2, temperaturas as temperaturas2
from heat_loss_with_ice_graph import tiempos as tiempos3, temperaturas as temperaturas3

# Crear un gráfico comparativo
plt.figure(figsize=(12, 8))

# Gráfico 1
plt.plot(tiempos1, temperaturas1, label="Sin pérdidas de calor", linestyle='-', color='blue')

# Gráfico 2
plt.plot(tiempos2, temperaturas2, label="Con pérdidas de calor", linestyle='--', color='orange')

# Gráfico 3
plt.plot(tiempos3, temperaturas3, label="Con pérdidas de calor y hielo", linestyle='-.', color='green')

# Configuración del gráfico
plt.title('Comparación de Curvas de Temperatura')
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.legend()
plt.xlim(0, max(max(tiempos1), max(tiempos2), max(tiempos3)) * 1)  # Aumentar la escala del eje x
plt.show()