"""
Versión modularizada del heat_loss_graph.py original usando el nuevo código modular.
"""
import numpy as np
import matplotlib.pyplot as plt
from heat_simulation import HeatSimulationParameters, HeatSimulator, HeatPlotter


def generar_datos_como_original():
    """Genera los mismos datos que el heat_loss_graph.py original pero usando el código modular."""
    
    # Usar los mismos parámetros que el archivo original
    params = HeatSimulationParameters(
        masa=1.0,
        calor_especifico=4186,
        potencia=360,
        T_amb=20,
        T_inicial=20,
        tiempo_total=2500,
        dt=1.0,
        radio=0.05,
        altura=0.13,
        espesor_acero=0.001,
        espesor_poliuretano=0.001,
        k_acero=16,
        k_poliuretano=0.03
    )
    
    # Crear el simulador y ejecutar
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular()
    
    return tiempos, temperaturas


# Generar datos al importar el módulo (para compatibilidad)
tiempos, temperaturas = generar_datos_como_original()

if __name__ == "__main__":
    # Crear el gráfico usando el plotter modular
    fig = HeatPlotter.plot_single_simulation(
        tiempos, temperaturas,
        titulo='Curva de Temperatura con Pérdidas de Calor Reales (Modular)',
        etiqueta="Temperatura del agua"
    )
    
    plt.show()
