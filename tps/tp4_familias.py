"""
TP 4: Generar familias de curvas con distribuciones normales y uniformes de parámetros iniciales
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from utils.heat_simulation import HeatSimulationParameters, HeatSimulator


class ParameterDistribution:
    """Clase para generar distribuciones de parámetros."""
    
    @staticmethod
    def distribucion_uniforme_resistencias(n: int = 5, base: float = 0.4, variacion: float = 0.05) -> List[float]:
        """Genera n valores de resistencia con distribución uniforme."""
        min_val = base - variacion
        max_val = base + variacion
        return np.random.uniform(min_val, max_val, n).tolist()
    
    @staticmethod
    def distribucion_normal_temperatura_inicial(n: int = 5, media: float = 10, std: float = 5) -> List[float]:
        """Genera n temperaturas iniciales con distribución normal."""
        return np.random.normal(media, std, n).tolist()
    
    @staticmethod
    def distribucion_uniforme_temperatura_ambiente(n: int = 8, min_temp: float = -20, max_temp: float = 50) -> List[float]:
        """Genera n temperaturas ambiente con distribución uniforme."""
        return np.random.uniform(min_temp, max_temp, n).tolist()
    
    @staticmethod
    def distribucion_normal_tension(n: int = 5, media: float = 12, std: float = 4) -> List[float]:
        """Genera n tensiones con distribución normal."""
        return np.random.normal(media, std, n).tolist()


class HeatPlotter:
    """Clase para generar gráficos de las simulaciones."""
    
    @staticmethod
    def plot_family_curves(simulaciones: List[Tuple], titulo: str):
        """
        Genera gráfico de familia de curvas.
        
        Args:
            simulaciones: Lista de tuplas (tiempos, temperaturas, etiqueta)
            titulo: Título del gráfico
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Generar un color diferente para cada curva usando colores predefinidos
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
        for i, (tiempos, temperaturas, etiqueta) in enumerate(simulaciones):
            # Convertir tiempos a minutos para el eje X
            tiempos_min = np.array(tiempos) / 60.0
            color = colors[i % len(colors)]  # Ciclar colores si hay más de 10 curvas
            ax.plot(tiempos_min, temperaturas, 
                   color=color, linewidth=2, 
                   label=etiqueta, alpha=0.8)
        
        ax.set_xlabel('Tiempo (minutos)', fontsize=12)
        ax.set_ylabel('Temperatura (°C)', fontsize=12)
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.show()
        
        return fig


def ejecutar_tp4_resistencias():
    """4.A: Distribución uniforme de 5 valores próximos de resistencias."""
    print("=== TP4.A - Distribución Uniforme de Resistencias ===")
    print("Generando 5 valores de resistencia con distribución uniforme...")
    
    # Generar 5 valores de resistencia con distribución uniforme
    resistencias = ParameterDistribution.distribucion_uniforme_resistencias(n=5, base=0.4, variacion=0.05)
    
    simulaciones = []
    
    for i, resistencia in enumerate(resistencias):
        # Crear parámetros con resistencia específica
        params = HeatSimulationParameters(resistencia=resistencia)
        # Actualizar potencia basada en tensión y resistencia
        params.actualizar_potencia_desde_tension(params.tension)
        
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(parar_en_100c=True)
        
        etiqueta = f"R = {resistencia:.3f} Ω (P = {params.potencia:.0f} W)"
        simulaciones.append((tiempos, temperaturas, etiqueta))
        print(f"  Simulación {i+1}: R = {resistencia:.3f} Ω, P = {params.potencia:.0f} W")
    
    print("\nGenerando gráfico de familias de curvas...")
    fig = HeatPlotter.plot_family_curves(
        simulaciones, 
        "TP4.A - Familia de Curvas con Distribución Uniforme de Resistencias"
    )
    
    return fig, simulaciones


def ejecutar_tp4_temperaturas_iniciales():
    """4.B: Distribución normal de temperaturas iniciales (μ=10, σ=5)."""
    print("=== TP4.B - Distribución Normal de Temperaturas Iniciales ===")
    print("Generando temperaturas iniciales con distribución normal (μ=10°C, σ=5°C)...")
    
    # Generar temperaturas iniciales con distribución normal
    temps_iniciales = ParameterDistribution.distribucion_normal_temperatura_inicial(n=5, media=10, std=5)
    
    simulaciones = []
    
    for i, temp_inicial in enumerate(temps_iniciales):
        # Crear parámetros con temperatura inicial específica
        params = HeatSimulationParameters(T_inicial=temp_inicial)
        
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(parar_en_100c=True)
        
        etiqueta = f"T₀ = {temp_inicial:.1f} °C"
        simulaciones.append((tiempos, temperaturas, etiqueta))
        print(f"  Simulación {i+1}: T₀ = {temp_inicial:.1f} °C")
    
    print("\nGenerando gráfico de familias de curvas...")
    fig = HeatPlotter.plot_family_curves(
        simulaciones, 
        "TP4.B - Familia de Curvas con Distribución Normal de Temperaturas Iniciales"
    )
    
    return fig, simulaciones


def ejecutar_tp4_temperaturas_ambiente():
    """4.C: Distribución uniforme de temperaturas ambiente (-20°C a 50°C)."""
    print("=== TP4.C - Distribución Uniforme de Temperaturas Ambiente ===")
    print("Generando temperaturas ambiente con distribución uniforme (-20°C a 50°C)...")
    
    # Generar temperaturas ambiente con distribución uniforme
    temps_ambiente = ParameterDistribution.distribucion_uniforme_temperatura_ambiente(n=8, min_temp=-20, max_temp=50)
    
    simulaciones = []
    
    for i, temp_ambiente in enumerate(temps_ambiente):
        # Crear parámetros con temperatura ambiente específica
        params = HeatSimulationParameters(T_amb=temp_ambiente)
        
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(parar_en_100c=True)
        
        etiqueta = f"T_amb = {temp_ambiente:.1f} °C"
        simulaciones.append((tiempos, temperaturas, etiqueta))
        print(f"  Simulación {i+1}: T_ambiente = {temp_ambiente:.1f} °C")
    
    print("\nGenerando gráfico de familias de curvas...")
    fig = HeatPlotter.plot_family_curves(
        simulaciones, 
        "TP4.C - Familia de Curvas con Distribución Uniforme de Temperaturas Ambiente"
    )
    
    return fig, simulaciones


def ejecutar_tp4_tensiones_12v():
    """4.D: Distribución normal de tensiones cercanas a 12V (μ=12, σ=4)."""
    print("=== TP4.D - Distribución Normal de Tensiones (12V) ===")
    print("Generando tensiones con distribución normal (μ=12V, σ=4V)...")
    
    # Generar tensiones con distribución normal
    tensiones = ParameterDistribution.distribucion_normal_tension(n=5, media=12, std=4)
    
    simulaciones = []
    print(f"{'Tensión (V)':<12} {'Potencia (W)':<12} {'Tiempo (min)':<12} {'Temp Final (°C)':<12}")
    print("-" * 50)
    
    for i, tension in enumerate(tensiones):
        # Crear parámetros con tensión específica
        params = HeatSimulationParameters()
        params.actualizar_potencia_desde_tension(tension)
        
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(parar_en_100c=True)
        
        etiqueta = f"V = {tension:.1f} V (P = {params.potencia:.0f} W)"
        simulaciones.append((tiempos, temperaturas, etiqueta))
        
        tiempo_min = len(tiempos) * params.dt / 60  # Convertir a minutos
        temp_final = temperaturas[-1]
        print(f"{tension:<12.1f} {params.potencia:<12.0f} {tiempo_min:<12.2f} {temp_final:<12.2f}")
    
    print("\nGenerando gráfico de familias de curvas...")
    fig = HeatPlotter.plot_family_curves(
        simulaciones, 
        "TP4.D - Familia de Curvas con Distribución Normal de Tensiones (12V)"
    )
    
    return fig, simulaciones


def mostrar_info_tp4():
    """Muestra información detallada sobre TP4."""
    print("=== Información del TP4 - Familias de Curvas ===")
    print()
    print("Este módulo implementa la generación de familias de curvas de")
    print("temperatura utilizando distribuciones estadísticas de los parámetros")
    print("de entrada del sistema de calentamiento.")
    print()
    print("Funcionalidades disponibles:")
    print("• TP4.A: Distribución uniforme de resistencias (5 valores)")
    print("• TP4.B: Distribución normal de temperaturas iniciales (μ=10, σ=5)")
    print("• TP4.C: Distribución uniforme de temperaturas ambiente (-20 a 50°C)")
    print("• TP4.D: Distribución normal de tensiones 12V (μ=12, σ=4)")
    print()
    print("Propósito académico:")
    print("- Análisis de sensibilidad paramétrica")
    print("- Estudio del impacto de variaciones en parámetros")
    print("- Aplicación de distribuciones estadísticas")
    print("- Visualización de familias de curvas")
    print()
    print("Distribuciones utilizadas:")
    print("- Uniforme: Valores equidistribuidos en un rango")
    print("- Normal (Gaussiana): Concentrados alrededor de la media")


if __name__ == "__main__":
    # Menú de prueba para ejecución directa
    print("=== TP4 - Familias de Curvas con Distribuciones ===")
    print("1. Distribución uniforme de resistencias")
    print("2. Distribución normal de temperaturas iniciales")
    print("3. Distribución uniforme de temperaturas ambiente")
    print("4. Distribución normal de tensiones (12V)")
    print("5. Información del TP4")
    
    try:
        opcion = input("\nSeleccione una opción (1-5): ")
        
        if opcion == "1":
            ejecutar_tp4_resistencias()
        elif opcion == "2":
            ejecutar_tp4_temperaturas_iniciales()
        elif opcion == "3":
            ejecutar_tp4_temperaturas_ambiente()
        elif opcion == "4":
            ejecutar_tp4_tensiones_12v()
        elif opcion == "5":
            mostrar_info_tp4()
        else:
            print("Opción no válida.")
            
    except KeyboardInterrupt:
        print("\nEjecución cancelada.")
