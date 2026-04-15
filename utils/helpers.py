"""
utils/helpers.py — Sistema de consola e interfaz de usuario
"""

import os

MAX_INTENTOS = 3

# ══════════════════════════════════════════════
#  PANTALLA
# ══════════════════════════════════════════════

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print("\n" + "═" * 50)
    print("  📈  BUSINESS DASHBOARD  v2.0")
    print("  Panel de Gestión Empresarial Python")
    print("═" * 50)


def separador(char="─", ancho=50):
    print("  " + char * ancho)


def titulo(texto):
    print("\n" + "═" * 50)
    print(f"  {texto}")
    print("═" * 50 + "\n")


def subtitulo(texto):
    print(f"\n  ── {texto} ──\n")


def ok(texto):
    print(f"\n  ✅  {texto}")


def error(texto):
    print(f"\n  ❌  {texto}")


def advertencia(texto):
    print(f"\n  ⚠️   {texto}")


def info(texto):
    print(f"  ℹ️   {texto}")


def pausa():
    input("\n  Presiona Enter para continuar...")


# ══════════════════════════════════════════════
#  MENÚ DE OPCIONES NUMERADAS
# ══════════════════════════════════════════════

def mostrar_menu(opciones: list):
    """
    Recibe lista de strings y las imprime numeradas.
    El último elemento siempre es la opción 0 (volver/salir).
    """
    print()
    for i, opcion in enumerate(opciones[:-1], 1):
        print(f"  [{i}]  {opcion}")
    print(f"  [0]  {opciones[-1]}")
    print()


def pedir_opcion_menu(total_opciones: int, intentos=MAX_INTENTOS):
    """
    Pide una opción del 0 al total_opciones.
    Devuelve int o None si agota intentos.
    """
    validas = [str(i) for i in range(0, total_opciones + 1)]
    for intento in range(1, intentos + 1):
        raw = input("  Selecciona una opción: ").strip()
        if raw in validas:
            return int(raw)
        restantes = intentos - intento
        if restantes > 0:
            print(f"  ⚠️   Opción inválida. Elige entre 0 y {total_opciones}. "
                  f"Intentos restantes: {restantes}")
        else:
            print(f"  ❌  Opción inválida. Sin más intentos.")
    advertencia("Se agotaron los intentos. Volviendo al menú anterior.")
    pausa()
    return None


# ══════════════════════════════════════════════
#  ENTRADAS VALIDADAS
# ══════════════════════════════════════════════

def pedir_texto(prompt, minimo=2, maximo=60, intentos=MAX_INTENTOS):
    """Texto libre con validación de longitud."""
    for intento in range(1, intentos + 1):
        valor = input(f"  {prompt}: ").strip()
        if len(valor) < minimo:
            restantes = intentos - intento
            msg = f"Mínimo {minimo} caracteres."
            _feedback_intento(msg, restantes)
            if restantes == 0:
                return None
        elif len(valor) > maximo:
            restantes = intentos - intento
            msg = f"Máximo {maximo} caracteres."
            _feedback_intento(msg, restantes)
            if restantes == 0:
                return None
        else:
            return valor
    return None


def pedir_email(prompt="Email", intentos=MAX_INTENTOS):
    """Email con validación de formato básico."""
    for intento in range(1, intentos + 1):
        valor = input(f"  {prompt}: ").strip().lower()
        partes = valor.split("@")
        valido = (
            len(partes) == 2
            and len(partes[0]) > 0
            and "." in partes[1]
            and len(partes[1]) > 2
            and len(valor) >= 6
        )
        if valido:
            return valor
        restantes = intentos - intento
        _feedback_intento("Email inválido. Ejemplo válido: nombre@empresa.com", restantes)
        if restantes == 0:
            return None
    return None


def pedir_id(prompt="ID", intentos=MAX_INTENTOS):
    """Número entero positivo."""
    for intento in range(1, intentos + 1):
        raw = input(f"  {prompt}: ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        restantes = intentos - intento
        _feedback_intento("Debe ser un número entero positivo (ej: 1, 2, 3).", restantes)
        if restantes == 0:
            return None
    return None


def pedir_confirmacion(prompt="¿Confirmas?") -> bool:
    """Pide s/n. Devuelve True si confirma."""
    raw = input(f"\n  {prompt} (s/n): ").strip().lower()
    return raw == "s"


# ══════════════════════════════════════════════
#  TABLAS EN CONSOLA
# ══════════════════════════════════════════════

def imprimir_tabla(encabezados: list, filas: list, anchos: list):
    """
    Imprime una tabla alineada en consola.
    encabezados : ["ID", "NOMBRE", ...]
    filas       : [["1", "María", ...], ...]
    anchos      : [4, 22, ...]
    """
    print()
    # Encabezado
    fila_enc = "  " + "  ".join(str(h).ljust(anchos[i]) for i, h in enumerate(encabezados))
    print(fila_enc)
    print("  " + "─" * (sum(anchos) + 2 * len(anchos)))
    # Filas
    for fila in filas:
        linea = "  " + "  ".join(str(c).ljust(anchos[i]) for i, c in enumerate(fila))
        print(linea)
    print()


# ══════════════════════════════════════════════
#  INTERNO
# ══════════════════════════════════════════════

def _feedback_intento(mensaje, restantes):
    if restantes > 0:
        print(f"  ⚠️   {mensaje} Intentos restantes: {restantes}")
    else:
        print(f"  ❌  {mensaje} Sin más intentos. Operación cancelada.")
        pausa()
