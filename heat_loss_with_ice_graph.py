import numpy as np
import matplotlib.pyplot as plt

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

# Inicialización
T_agua = 20  # Temperatura inicial en °C
T_hielo_actual = T_hielo
masa_agua = masa
masa_hielo_restante = masa_hielo_total
energia_fusion_restante = masa_hielo_total * calor_fusion_hielo

tiempos = [0]
temperaturas = [T_agua]

# Simulación segundo a segundo
for t in range(1, tiempo_total + 1):
    # Energía neta del calefactor (potencia) en este paso de tiempo (dt=1)
    energia_calefactor_dt = potencia * dt
    # Pérdida de calor al ambiente en este paso
    perdida_ambiente_dt = U * area_total * (T_agua - T_amb) * dt
    
    # Energía neta disponible del calefactor para el sistema
    energia_neta_disponible_dt = energia_calefactor_dt - perdida_ambiente_dt
    if energia_neta_disponible_dt < 0:
        energia_neta_disponible_dt = 0

    energia_para_calentar_agua_final_dt = energia_neta_disponible_dt # Energía del calefactor que podría calentar el agua

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
            masa_agua_antes_conv = masa_agua # Para cálculo de enfriamiento del agua

            # Aplicar energia_conv_dt para calentar hielo a 0°C
            if T_hielo_actual < 0:
                calor_necesario_hielo_a_0_conv = masa_hielo_restante * calor_especifico_hielo * abs(T_hielo_actual)
                absorbido_calentar_conv = min(energia_conv_dt, calor_necesario_hielo_a_0_conv)
                T_hielo_actual += absorbido_calentar_conv / (masa_hielo_restante * calor_especifico_hielo)
                energia_conv_dt -= absorbido_calentar_conv
                energia_efectiva_transferida_conv += absorbido_calentar_conv
            
            # Aplicar energia_conv_dt restante para derretir hielo a 0°C
            if T_hielo_actual == 0 and energia_conv_dt > 0 and masa_hielo_restante > 0:
                calor_necesario_fusion_conv = masa_hielo_restante * calor_fusion_hielo
                absorbido_fusion_conv = min(energia_conv_dt, calor_necesario_fusion_conv)
                masa_derretida_conv = absorbido_fusion_conv / calor_fusion_hielo
                masa_agua += masa_derretida_conv
                masa_hielo_restante -= masa_derretida_conv
                energia_efectiva_transferida_conv += absorbido_fusion_conv

            # Enfriar el agua debido a la energía cedida por convección
            if masa_agua_antes_conv > 0 and energia_efectiva_transferida_conv > 0:
                T_agua -= energia_efectiva_transferida_conv / (masa_agua_antes_conv * calor_especifico)

        # 2. Aplicar energía del calefactor (energia_para_calentar_agua_final_dt) al hielo
        if T_hielo_actual is not None and masa_hielo_restante > 0: # Verificar de nuevo por si se derritió todo por convección
            # Calentar hielo a 0°C con energía del calefactor
            if T_hielo_actual < 0:
                calor_necesario_hielo_a_0_calefactor = masa_hielo_restante * calor_especifico_hielo * abs(T_hielo_actual)
                gastado_calentar_hielo_calefactor = min(energia_para_calentar_agua_final_dt, calor_necesario_hielo_a_0_calefactor)
                T_hielo_actual += gastado_calentar_hielo_calefactor / (masa_hielo_restante * calor_especifico_hielo)
                energia_para_calentar_agua_final_dt -= gastado_calentar_hielo_calefactor
            
            # Derretir hielo a 0°C con energía restante del calefactor
            if T_hielo_actual == 0 and masa_hielo_restante > 0: # Verificar T_hielo_actual de nuevo
                calor_necesario_fusion_calefactor = masa_hielo_restante * calor_fusion_hielo
                gastado_fusion_hielo_calefactor = min(energia_para_calentar_agua_final_dt, calor_necesario_fusion_calefactor)
                masa_derretida_calefactor = gastado_fusion_hielo_calefactor / calor_fusion_hielo
                masa_agua += masa_derretida_calefactor
                masa_hielo_restante -= masa_derretida_calefactor
                energia_para_calentar_agua_final_dt -= gastado_fusion_hielo_calefactor
        
        if masa_hielo_restante <= 0: # Si todo el hielo se derritió en este paso
            T_hielo_actual = None
            energia_fusion_restante = 0


    # 3. Aplicar la energía restante del calefactor para calentar el agua
    if energia_para_calentar_agua_final_dt > 0 and masa_agua > 0:
        T_agua += energia_para_calentar_agua_final_dt / (masa_agua * calor_especifico)

    # Restricciones de temperatura finales para el paso
    if T_hielo_actual is not None and masa_hielo_restante > 0:
        if T_hielo_actual < 0 :
             T_agua = max(T_agua, T_hielo_actual) # Agua no puede estar más fría que el hielo con el que está en contacto
        else: # Hielo está a 0°C
             T_agua = max(T_agua, 0) # Agua no puede estar por debajo de 0°C si hay hielo a 0°C
    elif T_agua < 0: # No hay hielo, el agua no debería congelarse espontáneamente
        T_agua = 0
    
    tiempos.append(t)
    temperaturas.append(T_agua)
    if T_agua >= 100:
        break  # Alcanzamos 100°C

if __name__ == "__main__":
    # Código para ejecutar el gráfico
    plt.figure(figsize=(10,6))
    
    # Convertir tiempos a minutos para el eje X
    tiempos_min_plot = np.array(tiempos) / 60.0
    
    plt.plot(tiempos_min_plot, temperaturas, label="Temperatura del agua con hielo")
    plt.axhline(100, color='r', linestyle='--', label="100 °C")
    plt.title('Curva de Temperatura con Pérdidas de Calor y Hielo')
    plt.xlabel('Tiempo (min)') # Etiqueta del eje X actualizada
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.legend()
    
    # Ajustar los ticks del eje X para que sean más legibles en minutos
    max_tiempo_min = max(tiempos_min_plot) if tiempos_min_plot.size > 0 else 0
    # Generar ticks cada 2 minutos si el total es > 10 min, sino cada 1 minuto.
    tick_spacing = 2 if max_tiempo_min > 40 else 1
    if max_tiempo_min == 0: 
        plt.xticks([0])
    else:
        upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
        plt.xticks(np.arange(0, upper_limit, tick_spacing))
    
    plt.show()