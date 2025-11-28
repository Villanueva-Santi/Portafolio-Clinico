# core/scripts/validar_estudiantes.py
import os
import django
import sys

# 🔹 Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 🔹 Configurar correctamente el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import Estudiante, Grupo, CursoClinico

def validar_estudiantes():
    print("\n--- VALIDACIÓN DE ESTUDIANTES ---\n")
    
    estudiantes = Estudiante.objects.all()
    total = estudiantes.count()

    if total == 0:
        print("⚠️ No hay estudiantes registrados en la base de datos.")
        return

    print(f"Total de estudiantes encontrados: {total}\n")
    errores = []

    for est in estudiantes:
        # ✅ Validaciones básicas
        if not est.cedula:
            errores.append((est, "❌ Falta cédula"))
        if not est.nombre1:
            errores.append((est, "❌ Falta nombre"))
        if not est.apell1:
            errores.append((est, "❌ Falta apellido"))
        if not est.correo:
            errores.append((est, "❌ Falta correo electrónico"))
        if not est.codigoEstudiantil:
            errores.append((est, "❌ Falta código estudiantil"))
        if not est.idFuncion:
            errores.append((est, "❌ No tiene función asignada"))
        if not est.semestreActual:
            errores.append((est, "⚠️ No tiene semestre asignado"))
        if not est.fechaDesde:
            errores.append((est, "⚠️ No tiene fecha de inicio registrada"))

        # ✅ Validar que tenga grupo asignado y curso asociado
        if not est.idGrupo:
            errores.append((est, "❌ No está asignado a ningún grupo"))
        else:
            grupo = est.idGrupo
            if not grupo.idCurso:
                errores.append((est, "❌ Su grupo no tiene curso asociado"))
            else:
                curso = grupo.idCurso
                if not CursoClinico.objects.filter(idCurso=curso.idCurso).exists():
                    errores.append((est, "❌ El curso asignado al grupo no existe en la base de datos"))

    # ✅ Mostrar resultados finales
    if errores:
        print("🔎 Se detectaron inconsistencias en los siguientes registros:\n")
        for est, err in errores:
            print(f"- {est.nombre1} {est.apell1} ({est.cedula}) → {err}")
    else:
        print("✅ Todos los estudiantes tienen datos completos, grupos válidos y relaciones coherentes.")

    print("\n--- VALIDACIÓN FINALIZADA ---\n")

# 🟢 Ejecutar la función si el script se corre directamente
if __name__ == "__main__":
    validar_estudiantes()
    print("✅ Verificación de estudiantes completada correctamente.")

