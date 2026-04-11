"""
Módulo de Reportes y Estadísticas
"""

from utils.helpers import clear_screen


class ReportGenerator:
    def __init__(self, task_manager, employee_manager):
        self.task_mgr = task_manager
        self.emp_mgr = employee_manager

    def summary(self):
        tasks = self.task_mgr.get_all()
        employees = self.emp_mgr.get_all()

        total_tasks = len(tasks)
        completed = len([t for t in tasks if t["status"] == "COMPLETADA"])
        pending = total_tasks - completed
        high_priority = len([t for t in tasks if t["priority"] == "ALTA" and t["status"] == "PENDIENTE"])

        active_emp = len([e for e in employees if e["active"]])
        departments = set(e["department"] for e in employees if e["active"])

        print("\n  📊  RESUMEN GENERAL")
        print("  " + "═" * 40)
        print(f"\n  👥 Empleados activos    : {active_emp}")
        print(f"  🏢 Departamentos        : {len(departments)}")
        print(f"\n  📋 Total de tareas      : {total_tasks}")
        print(f"  ✅ Completadas          : {completed}")
        print(f"  ⏳ Pendientes           : {pending}")
        print(f"  🔴 Alta prioridad pend. : {high_priority}")

        if total_tasks > 0:
            rate = (completed / total_tasks) * 100
            bar_filled = int(rate / 5)
            bar = "█" * bar_filled + "░" * (20 - bar_filled)
            print(f"\n  Progreso: [{bar}] {rate:.1f}%")

    def by_department(self):
        employees = self.emp_mgr.get_active()
        if not employees:
            print("\n  ⚠️  No hay empleados activos.")
            return

        dept_map = {}
        for e in employees:
            dept_map.setdefault(e["department"], []).append(e["name"])

        print("\n  🏢  EMPLEADOS POR DEPARTAMENTO\n")
        for dept, names in sorted(dept_map.items()):
            print(f"  📁 {dept} ({len(names)} personas)")
            for n in names:
                print(f"      • {n}")

    def task_by_person(self):
        tasks = self.task_mgr.get_all()
        if not tasks:
            print("\n  ⚠️  No hay tareas registradas.")
            return

        person_map = {}
        for t in tasks:
            person_map.setdefault(t["assigned_to"], []).append(t)

        print("\n  📋  TAREAS POR PERSONA\n")
        for person, ptasks in sorted(person_map.items()):
            done = len([t for t in ptasks if t["status"] == "COMPLETADA"])
            print(f"  👤 {person}: {len(ptasks)} tarea(s) | ✅ {done} completada(s)")
            for t in ptasks:
                icon = "✅" if t["status"] == "COMPLETADA" else "⏳"
                print(f"      {icon} [{t['priority']}] {t['title']}")

    def menu(self):
        while True:
            clear_screen()
            print("\n  📊  REPORTES Y ESTADÍSTICAS\n")
            print("  [1] Resumen general")
            print("  [2] Empleados por departamento")
            print("  [3] Tareas por persona")
            print("  [0] Volver\n")

            opt = input("  Opción: ").strip()

            if opt == "1":
                self.summary()
            elif opt == "2":
                self.by_department()
            elif opt == "3":
                self.task_by_person()
            elif opt == "0":
                break

            input("\n  Presiona Enter para continuar...")
