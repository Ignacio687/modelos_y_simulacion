"""
TP3 - Gráficos de Temperatura
=============================

Ignacio Chaves - Legajo: 61.220
Modelos y Simulación - UTN FRBA

Este módulo genera diferentes tipos de gráficos para visualizar el comportamiento térmico
del calentador eléctrico bajo diferentes condiciones.
"""

import numpy as np
import matplotlib.pyplot as plt

from utils.heat_simulation import HeatSimulator, HeatSimulationParameters, HeatPlotter


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
    tiempos, temperaturas = sim.simular(parar_en_100c=True)
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min, temperaturas, 'b-', linewidth=2, label='Sin pérdidas térmicas')
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    
    plt.title('Calentamiento sin Pérdidas Térmicas', fontsize=14, fontweight='bold')
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
    tiempos, temperaturas = sim.simular(parar_en_100c=True)
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min, temperaturas, 'g-', linewidth=2, label='Con pérdidas térmicas')
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    
    plt.title('Calentamiento con Pérdidas Térmicas', fontsize=14, fontweight='bold')
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
    """Genera gráfico simulando el efecto del hielo (utiliza implementación del TP2)."""
    print("\n📈 Generando gráfico con efecto hielo...")
    print("💡 Nota: Esta funcionalidad utiliza la implementación mejorada del TP2")
    
    # Importar y ejecutar la función del TP2 que tiene la implementación correcta
    from tps import tp2_hielo
    tp2_hielo.ejecutar_tp2_hielo()
    
    input("\nPresiona Enter para continuar...")


def ejecutar_comparacion_completa():
    """Alias para compatibilidad."""
    return comparacion_completa()


def comparacion_completa():
    """Genera una comparación de los tres escenarios utilizando las implementaciones del TP2."""
    print("\n📊 Generando comparación completa de escenarios...")
    print("💡 Nota: Utiliza las implementaciones mejoradas del TP2")
    
    # Escenario 1: Sin pérdidas (usando TP2 parameters)
    print("- Simulación sin pérdidas...")
    params1 = HeatSimulationParameters(
        masa=1.0, potencia=360, T_inicial=20, T_amb=20, tiempo_total=1200,
        k_acero=1e6, k_poliuretano=1e6
    )
    sim1 = HeatSimulator(params1)
    tiempos1, temps1 = sim1.simular(parar_en_100c=True)
    
    # Escenario 2: Con pérdidas (usando TP2 parameters)
    print("- Simulación con pérdidas...")
    params2 = HeatSimulationParameters(
        masa=1.0, potencia=360, T_inicial=20, T_amb=20, tiempo_total=3600
    )
    sim2 = HeatSimulator(params2)
    tiempos2, temps2 = sim2.simular(parar_en_100c=True)
    
    # Escenario 3: Con hielo (usando la física completa del TP2)
    print("- Simulación con pérdidas y hielo...")
    
    # Parámetros del TP2 hielo (valores exactos)
    masa_agua = 1.0
    calor_especifico = 4186
    potencia = 360
    T_amb = 20
    dt = 1
    tiempo_total = 2500
    
    # Coeficiente U del TP2
    R_acero = 0.001 / 16
    R_poliuretano = 0.001 / 0.03
    R_total = R_acero + R_poliuretano
    U = 1 / R_total
    
    # Geometría
    radio = 0.05
    altura = 0.13
    area_lateral = 2 * np.pi * radio * altura
    area_superior = np.pi * radio**2
    area_total = area_lateral + area_superior
    
    # Propiedades del hielo (TP2 completas)
    masa_hielo = 0.05  # kg por cubito
    calor_fusion_hielo = 334000  # J/kg
    T_hielo = -5  # Temperatura inicial del hielo en °C
    calor_especifico_hielo = 2100  # J/(kg·°C)
    h_agua_hielo = 500  # W/m²K, coeficiente de película
    lado_cubo = 0.03  # metros, lado de cada cubito
    n_cubos = 2
    superficie_hielo = 6 * lado_cubo**2 * n_cubos
    masa_hielo_total = masa_hielo * n_cubos
    
    # Inicialización del escenario con hielo
    T_agua = 20.0
    T_hielo_actual = T_hielo
    masa_hielo_restante = masa_hielo_total
    energia_fusion_restante = masa_hielo_total * calor_fusion_hielo
    
    tiempos3 = [0]
    temps3 = [T_agua]
    
    # Simulación con física completa del hielo
    for t in range(1, tiempo_total + 1):
        # Energía del calefactor y pérdidas
        energia_calefactor_dt = potencia * dt
        perdida_ambiente_dt = U * area_total * (T_agua - T_amb) * dt
        energia_neta_disponible_dt = energia_calefactor_dt - perdida_ambiente_dt
        if energia_neta_disponible_dt < 0:
            energia_neta_disponible_dt = 0

        energia_para_calentar_agua_final_dt = energia_neta_disponible_dt

        # Interacción agua-hielo (solo después de t=120, 2 minutos)
        if t >= 120 and masa_hielo_restante > 0 and T_hielo_actual is not None:
            
            # 1. Transferencia convectiva de calor del agua al hielo
            if T_agua > T_hielo_actual:
                Q_conv_potencia = h_agua_hielo * superficie_hielo * (T_agua - T_hielo_actual)
                energia_conv_dt = Q_conv_potencia * dt
                
                # Limitar para no enfriar el agua por debajo de T_hielo_actual
                max_energia_cesible_agua = masa_agua * calor_especifico * (T_agua - T_hielo_actual)
                energia_conv_dt = min(energia_conv_dt, max_energia_cesible_agua)
                energia_efectiva_transferida_conv = 0

                # Aplicar energia_conv_dt para calentar hielo a 0°C
                if T_hielo_actual < 0:
                    calor_necesario_hielo_a_0_conv = masa_hielo_restante * calor_especifico_hielo * abs(T_hielo_actual)
                    absorbido_calentar_conv = min(energia_conv_dt, calor_necesario_hielo_a_0_conv)
                    T_hielo_actual += absorbido_calentar_conv / (masa_hielo_restante * calor_especifico_hielo)
                    energia_conv_dt -= absorbido_calentar_conv
                    energia_efectiva_transferida_conv += absorbido_calentar_conv
                
                # Aplicar energia_conv_dt restante para derretir hielo a 0°C
                if T_hielo_actual >= 0 and energia_conv_dt > 0 and masa_hielo_restante > 0:
                    masa_derretida_conv = min(energia_conv_dt / calor_fusion_hielo, masa_hielo_restante)
                    masa_agua += masa_derretida_conv
                    masa_hielo_restante -= masa_derretida_conv
                    energia_fusion_restante -= masa_derretida_conv * calor_fusion_hielo
                    superficie_hielo = 6 * lado_cubo**2 * (masa_hielo_restante / masa_hielo_total)
                    energia_conv_dt -= masa_derretida_conv * calor_fusion_hielo
                    energia_efectiva_transferida_conv += masa_derretida_conv * calor_fusion_hielo

                # Enfriar el agua por la energía transferida al hielo
                if energia_efectiva_transferida_conv > 0 and masa_agua > 0:
                    T_agua -= energia_efectiva_transferida_conv / (masa_agua * calor_especifico)

            # 2. Aplicar energía del calefactor al hielo si aún queda
            if T_hielo_actual is not None and masa_hielo_restante > 0:
                # Calentar hielo a 0°C con energía del calefactor
                if T_hielo_actual < 0:
                    calor_necesario_hielo_a_0_calefactor = masa_hielo_restante * calor_especifico_hielo * abs(T_hielo_actual)
                    gastado_calentar_hielo_calefactor = min(energia_para_calentar_agua_final_dt, calor_necesario_hielo_a_0_calefactor)
                    T_hielo_actual += gastado_calentar_hielo_calefactor / (masa_hielo_restante * calor_especifico_hielo)
                    energia_para_calentar_agua_final_dt -= gastado_calentar_hielo_calefactor
                
                # Derretir hielo a 0°C con energía restante del calefactor
                if T_hielo_actual >= 0 and masa_hielo_restante > 0:
                    calor_necesario_fusion_calefactor = masa_hielo_restante * calor_fusion_hielo
                    gastado_fusion_hielo_calefactor = min(energia_para_calentar_agua_final_dt, calor_necesario_fusion_calefactor)
                    masa_derretida_calefactor = gastado_fusion_hielo_calefactor / calor_fusion_hielo
                    masa_agua += masa_derretida_calefactor
                    masa_hielo_restante -= masa_derretida_calefactor
                    energia_para_calentar_agua_final_dt -= gastado_fusion_hielo_calefactor

        # 3. Verificar si el hielo se derritió completamente
        if masa_hielo_restante <= 0:
            T_hielo_actual = None
            energia_fusion_restante = 0

        # 4. Aplicar la energía restante del calefactor para calentar el agua
        if energia_para_calentar_agua_final_dt > 0 and masa_agua > 0:
            T_agua += energia_para_calentar_agua_final_dt / (masa_agua * calor_especifico)

        # Restricciones de temperatura finales
        if T_hielo_actual is not None and masa_hielo_restante > 0:
            if T_hielo_actual < 0:
                T_agua = max(T_agua, T_hielo_actual)
            else:
                T_agua = max(T_agua, 0)
        elif T_agua < 0:
            T_agua = 0
        
        tiempos3.append(t)
        temps3.append(T_agua)
        
        if T_agua >= 100:
            break
    
    # Crear gráfico comparativo
    plt.figure(figsize=(12, 8))
    
    plt.plot(np.array(tiempos1)/60, temps1, 'b-', linewidth=2, label='Sin pérdidas térmicas')
    plt.plot(np.array(tiempos2)/60, temps2, 'g-', linewidth=2, label='Con pérdidas térmicas')
    plt.plot(np.array(tiempos3)/60, temps3, 'orange', linewidth=2, label='Con pérdidas + hielo')
    
    plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
    plt.axvline(2, color='cyan', linestyle=':', alpha=0.5, label='Adición de hielo')
    
    plt.title('Comparación de Escenarios de Calentamiento', fontsize=14, fontweight='bold')
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
    print(f"   • Con hielo: {tiempos3[-1]/60:.2f} min para 100°C")
    
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
        tiempos, temperaturas = sim.simular(parar_en_100c=True)
        
        # Crear gráfico
        plt.figure(figsize=(10, 6))
        tiempos_min = np.array(tiempos) / 60.0
        
        plt.plot(tiempos_min, temperaturas, 'purple', linewidth=2, label='Simulación personalizada')
        plt.axhline(100, color='r', linestyle='--', alpha=0.7, label='100°C (ebullición)')
        
        plt.title('Simulación Personalizada', fontsize=14, fontweight='bold')
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
