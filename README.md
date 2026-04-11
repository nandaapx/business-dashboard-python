# 📈 Business Dashboard — Panel de Gestión Empresarial en Python

> Proyecto Python diseñado para aprender y practicar **Git & GitHub** en un contexto real y útil para empresas.

---

## 🗂️ Estructura del Proyecto

```
business_dashboard/
│
├── main.py                  ← Punto de entrada principal
├── requirements.txt         ← Dependencias
├── .gitignore               ← Archivos ignorados por Git
├── README.md                ← Este archivo
│
├── modules/
│   ├── __init__.py
│   ├── tasks.py             ← Gestión de tareas/proyectos
│   ├── employees.py         ← Gestión de empleados
│   └── reports.py           ← Reportes y estadísticas
│
└── utils/
    ├── __init__.py
    └── helpers.py           ← Funciones utilitarias
```

---

## 🚀 Cómo Ejecutar

```bash
# Requisito: Python 3.8+
python main.py
```

---

## 🌿 GUÍA COMPLETA: Git & GitHub Paso a Paso

### PASO 1 — Configuración inicial de Git (solo una vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@ejemplo.com"

# Verificar configuración
git config --list
```

---

### PASO 2 — Inicializar el repositorio local

```bash
# Entra a la carpeta del proyecto
cd business_dashboard

# Inicializa Git
git init

# Verifica el estado (todos los archivos aparecerán en rojo = sin rastrear)
git status
```

---

### PASO 3 — Primer commit

```bash
# Agrega TODOS los archivos al área de preparación (staging)
git add .

# Verifica qué está listo para confirmar
git status

# Crea tu primer commit
git commit -m "feat: primer commit - estructura base del proyecto"

# Ver historial de commits
git log --oneline
```

---

### PASO 4 — Subir a GitHub (repositorio en la nube)

```bash
# 1. Ve a https://github.com → New Repository
# 2. Nombre sugerido: business-dashboard-python
# 3. NO inicialices con README ni .gitignore (ya los tienes)
# 4. Copia la URL que te da GitHub, por ejemplo:
#    https://github.com/tu-usuario/business-dashboard-python.git

# Conecta tu repo local con GitHub
git remote add origin https://github.com/tu-usuario/business-dashboard-python.git

# Renombra la rama principal a "main" (buena práctica)
git branch -M main

# ¡Sube el código!
git push -u origin main
```

---

### PASO 5 — Clonar el repositorio en otro equipo

```bash
# En otra máquina o carpeta nueva:
git clone https://github.com/tu-usuario/business-dashboard-python.git

# Entrar al proyecto clonado
cd business-dashboard-python

# Ejecutar
python main.py
```

---

### PASO 6 — Flujo de trabajo diario con ramas (branches)

```bash
# ── Crear una nueva funcionalidad ──────────────────────────
git checkout -b feature/exportar-excel

# Realiza cambios en el código...
# Luego:
git add .
git commit -m "feat: agregar exportación a Excel"

# Subir la rama a GitHub
git push origin feature/exportar-excel

# ── Fusionar con main cuando esté lista ───────────────────
git checkout main
git merge feature/exportar-excel

# Subir main actualizado
git push origin main

# Eliminar rama ya fusionada (opcional, limpieza)
git branch -d feature/exportar-excel
git push origin --delete feature/exportar-excel
```

---

### PASO 7 — Mantener el código actualizado

```bash
# Descargar cambios del repositorio remoto
git pull origin main

# Ver diferencias antes de hacer commit
git diff

# Ver historial visual de ramas
git log --oneline --graph --all
```

---

### PASO 8 — Deshacer errores comunes

```bash
# Deshacer cambios en un archivo (antes del commit)
git checkout -- nombre_archivo.py

# Sacar un archivo del staging
git reset HEAD nombre_archivo.py

# Volver al commit anterior (sin perder cambios)
git reset --soft HEAD~1

# Ver commits y sus hashes
git log --oneline
```

---

## 🌱 Convención de Commits (Conventional Commits)

| Prefijo    | Uso                                      |
|------------|------------------------------------------|
| `feat:`    | Nueva funcionalidad                      |
| `fix:`     | Corrección de bug                        |
| `docs:`    | Cambios en documentación                 |
| `refactor:`| Mejora de código sin cambiar funciones   |
| `style:`   | Formato, espacios (sin cambios lógicos)  |
| `test:`    | Agregar o modificar pruebas              |
| `chore:`   | Tareas de mantenimiento                  |

**Ejemplo:**
```bash
git commit -m "feat: agregar reporte de productividad por departamento"
git commit -m "fix: corregir error al eliminar empleado inexistente"
git commit -m "docs: actualizar instrucciones de instalación en README"
```

---

## 💡 Ideas para Expandir el Proyecto

| Módulo | Descripción |
|--------|-------------|
| 📊 `ventas.py` | Registro de ventas con totales y gráficos ASCII |
| 📅 `agenda.py` | Calendario de reuniones y recordatorios |
| 💰 `finanzas.py` | Control de gastos e ingresos del mes |
| 📦 `inventario.py` | Gestión de productos y stock |
| 🔐 `auth.py` | Sistema de login con roles (admin/usuario) |
| 📧 `notificaciones.py` | Envío de reportes por email con `smtplib` |

---

## 🛠️ Tecnologías

- **Python 3.8+** — Sin dependencias externas
- **Git** — Control de versiones
- **GitHub** — Repositorio en la nube

---

## 📄 Licencia

MIT — Libre para usar, modificar y distribuir.
