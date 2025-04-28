import matplotlib.pyplot as plt

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
    plt.plot(tiempos, temperaturas, label="Temperatura del agua")
    plt.axhline(100, color='r', linestyle='--', label="100 °C")
    plt.title('Curva de Temperatura sin Pérdidas de Calor')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.legend()
    plt.show()
