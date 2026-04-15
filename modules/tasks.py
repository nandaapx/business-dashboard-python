"""
modules/tasks.py — Gestión de Tareas
"""

from datetime import datetime
from utils.helpers import (
    clear_screen, titulo, subtitulo, separador,
    ok, error, advertencia, pausa,
    mostrar_menu, pedir_opcion_menu,
    pedir_texto, pedir_id, pedir_confirmacion,
    imprimir_tabla, MAX_INTENTOS
)

PRIORIDADES = ["ALTA", "MEDIA", "BAJA"]
ICONOS_PRIO = {"ALTA": "🔴", "MEDIA": "🟡", "BAJA": "🟢"}


class TaskManager:

    def __init__(self):
        self.tasks = []
        self._next_id = 1

    # ══════════════════════════════════════════
    #  CRUD
    # ══════════════════════════════════════════

    def add_task(self, title, description, priority, assigned_to):
        if any(t["title"].lower() == title.lower() for t in self.tasks):
            error(f"Ya existe una tarea llamada '{title}'.")
            pausa()
            return None
        task = {
            "id":           self._next_id,
            "title":        title,
            "description":  description,
            "priority":     priority.upper(),
            "assigned_to":  assigned_to,
            "status":       "PENDIENTE",
            "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None,
        }
        self.tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id):
        task = self._find(task_id)
        if not task:
            error(f"No existe ninguna tarea con ID {task_id}.")
            pausa()
            return False
        if task["status"] == "COMPLETADA":
            advertencia(f"La tarea '{task['title']}' ya estaba completada.")
            pausa()
            return False
        task["status"] = "COMPLETADA"
        task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return True

    def delete_task(self, task_id):
        task = self._find(task_id)
        if not task:
            error(f"No existe ninguna tarea con ID {task_id}.")
            pausa()
            return False
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        return True

    def get_all(self):
        return self.tasks

    # ══════════════════════════════════════════
    #  MENÚ
    # ══════════════════════════════════════════

    def menu(self, emp_mgr=None):
        while True:
            clear_screen()
            titulo("✅  GESTIÓN DE TAREAS")

            self._print_tasks(self.tasks)

            mostrar_menu([
                "Agregar nueva tarea",
                "Marcar tarea como completada",
                "Eliminar tarea",
                "Volver al menú principal",
            ])

            opt = pedir_opcion_menu(3)
            if opt is None or opt == 0:
                break
            elif opt == 1:
                self._flujo_agregar(emp_mgr)
            elif opt == 2:
                self._flujo_completar()
            elif opt == 3:
                self._flujo_eliminar()

    # ══════════════════════════════════════════
    #  FLUJOS
    # ══════════════════════════════════════════

    def _flujo_agregar(self, emp_mgr):
        clear_screen()
        titulo("✅  NUEVA TAREA")

        # ── Paso 1: Título ───────────────────────
        subtitulo("Paso 1 de 4 — Título")
        title = pedir_texto("Título de la tarea", minimo=3, maximo=50)
        if title is None:
            return
        if any(t["title"].lower() == title.lower() for t in self.tasks):
            error(f"Ya existe una tarea llamada '{title}'.")
            pausa()
            return

        # ── Paso 2: Descripción ──────────────────
        clear_screen()
        titulo("✅  NUEVA TAREA")
        subtitulo("Paso 2 de 4 — Descripción")
        print(f"  Título: {title}\n")
        description = pedir_texto("Descripción", minimo=5, maximo=120)
        if description is None:
            return

        # ── Paso 3: Prioridad ────────────────────
        clear_screen()
        titulo("✅  NUEVA TAREA")
        subtitulo("Paso 3 de 4 — Prioridad")
        print(f"  Título: {title}\n")
        for i, p in enumerate(PRIORIDADES, 1):
            print(f"  [{i}]  {ICONOS_PRIO[p]}  {p}")
        print()

        prio_opt = pedir_opcion_menu(len(PRIORIDADES))
        if prio_opt is None or prio_opt == 0:
            return
        priority = PRIORIDADES[prio_opt - 1]

        # ── Paso 4: Asignar empleado ─────────────
        clear_screen()
        titulo("✅  NUEVA TAREA")
        subtitulo("Paso 4 de 4 — Asignar a empleado")
        print(f"  Título   : {title}")
        print(f"  Prioridad: {ICONOS_PRIO[priority]} {priority}\n")

        assigned = self._pedir_asignado(emp_mgr)
        if assigned is None:
            return

        # ── Guardar ──────────────────────────────
        task = self.add_task(title, description, priority, assigned)
        if task:
            clear_screen()
            titulo("✅  NUEVA TAREA")
            ok("Tarea creada exitosamente.")
            print(f"\n  ID        : #{task['id']}")
            print(f"  Título    : {task['title']}")
            print(f"  Prioridad : {ICONOS_PRIO[task['priority']]} {task['priority']}")
            print(f"  Asignado  : {task['assigned_to']}")
            print(f"  Estado    : ⏳ PENDIENTE")
            pausa()

    def _flujo_completar(self):
        clear_screen()
        titulo("✅  COMPLETAR TAREA")

        pendientes = [t for t in self.tasks if t["status"] == "PENDIENTE"]
        if not pendientes:
            advertencia("No hay tareas pendientes para completar.")
            pausa()
            return

        self._print_tasks(pendientes)

        task_id = pedir_id("ID de la tarea a completar")
        if task_id is None:
            return

        task = self._find(task_id)
        if task and task["status"] != "PENDIENTE":
            advertencia(f"La tarea #{task_id} ya está completada.")
            pausa()
            return

        if task and pedir_confirmacion(f"¿Marcar '{task['title']}' como completada?"):
            if self.complete_task(task_id):
                ok(f"Tarea '{task['title']}' marcada como completada.")
                pausa()
        else:
            advertencia("Operación cancelada.")
            pausa()

    def _flujo_eliminar(self):
        clear_screen()
        titulo("🗑️   ELIMINAR TAREA")

        if not self.tasks:
            advertencia("No hay tareas registradas.")
            pausa()
            return

        self._print_tasks(self.tasks)

        task_id = pedir_id("ID de la tarea a eliminar")
        if task_id is None:
            return

        task = self._find(task_id)
        if not task:
            error(f"No existe ninguna tarea con ID {task_id}.")
            pausa()
            return

        print(f"\n  Tarea seleccionada: [{task['priority']}] {task['title']}")
        if pedir_confirmacion("¿Confirmas eliminar esta tarea?"):
            if self.delete_task(task_id):
                ok("Tarea eliminada correctamente.")
                pausa()
        else:
            advertencia("Eliminación cancelada.")
            pausa()

    # ══════════════════════════════════════════
    #  ASIGNACIÓN CON 3 INTENTOS
    # ══════════════════════════════════════════

    def _pedir_asignado(self, emp_mgr):
        """Pide nombre de empleado activo con MAX_INTENTOS intentos."""
        activos = emp_mgr.get_active() if emp_mgr else []

        if emp_mgr and not activos:
            advertencia("No hay empleados activos. Registra empleados primero.")
            pausa()
            return None

        if activos:
            print("  Empleados activos disponibles:\n")
            for e in activos:
                print(f"    • {e['name']}  ({e['department']})")
            print()

        for intento in range(1, MAX_INTENTOS + 1):
            nombre = input("  Asignar a (escribe el nombre exacto): ").strip()
            restantes = MAX_INTENTOS - intento

            if not nombre:
                if restantes > 0:
                    print(f"  ⚠️   El nombre no puede estar vacío. "
                          f"Intentos restantes: {restantes}")
                else:
                    print("  ❌  Sin más intentos. Operación cancelada.")
                    pausa()
                continue

            if emp_mgr is None:
                return nombre

            nombre_exacto = emp_mgr.get_name_exact(nombre)
            if nombre_exacto:
                return nombre_exacto

            if restantes > 0:
                print(f"  ❌  '{nombre}' no es un empleado activo registrado.")
                print(f"  ⚠️   Escribe el nombre exactamente como aparece en la lista.")
                print(f"       Intentos restantes: {restantes}")
            else:
                print(f"  ❌  '{nombre}' no es un empleado activo registrado.")
                print("  ❌  Se agotaron los 3 intentos. Operación cancelada.")
                pausa()

        return None

    # ══════════════════════════════════════════
    #  HELPERS INTERNOS
    # ══════════════════════════════════════════

    def _find(self, task_id):
        return next((t for t in self.tasks if t["id"] == task_id), None)

    def _print_tasks(self, lista):
        if not lista:
            print("  (sin tareas registradas)\n")
            return
        encabezados = ["ID", "TÍTULO", "PRIO", "ESTADO", "ASIGNADO A"]
        anchos      = [4,   26,       6,      13,        20]
        filas = []
        for t in lista:
            estado = "✅ COMPLETADA" if t["status"] == "COMPLETADA" else "⏳ PENDIENTE"
            filas.append([
                f"#{t['id']}",
                t["title"][:25],
                f"{ICONOS_PRIO.get(t['priority'], '')} {t['priority']}",
                estado,
                t["assigned_to"][:19],
            ])
        imprimir_tabla(encabezados, filas, anchos)
