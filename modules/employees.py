"""
modules/employees.py — Gestión de Empleados
"""

from datetime import datetime
from utils.helpers import (
    clear_screen, titulo, subtitulo, separador,
    ok, error, advertencia, pausa,
    mostrar_menu, pedir_opcion_menu,
    pedir_texto, pedir_email, pedir_id,
    pedir_confirmacion, imprimir_tabla,
    MAX_INTENTOS
)

DEPARTAMENTOS = [
    "Tecnología",
    "Recursos Humanos",
    "Ventas",
    "Marketing",
    "Finanzas",
    "Operaciones",
    "Legal",
]


class EmployeeManager:

    def __init__(self):
        self.employees = []
        self._next_id = 1

    # ══════════════════════════════════════════
    #  CRUD
    # ══════════════════════════════════════════

    def add_employee(self, name, department, role, email):
        if any(e["email"] == email for e in self.employees):
            error(f"Ya existe un empleado con el email '{email}'.")
            pausa()
            return None
        if any(e["name"].lower() == name.lower() for e in self.employees):
            error(f"Ya existe un empleado llamado '{name}'.")
            pausa()
            return None
        emp = {
            "id":         self._next_id,
            "name":       name,
            "department": department,
            "role":       role,
            "email":      email,
            "active":     True,
            "hire_date":  datetime.now().strftime("%Y-%m-%d"),
        }
        self.employees.append(emp)
        self._next_id += 1
        return emp

    def deactivate(self, emp_id):
        emp = self._find(emp_id)
        if not emp:
            error(f"No existe ningún empleado con ID {emp_id}.")
            pausa()
            return False
        if not emp["active"]:
            advertencia(f"'{emp['name']}' ya estaba inactivo.")
            pausa()
            return False
        emp["active"] = False
        return True

    def get_all(self):
        return self.employees

    def get_active(self):
        return [e for e in self.employees if e["active"]]

    def exists_active(self, name: str) -> bool:
        return any(e["name"].lower() == name.lower() for e in self.employees if e["active"])

    def get_name_exact(self, name: str):
        """Devuelve el nombre con capitalización original del registro."""
        for e in self.employees:
            if e["active"] and e["name"].lower() == name.lower():
                return e["name"]
        return None

    # ══════════════════════════════════════════
    #  MENÚ
    # ══════════════════════════════════════════

    def menu(self):
        while True:
            clear_screen()
            titulo("👥  GESTIÓN DE EMPLEADOS")

            self._print_employees(self.employees)

            mostrar_menu([
                "Agregar nuevo empleado",
                "Desactivar empleado",
                "Volver al menú principal",
            ])

            opt = pedir_opcion_menu(2)
            if opt is None or opt == 0:
                break
            elif opt == 1:
                self._flujo_agregar()
            elif opt == 2:
                self._flujo_desactivar()

    # ══════════════════════════════════════════
    #  FLUJOS
    # ══════════════════════════════════════════

    def _flujo_agregar(self):
        clear_screen()
        titulo("👥  NUEVO EMPLEADO")

        # ── Paso 1: Nombre ──────────────────────
        subtitulo("Paso 1 de 4 — Nombre")
        name = pedir_texto("Nombre completo", minimo=3, maximo=50)
        if name is None:
            return
        if any(e["name"].lower() == name.lower() for e in self.employees):
            error(f"Ya existe un empleado llamado '{name}'.")
            pausa()
            return

        # ── Paso 2: Departamento ─────────────────
        clear_screen()
        titulo("👥  NUEVO EMPLEADO")
        subtitulo("Paso 2 de 4 — Departamento")
        print(f"  Nombre registrado: {name}\n")
        for i, d in enumerate(DEPARTAMENTOS, 1):
            print(f"  [{i}]  {d}")
        print()

        dept_opt = pedir_opcion_menu(len(DEPARTAMENTOS))
        if dept_opt is None or dept_opt == 0:
            return
        department = DEPARTAMENTOS[dept_opt - 1]

        # ── Paso 3: Cargo ────────────────────────
        clear_screen()
        titulo("👥  NUEVO EMPLEADO")
        subtitulo("Paso 3 de 4 — Cargo")
        print(f"  Nombre      : {name}")
        print(f"  Departamento: {department}\n")
        role = pedir_texto("Cargo", minimo=2, maximo=40)
        if role is None:
            return

        # ── Paso 4: Email ────────────────────────
        clear_screen()
        titulo("👥  NUEVO EMPLEADO")
        subtitulo("Paso 4 de 4 — Email")
        print(f"  Nombre      : {name}")
        print(f"  Departamento: {department}")
        print(f"  Cargo       : {role}\n")
        email = pedir_email("Email corporativo")
        if email is None:
            return

        # ── Guardar ──────────────────────────────
        emp = self.add_employee(name, department, role, email)
        if emp:
            clear_screen()
            titulo("👥  NUEVO EMPLEADO")
            ok(f"Empleado registrado exitosamente.")
            print(f"\n  ID          : #{emp['id']}")
            print(f"  Nombre      : {emp['name']}")
            print(f"  Departamento: {emp['department']}")
            print(f"  Cargo       : {emp['role']}")
            print(f"  Email       : {emp['email']}")
            pausa()

    def _flujo_desactivar(self):
        clear_screen()
        titulo("❌  DESACTIVAR EMPLEADO")

        activos = self.get_active()
        if not activos:
            advertencia("No hay empleados activos para desactivar.")
            pausa()
            return

        self._print_employees(activos)

        emp_id = pedir_id("ID del empleado a desactivar")
        if emp_id is None:
            return

        emp = self._find(emp_id)
        if emp and pedir_confirmacion(f"¿Desactivar a '{emp['name']}'?"):
            if self.deactivate(emp_id):
                ok(f"Empleado '{emp['name']}' desactivado correctamente.")
                pausa()
        else:
            advertencia("Operación cancelada.")
            pausa()

    # ══════════════════════════════════════════
    #  HELPERS INTERNOS
    # ══════════════════════════════════════════

    def _find(self, emp_id):
        return next((e for e in self.employees if e["id"] == emp_id), None)

    def _print_employees(self, lista):
        if not lista:
            print("  (sin empleados registrados)\n")
            return
        encabezados = ["ID", "ST", "NOMBRE", "DEPARTAMENTO", "CARGO", "EMAIL"]
        anchos      = [4,   2,   20,      18,             18,     22]
        filas = []
        for e in lista:
            filas.append([
                f"#{e['id']}",
                "✅" if e["active"] else "❌",
                e["name"][:19],
                e["department"][:17],
                e["role"][:17],
                e["email"][:21],
            ])
        imprimir_tabla(encabezados, filas, anchos)
