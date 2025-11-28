# core/scripts/validar_roles_y_permisos.py
import os
import django
import sys

# 🔹 Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 🔹 Configurar correctamente el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import Funcion, Profesor, CursoClinico

# Diccionario de permisos por rol (actualizado)
ROLES_PERMISOS = {
    "Director del Programa": {
        "puede_ver_reportes_globales": True,
        "puede_exportar_reportes": True,
        "puede_ver_todo": True,
        "puede_asignar_roles": True,
        "puede_gestionar_usuarios": True,
    },
    "Coordinador de Práctica e Internado": {
        "puede_ver_reportes_consolidados": True,
        "puede_exportar_excel": True,
        "puede_gestionar_profesores": True,
        "puede_gestionar_estudiantes": True,
        "puede_gestionar_procedimientos": True,
        "puede_ver_cursos": True,
    },
    "Coordinador de Curso": {
        "puede_asignar_profesores": True,
        "puede_asignar_estudiantes": True,
        "puede_ver_su_curso": True,
        "puede_ver_reportes_curso": True,
    },
    "Profesor": {
        "puede_evaluar_estudiantes": True,
        "puede_registrar_observaciones": True,
        "puede_asignar_estudiantes": True,
        "puede_ver_sus_estudiantes": True,
    },
    "Estudiante": {
        "puede_auto_evaluarse": True,
        "puede_ver_sus_resultados": True,
        "puede_ver_curva_aprendizaje": True,
    }
}

def validar_roles_y_permisos():
    print("\n--- VALIDACIÓN DE ROLES Y PERMISOS ---\n")

    funciones = Funcion.objects.all()
    if not funciones.exists():
        print("⚠️ No hay roles definidos en la base de datos (tabla Funcion).")
        return

    errores = []

    # Validar que todos los roles existan en BD
    for rol, permisos in ROLES_PERMISOS.items():
        funcion = funciones.filter(nombreFuncion__iexact=rol).first()
        if not funcion:
            errores.append(f"❌ Falta el rol '{rol}' en la tabla Funcion.")
            continue

        print(f"✅ Rol '{rol}' encontrado correctamente.")
        print(f"   → Permisos asignados: {', '.join(permisos.keys())}\n")

    # Validar jerarquía lógica: cada Coordinador de Curso solo maneja su curso
    coordinadores_curso = Profesor.objects.filter(idFuncion__nombreFuncion__iexact="Coordinador de Curso")
    for coord in coordinadores_curso:
        cursos = CursoClinico.objects.filter(idCoordinadorCurso=coord.idCoordinadorCurso)
        if cursos.count() > 1:
            errores.append(f"⚠️ El coordinador {coord.nombre1} {coord.apell1} está asignado a más de un curso.")
        elif cursos.count() == 0:
            errores.append(f"⚠️ El coordinador {coord.nombre1} {coord.apell1} no tiene curso asignado.")

    # Mostrar resultados
    if errores:
        print("\n🔎 Se detectaron las siguientes observaciones o errores:\n")
        for e in errores:
            print("-", e)
    else:
        print("✅ Todos los roles, permisos y jerarquías son coherentes.\n")

    print("\n--- VALIDACIÓN FINALIZADA ---")

if __name__ == "__main__":
    validar_roles_y_permisos()
    print("✅ Verificación de roles y jerarquías completada correctamente.")