#!/usr/bin/env python3
"""
Script de prueba final para verificar que todos los TPs funcionan correctamente.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_imports():
    """Prueba que todos los imports funcionen correctamente."""
    print("=== PRUEBA DE IMPORTS ===")
    
    try:
        print("Probando TP1...")
        from tps.tp1_diseño import ejecutar_tp1
        print("✅ TP1 - OK")
        
        print("Probando TP2...")
        from tps.tp2_perdidas import ejecutar_tp2
        from tps.tp2_hielo import ejecutar_tp2_hielo
        print("✅ TP2 - OK")
        
        print("Probando TP3...")
        from tps.tp3_graficos import ejecutar_tp3, ejecutar_comparacion_completa
        print("✅ TP3 - OK")
        
        print("Probando TP4...")
        from tps.tp4_familias import (
            ejecutar_tp4_resistencias, ejecutar_tp4_temperaturas_iniciales,
            ejecutar_tp4_temperaturas_ambiente, ejecutar_tp4_tensiones_12v,
            ejecutar_tp4_tensiones_220v, mostrar_info_tp4
        )
        print("✅ TP4 - OK")
        
        print("Probando TP5...")
        from tps.tp5_estocasticos import (
            ejecutar_tp5_evento_basico, ejecutar_tp5_multiples_simulaciones,
            ejecutar_tp5_tp4_con_eventos
        )
        print("✅ TP5 - OK")
        
        print("Probando core...")
        from utils.heat_simulation import HeatSimulationParameters, HeatSimulator
        print("✅ Core - OK")
        
        print("\n🎉 TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE!")
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_functionality():
    """Prueba funcionalidad básica del simulador."""
    print("\n=== PRUEBA DE FUNCIONALIDAD BÁSICA ===")
    
    try:
        from utils.heat_simulation import HeatSimulationParameters, HeatSimulator
        
        # Crear parámetros y simulador
        params = HeatSimulationParameters()
        simulator = HeatSimulator(params)
        
        # Ejecutar simulación básica
        tiempos, temperaturas = simulator.simular()
        
        print(f"✅ Simulación básica completada:")
        print(f"   - Puntos de tiempo: {len(tiempos)}")
        print(f"   - Temperatura inicial: {temperaturas[0]:.1f}°C")
        print(f"   - Temperatura final: {temperaturas[-1]:.1f}°C")
        print(f"   - Tiempo total: {tiempos[-1]:.0f} segundos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False


def test_menu_structure():
    """Prueba que la estructura del menú principal funcione."""
    print("\n=== PRUEBA DE ESTRUCTURA DEL MENÚ ===")
    
    try:
        from main import MenuPrincipal
        
        menu = MenuPrincipal()
        
        # Verificar que todas las opciones de TPs existan
        expected_tps = ["1", "2", "3", "4", "5"]
        
        for tp_num in expected_tps:
            if tp_num not in menu.opciones_tp:
                print(f"❌ TP {tp_num} no encontrado en menú")
                return False
            
            tp_data = menu.opciones_tp[tp_num]
            if 'titulo' not in tp_data or 'opciones' not in tp_data:
                print(f"❌ TP {tp_num} mal estructurado")
                return False
        
        print("✅ Estructura del menú verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error en estructura del menú: {e}")
        return False


def main():
    """Función principal de pruebas."""
    print("🧪 PRUEBAS DE SISTEMA COMPLETO")
    print("=" * 50)
    
    tests = [
        test_all_imports,
        test_basic_functionality,
        test_menu_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\nPuedes ejecutar:")
        print("  python main.py")
        print("\nPara usar el simulador interactivo.")
    else:
        print("❌ Hay problemas que resolver.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
