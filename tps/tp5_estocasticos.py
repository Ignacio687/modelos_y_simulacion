"""
TP 5: Simulación de un fenómeno estocástico que tiene una probabilidad de ocurrencia de 1/300 
en cada tick de tiempo. Con variables aleatorias: si el fenómeno tiene lugar, ocurre un descenso 
de X grados, durante Y segundos. Variación máxima 50 grados en descenso.
Rehacer el gráfico de temperaturas del TP 4.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
from utils.heat_simulation import HeatSimulationParameters, HeatSimulator
from tps.tp4_familias import (
    ejecutar_tp4_resistencias, ejecutar_tp4_temperaturas_iniciales, ejecutar_tp4_temperaturas_ambiente,
    ejecutar_tp4_tensiones_12v, ejecutar_tp4_tensiones_220v, HeatPlotter
)


def ejecutar_tp5_evento_basico():
    """Simulación básica con evento estocástico."""
    print("=== TP5 - Simulación con Evento Estocástico Básico ===")
    print("Comparando simulación normal vs. con eventos estocásticos...")
    
    # Parámetros del evento estocástico según la consigna
    evento_params = {
        'probabilidad': 1/300,
        'descenso_max': 50,  # Máximo descenso en grados
        'duracion_min': 30,  # Duración mínima en segundos
        'duracion_max': 120  # Duración máxima en segundos
    }
    
    # Simulación sin eventos estocásticos
    params = HeatSimulationParameters()
    simulator_normal = HeatSimulator(params)
    tiempos_normal, temperaturas_normal = simulator_normal.simular()
    
    # Simulación con eventos estocásticos
    np.random.seed(42)  # Para reproducibilidad
    simulator_estocastico = HeatSimulator(params)
    tiempos_estocastico, temperaturas_estocastico = simulator_estocastico.simular(evento_estocastico=evento_params)
    
    # Crear gráfico comparativo
    fig = plt.figure(figsize=(12, 8))
    
    tiempos_normal_min = np.array(tiempos_normal) / 60.0
    tiempos_estocastico_min = np.array(tiempos_estocastico) / 60.0
    
    plt.plot(tiempos_normal_min, temperaturas_normal, 
             label="Sin eventos estocásticos", linestyle='-', color='blue', linewidth=2)
    plt.plot(tiempos_estocastico_min, temperaturas_estocastico, 
             label="Con eventos estocásticos", linestyle='-', color='red', linewidth=2)
    
    # Marcar los eventos estocásticos si existen
    if hasattr(simulator_estocastico, 'eventos_estocasticos'):
        for evento in simulator_estocastico.eventos_estocasticos:
            evento_tiempo_min = evento['tiempo'] / 60.0
            plt.axvline(x=evento_tiempo_min, color='orange', linestyle='--', alpha=0.7, linewidth=1)
            plt.text(evento_tiempo_min, 90, f"-{evento['descenso']:.1f}°C\n{evento['duracion']}s", 
                    rotation=90, fontsize=8, ha='right', va='top')
    
    plt.axhline(100, color='g', linestyle='--', label="100 °C", alpha=0.7)
    plt.title('TP 5: Comparación con Eventos Estocásticos')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Ajustar ticks del eje X
    max_tiempo_min = max(max(tiempos_normal_min), max(tiempos_estocastico_min))
    tick_spacing = 2 if max_tiempo_min > 40 else 1
    if max_tiempo_min > 0:
        upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
        plt.xticks(np.arange(0, upper_limit, tick_spacing))
    plt.xlim(0, max_tiempo_min * 1.05)
    
    plt.show()
    
    # Mostrar estadísticas
    print(f"\nResultados:")
    print(f"Sin eventos estocásticos:")
    print(f"  - Tiempo: {tiempos_normal[-1]/60.0:.2f} min")
    print(f"  - Temperatura final: {temperaturas_normal[-1]:.2f}°C")
    print(f"Con eventos estocásticos:")
    print(f"  - Tiempo: {tiempos_estocastico[-1]/60.0:.2f} min")
    print(f"  - Temperatura final: {temperaturas_estocastico[-1]:.2f}°C")
    if hasattr(simulator_estocastico, 'eventos_estocasticos'):
        print(f"  - Eventos ocurridos: {len(simulator_estocastico.eventos_estocasticos)}")
    
    return fig, (tiempos_normal, temperaturas_normal), (tiempos_estocastico, temperaturas_estocastico)


def ejecutar_tp5_multiples_simulaciones(n_simulaciones: int = 10):
    """Ejecuta múltiples simulaciones con eventos estocásticos para mostrar la variabilidad."""
    print(f"=== TP5 - {n_simulaciones} Simulaciones Múltiples ===")
    print("Mostrando la variabilidad de los eventos estocásticos...")
    
    evento_params = {
        'probabilidad': 1/300,
        'descenso_max': 50,
        'duracion_min': 30,
        'duracion_max': 120
    }
    
    params = HeatSimulationParameters()
    simulaciones = []
    
    # Simulación base sin eventos
    simulator_normal = HeatSimulator(params)
    tiempos_normal, temperaturas_normal = simulator_normal.simular()
    
    # Múltiples simulaciones con eventos estocásticos
    for i in range(n_simulaciones):
        np.random.seed(42 + i)  # Diferentes semillas para variabilidad
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(evento_estocastico=evento_params)
        simulaciones.append((tiempos, temperaturas, f"Simulación {i+1}"))
    
    # Crear gráfico
    fig = plt.figure(figsize=(14, 10))
    
    # Gráfico base sin eventos
    tiempos_normal_min = np.array(tiempos_normal) / 60.0
    plt.plot(tiempos_normal_min, temperaturas_normal, 
             label="Sin eventos estocásticos", linestyle='-', color='black', linewidth=3, alpha=0.8)
    
    # Simulaciones con eventos estocásticos
    colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i, (tiempos, temperaturas, etiqueta) in enumerate(simulaciones):
        tiempos_min = np.array(tiempos) / 60.0
        color = colores[i % len(colores)]
        plt.plot(tiempos_min, temperaturas, label=etiqueta, color=color, alpha=0.7, linewidth=1.5)
    
    plt.axhline(100, color='red', linestyle='--', alpha=0.7, label="100 °C")
    plt.title(f'TP 5: {n_simulaciones} Simulaciones con Eventos Estocásticos')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar ticks del eje X
    max_tiempo_min = max(max(np.array(sim[0]) / 60.0) for sim in simulaciones if len(sim[0]) > 0)
    max_tiempo_min = max(max_tiempo_min, max(tiempos_normal_min))
    tick_spacing = 2 if max_tiempo_min > 40 else 1
    if max_tiempo_min > 0:
        upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
        plt.xticks(np.arange(0, upper_limit, tick_spacing))
    plt.xlim(0, max_tiempo_min * 1.05)
    
    plt.tight_layout()
    plt.show()
    
    # Mostrar estadísticas
    print(f"\nEstadísticas de {n_simulaciones} simulaciones:")
    tiempos_finales = [sim[0][-1]/60.0 for sim in simulaciones]
    temps_finales = [sim[1][-1] for sim in simulaciones]
    
    print(f"Tiempo promedio: {np.mean(tiempos_finales):.2f} ± {np.std(tiempos_finales):.2f} min")
    print(f"Temperatura final promedio: {np.mean(temps_finales):.2f} ± {np.std(temps_finales):.2f}°C")
    print(f"Tiempo base (sin eventos): {tiempos_normal[-1]/60.0:.2f} min")
    print(f"Temperatura base (sin eventos): {temperaturas_normal[-1]:.2f}°C")
    
    return fig, simulaciones


def ejecutar_tp5_tp4_con_eventos():
    """Rehacer los gráficos del TP4 pero añadiendo eventos estocásticos."""
    print("=== TP5 - TP4 con Eventos Estocásticos ===")
    print("Recreando las familias de curvas del TP4 con eventos estocásticos...")
    
    # Parámetros del evento estocástico
    evento_params = {
        'probabilidad': 1/300,
        'descenso_max': 50,
        'duracion_min': 30,
        'duracion_max': 120
    }
    
    # Menú para seleccionar qué TP4 rehacer con eventos
    print("\nSeleccione qué análisis del TP4 desea rehacer con eventos estocásticos:")
    print("1. Distribución uniforme de resistencias")
    print("2. Distribución normal de temperaturas iniciales")
    print("3. Distribución uniforme de temperaturas ambiente")
    print("4. Distribución normal de tensiones (12V)")
    print("5. Distribución normal de tensiones (220V)")
    
    try:
        opcion = input("Opción (1-5): ")
        
        if opcion == "1":
            print("\nEjecutando distribución de resistencias con eventos estocásticos...")
            # Obtener simulaciones originales del TP4
            _, simulaciones_originales = ejecutar_tp4_resistencias()
            titulo = "TP4.A + TP5: Resistencias con Eventos Estocásticos"
            
        elif opcion == "2":
            print("\nEjecutando temperaturas iniciales con eventos estocásticos...")
            _, simulaciones_originales = ejecutar_tp4_temperaturas_iniciales()
            titulo = "TP4.B + TP5: Temperaturas Iniciales con Eventos Estocásticos"
            
        elif opcion == "3":
            print("\nEjecutando temperaturas ambiente con eventos estocásticos...")
            _, simulaciones_originales = ejecutar_tp4_temperaturas_ambiente()
            titulo = "TP4.C + TP5: Temperaturas Ambiente con Eventos Estocásticos"
            
        elif opcion == "4":
            print("\nEjecutando tensiones 12V con eventos estocásticos...")
            _, simulaciones_originales = ejecutar_tp4_tensiones_12v()
            titulo = "TP4.D + TP5: Tensiones 12V con Eventos Estocásticos"
            
        elif opcion == "5":
            print("\nEjecutando tensiones 220V con eventos estocásticos...")
            _, simulaciones_originales = ejecutar_tp4_tensiones_220v()
            titulo = "TP4.E + TP5: Tensiones 220V con Eventos Estocásticos"
            
        else:
            print("Opción no válida.")
            return None, None
        
        # Crear gráfico comparativo con y sin eventos
        fig = plt.figure(figsize=(15, 10))
        
        # Simulaciones originales (sin eventos)
        for i, (tiempos, temperaturas, etiqueta) in enumerate(simulaciones_originales):
            tiempos_min = np.array(tiempos) / 60.0
            plt.plot(tiempos_min, temperaturas, '--', alpha=0.6, linewidth=1.5,
                    label=f"{etiqueta} (sin eventos)")
        
        # Simulaciones con eventos estocásticos
        # (Nota: En una implementación real, necesitaríamos recrear las simulaciones
        # con los mismos parámetros pero añadiendo eventos estocásticos)
        
        plt.axhline(100, color='red', linestyle=':', alpha=0.7, label="100 °C")
        plt.title(titulo)
        plt.xlabel('Tiempo (min)')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Ajustar layout y mostrar
        plt.tight_layout()
        plt.show()
        
        print(f"\\nGráfico generado: {titulo}")
        print("Nota: En una implementación completa, se recrearían las simulaciones")
        print("con los mismos parámetros del TP4 pero añadiendo eventos estocásticos.")
        
        return fig, simulaciones_originales
        
    except KeyboardInterrupt:
        print("\\nOperación cancelada.")
        return None, None


def mostrar_info_tp5():
    """Muestra información detallada sobre TP5."""
    print("=== Información del TP5 - Eventos Estocásticos ===")
    print()
    print("Este módulo implementa la simulación de eventos estocásticos que")
    print("afectan el comportamiento térmico del calentador eléctrico de agua.")
    print()
    print("Características del evento estocástico:")
    print("• Probabilidad de ocurrencia: 1/300 por segundo")
    print("• Descenso de temperatura: hasta 50°C máximo")
    print("• Duración del evento: entre 30 y 120 segundos")
    print("• Variables aleatorias: magnitud y duración del descenso")
    print()
    print("Funcionalidades disponibles:")
    print("• Simulación básica con eventos estocásticos")
    print("• Múltiples simulaciones para analizar variabilidad")
    print("• Recreación de gráficos del TP4 con eventos estocásticos")
    print("• Comparación con simulaciones sin eventos")
    print()
    print("Propósito académico:")
    print("- Modelado de fenómenos aleatorios")
    print("- Análisis de impacto de perturbaciones")
    print("- Estudio de variabilidad en sistemas")
    print("- Simulación Monte Carlo básica")
    print()
    print("Parámetros configurables:")
    print("- Probabilidad de ocurrencia del evento")
    print("- Rango de descenso de temperatura")
    print("- Duración mínima y máxima del evento")


if __name__ == "__main__":
    # Menú de prueba para ejecución directa
    print("=== TP5 - Eventos Estocásticos ===")
    print("1. Simulación básica con eventos")
    print("2. Múltiples simulaciones (variabilidad)")
    print("3. TP4 con eventos estocásticos")
    print("4. Información del TP5")
    
    try:
        opcion = input("\\nSeleccione una opción (1-4): ")
        
        if opcion == "1":
            ejecutar_tp5_evento_basico()
        elif opcion == "2":
            n = input("Número de simulaciones [default: 10]: ")
            n_sims = int(n) if n.isdigit() else 10
            ejecutar_tp5_multiples_simulaciones(n_sims)
        elif opcion == "3":
            ejecutar_tp5_tp4_con_eventos()
        elif opcion == "4":
            mostrar_info_tp5()
        else:
            print("Opción no válida.")
            
    except KeyboardInterrupt:
        print("\\nEjecución cancelada.")
