"""
Test script sin gráficos para verificar que todo el código modularizado funciona correctamente.
"""
import numpy as np
from heat_simulation import (
    HeatSimulationParameters, 
    HeatSimulator, 
    HeatPlotter,
    ParameterDistribution,
    simular_calentamiento_basico
)
from tp4_parameter_families import (
    tp4a_resistencias, tp4b_temperaturas_iniciales, 
    tp4c_temperaturas_ambiente, tp4d_tensiones_12v
)
from tp5_stochastic_events import tp5_evento_estocastico_basico


def test_simulacion_basica():
    """Prueba la simulación básica."""
    print("✓ Probando simulación básica...")
    
    tiempos, temperaturas = simular_calentamiento_basico()
    assert len(tiempos) > 0, "No se generaron datos de tiempo"
    assert len(temperaturas) > 0, "No se generaron datos de temperatura"
    assert temperaturas[-1] >= 100, "No se alcanzó 100°C"
    
    print(f"  Tiempo final: {tiempos[-1]/60:.1f} min, Temp final: {temperaturas[-1]:.1f}°C")
    return True


def test_parametros_personalizados():
    """Prueba simulación con parámetros personalizados."""
    print("✓ Probando parámetros personalizados...")
    
    params = HeatSimulationParameters(masa=0.5, potencia=800, T_inicial=10)
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular()
    
    assert len(tiempos) > 0, "No se generaron datos"
    assert temperaturas[0] == 10, "Temperatura inicial incorrecta"
    assert temperaturas[-1] >= 100, "No se alcanzó 100°C"
    
    print(f"  Masa: {params.masa}kg, Potencia: {params.potencia}W")
    return True


def test_eventos_estocasticos():
    """Prueba eventos estocásticos."""
    print("✓ Probando eventos estocásticos...")
    
    np.random.seed(42)
    params = HeatSimulationParameters()
    evento_config = {
        'probabilidad': 1/100,  # Alta probabilidad para garantizar eventos
        'descenso_max': 20,
        'duracion_min': 30,
        'duracion_max': 60
    }
    
    simulator = HeatSimulator(params)
    tiempos, temperaturas = simulator.simular(evento_estocastico=evento_config)
    
    assert len(simulator.eventos_estocasticos) > 0, "No se generaron eventos estocásticos"
    print(f"  Eventos detectados: {len(simulator.eventos_estocasticos)}")
    return True


def test_tp4_distribuciones():
    """Prueba las distribuciones del TP4."""
    print("✓ Probando distribuciones TP4...")
    
    # Test generación de distribuciones
    resistencias = ParameterDistribution.distribucion_uniforme_resistencias(5)
    temps_iniciales = ParameterDistribution.distribucion_normal_temperatura_inicial(5)
    temps_ambiente = ParameterDistribution.distribucion_uniforme_temperatura_ambiente(8)
    tensiones = ParameterDistribution.distribucion_normal_tension(5)
    
    assert len(resistencias) == 5, "Error en distribución de resistencias"
    assert len(temps_iniciales) == 5, "Error en distribución de temperaturas iniciales"
    assert len(temps_ambiente) == 8, "Error en distribución de temperaturas ambiente"
    assert len(tensiones) == 5, "Error en distribución de tensiones"
    
    print(f"  Resistencias: {len(resistencias)} valores")
    print(f"  Temps iniciales: {len(temps_iniciales)} valores") 
    print(f"  Temps ambiente: {len(temps_ambiente)} valores")
    print(f"  Tensiones: {len(tensiones)} valores")
    return True


def test_tp4_simulaciones():
    """Prueba simulaciones del TP4."""
    print("✓ Probando simulaciones TP4...")
    
    np.random.seed(42)
    
    # Test TP4A - cerrar gráficos inmediatamente
    import matplotlib.pyplot as plt
    plt.ioff()  # Turn off interactive mode
    
    fig, simulaciones = tp4a_resistencias()
    plt.close(fig)
    assert len(simulaciones) == 5, "Error en simulaciones de resistencias"
    
    fig, simulaciones = tp4b_temperaturas_iniciales()
    plt.close(fig)
    assert len(simulaciones) == 5, "Error en simulaciones de temperaturas iniciales"
    
    print(f"  TP4A: {len(simulaciones)} simulaciones de resistencias")
    print(f"  TP4B: {len(simulaciones)} simulaciones de temperaturas")
    return True


def test_tp5_eventos():
    """Prueba simulaciones del TP5.""" 
    print("✓ Probando simulaciones TP5...")
    
    np.random.seed(42)
    import matplotlib.pyplot as plt
    plt.ioff()  # Turn off interactive mode
    
    fig, normal, estocastico = tp5_evento_estocastico_basico()
    plt.close(fig)
    
    assert len(normal[0]) > 0, "Error en simulación normal"
    assert len(estocastico[0]) > 0, "Error en simulación estocástica"
    
    print(f"  Simulación normal: {len(normal[0])} puntos")
    print(f"  Simulación estocástica: {len(estocastico[0])} puntos")
    return True


def test_compatibilidad():
    """Prueba compatibilidad con código original."""
    print("✓ Probando compatibilidad...")
    
    from heat_loss_graph_modular import tiempos, temperaturas
    from heat_loss_graph import tiempos as tiempos_orig, temperaturas as temperaturas_orig
    
    diff = abs(temperaturas[-1] - temperaturas_orig[-1])
    assert diff < 0.1, f"Diferencia de temperatura demasiado grande: {diff}"
    
    print(f"  Diferencia de temperatura final: {diff:.6f}°C")
    return True


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests."""
    print("=" * 60)
    print("EJECUTANDO TESTS COMPLETOS DEL CÓDIGO MODULARIZADO")
    print("=" * 60)
    
    tests = [
        test_simulacion_basica,
        test_parametros_personalizados,
        test_eventos_estocasticos,
        test_tp4_distribuciones,
        test_tp4_simulaciones,
        test_tp5_eventos,
        test_compatibilidad
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Error en {test.__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTADOS: {passed} tests pasados, {failed} tests fallaron")
    
    if failed == 0:
        print("🎉 ¡TODOS LOS TESTS PASARON! El código modularizado funciona correctamente.")
        print("\nEl código está listo para usar en los TPs 4 y 5.")
        print("\nPara ejecutar los TPs completos:")
        print("  python tp4_parameter_families.py")
        print("  python tp5_stochastic_events.py")
        print("  python demo_completo.py")
    else:
        print("⚠️  Algunos tests fallaron. Revisar los errores arriba.")
    
    return failed == 0


if __name__ == "__main__":
    ejecutar_todos_los_tests()
