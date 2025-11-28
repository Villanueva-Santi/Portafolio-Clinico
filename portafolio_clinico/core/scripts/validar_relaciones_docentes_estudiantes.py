# core/scripts/validar_relaciones_docentes_estudiantes.py
import os
import django
import sys

# 🔹 Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 🔹 Configurar correctamente el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import Estudiante, Profesor, Grupo, CursoClinico

def validar_relaciones():
    print("\n--- VALIDACIÓN DE RELACIONES ENTRE DOCENTES Y ESTUDIANTES ---\n")

    errores = []
    total_estudiantes = Estudiante.objects.count()
    total_profesores = Profesor.objects.count()
    total_grupos = Grupo.objects.count()
    total_cursos = CursoClinico.objects.count()

    print(f"👩‍🎓 Total de estudiantes: {total_estudiantes}")
    print(f"👨‍🏫 Total de profesores: {total_profesores}")
    print(f"👥 Total de grupos: {total_grupos}")
    print(f"📘 Total de cursos: {total_cursos}\n")

    # Validar que cada estudiante pertenezca a un grupo válido con curso asociado
    for est in Estudiante.objects.select_related("idGrupo__idCurso"):
        if not est.idGrupo:
            errores.append((f"{est.nombre1} {est.apell1}", "❌ No pertenece a ningún grupo."))
            continue

        grupo = est.idGrupo
        if not grupo.idCurso:
            errores.append((f"{est.nombre1} {est.apell1}", f"❌ Grupo {grupo.codigoGrupo} no tiene curso asociado."))
        elif not CursoClinico.objects.filter(pk=grupo.idCurso.idCurso).exists():
            errores.append((f"{est.nombre1} {est.apell1}", f"❌ Curso {grupo.idCurso} no existe en BD."))

    # Validar profesores asignados
    for grupo in Grupo.objects.select_related("cedulaProfesor", "idCurso"):
        if not grupo.cedulaProfesor:
            errores.append((f"Grupo {grupo.codigoGrupo}", "⚠️ No tiene profesor asignado."))
        elif not grupo.idCurso:
            errores.append((f"Grupo {grupo.codigoGrupo}", "❌ No tiene curso clínico asignado."))
        elif not Profesor.objects.filter(pk=grupo.cedulaProfesor.cedula).exists():
            errores.append((f"Grupo {grupo.codigoGrupo}", f"❌ Profesor {grupo.cedulaProfesor} no existe en BD."))

    # Validar relación entre cursos y grupos
    for curso in CursoClinico.objects.all():
        grupos_curso = Grupo.objects.filter(idCurso=curso)
        if grupos_curso.count() == 0:
            errores.append((f"Curso {curso.codigoCurso}", "⚠️ No tiene grupos asociados."))
        if grupos_curso.count() > 5:
            errores.append((f"Curso {curso.codigoCurso}", "❌ Tiene más de 5 grupos asociados (límite sugerido)."))

    # Mostrar resultados finales
    if errores:
        print("🔎 Se detectaron las siguientes inconsistencias:\n")
        for entidad, detalle in errores:
            print(f"- {entidad}: {detalle}")
    else:
        print("✅ Todas las relaciones entre estudiantes, grupos, cursos y profesores son coherentes.")

    print("\n--- VALIDACIÓN FINALIZADA ---\n")

if __name__ == "__main__":
    validar_relaciones()
    print("✅ Validación completa de relaciones ejecutada correctamente.")
