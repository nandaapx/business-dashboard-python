"""
╔══════════════════════════════════════════════════════╗
║         BUSINESS DASHBOARD v2.0                      ║
║         Panel de Gestión Empresarial Python          ║
╚══════════════════════════════════════════════════════╝
"""

import json
from modules.tasks     import TaskManager
from modules.reports   import ReportGenerator
from modules.employees import EmployeeManager
from utils.helpers import (
    clear_screen, print_banner, titulo,
    mostrar_menu, pedir_opcion_menu,
    ok, advertencia, pausa
)


def run():
    task_mgr   = TaskManager()
    emp_mgr    = EmployeeManager()
    report_gen = ReportGenerator(task_mgr, emp_mgr)

    while True:
        clear_screen()
        print_banner()

        mostrar_menu([
            "👥   Gestión de Empleados",
            "✅   Gestión de Tareas / Proyectos",
            "📊   Reportes y Estadísticas",
            "💾   Exportar datos a JSON",
            "🚪   Salir",
        ])

        opt = pedir_opcion_menu(4)

        if opt is None:
            continue
        elif opt == 1:
            emp_mgr.menu()
        elif opt == 2:
            task_mgr.menu(emp_mgr)
        elif opt == 3:
            report_gen.menu()
        elif opt == 4:
            _exportar(task_mgr, emp_mgr)
        elif opt == 0:
            clear_screen()
            print("\n  👋  ¡Hasta pronto!\n")
            break


def _exportar(task_mgr, emp_mgr):
    clear_screen()
    titulo("💾  EXPORTAR DATOS")

    data = {
        "empleados": emp_mgr.get_all(),
        "tareas":    task_mgr.get_all(),
    }

    if not data["empleados"] and not data["tareas"]:
        advertencia("No hay datos para exportar.")
        pausa()
        return

    nombre_archivo = "export_data.json"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    ok(f"Datos exportados correctamente en '{nombre_archivo}'.")
    print(f"\n  Empleados exportados : {len(data['empleados'])}")
    print(f"  Tareas exportadas    : {len(data['tareas'])}")
    pausa()


if __name__ == "__main__":
    run()
