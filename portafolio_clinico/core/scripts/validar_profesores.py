# core/scripts/validar_profesores.py
import os
import sys
import pathlib
import django

# 🔹 Asegurar que Python conozca la raíz del proyecto
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# 🔹 Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import Profesor

def validar_profesores():
    print("\n--- VALIDACIÓN DE PROFESORES ---\n")
    
    profesores = Profesor.objects.all()
    total = profesores.count()

    if total == 0:
        print("⚠️ No hay profesores registrados en la base de datos.")
        return

    print(f"Total de profesores encontrados: {total}\n")
    errores = []

    for prof in profesores:
        if not prof.cedula:
            errores.append((prof, "❌ Falta cédula"))
        if not prof.nombre1:
            errores.append((prof, "❌ Falta nombre"))
        if not prof.apell1:
            errores.append((prof, "❌ Falta apellido"))
        if not prof.correo:
            errores.append((prof, "❌ Falta correo electrónico"))
        if not prof.cursoAsignado:
            errores.append((prof, "❌ No tiene curso asignado"))
        if not prof.semestreAsignacion:
            errores.append((prof, "⚠️ No tiene semestre de asignación"))
        if not prof.idFuncion:
            errores.append((prof, "❌ No tiene función asignada"))

    if errores:
        print("🔎 Se detectaron inconsistencias en los siguientes registros:\n")
        for prof, err in errores:
            print(f"- {prof.nombre1} {prof.apell1} ({prof.cedula}) → {err}")
    else:
        print("✅ Todos los profesores tienen datos completos y válidos.")

    print("\n--- VALIDACIÓN FINALIZADA ---\n")

if __name__ == "__main__":
    validar_profesores()
