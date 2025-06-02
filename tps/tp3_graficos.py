"""
TP3 - Gráficos de Temperatura
=============================

Ignacio Chaves - Legajo: 61.220
Modelos y Simulación - UTN FRBA

Este módulo genera diferentes tipos de gráficos para visualizar el comportamiento térmico
del calentador eléctrico bajo diferentes condiciones.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Agregar path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils'))

from heat_simulation import HeatSimulator, HeatSimulationParameters, HeatPlotter


def ejecutar_tp3():
    """
    Ejecuta el menú principal del TP3 con opciones de gráficos.
    """
    while True:
        print("\n" + "="*60)
        print("📊 TP3 - GRÁFICOS DE TEMPERATURA 📊")
        print("="*60)
        print("\n📋 Opciones disponibles:")
        print("   [1] Gráfico sin pérdidas térmicas")
        print("   [2] Gráfico con pérdidas térmicas")
        print("   [3] Gráfico con pérdidas térmicas y efecto hielo")
        print("   [4] Comparación de los tres escenarios")
        print("   [5] Gráfico personalizado")
        print("   [0] Volver al menú principal")
        
        opcion = input("\n🎯 Selecciona una opción: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            grafico_sin_perdidas()
        elif opcion == "2":
            grafico_con_perdidas()
        elif opcion == "3":
            grafico_con_hielo()
        elif opcion == "4":
            comparacion_completa()
        elif opcion == "5":
            grafico_personalizado()
        else:
            print("❌ Opción no válida!")
            input("Presiona Enter para continuar...")


def grafico_sin_perdidas():
    """Genera gráfico de temperatura sin pérdidas térmicas."""
    print("\n📈 Generando gráfico sin pérdidas térmicas...")
    
    # Crear parámetros sin pérdidas (alta conductividad térmica)
    params = HeatSimulationParameters(
        masa=1.0,
        potencia=360,
        T_inicial=20,
        T_amb=20,
        tiempo_total=1200,  # 20 minutos
        k_acero=1e6,  # Muy alta conductividad = sin pérdidas
        k_poliuretano=1e6
    )
    
    sim = HeatSimulator(params)
    tiempos, temperaturas = sim.simular()
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min, temperaturas, 'b-', linewidth=2, label='Sin pérdidas térmicas')
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    
    plt.title('🔥 Calentamiento sin Pérdidas Térmicas', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print(f"✅ Tiempo para alcanzar 100°C: {tiempos[-1]/60:.2f} minutos")
    input("Presiona Enter para continuar...")


def grafico_con_perdidas():
    """Genera gráfico de temperatura con pérdidas térmicas."""
    print("\n📈 Generando gráfico con pérdidas térmicas...")
    
    # Crear parámetros con pérdidas (valores por defecto)
    params = HeatSimulationParameters(
        masa=1.0,
        potencia=360,
        T_inicial=20,
        T_amb=20,
        tiempo_total=3600  # 1 hora
    )
    
    sim = HeatSimulator(params)
    tiempos, temperaturas = sim.simular()
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min, temperaturas, 'g-', linewidth=2, label='Con pérdidas térmicas')
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    
    plt.title('🔥 Calentamiento con Pérdidas Térmicas', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    if temperaturas[-1] >= 100:
        print(f"✅ Tiempo para alcanzar 100°C: {tiempos[-1]/60:.2f} minutos")
    else:
        print(f"⚠️ No se alcanzó 100°C. Temperatura máxima: {max(temperaturas):.2f}°C")
    
    input("Presiona Enter para continuar...")


def grafico_con_hielo():
    """Genera gráfico simulando el efecto del hielo."""
    print("\n📈 Generando gráfico con efecto hielo simulado...")
    
    # Crear parámetros base
    params = HeatSimulationParameters(
        masa=1.0,
        potencia=360,
        T_inicial=20,
        T_amb=20,
        tiempo_total=3600
    )
    
    sim = HeatSimulator(params)
    
    # Simular con evento de enfriamiento que simula el hielo
    evento_hielo = {
        'probabilidad': 1.0,  # Ocurre seguro en t=120
        'descenso_max': 15,   # Descenso de 15°C
        'duracion_min': 300,  # 5 minutos
        'duracion_max': 300
    }
    
    # Modificar la simulación para que el evento ocurra exactamente en t=120
    sim.reset()
    for t in range(1, sim.params.tiempo_total + 1):
        # Calcular pérdidas y energía neta
        perdida = sim.params.U * sim.params.area_total * (sim.T_actual - sim.params.T_amb)
        energia_neta = sim.params.potencia - perdida
        
        if energia_neta < 0:
            energia_neta = 0
        
        # Simular adición de hielo en t=120 (2 minutos)
        if t == 120:
            sim.T_actual -= 15  # Descenso inmediato por el hielo
        
        # Aplicar cambio de temperatura normal
        dT = (energia_neta * sim.params.dt) / (sim.params.masa * sim.params.calor_especifico)
        sim.T_actual += dT
        
        sim.tiempos.append(t)
        sim.temperaturas.append(sim.T_actual)
        
        if sim.T_actual >= 100:
            break
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(sim.tiempos) / 60.0
    
    plt.plot(tiempos_min, sim.temperaturas, 'orange', linewidth=2, label='Con efecto hielo')
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    plt.axvline(2, color='cyan', linestyle=':', alpha=0.7, label='Adición de hielo (2 min)')
    
    plt.title('🧊 Calentamiento con Efecto Hielo', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print(f"✅ Tiempo para alcanzar 100°C: {sim.tiempos[-1]/60:.2f} minutos")
    input("Presiona Enter para continuar...")


def comparacion_completa():
    """Genera una comparación de los tres escenarios."""
    print("\n📊 Generando comparación completa de escenarios...")
    
    # Escenario 1: Sin pérdidas
    params1 = HeatSimulationParameters(
        masa=1.0, potencia=360, T_inicial=20, T_amb=20, tiempo_total=1200,
        k_acero=1e6, k_poliuretano=1e6
    )
    sim1 = HeatSimulator(params1)
    tiempos1, temps1 = sim1.simular()
    
    # Escenario 2: Con pérdidas
    params2 = HeatSimulationParameters(
        masa=1.0, potencia=360, T_inicial=20, T_amb=20, tiempo_total=3600
    )
    sim2 = HeatSimulator(params2)
    tiempos2, temps2 = sim2.simular()
    
    # Escenario 3: Con hielo (simulado)
    params3 = HeatSimulationParameters(
        masa=1.0, potencia=360, T_inicial=20, T_amb=20, tiempo_total=3600
    )
    sim3 = HeatSimulator(params3)
    sim3.reset()
    
    for t in range(1, sim3.params.tiempo_total + 1):
        perdida = sim3.params.U * sim3.params.area_total * (sim3.T_actual - sim3.params.T_amb)
        energia_neta = sim3.params.potencia - perdida
        if energia_neta < 0:
            energia_neta = 0
        
        if t == 120:  # Hielo en 2 minutos
            sim3.T_actual -= 15
        
        dT = (energia_neta * sim3.params.dt) / (sim3.params.masa * sim3.params.calor_especifico)
        sim3.T_actual += dT
        
        sim3.tiempos.append(t)
        sim3.temperaturas.append(sim3.T_actual)
        
        if sim3.T_actual >= 100:
            break
    
    # Crear gráfico comparativo
    plt.figure(figsize=(12, 8))
    
    plt.plot(np.array(tiempos1)/60, temps1, 'b-', linewidth=2, label='Sin pérdidas térmicas')
    plt.plot(np.array(tiempos2)/60, temps2, 'g-', linewidth=2, label='Con pérdidas térmicas')
    plt.plot(np.array(sim3.tiempos)/60, sim3.temperaturas, 'orange', linewidth=2, label='Con pérdidas + hielo')
    
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    plt.axvline(2, color='cyan', linestyle=':', alpha=0.5, label='Adición de hielo')
    
    plt.title('📊 Comparación de Escenarios de Calentamiento', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Mostrar resultados
    print("\n📊 Resultados comparativos:")
    print(f"   • Sin pérdidas: {tiempos1[-1]/60:.2f} min para 100°C")
    print(f"   • Con pérdidas: {tiempos2[-1]/60:.2f} min para 100°C")
    print(f"   • Con hielo: {sim3.tiempos[-1]/60:.2f} min para 100°C")
    
    input("Presiona Enter para continuar...")


def grafico_personalizado():
    """Permite al usuario personalizar parámetros y generar gráfico."""
    print("\n⚙️ Configuración personalizada")
    print("="*40)
    
    try:
        masa = float(input("Masa de agua (kg) [1.0]: ") or "1.0")
        potencia = float(input("Potencia (W) [360]: ") or "360")
        T_inicial = float(input("Temperatura inicial (°C) [20]: ") or "20")
        T_ambiente = float(input("Temperatura ambiente (°C) [20]: ") or "20")
        tiempo_max = int(input("Tiempo máximo (min) [60]: ") or "60") * 60
        
        print("\nOpciones de pérdidas térmicas:")
        print("   [1] Sin pérdidas")
        print("   [2] Con pérdidas (valores por defecto)")
        print("   [3] Pérdidas personalizadas")
        
        perdidas_opcion = input("Selecciona opción [2]: ") or "2"
        
        if perdidas_opcion == "1":
            params = HeatSimulationParameters(
                masa=masa, potencia=potencia, T_inicial=T_inicial, T_amb=T_ambiente,
                tiempo_total=tiempo_max, k_acero=1e6, k_poliuretano=1e6
            )
        elif perdidas_opcion == "3":
            k_acero = float(input("Conductividad térmica acero (W/mK) [16]: ") or "16")
            k_poliuretano = float(input("Conductividad térmica poliuretano (W/mK) [0.03]: ") or "0.03")
            params = HeatSimulationParameters(
                masa=masa, potencia=potencia, T_inicial=T_inicial, T_amb=T_ambiente,
                tiempo_total=tiempo_max, k_acero=k_acero, k_poliuretano=k_poliuretano
            )
        else:
            params = HeatSimulationParameters(
                masa=masa, potencia=potencia, T_inicial=T_inicial, T_amb=T_ambiente,
                tiempo_total=tiempo_max
            )
        
        # Ejecutar simulación
        sim = HeatSimulator(params)
        tiempos, temperaturas = sim.simular()
        
        # Crear gráfico
        plt.figure(figsize=(10, 6))
        tiempos_min = np.array(tiempos) / 60.0
        
        plt.plot(tiempos_min, temperaturas, 'purple', linewidth=2, label='Simulación personalizada')
        plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
        
        plt.title('⚙️ Simulación Personalizada', fontsize=14, fontweight='bold')
        plt.xlabel('Tiempo (min)', fontsize=12)
        plt.ylabel('Temperatura (°C)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        print(f"✅ Simulación completada en {tiempos[-1]/60:.2f} minutos")
        print(f"   Temperatura final: {temperaturas[-1]:.2f}°C")
        
    except ValueError:
        print("❌ Error en los parámetros ingresados!")
    
    input("Presiona Enter para continuar...")


def ejecutar_comparacion_completa():
    """Función de acceso directo para la comparación completa."""
    comparacion_completa()


if __name__ == "__main__":
    ejecutar_tp3()
