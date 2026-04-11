"""
Utilidades generales del proyecto
"""

import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print("""
  ╔══════════════════════════════════════════════════════╗
  ║        📈  BUSINESS DASHBOARD v1.0                  ║
  ║        Panel de Gestión Empresarial en Python        ║
  ╚══════════════════════════════════════════════════════╝
    """)
