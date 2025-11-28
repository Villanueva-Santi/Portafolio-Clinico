# core/scripts/validar_cursos_y_grupos.py
import os
import django
import sys

# 🔹 Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 🔹 Configurar correctamente el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import CursoClinico, Grupo, Estudiante, Profesor

def validar_cursos_y_grupos():
    print("\n--- VALIDACIÓN DE CURSOS Y GRUPOS ---\n")

    errores = []
    total_cursos = CursoClinico.objects.count()
    total_grupos = Grupo.objects.count()

    print(f"📘 Total de cursos encontrados: {total_cursos}")
    print(f"👥 Total de grupos encontrados: {total_grupos}\n")

    # --- Validar Cursos ---
    for curso in CursoClinico.objects.all():
        if not curso.codigoCurso:
            errores.append((curso, "❌ Falta código del curso"))
        if not curso.nombreCurso:
            errores.append((curso, "❌ Falta nombre del curso"))
        if not curso.periodoAcademico:
            errores.append((curso, "⚠️ No tiene periodo académico definido"))
        if not curso.semestre:
            errores.append((curso, "⚠️ No tiene semestre asociado"))
        if curso.fechaDesde and curso.fechaHasta and curso.fechaDesde > curso.fechaHasta:
            errores.append((curso, "❌ Fecha desde es mayor que fecha hasta"))

    # --- Validar Grupos ---
    for grupo in Grupo.objects.all():
        if not grupo.codigoGrupo:
            errores.append((grupo, "❌ Falta código de grupo"))
        if not grupo.idCurso:
            errores.append((grupo, "❌ No tiene curso asignado"))
        if not grupo.semestre:
            errores.append((grupo, "⚠️ No tiene semestre asociado"))

        # Contar estudiantes en el grupo
        estudiantes_en_grupo = Estudiante.objects.filter(idGrupo=grupo).count()
        if estudiantes_en_grupo > 6:
            errores.append((grupo, f"⚠️ Tiene {estudiantes_en_grupo} estudiantes (máximo permitido: 6)"))

        # Validar profesor asignado
        if hasattr(grupo, 'cedulaProfesor') and grupo.cedulaProfesor:
            grupos_profesor = Grupo.objects.filter(cedulaProfesor=grupo.cedulaProfesor).count()
            if grupos_profesor > 2:
                errores.append((grupo, f"⚠️ El profesor {grupo.cedulaProfesor} tiene {grupos_profesor} grupos asignados (máximo permitido: 2)"))

    # --- Mostrar resultados ---
    if errores:
        print("🔎 Se detectaron inconsistencias:\n")
        for obj, err in errores:
            if isinstance(obj, CursoClinico):
                print(f"[Curso] {obj.nombreCurso} ({obj.codigoCurso}) → {err}")
            elif isinstance(obj, Grupo):
                print(f"[Grupo] {obj.codigoGrupo} (Curso: {obj.idCurso}) → {err}")
    else:
        print("✅ Todos los cursos y grupos están correctamente configurados y cumplen las reglas de negocio.")

    print("\n--- VALIDACIÓN FINALIZADA ---\n")

if __name__ == "__main__":
    validar_cursos_y_grupos()
    print("✅ Verificación de cursos y grupos completada correctamente.")
