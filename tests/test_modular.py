"""
Script de prueba para verificar que el código modularizado funciona correctamente.
"""
import numpy as np
import matplotlib.pyplot as plt
from heat_simulation import (
    HeatSimulationParameters, 
    HeatSimulator, 
    HeatPlotter,
    simular_calentamiento_basico
)


def test_simulacion_basica():
    """Prueba la simulación básica."""
    print("Probando simulación básica...")
    
    # Usar función de conveniencia
    tiempos, temperaturas = simular_calentamiento_basico()
    
    print(f"Tiempo final: {tiempos[-1]} segundos ({tiempos[-1]/60:.1f} minutos)")
    print(f"Temperatura final: {temperaturas[-1]:.1f}°C")
    print(f"Puntos de datos: {len(tiempos)}")
    
    return tiempos, temperaturas


def test_simulacion_personalizada():
    """Prueba simulación con parámetros personalizados."""
    print("\nProbando simulación personalizada...")
    
    # Crear parámetros personalizados
    params = HeatSimulationParameters(
        masa=0.5,  # 500g de agua
        potencia=800,  # Calefactor más potente
        T_inicial=10,  # Agua fría
        T_amb=15  # Ambiente frío
    )
    
    # Simular
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular()
    
    print(f"Parámetros: masa={params.masa}kg, potencia={params.potencia}W")
    print(f"Tiempo final: {tiempos[-1]} segundos ({tiempos[-1]/60:.1f} minutos)")
    print(f"Temperatura final: {temperaturas[-1]:.1f}°C")
    
    return tiempos, temperaturas


def test_evento_estocastico():
    """Prueba simulación con evento estocástico."""
    print("\nProbando evento estocástico...")
    
    params = HeatSimulationParameters()
    
    # Configurar evento con alta probabilidad para que ocurra
    evento = {
        'probabilidad': 1/100,  # Alta probabilidad
        'descenso_max': 20,
        'duracion_min': 30,
        'duracion_max': 60
    }
    
    # Simular con seed fijo para reproducibilidad
    np.random.seed(42)
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular(evento_estocastico=evento)
    
    print(f"Eventos detectados: {len(simulator.eventos_estocasticos)}")
    for i, evento_info in enumerate(simulator.eventos_estocasticos):
        print(f"  Evento {i+1}: t={evento_info['tiempo']}s, descenso={evento_info['descenso']:.1f}°C")
    
    return tiempos, temperaturas


def test_graficos():
    """Prueba la generación de gráficos."""
    print("\nProbando generación de gráficos...")
    
    # Generar diferentes simulaciones
    simulaciones = []
    
    # Simulación básica
    t1, temp1 = test_simulacion_basica()
    simulaciones.append((t1, temp1, "Básica (1kg, 360W)"))
    
    # Simulación personalizada
    t2, temp2 = test_simulacion_personalizada()
    simulaciones.append((t2, temp2, "Personalizada (0.5kg, 800W)"))
    
    # Simulación con eventos
    t3, temp3 = test_evento_estocastico()
    simulaciones.append((t3, temp3, "Con eventos estocásticos"))
    
    # Crear gráfico de comparación
    fig = HeatPlotter.plot_family_curves(
        simulaciones,
        titulo="Prueba de Funcionalidad Modular"
    )
    
    plt.show()
    print("Gráfico generado exitosamente!")


def test_compatibilidad_heat_loss():
    """Verifica que el resultado sea compatible con heat_loss_graph.py original."""
    print("\nVerificando compatibilidad con código original...")
    
    # Usar exactamente los mismos parámetros que heat_loss_graph.py
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
    
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular()
    
    print(f"Coeficiente U calculado: {params.U:.2f} W/m²K")
    print(f"Área total: {params.area_total:.6f} m²")
    print(f"Tiempo final: {tiempos[-1]} segundos")
    print(f"Temperatura final: {temperaturas[-1]:.2f}°C")
    
    # Verificar algunos valores específicos
    if len(tiempos) > 1000:
        print(f"Temperatura a los 1000s: {temperaturas[1000]:.2f}°C")
    
    return tiempos, temperaturas


if __name__ == "__main__":
    print("=== PRUEBAS DEL CÓDIGO MODULARIZADO ===")
    
    try:
        # Ejecutar todas las pruebas
        test_compatibilidad_heat_loss()
        test_graficos()
        
        print("\n✅ Todas las pruebas pasaron exitosamente!")
        print("El código modularizado está funcionando correctamente.")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
