import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Any


class HeatSimulationParameters:
    """Clase para almacenar todos los parámetros de la simulación térmica."""
    
    def __init__(self,
                 masa: float = 1.0,
                 calor_especifico: float = 4186,
                 potencia: float = 360,
                 T_amb: float = 20,
                 T_inicial: float = 20,
                 tiempo_total: int = 2500,
                 dt: float = 1.0,
                 radio: float = 0.05,
                 altura: float = 0.13,
                 espesor_acero: float = 0.001,
                 espesor_poliuretano: float = 0.001,
                 k_acero: float = 16,
                 k_poliuretano: float = 0.03,
                 tension: float = 12.0,  # Voltios
                 resistencia: float = 0.4):  # Ohms, para calcular potencia = V²/R
        
        self.masa = masa
        self.calor_especifico = calor_especifico
        self.potencia = potencia
        self.T_amb = T_amb
        self.T_inicial = T_inicial
        self.tiempo_total = tiempo_total
        self.dt = dt
        self.radio = radio
        self.altura = altura
        self.espesor_acero = espesor_acero
        self.espesor_poliuretano = espesor_poliuretano
        self.k_acero = k_acero
        self.k_poliuretano = k_poliuretano
        self.tension = tension
        self.resistencia = resistencia
        
        # Calcular parámetros derivados
        self._calcular_parametros_derivados()
    
    def _calcular_parametros_derivados(self):
        """Calcula parámetros derivados a partir de los básicos."""
        # Coeficiente de transmisión térmica U
        R_acero = self.espesor_acero / self.k_acero
        R_poliuretano = self.espesor_poliuretano / self.k_poliuretano
        R_total = R_acero + R_poliuretano
        self.U = 1 / R_total
        
        # Geometría del cilindro
        self.area_lateral = 2 * np.pi * self.radio * self.altura
        self.area_superior = np.pi * self.radio**2
        self.area_total = self.area_lateral + self.area_superior
        
        # Potencia basada en tensión y resistencia (si se especifica)
        if hasattr(self, 'usar_tension_resistencia') and self.usar_tension_resistencia:
            self.potencia = self.tension**2 / self.resistencia
    
    def actualizar_potencia_desde_tension(self, tension: float):
        """Actualiza la potencia basada en la tensión y resistencia."""
        self.tension = tension
        self.potencia = self.tension**2 / self.resistencia


class HeatSimulator:
    """Simulador de calentamiento de agua con pérdidas térmicas."""
    
    def __init__(self, params: HeatSimulationParameters):
        self.params = params
        self.reset()
    
    def reset(self):
        """Reinicia la simulación."""
        self.tiempos = [0]
        self.temperaturas = [self.params.T_inicial]
        self.T_actual = self.params.T_inicial
        self.tiempo_actual = 0
        self.eventos_estocasticos = []  # Para TP5
    
    def simular(self, evento_estocastico: Optional[Dict] = None) -> Tuple[List[float], List[float]]:
        """
        Ejecuta la simulación completa.
        
        Args:
            evento_estocastico: Diccionario con parámetros para eventos estocásticos (TP5)
                - probabilidad: float (ej: 1/300)
                - descenso_max: float (ej: 50)
                - duracion_min: int (segundos mínimos)
                - duracion_max: int (segundos máximos)
        
        Returns:
            Tupla (tiempos, temperaturas)
        """
        self.reset()
        
        evento_activo = False
        evento_descenso = 0
        evento_tiempo_restante = 0
        
        for t in range(1, self.params.tiempo_total + 1):
            self.tiempo_actual = t
            
            # TP5: Verificar eventos estocásticos
            if evento_estocastico and not evento_activo:
                if np.random.random() < evento_estocastico['probabilidad']:
                    evento_activo = True
                    evento_descenso = np.random.uniform(0, evento_estocastico['descenso_max'])
                    evento_tiempo_restante = np.random.randint(
                        evento_estocastico['duracion_min'], 
                        evento_estocastico['duracion_max'] + 1
                    )
                    self.eventos_estocasticos.append({
                        'tiempo': t,
                        'descenso': evento_descenso,
                        'duracion': evento_tiempo_restante
                    })
            
            # Calcular pérdidas y energía neta
            perdida = self.params.U * self.params.area_total * (self.T_actual - self.params.T_amb)
            energia_neta = self.params.potencia - perdida
            
            if energia_neta < 0:
                energia_neta = 0
            
            # Aplicar cambio de temperatura
            dT = (energia_neta * self.params.dt) / (self.params.masa * self.params.calor_especifico)
            self.T_actual += dT
            
            # TP5: Aplicar evento estocástico si está activo
            if evento_activo:
                # Aplicar descenso temporal
                descenso_por_segundo = evento_descenso / evento_tiempo_restante
                self.T_actual -= descenso_por_segundo
                evento_tiempo_restante -= 1
                
                if evento_tiempo_restante <= 0:
                    evento_activo = False
            
            self.tiempos.append(t)
            self.temperaturas.append(self.T_actual)
            
            if self.T_actual >= 100:
                break  # Alcanzamos 100°C
        
        return self.tiempos, self.temperaturas


class HeatPlotter:
    """Clase para generar gráficos de las simulaciones térmicas."""
    
    @staticmethod
    def plot_single_simulation(tiempos: List[float], temperaturas: List[float], 
                             titulo: str = "Curva de Temperatura", 
                             etiqueta: str = "Temperatura del agua",
                             color: str = 'blue',
                             linestyle: str = '-') -> plt.Figure:
        """Grafica una única simulación."""
        fig = plt.figure(figsize=(10, 6))
        
        tiempos_min = np.array(tiempos) / 60.0
        
        plt.plot(tiempos_min, temperaturas, label=etiqueta, color=color, linestyle=linestyle)
        plt.axhline(100, color='r', linestyle='--', label="100 °C")
        plt.title(titulo)
        plt.xlabel('Tiempo (min)')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.legend()
        
        HeatPlotter._ajustar_ticks_x(tiempos_min)
        
        return fig
    
    @staticmethod
    def plot_family_curves(simulaciones: List[Tuple[List[float], List[float], str]], 
                          titulo: str = "Familia de Curvas de Temperatura",
                          colores: Optional[List[str]] = None) -> plt.Figure:
        """Grafica múltiples simulaciones en el mismo gráfico."""
        fig = plt.figure(figsize=(12, 8))
        
        if colores is None:
            colores = plt.cm.tab10(np.linspace(0, 1, len(simulaciones)))
        
        max_tiempo_min = 0
        
        for i, (tiempos, temperaturas, etiqueta) in enumerate(simulaciones):
            tiempos_min = np.array(tiempos) / 60.0
            color = colores[i % len(colores)]
            plt.plot(tiempos_min, temperaturas, label=etiqueta, color=color)
            max_tiempo_min = max(max_tiempo_min, max(tiempos_min) if len(tiempos_min) > 0 else 0)
        
        plt.axhline(100, color='r', linestyle='--', label="100 °C", alpha=0.7)
        plt.title(titulo)
        plt.xlabel('Tiempo (min)')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.legend()
        
        HeatPlotter._ajustar_ticks_x_max(max_tiempo_min)
        
        return fig
    
    @staticmethod
    def _ajustar_ticks_x(tiempos_min: np.ndarray):
        """Ajusta los ticks del eje X para mejor legibilidad."""
        max_tiempo_min = max(tiempos_min) if tiempos_min.size > 0 else 0
        HeatPlotter._ajustar_ticks_x_max(max_tiempo_min)
    
    @staticmethod
    def _ajustar_ticks_x_max(max_tiempo_min: float):
        """Ajusta los ticks del eje X basado en el tiempo máximo."""
        tick_spacing = 2 if max_tiempo_min > 40 else 1
        if max_tiempo_min == 0:
            plt.xticks([0])
        else:
            upper_limit = np.ceil(max_tiempo_min / tick_spacing) * tick_spacing + tick_spacing / 2
            plt.xticks(np.arange(0, upper_limit, tick_spacing))


class ParameterDistribution:
    """Generador de distribuciones de parámetros para TP4."""
    
    @staticmethod
    def distribucion_uniforme_resistencias(n: int = 5, base: float = 0.4, variacion: float = 0.05) -> List[float]:
        """4.A: Distribución uniforme de resistencias."""
        return np.random.uniform(base - variacion, base + variacion, n).tolist()
    
    @staticmethod
    def distribucion_normal_temperatura_inicial(n: int = 5, media: float = 10, std: float = 5) -> List[float]:
        """4.B: Distribución normal de temperaturas iniciales."""
        return np.random.normal(media, std, n).tolist()
    
    @staticmethod
    def distribucion_uniforme_temperatura_ambiente(n: int = 8, min_temp: float = -20, max_temp: float = 50) -> List[float]:
        """4.C: Distribución uniforme de temperaturas ambiente."""
        return np.random.uniform(min_temp, max_temp, n).tolist()
    
    @staticmethod
    def distribucion_normal_tension(n: int = 5, media: float = 12, std: float = 4) -> List[float]:
        """4.D: Distribución normal de tensiones."""
        return np.random.normal(media, std, n).tolist()


# Funciones de conveniencia para uso directo
def simular_calentamiento_basico(params: Optional[HeatSimulationParameters] = None) -> Tuple[List[float], List[float]]:
    """Función de conveniencia para simulación básica."""
    if params is None:
        params = HeatSimulationParameters()
    
    simulator = HeatSimulator(params)
    return simulator.simular()


def simular_con_evento_estocastico(params: Optional[HeatSimulationParameters] = None,
                                 probabilidad: float = 1/300,
                                 descenso_max: float = 50,
                                 duracion_min: int = 30,
                                 duracion_max: int = 120) -> Tuple[List[float], List[float]]:
    """Función de conveniencia para simulación con eventos estocásticos (TP5)."""
    if params is None:
        params = HeatSimulationParameters()
    
    evento = {
        'probabilidad': probabilidad,
        'descenso_max': descenso_max,
        'duracion_min': duracion_min,
        'duracion_max': duracion_max
    }
    
    simulator = HeatSimulator(params)
    return simulator.simular(evento_estocastico=evento)


if __name__ == "__main__":
    # Ejemplo de uso
    params = HeatSimulationParameters()
    tiempos, temperaturas = simular_calentamiento_basico(params)
    
    fig = HeatPlotter.plot_single_simulation(
        tiempos, temperaturas, 
        "Simulación Básica de Calentamiento"
    )
    plt.show()
