"""
╔══════════════════════════════════════════════════════╗
║         BUSINESS DASHBOARD - PANEL EMPRESARIAL       ║
║         Herramienta de gestión para empresas         ║
╚══════════════════════════════════════════════════════╝
"""
 
from modules.tasks import TaskManager
from modules.reports import ReportGenerator
from modules.employees import EmployeeManager
from utils.helpers import clear_screen, print_banner
import json
 
 
def main_menu():
    clear_screen()
    print_banner()
    print("\n  📋  MENÚ PRINCIPAL\n")
    print("  [1] 👥  Gestión de Empleados")
    print("  [2] ✅  Gestión de Tareas / Proyectos")
    print("  [3] 📊  Reportes y Estadísticas")
    print("  [4] 💾  Exportar Datos (JSON)")
    print("  [0] 🚪  Salir\n")
    return input("  Selecciona una opción: ").strip()
 
 
def run():
    task_mgr = TaskManager()
    emp_mgr = EmployeeManager()
    report_gen = ReportGenerator(task_mgr, emp_mgr)
 
    while True:
        option = main_menu()
 
        if option == "1":
            emp_mgr.menu()
        elif option == "2":
            task_mgr.menu(emp_mgr)
        elif option == "3":
            report_gen.menu()
        elif option == "4":
            data = {
                "empleados": emp_mgr.get_all(),
                "tareas": task_mgr.get_all()
            }
            with open("export_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("\n  ✅ Datos exportados en 'export_data.json'")
            input("\n  Presiona Enter para continuar...")
        elif option == "0":
            print("\n  👋 ¡Hasta Luego!\n")
            break
        else:
            print("\n  ⚠️  Opción inválida. Elige entre 0 y 4.")
            input("  Presiona Enter para continuar...")
 
 
if __name__ == "__main__":
    run()
 