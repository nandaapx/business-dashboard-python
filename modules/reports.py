"""
modules/reports.py — Reportes y Estadísticas
"""

from utils.helpers import (
    clear_screen, titulo, subtitulo, separador,
    ok, advertencia, pausa,
    mostrar_menu, pedir_opcion_menu,
    imprimir_tabla
)


class ReportGenerator:

    def __init__(self, task_manager, employee_manager):
        self.task_mgr = task_manager
        self.emp_mgr  = employee_manager

    # ══════════════════════════════════════════
    #  MENÚ
    # ══════════════════════════════════════════

    def menu(self):
        while True:
            clear_screen()
            titulo("📊  REPORTES Y ESTADÍSTICAS")

            tasks     = self.task_mgr.get_all()
            employees = self.emp_mgr.get_all()

            if not employees and not tasks:
                advertencia("No hay datos registrados aún.")
                print("  Agrega empleados y tareas primero.\n")
                mostrar_menu(["Volver al menú principal"])
                pedir_opcion_menu(0)
                break

            # Mini resumen siempre visible
            self._mini_resumen(tasks, employees)

            mostrar_menu([
                "Resumen general completo",
                "Empleados por departamento",
                "Tareas por persona",
                "Volver al menú principal",
            ])

            opt = pedir_opcion_menu(3)
            if opt is None or opt == 0:
                break
            elif opt == 1:
                self._resumen_completo(tasks, employees)
            elif opt == 2:
                self._por_departamento()
            elif opt == 3:
                self._por_persona(tasks)

    # ══════════════════════════════════════════
    #  REPORTES
    # ══════════════════════════════════════════

    def _mini_resumen(self, tasks, employees):
        total    = len(tasks)
        done     = sum(1 for t in tasks if t["status"] == "COMPLETADA")
        activos  = sum(1 for e in employees if e["active"])
        pct      = round((done / total) * 100) if total > 0 else 0
        filled   = pct // 5
        barra    = "█" * filled + "░" * (20 - filled)

        separador("─", 48)
        print(f"  👥 Empleados activos : {activos}   "
              f"📋 Tareas: {total}   ✅ {done}   ⏳ {total - done}")
        print(f"  Progreso  [{barra}] {pct}%")
        separador("─", 48)

    def _resumen_completo(self, tasks, employees):
        clear_screen()
        titulo("📊  RESUMEN GENERAL")

        total    = len(tasks)
        done     = sum(1 for t in tasks if t["status"] == "COMPLETADA")
        pending  = total - done
        high     = sum(1 for t in tasks
                       if t["priority"] == "ALTA" and t["status"] == "PENDIENTE")
        activos  = sum(1 for e in employees if e["active"])
        inactivos = len(employees) - activos
        deptos   = set(e["department"] for e in employees if e["active"])

        print(f"  👥  Empleados activos     : {activos}")
        print(f"  ❌  Empleados inactivos   : {inactivos}")
        print(f"  🏢  Departamentos activos : {len(deptos)}")
        separador()
        print(f"  📋  Total de tareas       : {total}")
        print(f"  ✅  Completadas           : {done}")
        print(f"  ⏳  Pendientes            : {pending}")
        print(f"  🔴  Alta prioridad pend.  : {high}")

        if total > 0:
            pct    = round((done / total) * 100)
            filled = pct // 5
            barra  = "█" * filled + "░" * (20 - filled)
            print(f"\n  Progreso general:")
            print(f"  [{barra}] {pct}%")

        pausa()

    def _por_departamento(self):
        clear_screen()
        titulo("🏢  EMPLEADOS POR DEPARTAMENTO")

        activos = self.emp_mgr.get_active()
        if not activos:
            advertencia("No hay empleados activos registrados.")
            pausa()
            return

        dept_map = {}
        for e in activos:
            dept_map.setdefault(e["department"], []).append(e)

        for dept, emps in sorted(dept_map.items()):
            subtitulo(f"{dept}  ({len(emps)} persona(s))")
            for e in emps:
                print(f"  • #{e['id']}  {e['name']}  —  {e['role']}")
            print()

        pausa()

    def _por_persona(self, tasks):
        clear_screen()
        titulo("📋  TAREAS POR PERSONA")

        if not tasks:
            advertencia("No hay tareas registradas.")
            pausa()
            return

        person_map = {}
        for t in tasks:
            person_map.setdefault(t["assigned_to"], []).append(t)

        for persona, lista in sorted(person_map.items()):
            done = sum(1 for t in lista if t["status"] == "COMPLETADA")
            subtitulo(f"{persona}  —  {len(lista)} tarea(s)  |  ✅ {done} completada(s)")
            for t in lista:
                icono  = "✅" if t["status"] == "COMPLETADA" else "⏳"
                prio   = {"ALTA": "🔴", "MEDIA": "🟡", "BAJA": "🟢"}.get(t["priority"], "")
                print(f"  {icono}  [{prio} {t['priority']}]  {t['title']}")
            print()

        pausa()
