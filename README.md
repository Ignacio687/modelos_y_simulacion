# Simulador de Calentador Eléctrico

**Autor:** Ignacio Chaves (Legajo: 61.220)  
**Materia:** Modelos y Simulación - Universidad de Mendoza

## Descripción

Este repositorio contiene un simulador completo de calentador eléctrico desarrollado en Python que modela el comportamiento térmico de un sistema de calentamiento de agua. El proyecto implementa múltiples aspectos de la simulación física incluyendo transferencia de calor, pérdidas térmicas, efectos de cambio de fase (hielo), y eventos estocásticos.

## Funcionalidades

### TP1 - Diseño de Parámetros
- Cálculo y optimización de parámetros del calentador (resistencia, potencia, geometría)
- Selección de materiales y dimensiones del recipiente

### TP2 - Pérdidas Térmicas
- Simulación con pérdidas de calor al ambiente
- Modelo físico completo de transferencia de calor con hielo (derretimiento, convección)

### TP3 - Visualización Gráfica
- Gráficos comparativos de temperatura vs tiempo
- Escenarios: sin pérdidas, con pérdidas, y con efectos de hielo

### TP4 - Análisis de Sensibilidad
- Familias de curvas con distribuciones estadísticas de parámetros:
  - Distribución uniforme de resistencias
  - Distribución normal de temperaturas iniciales
  - Distribución uniforme de temperaturas ambiente
  - Distribución normal de tensiones (12V)

### TP5 - Eventos Estocásticos
- Simulación de perturbaciones aleatorias (descensos de temperatura)
- Probabilidad de ocurrencia: 1/300 por tick de tiempo
- Análisis comparativo con y sin eventos estocásticos

## Estructura del Proyecto

```
modelos_y_simulacion/
├── main.py                 # Punto de entrada principal con menú interactivo
├── tps/                    # Módulos de cada trabajo práctico
│   ├── tp1_diseño.py
│   ├── tp2_perdidas.py
│   ├── tp2_hielo.py
│   ├── tp3_graficos.py
│   ├── tp4_familias.py
│   └── tp5_estocasticos.py
├── utils/                  # Utilitarios y simulador principal
│   └── heat_simulation.py  # Clase HeatSimulator con toda la física
└── tests/                  # Scripts de prueba y validación
```

## Instalación y Uso

### Requisitos
- Python 3.8+
- numpy
- matplotlib

### Instalación
```bash
# Clonar el repositorio
git clone <repo-url>
cd modelos_y_simulacion

# Crear entorno virtual (recomendado)
python -m venv env
source env/bin/activate  # Linux/macOS
# o: env\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución
```bash
# Ejecutar el menú principal interactivo
python main.py

# Ejecutar un TP específico directamente
python -m tps.tp1_diseño
python -m tps.tp2_perdidas
# etc.
```

### Uso del Simulador

El programa presenta un menú interactivo que permite:

1. **Seleccionar un TP** (1-5)
2. **Elegir una funcionalidad específica** dentro del TP
3. **Ver gráficos y resultados** automáticamente

Ejemplo de flujo:
1. Ejecutar `python main.py`
2. Seleccionar "3" para TP3 (Gráficos)
3. Seleccionar "4" para comparación completa
4. El programa generará y mostrará los gráficos comparativos

## Características Técnicas

- **Modelo físico realista**: Incluye conducción, convección, y cambios de fase
- **Parámetros configurables**: Masa, potencia, geometría, materiales
- **Visualización avanzada**: Gráficos interactivos con matplotlib
- **Análisis estadístico**: Distribuciones normales y uniformes
- **Eventos aleatorios**: Simulación Monte Carlo de perturbaciones

## Testing

```bash
# Ejecutar todas las pruebas
python test_final.py

# Pruebas específicas
python tests/demo_completo.py
```

---

*Desarrollado para el curso de Modelos y Simulación, implementando conceptos de transferencia de calor, análisis numérico, y simulación estocástica.*