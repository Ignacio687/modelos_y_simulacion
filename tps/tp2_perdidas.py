#!/usr/bin/env python3
"""
TP2 - PÉRDIDAS TÉRMICAS Y SIMULACIÓN CON HIELO
==============================================

Este módulo implementa:
1. Cálculo de pérdidas térmicas del calentador
2. Simulación con transferencia de calor al ambiente
3. Simulación especial con cubitos de hielo (análisis extra)

Autor: Ignacio Chaves (Legajo: 61.220)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Agregar path para importar utilidades
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from heat_simulation import HeatSimulator, HeatSimulationParameters

# =============================================================================
# PARÁMETROS DEL SISTEMA
# =============================================================================

# Parámetros básicos del calentador
MASA_AGUA = 1.0  # kg
CALOR_ESPECIFICO = 4186  # J/(kg°C)
POTENCIA = 360  # W
T_AMBIENTE = 20  # °C
T_INICIAL = 20  # °C
T_OBJETIVO = 100  # °C

# Geometría del calentador (cilindro)
RADIO = 0.05  # m
ALTURA = 0.13  # m
AREA_LATERAL = 2 * np.pi * RADIO * ALTURA
AREA_SUPERIOR = np.pi * RADIO**2
AREA_TOTAL = AREA_LATERAL + AREA_SUPERIOR  # m²

# Propiedades térmicas del aislamiento
R_ACERO = 0.001 / 16  # Resistencia térmica del acero
R_POLIURETANO = 0.001 / 0.03  # Resistencia térmica del poliuretano
R_TOTAL = R_ACERO + R_POLIURETANO
U_COEFF = 1 / R_TOTAL  # Coeficiente de transmisión térmica [W/(m²·K)]

# Parámetros para simulación con hielo
MASA_HIELO_POR_CUBO = 0.05  # kg
CALOR_FUSION_HIELO = 334000  # J/kg
T_HIELO_INICIAL = -5  # °C
CALOR_ESPECIFICO_HIELO = 2100  # J/(kg·K)
N_CUBOS = 2
MASA_HIELO_TOTAL = MASA_HIELO_POR_CUBO * N_CUBOS

# Transferencia de calor agua-hielo
H_AGUA_HIELO = 500  # W/(m²·K) - coeficiente de película
LADO_CUBO = 0.03  # m
SUPERFICIE_HIELO = 6 * LADO_CUBO**2 * N_CUBOS  # área total de los cubos

# =============================================================================
# FUNCIONES DE CÁLCULO
# =============================================================================

def calcular_parametros_termicos():
    """Calcula y muestra los parámetros térmicos del sistema."""
    print("="*50)
    print("TP2 - PARÁMETROS DE PÉRDIDAS TÉRMICAS")
    print("="*50)
    
    print(f"Geometría del calentador:")
    print(f"  Radio: {RADIO:.3f} m")
    print(f"  Altura: {ALTURA:.3f} m")
    print(f"  Área lateral: {AREA_LATERAL:.6f} m²")
    print(f"  Área superior: {AREA_SUPERIOR:.6f} m²")
    print(f"  Área total: {AREA_TOTAL:.6f} m²")
    
    print(f"\nPropiedades térmicas:")
    print(f"  Resistencia térmica acero: {R_ACERO:.6f} K·m²/W")
    print(f"  Resistencia térmica poliuretano: {R_POLIURETANO:.6f} K·m²/W")
    print(f"  Resistencia térmica total: {R_TOTAL:.6f} K·m²/W")
    print(f"  Coeficiente U: {U_COEFF:.3f} W/(m²·K)")
    
    # Calcular pérdida máxima (a 100°C)
    perdida_maxima = U_COEFF * AREA_TOTAL * (T_OBJETIVO - T_AMBIENTE)
    porcentaje_perdida = (perdida_maxima / POTENCIA) * 100
    
    print(f"\nAnálisis de pérdidas térmicas:")
    print(f"  Pérdida máxima a 100°C: {perdida_maxima:.2f} W")
    print(f"  Porcentaje de potencia perdida: {porcentaje_perdida:.1f}%")
    print(f"  Potencia neta disponible: {POTENCIA - perdida_maxima:.2f} W")

def simular_sin_perdidas():
    """Simula el calentamiento sin pérdidas térmicas."""
    print("\n" + "="*50)
    print("SIMULACIÓN SIN PÉRDIDAS TÉRMICAS")
    print("="*50)
    
    # Tiempo teórico para calentar de 20°C a 100°C
    energia_total = MASA_AGUA * CALOR_ESPECIFICO * (T_OBJETIVO - T_INICIAL)
    tiempo_teorico = energia_total / POTENCIA
    
    print(f"Energía total requerida: {energia_total:.0f} J")
    print(f"Tiempo teórico: {tiempo_teorico:.1f} s ({tiempo_teorico/60:.1f} min)")
    
    # Crear simulación sin pérdidas (U = 0)
    params = HeatSimulationParameters(
        masa=MASA_AGUA,
        calor_especifico=CALOR_ESPECIFICO,
        potencia=POTENCIA,
        T_inicial=T_INICIAL,
        T_amb=T_AMBIENTE,
        tiempo_total=int(tiempo_teorico * 1.5),  # 50% más tiempo del teórico
        k_acero=1e6,  # Muy alta conductividad = sin pérdidas
        k_poliuretano=1e6  # Muy alta conductividad = sin pérdidas
    )
    
    sim = HeatSimulator(params)
    tiempos, temperaturas = sim.simular()
    
    return tiempos, temperaturas

def simular_con_perdidas():
    """Simula el calentamiento con pérdidas térmicas."""
    print("\n" + "="*50)
    print("SIMULACIÓN CON PÉRDIDAS TÉRMICAS")
    print("="*50)
    
    # Coeficiente de pérdidas para HeatSimulation
    coef_perdidas = U_COEFF * AREA_TOTAL
    
    print(f"Coeficiente de pérdidas: {coef_perdidas:.6f} W/K")
    
    # Crear simulación con pérdidas (usando los valores por defecto de k)
    params = HeatSimulationParameters(
        masa=MASA_AGUA,
        calor_especifico=CALOR_ESPECIFICO,
        potencia=POTENCIA,
        T_inicial=T_INICIAL,
        T_amb=T_AMBIENTE,
        tiempo_total=3600  # 1 hora máximo
    )
    
    sim = HeatSimulator(params)
    tiempos, temperaturas = sim.simular()
    
    # Verificar si se alcanzó la temperatura objetivo
    if temperaturas[-1] < T_OBJETIVO:
        temp_equilibrio = sim.calcular_temp_equilibrio()
        print(f"ATENCIÓN: La temperatura de equilibrio ({temp_equilibrio:.1f}°C) es menor que el objetivo ({T_OBJETIVO}°C)")
        print(f"Temperatura alcanzada: {temperaturas[-1]:.1f}°C en {tiempos[-1]:.0f} s")
    else:
        print(f"Tiempo para alcanzar {T_OBJETIVO}°C: {tiempos[-1]:.1f} s ({tiempos[-1]/60:.1f} min)")
    
    return tiempos, temperaturas

def simular_con_hielo():
    """Simula el sistema con cubitos de hielo (análisis especial)."""
    print("\n" + "="*50)
    print("SIMULACIÓN ESPECIAL CON HIELO")
    print("="*50)
    
    print(f"Parámetros del hielo:")
    print(f"  Número de cubos: {N_CUBOS}")
    print(f"  Masa total: {MASA_HIELO_TOTAL:.3f} kg")
    print(f"  Temperatura inicial: {T_HIELO_INICIAL}°C")
    print(f"  Superficie total: {SUPERFICIE_HIELO:.6f} m²")
    
    # Inicialización
    dt = 1  # s
    tiempo_max = 2500  # s
    tiempo_hielo = 120  # s - momento en que se agrega el hielo
    
    T_agua = T_INICIAL
    T_hielo = T_HIELO_INICIAL
    masa_agua = MASA_AGUA
    masa_hielo_restante = MASA_HIELO_TOTAL
    
    tiempos = [0]
    temperaturas = [T_agua]
    
    for t in range(1, tiempo_max + 1):
        # Energía del calefactor
        energia_calefactor = POTENCIA * dt
        
        # Pérdidas al ambiente
        perdida_ambiente = U_COEFF * AREA_TOTAL * (T_agua - T_AMBIENTE) * dt
        
        # Energía neta disponible
        energia_neta = energia_calefactor - perdida_ambiente
        if energia_neta < 0:
            energia_neta = 0
        
        energia_disponible = energia_neta
        
        # Interacción con hielo (después del tiempo_hielo)
        if t >= tiempo_hielo and masa_hielo_restante > 0:
            
            # 1. Transferencia convectiva agua → hielo
            if T_agua > T_hielo:
                Q_conv = H_AGUA_HIELO * SUPERFICIE_HIELO * (T_agua - T_hielo) * dt
                max_energia_agua = masa_agua * CALOR_ESPECIFICO * (T_agua - T_hielo)
                energia_conv = min(Q_conv, max_energia_agua)
                
                energia_efectiva = 0
                masa_agua_inicial = masa_agua
                
                # Calentar hielo hasta 0°C
                if T_hielo < 0:
                    energia_calentar = masa_hielo_restante * CALOR_ESPECIFICO_HIELO * abs(T_hielo)
                    energia_usada = min(energia_conv, energia_calentar)
                    T_hielo += energia_usada / (masa_hielo_restante * CALOR_ESPECIFICO_HIELO)
                    energia_conv -= energia_usada
                    energia_efectiva += energia_usada
                
                # Derretir hielo a 0°C
                if T_hielo == 0 and energia_conv > 0 and masa_hielo_restante > 0:
                    energia_fusion = masa_hielo_restante * CALOR_FUSION_HIELO
                    energia_usada = min(energia_conv, energia_fusion)
                    masa_derretida = energia_usada / CALOR_FUSION_HIELO
                    masa_agua += masa_derretida
                    masa_hielo_restante -= masa_derretida
                    energia_efectiva += energia_usada
                
                # Enfriar el agua
                if masa_agua_inicial > 0 and energia_efectiva > 0:
                    T_agua -= energia_efectiva / (masa_agua_inicial * CALOR_ESPECIFICO)
            
            # 2. Aplicar energía del calefactor al hielo
            if masa_hielo_restante > 0:
                # Calentar hielo hasta 0°C
                if T_hielo < 0:
                    energia_calentar = masa_hielo_restante * CALOR_ESPECIFICO_HIELO * abs(T_hielo)
                    energia_usada = min(energia_disponible, energia_calentar)
                    T_hielo += energia_usada / (masa_hielo_restante * CALOR_ESPECIFICO_HIELO)
                    energia_disponible -= energia_usada
                
                # Derretir hielo a 0°C
                if T_hielo == 0 and masa_hielo_restante > 0:
                    energia_fusion = masa_hielo_restante * CALOR_FUSION_HIELO
                    energia_usada = min(energia_disponible, energia_fusion)
                    masa_derretida = energia_usada / CALOR_FUSION_HIELO
                    masa_agua += masa_derretida
                    masa_hielo_restante -= masa_derretida
                    energia_disponible -= energia_usada
            
            # Limpiar variables si no queda hielo
            if masa_hielo_restante <= 0:
                T_hielo = None
                masa_hielo_restante = 0
        
        # 3. Calentar el agua con energía restante
        if energia_disponible > 0 and masa_agua > 0:
            T_agua += energia_disponible / (masa_agua * CALOR_ESPECIFICO)
        
        # Restricciones de temperatura
        if masa_hielo_restante > 0 and T_hielo is not None:
            if T_hielo < 0:
                T_agua = max(T_agua, T_hielo)
            else:
                T_agua = max(T_agua, 0)
        elif T_agua < 0:
            T_agua = 0
        
        tiempos.append(t)
        temperaturas.append(T_agua)
        
        if T_agua >= T_OBJETIVO:
            break
    
    print(f"Tiempo final de simulación: {tiempos[-1]:.0f} s ({tiempos[-1]/60:.1f} min)")
    print(f"Temperatura final: {temperaturas[-1]:.1f}°C")
    print(f"Masa final de agua: {masa_agua:.3f} kg")
    print(f"Hielo restante: {masa_hielo_restante:.3f} kg")
    
    return tiempos, temperaturas

def graficar_comparacion():
    """Genera gráfico comparativo de todas las simulaciones."""
    print("\n" + "="*50)
    print("GENERANDO GRÁFICO COMPARATIVO")
    print("="*50)
    
    # Ejecutar todas las simulaciones
    t_sin, T_sin = simular_sin_perdidas()
    t_con, T_con = simular_con_perdidas()
    t_hielo, T_hielo = simular_con_hielo()
    
    # Crear figura
    plt.figure(figsize=(12, 8))
    
    # Convertir tiempos a minutos
    t_sin_min = np.array(t_sin) / 60
    t_con_min = np.array(t_con) / 60
    t_hielo_min = np.array(t_hielo) / 60
    
    # Graficar curvas
    plt.plot(t_sin_min, T_sin, 'b-', linewidth=2, label='Sin pérdidas térmicas')
    plt.plot(t_con_min, T_con, 'r-', linewidth=2, label='Con pérdidas térmicas')
    plt.plot(t_hielo_min, T_hielo, 'g-', linewidth=2, label='Con pérdidas y hielo')
    
    # Líneas de referencia
    plt.axhline(y=T_OBJETIVO, color='k', linestyle='--', alpha=0.7, label=f'{T_OBJETIVO}°C objetivo')
    plt.axvline(x=120/60, color='orange', linestyle=':', alpha=0.7, label='Adición de hielo (2 min)')
    
    # Configuración del gráfico
    plt.title('TP2 - Comparación de Simulaciones de Calentamiento\nIgnacio Chaves (Legajo: 61.220)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (min)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Ajustar límites
    max_tiempo = max(max(t_sin_min), max(t_con_min), max(t_hielo_min))
    plt.xlim(0, max_tiempo * 1.05)
    plt.ylim(T_INICIAL - 5, T_OBJETIVO + 5)
    
    plt.tight_layout()
    plt.show()

# =============================================================================
# FUNCIONES DE INTERFAZ PARA MAIN.PY
# =============================================================================

def ejecutar_tp2():
    """Función principal para ejecutar todo el TP2."""
    calcular_parametros_termicos()
    graficar_comparacion()

def ejecutar_calculo_perdidas():
    """Ejecuta solo el cálculo de parámetros térmicos."""
    calcular_parametros_termicos()

def ejecutar_simulacion_sin_perdidas():
    """Ejecuta solo la simulación sin pérdidas."""
    simular_sin_perdidas()

def ejecutar_simulacion_con_perdidas():
    """Ejecuta solo la simulación con pérdidas."""
    simular_con_perdidas()

def ejecutar_simulacion_hielo():
    """Ejecuta solo la simulación con hielo."""
    simular_con_hielo()

def ejecutar_grafico_comparativo():
    """Ejecuta solo el gráfico comparativo."""
    graficar_comparacion()

if __name__ == "__main__":
    ejecutar_tp2()
