"""
TP 1: Diseño de Parámetros del Calentador Eléctrico
====================================================

Este módulo implementa el TP1 donde se establecen los parámetros de diseño
del calentador de agua eléctrico según las especificaciones del curso.
"""

import numpy as np
import matplotlib.pyplot as plt

from utils.heat_simulation import HeatSimulationParameters


def mostrar_parametros_diseño():
    """Muestra los parámetros de diseño seleccionados para el calentador."""
    print("=" * 60)
    print("TP 1 - PARÁMETROS DE DISEÑO DEL CALENTADOR ELÉCTRICO")
    print("=" * 60)
    print()
    
    # Parámetros de diseño según las especificaciones
    print("📋 ESPECIFICACIONES DE DISEÑO:")
    print("-" * 40)
    print("• Material aislante: Acero + Poliuretano")
    print("  - Acero: k = 16 W/m·K, espesor = 1 mm")
    print("  - Poliuretano: k = 0.03 W/m·K, espesor = 1 mm")
    print()
    print("• Forma del recipiente: Cilíndrica")
    print(f"  - Radio: 0.05 m (5 cm)")
    print(f"  - Altura: 0.13 m (13 cm)")
    print(f"  - Capacidad: ~1.0 litro")
    print()
    print("• Propósito: Calentar agua hasta 100°C")
    print("• Fluido: Agua (ρ = 1000 kg/m³, c = 4186 J/kg·°C)")
    print("• Tiempo objetivo: < 2500 segundos (~42 min)")
    print()
    print("• Alimentación eléctrica:")
    print("  - Tensión: 12V (versión portátil)")
    print("  - Resistencia: 0.4 Ω")
    print("  - Potencia: V²/R = 144/0.4 = 360 W")
    print()
    print("• Condiciones iniciales:")
    print("  - Temperatura inicial agua: 20°C")
    print("  - Temperatura ambiente: 20°C")
    print()


def calcular_parametros_termicos():
    """Calcula y muestra los parámetros térmicos derivados."""
    print("🔬 CÁLCULOS TÉRMICOS:")
    print("-" * 40)
    
    # Crear parámetros con valores de diseño
    params = HeatSimulationParameters()
    
    print(f"• Coeficiente de transmisión térmica U:")
    print(f"  - Resistencia térmica acero: {0.001/16:.6f} m²K/W")
    print(f"  - Resistencia térmica poliuretano: {0.001/0.03:.6f} m²K/W")
    print(f"  - Resistencia total: {0.001/16 + 0.001/0.03:.6f} m²K/W")
    print(f"  - U = 1/R_total = {params.U:.2f} W/m²K")
    print()
    
    print(f"• Geometría del cilindro:")
    print(f"  - Área lateral: 2π × {params.radio} × {params.altura} = {params.area_lateral:.6f} m²")
    print(f"  - Área superior: π × {params.radio}² = {params.area_superior:.6f} m²")
    print(f"  - Área total: {params.area_total:.6f} m²")
    print()
    
    print(f"• Capacidad calorífica del sistema:")
    print(f"  - Masa de agua: {params.masa} kg")
    print(f"  - Capacidad: m × c = {params.masa} × {params.calor_especifico} = {params.masa * params.calor_especifico} J/°C")
    print()


def calcular_aumento_temperatura_1s():
    """Calcula el aumento de temperatura después de 1 segundo sin pérdidas."""
    print("⏱️  CÁLCULO PARA t = 1 SEGUNDO (SIN PÉRDIDAS):")
    print("-" * 40)
    
    masa = 1.0  # kg
    c = 4186    # J/kg·°C
    potencia = 360  # W
    
    # Energía entregada en 1 segundo
    energia_1s = potencia * 1  # J
    
    # Aumento de temperatura
    delta_T = energia_1s / (masa * c)
    
    print(f"• Potencia del calefactor: {potencia} W")
    print(f"• Energía entregada en 1s: {energia_1s} J")
    print(f"• Capacidad calorífica: {masa} kg × {c} J/kg·°C = {masa * c} J/°C")
    print(f"• Aumento de temperatura: ΔT = {energia_1s} J ÷ {masa * c} J/°C")
    print(f"• ΔT = {delta_T:.6f} °C")
    print()
    print(f"📊 Resultado: La temperatura aumenta {delta_T:.6f}°C en el primer segundo")
    print()


def calcular_tiempo_sin_perdidas():
    """Calcula el tiempo necesario para alcanzar 100°C sin pérdidas."""
    print("🎯 TIEMPO TEÓRICO SIN PÉRDIDAS (20°C → 100°C):")
    print("-" * 40)
    
    masa = 1.0
    c = 4186
    delta_T = 80  # °C (de 20 a 100)
    potencia = 360
    
    Q_total = masa * c * delta_T
    tiempo_teorico = Q_total / potencia
    
    print(f"• Energía total necesaria: Q = m × c × ΔT")
    print(f"  Q = {masa} kg × {c} J/kg·°C × {delta_T}°C = {Q_total:,.0f} J")
    print(f"• Tiempo teórico: t = Q / P = {Q_total:,.0f} J ÷ {potencia} W")
    print(f"• t = {tiempo_teorico:.0f} segundos = {tiempo_teorico/60:.1f} minutos")
    print()


def graficar_temperatura_teorica():
    """Grafica la curva de temperatura teórica sin pérdidas usando la misma simulación que otros TPs."""
    print("📈 GENERANDO GRÁFICO TEÓRICO (SIN PÉRDIDAS)...")
    
    # Usar la misma simulación que en TP2/TP3 para consistencia
    from utils.heat_simulation import HeatSimulationParameters, HeatSimulator
    
    # Crear parámetros normales PERO simular sin pérdidas
    params = HeatSimulationParameters(
        masa=1.0,
        potencia=360,
        T_inicial=20,
        T_amb=20,
        tiempo_total=1200,  # 20 minutos
    )
    
    # Simular SIN pérdidas térmicas (U = 0)
    params_sin_perdidas = HeatSimulationParameters(
        masa=params.masa,
        potencia=params.potencia,
        T_inicial=params.T_inicial,
        T_amb=params.T_amb,
        tiempo_total=params.tiempo_total,
        k_acero=1e6,  # Conductividad muy alta = sin pérdidas
        k_poliuretano=1e6,
        espesor_acero=0.001,
        espesor_poliuretano=0.001
    )
    
    sim = HeatSimulator(params_sin_perdidas)
    tiempos, temperaturas = sim.simular(parar_en_100c=True)
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    tiempos_min = np.array(tiempos) / 60.0
    plt.plot(tiempos_min, temperaturas, 'b-', linewidth=2, label="Temperatura teórica")
    plt.axhline(100, color='r', linestyle='--', label="100°C (objetivo)")
    plt.axhline(20, color='g', linestyle=':', alpha=0.7, label="20°C (inicial)")
    
    plt.title('TP1: Curva de Temperatura Teórica del Calentador\n(Sin pérdidas de calor)')
    plt.xlabel('Tiempo (minutos)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Encontrar el tiempo donde se alcanza 100°C
    tiempo_100c = None
    for i, temp in enumerate(temperaturas):
        if temp >= 100:
            tiempo_100c = tiempos_min[i]
            break
    
    if tiempo_100c:
        plt.annotate(f'Tiempo total: {tiempo_100c:.1f} min', 
                    xy=(tiempo_100c, 100), xytext=(tiempo_100c*0.7, 90),
                    arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                    fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.show()
    
    if tiempo_100c:
        print(f"✅ Gráfico generado - Tiempo para 100°C: {tiempo_100c:.1f} minutos")
    else:
        print(f"✅ Gráfico generado - Tiempo final: {tiempos_min[-1]:.1f} minutos")
    
    return tiempos, temperaturas


def ejecutar_tp1():
    """Ejecuta todo el TP1 completo."""
    mostrar_parametros_diseño()
    calcular_parametros_termicos()
    calcular_aumento_temperatura_1s()
    calcular_tiempo_sin_perdidas()
    graficar_temperatura_teorica()
    
    print("=" * 60)
    print("✅ TP1 COMPLETADO")
    print("=" * 60)


def ejecutar_tp1_mostrar_parametros():
    """Ejecuta solo la parte de mostrar parámetros."""
    mostrar_parametros_diseño()


def ejecutar_tp1_calculos_termicos():
    """Ejecuta solo los cálculos térmicos."""
    calcular_parametros_termicos()


def ejecutar_tp1_aumento_1s():
    """Ejecuta solo el cálculo del aumento en 1 segundo."""
    calcular_aumento_temperatura_1s()


def ejecutar_tp1_tiempo_teorico():
    """Ejecuta solo el cálculo del tiempo teórico."""
    calcular_tiempo_sin_perdidas()


def ejecutar_tp1_grafico():
    """Ejecuta solo la generación del gráfico."""
    graficar_temperatura_teorica()


if __name__ == "__main__":
    ejecutar_tp1()
