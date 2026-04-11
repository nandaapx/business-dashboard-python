"""
Módulo de Gestión de Empleados
"""

from datetime import datetime
from utils.helpers import clear_screen


class EmployeeManager:
    def __init__(self):
        self.employees = []
        self._next_id = 1

    # ──────────────────────────────────────────
    #  CRUD
    # ──────────────────────────────────────────
    def add_employee(self, name: str, department: str, role: str, email: str):
        emp = {
            "id": self._next_id,
            "name": name,
            "department": department,
            "role": role,
            "email": email,
            "active": True,
            "hire_date": datetime.now().strftime("%Y-%m-%d")
        }
        self.employees.append(emp)
        self._next_id += 1
        return emp

    def deactivate(self, emp_id: int):
        emp = self._find(emp_id)
        if emp:
            emp["active"] = False
            return True
        return False

    def get_all(self):
        return self.employees

    def get_active(self):
        return [e for e in self.employees if e["active"]]

    # ──────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────
    def _find(self, emp_id: int):
        return next((e for e in self.employees if e["id"] == emp_id), None)

    def _print_employees(self, emp_list):
        if not emp_list:
            print("\n  ⚠️  No hay empleados para mostrar.")
            return
        print(f"\n  {'ID':<4} {'NOMBRE':<22} {'DEPARTAMENTO':<18} {'CARGO':<18} {'EMAIL'}")
        print("  " + "─" * 80)
        for e in emp_list:
            status = "✅" if e["active"] else "❌"
            print(f"  {e['id']:<4} {status} {e['name']:<20} {e['department']:<18} {e['role']:<18} {e['email']}")

    # ──────────────────────────────────────────
    #  Menú interactivo
    # ──────────────────────────────────────────
    def menu(self):
        while True:
            clear_screen()
            print("\n  👥  GESTIÓN DE EMPLEADOS\n")
            print("  [1] Agregar empleado")
            print("  [2] Ver todos los empleados")
            print("  [3] Desactivar empleado")
            print("  [0] Volver\n")

            opt = input("  Opción: ").strip()

            if opt == "1":
                print("\n  ── Nuevo Empleado ──")
                name = input("  Nombre completo: ").strip()
                dept = input("  Departamento: ").strip()
                role = input("  Cargo: ").strip()
                email = input("  Email: ").strip()
                e = self.add_employee(name, dept, role, email)
                print(f"\n  ✅ Empleado #{e['id']} registrado.")

            elif opt == "2":
                self._print_employees(self.employees)

            elif opt == "3":
                self._print_employees(self.get_active())
                try:
                    eid = int(input("\n  ID del empleado a desactivar: "))
                    if self.deactivate(eid):
                        print("  ✅ Empleado desactivado.")
                    else:
                        print("  ⚠️  Empleado no encontrado.")
                except ValueError:
                    print("  ⚠️  ID inválido.")

            elif opt == "0":
                break

            input("\n  Presiona Enter para continuar...")
