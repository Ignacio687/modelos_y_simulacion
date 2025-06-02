"""
Demostración completa del código modularizado para los TPs 4 y 5.
Este archivo muestra cómo usar todas las clases y funciones creadas.
"""
import numpy as np
import matplotlib.pyplot as plt
from heat_simulation import (
    HeatSimulationParameters, 
    HeatSimulator, 
    HeatPlotter, 
    ParameterDistribution,
    simular_calentamiento_basico,
    simular_con_evento_estocastico
)
from tp4_parameter_families import ejecutar_tp4
from tp5_stochastic_events import ejecutar_tp5


def demo_simulacion_basica():
    """Demuestra el uso básico del simulador."""
    print("=== DEMO: Simulación Básica ===")
    
    # Crear parámetros personalizados
    params = HeatSimulationParameters(
        masa=1.5,  # 1.5 kg de agua
        T_inicial=15,  # Empezar a 15°C
        T_amb=25,  # Ambiente a 25°C
        potencia=500  # Calefactor de 500W
    )
    
    # Ejecutar simulación
    tiempos, temperaturas = simular_calentamiento_basico(params)
    
    # Graficar
    fig = HeatPlotter.plot_single_simulation(
        tiempos, temperaturas,
        titulo="Demo: Simulación Personalizada",
        etiqueta="Agua 1.5kg, 500W, T₀=15°C"
    )
    plt.show()
    
    print(f"Tiempo para alcanzar 100°C: {tiempos[-1]/60:.1f} minutos")


def demo_comparacion_potencias():
    """Compara diferentes potencias de calefactores."""
    print("=== DEMO: Comparación de Potencias ===")
    
    potencias = [200, 360, 500, 800, 1200]  # Watts
    simulaciones = []
    
    for potencia in potencias:
        params = HeatSimulationParameters(potencia=potencia)
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular()
        etiqueta = f"{potencia}W"
        simulaciones.append((tiempos, temperaturas, etiqueta))
    
    fig = HeatPlotter.plot_family_curves(
        simulaciones,
        titulo="Comparación de Potencias de Calefactores"
    )
    plt.show()


def demo_efecto_temperatura_ambiente():
    """Demuestra el efecto de la temperatura ambiente."""
    print("=== DEMO: Efecto de Temperatura Ambiente ===")
    
    temps_ambiente = [-10, 0, 10, 20, 30, 40]  # °C
    simulaciones = []
    
    for temp_amb in temps_ambiente:
        params = HeatSimulationParameters(T_amb=temp_amb)
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular()
        etiqueta = f"T_amb = {temp_amb}°C"
        simulaciones.append((tiempos, temperaturas, etiqueta))
    
    fig = HeatPlotter.plot_family_curves(
        simulaciones,
        titulo="Efecto de la Temperatura Ambiente"
    )
    plt.show()


def demo_eventos_estocasticos():
    """Demuestra diferentes configuraciones de eventos estocásticos."""
    print("=== DEMO: Eventos Estocásticos ===")
    
    # Configuraciones de eventos
    configuraciones = [
        {"probabilidad": 1/500, "descenso_max": 20, "duracion_min": 20, "duracion_max": 60},
        {"probabilidad": 1/300, "descenso_max": 50, "duracion_min": 30, "duracion_max": 120},
        {"probabilidad": 1/200, "descenso_max": 30, "duracion_min": 40, "duracion_max": 80}
    ]
    
    params = HeatSimulationParameters()
    simulaciones = []
    
    # Simulación sin eventos
    tiempos_normal, temperaturas_normal = simular_calentamiento_basico(params)
    simulaciones.append((tiempos_normal, temperaturas_normal, "Sin eventos"))
    
    # Simulaciones con diferentes eventos
    for i, config in enumerate(configuraciones):
        np.random.seed(42 + i)  # Para reproducibilidad
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular(evento_estocastico=config)
        etiqueta = f"Eventos: P={config['probabilidad']:.4f}, Max={config['descenso_max']}°C"
        simulaciones.append((tiempos, temperaturas, etiqueta))
    
    fig = HeatPlotter.plot_family_curves(
        simulaciones,
        titulo="Comparación de Configuraciones de Eventos Estocásticos"
    )
    plt.show()


def demo_tension_resistencia():
    """Demuestra el cálculo de potencia desde tensión y resistencia."""
    print("=== DEMO: Cálculo desde Tensión y Resistencia ===")
    
    # Diferentes tensiones con resistencia fija
    tensiones = [110, 120, 220, 240]  # Voltios
    resistencia = 50  # Ohms
    simulaciones = []
    
    for tension in tensiones:
        params = HeatSimulationParameters(tension=tension, resistencia=resistencia)
        params.usar_tension_resistencia = True
        params._calcular_parametros_derivados()
        
        simulator = HeatSimulator(params)
        tiempos, temperaturas = simulator.simular()
        etiqueta = f"{tension}V → {params.potencia:.0f}W"
        simulaciones.append((tiempos, temperaturas, etiqueta))
    
    fig = HeatPlotter.plot_family_curves(
        simulaciones,
        titulo=f"Efecto de la Tensión (R = {resistencia}Ω)"
    )
    plt.show()


def demo_estadisticas_eventos():
    """Analiza estadísticas de eventos estocásticos."""
    print("=== DEMO: Estadísticas de Eventos ===")
    
    params = HeatSimulationParameters()
    evento_config = {
        'probabilidad': 1/300,
        'descenso_max': 50,
        'duracion_min': 30,
        'duracion_max': 120
    }
    
    # Ejecutar múltiples simulaciones
    n_simulaciones = 50
    eventos_por_simulacion = []
    tiempo_promedio_eventos = []
    descenso_promedio = []
    
    for i in range(n_simulaciones):
        np.random.seed(1000 + i)
        simulator = HeatSimulator(params)
        simulator.simular(evento_estocastico=evento_config)
        
        n_eventos = len(simulator.eventos_estocasticos)
        eventos_por_simulacion.append(n_eventos)
        
        if n_eventos > 0:
            tiempos_eventos = [e['tiempo'] for e in simulator.eventos_estocasticos]
            descensos = [e['descenso'] for e in simulator.eventos_estocasticos]
            tiempo_promedio_eventos.extend(tiempos_eventos)
            descenso_promedio.extend(descensos)
    
    # Crear gráficos de estadísticas
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Histograma de número de eventos por simulación
    axes[0,0].hist(eventos_por_simulacion, bins=range(max(eventos_por_simulacion)+2), 
                   alpha=0.7, edgecolor='black')
    axes[0,0].set_title("Número de Eventos por Simulación")
    axes[0,0].set_xlabel("Número de eventos")
    axes[0,0].set_ylabel("Frecuencia")
    axes[0,0].grid(True, alpha=0.3)
    
    # Distribución temporal de eventos
    if tiempo_promedio_eventos:
        axes[0,1].hist(np.array(tiempo_promedio_eventos)/60, bins=20, 
                       alpha=0.7, edgecolor='black', color='orange')
        axes[0,1].set_title("Distribución Temporal de Eventos")
        axes[0,1].set_xlabel("Tiempo (min)")
        axes[0,1].set_ylabel("Frecuencia")
        axes[0,1].grid(True, alpha=0.3)
    
    # Distribución de magnitud de descensos
    if descenso_promedio:
        axes[1,0].hist(descenso_promedio, bins=20, alpha=0.7, 
                       edgecolor='black', color='red')
        axes[1,0].set_title("Distribución de Descensos")
        axes[1,0].set_xlabel("Descenso (°C)")
        axes[1,0].set_ylabel("Frecuencia")
        axes[1,0].grid(True, alpha=0.3)
    
    # Estadísticas textuales
    axes[1,1].axis('off')
    stats_text = f"""
Estadísticas de {n_simulaciones} simulaciones:

Eventos promedio por simulación: {np.mean(eventos_por_simulacion):.2f}
Desviación estándar: {np.std(eventos_por_simulacion):.2f}
Simulaciones sin eventos: {eventos_por_simulacion.count(0)}

Probabilidad teórica: {evento_config['probabilidad']:.6f}
Eventos esperados en 2500s: {2500 * evento_config['probabilidad']:.2f}

Descenso promedio: {np.mean(descenso_promedio):.1f}°C
Descenso máximo observado: {max(descenso_promedio) if descenso_promedio else 0:.1f}°C
    """
    axes[1,1].text(0.1, 0.9, stats_text, transform=axes[1,1].transAxes, 
                   fontsize=12, verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.suptitle("Análisis Estadístico de Eventos Estocásticos", y=1.02, fontsize=16)
    plt.show()


def ejecutar_demo_completo():
    """Ejecuta toda la demostración."""
    print("=" * 50)
    print("DEMOSTRACIÓN COMPLETA DEL CÓDIGO MODULARIZADO")
    print("=" * 50)
    
    # Demostraciones básicas
    demo_simulacion_basica()
    demo_comparacion_potencias()
    demo_efecto_temperatura_ambiente()
    demo_tension_resistencia()
    demo_eventos_estocasticos()
    demo_estadisticas_eventos()
    
    print("\n" + "=" * 50)
    print("EJECUTANDO TP 4 COMPLETO")
    print("=" * 50)
    ejecutar_tp4()
    
    print("\n" + "=" * 50)
    print("EJECUTANDO TP 5 COMPLETO")
    print("=" * 50)
    ejecutar_tp5()
    
    print("\n" + "=" * 50)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 50)


if __name__ == "__main__":
    ejecutar_demo_completo()
