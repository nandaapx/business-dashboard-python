"""
Módulo de Gestión de Tareas / Proyectos
"""

from datetime import datetime
from utils.helpers import clear_screen


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._next_id = 1

    # ──────────────────────────────────────────
    #  CRUD
    # ──────────────────────────────────────────
    def add_task(self, title: str, description: str, priority: str, assigned_to: str):
        task = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "priority": priority.upper(),       # ALTA / MEDIA / BAJA
            "assigned_to": assigned_to,
            "status": "PENDIENTE",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None
        }
        self.tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id: int):
        task = self._find(task_id)
        if task:
            task["status"] = "COMPLETADA"
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return True
        return False

    def delete_task(self, task_id: int):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        return len(self.tasks) < before

    def get_all(self):
        return self.tasks

    def get_by_status(self, status: str):
        return [t for t in self.tasks if t["status"] == status.upper()]

    # ──────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────
    def _find(self, task_id: int):
        return next((t for t in self.tasks if t["id"] == task_id), None)

    def _print_tasks(self, task_list):
        if not task_list:
            print("\n  ⚠️  No hay tareas para mostrar.")
            return
        print(f"\n  {'ID':<4} {'TÍTULO':<25} {'PRIORIDAD':<10} {'ESTADO':<12} {'ASIGNADO A'}")
        print("  " + "─" * 65)
        icons = {"ALTA": "🔴", "MEDIA": "🟡", "BAJA": "🟢"}
        for t in task_list:
            icon = icons.get(t["priority"], "⚪")
            print(f"  {t['id']:<4} {t['title']:<25} {icon} {t['priority']:<8} {t['status']:<12} {t['assigned_to']}")

    # ──────────────────────────────────────────
    #  Menú interactivo
    # ──────────────────────────────────────────
    def menu(self):
        while True:
            clear_screen()
            print("\n  ✅  GESTIÓN DE TAREAS\n")
            print("  [1] Agregar tarea")
            print("  [2] Ver todas las tareas")
            print("  [3] Marcar tarea como completada")
            print("  [4] Eliminar tarea")
            print("  [0] Volver al menú principal\n")

            opt = input("  Opción: ").strip()

            if opt == "1":
                print("\n  ── Nueva Tarea ──")
                title = input("  Título: ").strip()
                desc = input("  Descripción: ").strip()
                priority = input("  Prioridad (ALTA / MEDIA / BAJA): ").strip()
                assigned = input("  Asignado a: ").strip()
                t = self.add_task(title, desc, priority, assigned)
                print(f"\n  ✅ Tarea #{t['id']} creada exitosamente.")

            elif opt == "2":
                self._print_tasks(self.tasks)

            elif opt == "3":
                self._print_tasks(self.tasks)
                try:
                    tid = int(input("\n  ID de tarea a completar: "))
                    if self.complete_task(tid):
                        print("  ✅ Tarea completada.")
                    else:
                        print("  ⚠️  Tarea no encontrada.")
                except ValueError:
                    print("  ⚠️  ID inválido.")

            elif opt == "4":
                self._print_tasks(self.tasks)
                try:
                    tid = int(input("\n  ID de tarea a eliminar: "))
                    if self.delete_task(tid):
                        print("  🗑️  Tarea eliminada.")
                    else:
                        print("  ⚠️  Tarea no encontrada.")
                except ValueError:
                    print("  ⚠️  ID inválido.")

            elif opt == "0":
                break

            input("\n  Presiona Enter para continuar...")
