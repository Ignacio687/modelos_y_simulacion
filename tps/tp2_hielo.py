"""
TP2 EXTRA - Simulación de Calentamiento con Hielo
================================================

Ignacio Chaves - Legajo: 61.220
Modelos y Simulación - UTN FRBA

Este módulo simula el calentamiento de agua con pérdidas térmicas y la adición de cubitos de hielo.
Incluye la física del derretimiento del hielo y la transferencia de calor entre agua y hielo.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Agregar path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constantes
masa = 1.0  # kg de agua
calor_especifico = 4186  # J/(kg°C)
potencia = 360  # Watts
T_amb = 20  # Temperatura ambiente en °C
dt = 1  # intervalo de tiempo en segundos
tiempo_total = 2500  # segundos

# Coeficiente de transmisión térmica U
R_acero = 0.001 / 16
R_poliuretano = 0.001 / 0.03
R_total = R_acero + R_poliuretano
U = 1 / R_total  # Coeficiente de transmisión térmica

# Geometría del cilindro
radio = 0.05  # metros
altura = 0.13  # metros
area_lateral = 2 * np.pi * radio * altura
area_superior = np.pi * radio**2
area_total = area_lateral + area_superior  # m²

# Propiedades del hielo
masa_hielo = 0.05  # kg por cubito
calor_fusion_hielo = 334000  # J/kg
T_hielo = -5  # Temperatura inicial del hielo en °C
calor_especifico_hielo = 2100  # J/(kg·°C)

# Parámetros para transferencia de calor entre agua y hielo
h_agua_hielo = 500  # W/m²K, coeficiente de película típico para agua en agitación
lado_cubo = 0.03  # metros, lado de cada cubito
n_cubos = 2
superficie_hielo = 6 * lado_cubo**2 * n_cubos  # área total de los cubos
masa_hielo_total = masa_hielo * n_cubos


def ejecutar_tp2_hielo():
    """
    Ejecuta la simulación de calentamiento de agua con pérdidas térmicas y cubitos de hielo.
    
    Esta función implementa la física completa del proceso incluyendo:
    - Calentamiento eléctrico con pérdidas al ambiente
    - Transferencia de calor entre agua y hielo
    - Derretimiento del hielo con cambio de fase
    - Visualización gráfica de la evolución de temperatura
    """
    print("\n" + "="*60)
    print("🧊 TP2 EXTRA - SIMULACIÓN CON HIELO 🧊")
    print("="*60)
    print("\n📋 Parámetros de la simulación:")
    print(f"   • Masa de agua: {masa} kg")
    print(f"   • Potencia del calefactor: {potencia} W")
    print(f"   • Temperatura ambiente: {T_amb}°C")
    print(f"   • Número de cubitos de hielo: {n_cubos}")
    print(f"   • Masa total de hielo: {masa_hielo_total:.3f} kg")
    print(f"   • Temperatura inicial del hielo: {T_hielo}°C")
    print(f"   • Tiempo de adición del hielo: 2 minutos")
    print(f"   • Coeficiente U (pérdidas): {U:.2f} W/m²K")
    
    input("\n🚀 Presiona Enter para iniciar la simulación...")
    
    # Inicialización
    T_agua = 20  # Temperatura inicial en °C
    T_hielo_actual = T_hielo
    masa_agua = masa
    masa_hielo_restante = masa_hielo_total
    energia_fusion_restante = masa_hielo_total * calor_fusion_hielo

    tiempos = [0]
    temperaturas = [T_agua]

    print("\n🔄 Ejecutando simulación...")
    
    # Simulación segundo a segundo
    for t in range(1, tiempo_total + 1):
        # Mostrar progreso cada 5 minutos
        if t % 300 == 0:
            print(f"   ⏱️ Tiempo: {t//60} min - Temperatura: {T_agua:.2f}°C")
        
        # Energía neta del calefactor (potencia) en este paso de tiempo (dt=1)
        energia_calefactor_dt = potencia * dt
        # Pérdida de calor al ambiente en este paso
        perdida_ambiente_dt = U * area_total * (T_agua - T_amb) * dt
        
        # Energía neta disponible del calefactor para el sistema
        energia_neta_disponible_dt = energia_calefactor_dt - perdida_ambiente_dt
        if energia_neta_disponible_dt < 0:
            energia_neta_disponible_dt = 0

        energia_para_calentar_agua_final_dt = energia_neta_disponible_dt

        # --- Interacción continua agua-hielo y aplicación de energía del calefactor (para t >= 120) ---
        if t >= 120 and masa_hielo_restante > 0 and T_hielo_actual is not None:
            
            # 1. Transferencia convectiva de calor del agua al hielo (si T_agua > T_hielo_actual)
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
                    superficie_hielo = 6 * lado_cubo**2 * (masa_hielo_restante / masa_hielo)
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

        # Restricciones de temperatura finales para el paso
        if T_hielo_actual is not None and masa_hielo_restante > 0:
            if T_hielo_actual < 0:
                T_agua = max(T_agua, T_hielo_actual)
            else:
                T_agua = max(T_agua, 0)
        elif T_agua < 0:
            T_agua = 0
        
        tiempos.append(t)
        temperaturas.append(T_agua)
        if T_agua >= 100:
            break  # Alcanzamos 100°C

    # Mostrar resultados
    tiempo_final_min = tiempos[-1] / 60
    print(f"\n📊 Resultados de la simulación:")
    print(f"   • Tiempo total: {tiempo_final_min:.2f} minutos")
    print(f"   • Temperatura final: {temperaturas[-1]:.2f}°C")
    if masa_hielo_restante > 0:
        print(f"   • Hielo restante: {masa_hielo_restante:.4f} kg")
    else:
        print(f"   • Todo el hielo se derritió")
    
    # Crear gráfico
    plt.figure(figsize=(12, 8))
    
    # Convertir tiempos a minutos para el eje X
    tiempos_min_plot = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min_plot, temperaturas, 'b-', linewidth=2, label="Temperatura del agua con hielo")
    plt.axhline(100, color='r', linestyle='--', linewidth=2, label="100°C (ebullición)")
    plt.axvline(2, color='orange', linestyle=':', alpha=0.7, label="Adición de hielo (2 min)")
    
    plt.title('🧊 Curva de Temperatura con Pérdidas de Calor y Hielo', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    
    # Ajustar los ticks del eje X para que sean más legibles en minutos
    max_tiempo_min = max(tiempos_min_plot) if tiempos_min_plot.size > 0 else 0
    tick_spacing = 2 if max_tiempo_min > 40 else 1
    if max_tiempo_min == 0: 
        plt.xticks([0])
    else:
        upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
        plt.xticks(np.arange(0, upper_limit, tick_spacing))
    
    plt.tight_layout()
    plt.show()
    
    input("\n✅ Simulación completada. Presiona Enter para continuar...")


if __name__ == "__main__":
    ejecutar_tp2_hielo()