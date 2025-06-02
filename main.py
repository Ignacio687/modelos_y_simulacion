#!/usr/bin/env python3
"""
SIMULADOR DE CALENTADOR ELÉCTRICO - IGNACIO CHAVES (Legajo: 61.220)
====================================================================

Archivo principal para ejecutar todos los Trabajos Prácticos del curso.
Permite seleccionar interactivamente el TP y punto específico a ejecutar.

Estructura del proyecto:
- TP1: Diseño de parámetros del calentador
- TP2: Cálculo de pérdidas térmicas + Simulación con hielo (extra)
- TP3: Gráficos con y sin pérdidas + Comparaciones
- TP4: Familias de curvas con distribuciones
- TP5: Eventos estocásticos

Uso: python main.py
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Callable

# Agregar paths para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'tps'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Importar módulos del proyecto
from tp1_diseño import ejecutar_tp1
from tp2_perdidas import ejecutar_tp2
from tp2_hielo import ejecutar_tp2_hielo
from tp3_graficos import ejecutar_tp3, ejecutar_comparacion_completa
from tp4_familias import (
    ejecutar_tp4_resistencias, ejecutar_tp4_temperaturas_iniciales,
    ejecutar_tp4_temperaturas_ambiente, ejecutar_tp4_tensiones_12v,
    ejecutar_tp4_tensiones_220v, mostrar_info_tp4
)
from tp5_estocasticos import (
    ejecutar_tp5_evento_basico, ejecutar_tp5_multiples_simulaciones,
    ejecutar_tp5_tp4_con_eventos
)


class MenuPrincipal:
    """Clase para manejar el menú interactivo del simulador."""
    
    def __init__(self):
        self.opciones_tp: Dict[str, Dict[str, Callable]] = {
            "1": {
                "titulo": "TP 1 - Diseño de Parámetros del Calentador",
                "opciones": {
                    "1": ("Ejecutar TP1 completo", ejecutar_tp1),
                }
            },
            "2": {
                "titulo": "TP 2 - Cálculo de Pérdidas Térmicas",
                "opciones": {
                    "1": ("Ejecutar TP2 - Cálculo de pérdidas", ejecutar_tp2),
                    "2": ("EXTRA - Simulación con hielo", ejecutar_tp2_hielo),
                }
            },
            "3": {
                "titulo": "TP 3 - Gráficos de Temperatura",
                "opciones": {
                    "1": ("Ejecutar TP3 - Gráficos básicos", ejecutar_tp3),
                    "2": ("Comparación completa de gráficos", ejecutar_comparacion_completa),
                }
            },
            "4": {
                "titulo": "TP 4 - Familias de Curvas con Distribuciones",
                "opciones": {
                    "1": ("4.A - Distribución uniforme de resistencias", ejecutar_tp4_resistencias),
                    "2": ("4.B - Distribución normal de temperaturas iniciales", ejecutar_tp4_temperaturas_iniciales),
                    "3": ("4.C - Distribución uniforme de temperaturas ambiente", ejecutar_tp4_temperaturas_ambiente),
                    "4": ("4.D - Distribución normal de tensiones (12V)", ejecutar_tp4_tensiones_12v),
                    "5": ("4.E - Distribución normal de tensiones (220V)", ejecutar_tp4_tensiones_220v),
                    "6": ("4.F - Información del TP4", mostrar_info_tp4),
                }
            },
            "5": {
                "titulo": "TP 5 - Eventos Estocásticos",
                "opciones": {
                    "1": ("5.1 - Simulación básica con eventos estocásticos", ejecutar_tp5_evento_basico),
                    "2": ("5.2 - Múltiples simulaciones estocásticas", ejecutar_tp5_multiples_simulaciones),
                    "3": ("5.3 - Familias del TP4 con eventos estocásticos", ejecutar_tp5_tp4_con_eventos),
                }
            }
        }
    
    def mostrar_banner(self):
        """Muestra el banner principal del programa."""
        print("=" * 80)
        print("🔥 SIMULADOR DE CALENTADOR ELÉCTRICO 🔥")
        print("   Ignacio Chaves - Legajo: 61.220")
        print("   Modelos y Simulación - UM (Universidad de Mendoza)")
        print("=" * 80)
        print("📋 Trabajos Prácticos Disponibles:")
        print()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal con todos los TPs."""
        for tp_num, tp_data in self.opciones_tp.items():
            print(f"  [{tp_num}] {tp_data['titulo']}")
        print(f"  [0] Salir")
        print()
    
    def mostrar_submenu(self, tp_num: str):
        """Muestra el submenú de un TP específico."""
        tp_data = self.opciones_tp[tp_num]
        print(f"\n📊 {tp_data['titulo']}")
        print("-" * 60)
        
        for opcion_num, (descripcion, _) in tp_data['opciones'].items():
            print(f"  [{tp_num}.{opcion_num}] {descripcion}")
        print(f"  [0] Volver al menú principal")
        print()
    
    def ejecutar_opcion(self, tp_num: str, opcion_num: str):
        """Ejecuta una opción específica de un TP."""
        try:
            tp_data = self.opciones_tp[tp_num]
            descripcion, funcion = tp_data['opciones'][opcion_num]
            
            print(f"\n🚀 Ejecutando: {descripcion}")
            print("=" * 60)
            
            # Ejecutar la función
            funcion()
            
            print("\n✅ Ejecución completada!")
            input("\nPresiona Enter para continuar...")
            
        except KeyError:
            print("❌ Opción no válida!")
        except Exception as e:
            print(f"❌ Error durante la ejecución: {e}")
            import traceback
            traceback.print_exc()
    
    def ejecutar(self):
        """Ejecuta el menú principal interactivo."""
        while True:
            # Limpiar pantalla (funciona en Linux/macOS/Windows)
            os.system('clear' if os.name == 'posix' else 'cls')
            
            self.mostrar_banner()
            self.mostrar_menu_principal()
            
            opcion = input("🎯 Selecciona un TP (0 para salir): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            
            if opcion not in self.opciones_tp:
                print("❌ Opción no válida!")
                input("Presiona Enter para continuar...")
                continue
            
            # Mostrar submenú del TP seleccionado
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                self.mostrar_banner()
                self.mostrar_submenu(opcion)
                
                sub_opcion = input(f"🎯 Selecciona una opción del TP{opcion} (0 para volver): ").strip()
                
                if sub_opcion == "0":
                    break
                
                if sub_opcion in self.opciones_tp[opcion]['opciones']:
                    self.ejecutar_opcion(opcion, sub_opcion)
                else:
                    print("❌ Opción no válida!")
                    input("Presiona Enter para continuar...")


def main():
    """Función principal del programa."""
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
