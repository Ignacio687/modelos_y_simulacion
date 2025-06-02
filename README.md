# Simulación de Calentamiento de Agua - Código Modularizado

## Ignacio Chaves, legajo: 61.220

Este proyecto contiene simulaciones de calentamiento de agua con pérdidas térmicas, implementado de forma modular para facilitar la reutilización en los TPs 4 y 5.

## ✅ Estado del Proyecto: COMPLETADO

- ✅ Modularización completa del código original
- ✅ TP4: Familias de curvas con distribuciones normales y uniformes 
- ✅ TP5: Eventos estocásticos implementados
- ✅ Compatibilidad 100% con código original verificada
- ✅ Tests completos pasando
- ✅ Documentación completa

## Estructura del Proyecto

### Archivos Principales Modulares

- **`heat_simulation.py`**: Módulo principal con todas las clases y funciones reutilizables
- **`tp4_parameter_families.py`**: Implementación del TP 4 (familias de curvas con distribuciones)
- **`tp5_stochastic_events.py`**: Implementación del TP 5 (eventos estocásticos)
- **`demo_completo.py`**: Demostración completa de todas las funcionalidades

### Archivos de Prueba y Validación

- **`test_modular.py`**: Tests con visualización gráfica
- **`test_completo_no_graficos.py`**: Tests completos sin gráficos
- **`compare_graphs_modular.py`**: Comparación usando código modular
- **`heat_loss_graph_modular.py`**: Wrapper de compatibilidad

### Archivos Originales (Mantenidos para Compatibilidad)

- **`heat_graph.py`**: Simulación básica sin pérdidas de calor
- **`heat_loss_graph.py`**: Simulación con pérdidas térmicas
- **`heat_loss_with_ice_graph.py`**: Simulación con hielo (incompleta)
- **`compare_graphs.py`**: Comparación de las tres simulaciones

## Clases Principales

### `HeatSimulationParameters`
Almacena todos los parámetros de la simulación térmica.

### `HeatSimulator`
Ejecuta las simulaciones de calentamiento con soporte para eventos estocásticos.

### `HeatPlotter`
Genera gráficos de las simulaciones individuales y familias de curvas.

### `ParameterDistribution`
Genera distribuciones de parámetros para el TP4.

## Uso Básico

```python
from heat_simulation import HeatSimulationParameters, HeatSimulator, HeatPlotter

# Crear parámetros
params = HeatSimulationParameters(potencia=500, T_inicial=15)

# Ejecutar simulación
simulator = HeatSimulator(params)
tiempos, temperaturas = simulator.simular()

# Graficar
fig = HeatPlotter.plot_single_simulation(tiempos, temperaturas)
```

## Ejecutar Ejemplos

```bash
# Verificar que todo funciona
python test_completo_no_graficos.py  # Tests rápidos sin gráficos
python test_modular.py               # Tests con visualización

# Ejecutar TPs completos
python tp4_parameter_families.py    # TP 4 completo
python tp5_stochastic_events.py     # TP 5 completo
python demo_completo.py             # Demostración completa

# Ejemplos básicos
python heat_simulation.py           # Ejemplo básico
python heat_loss_graph_modular.py   # Compatibilidad con original
python compare_graphs_modular.py    # Comparación modular
```

## Verificación y Tests

Para verificar que el código funciona correctamente:

```bash
python test_completo_no_graficos.py
```

Este comando ejecutará todos los tests y verificará:
- ✅ Simulación básica
- ✅ Parámetros personalizados  
- ✅ Eventos estocásticos
- ✅ Distribuciones del TP4
- ✅ Simulaciones del TP4
- ✅ Simulaciones del TP5
- ✅ Compatibilidad con código original