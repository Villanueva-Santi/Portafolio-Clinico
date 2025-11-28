# core/scripts/import_estudiantes.py
import pandas as pd
from django.db import transaction
from datetime import date
from core.models import CursoClinico, Grupo, Estudiante, Funcion
from django.core.exceptions import ValidationError

def procesar_excel(path):
    """
    Procesa un archivo Excel para cargar estudiantes, cursos y grupos.
    Cada fila debe tener: 
    Semestre, PeriodoAcademico, CodigoCurso, CursoNombre, CodigoEstudiantil, Cedula, 
    Nombre, Apellido, Correo, GrupoCodigo
    """
    df = pd.read_excel(path)
    errores = []

    # Obtener el año actual (por si no viene periodo en el Excel)
    current_year = date.today().year

    # Buscar función "Estudiante" para asignarla automáticamente
    try:
        funcion_estudiante = Funcion.objects.get(nombreFuncion__iexact='Estudiante')
    except Funcion.DoesNotExist:
        errores.append(('General', "⚠️ No existe la función 'Estudiante' en la tabla Funcion."))
        return errores

    for i, row in df.iterrows():
        try:
            with transaction.atomic():

                # 🔹 Detectar semestre y periodo académico
                semestre_str = str(row.get('Semestre', '1')).strip()
                try:
                    semestre = int(semestre_str)
                except ValueError:
                    semestre = 1  # valor por defecto si no es número válido

                periodo = str(row.get('PeriodoAcademico', '')).strip()
                if not periodo:
                    # Genera automáticamente el periodo si no viene en el Excel
                    periodo = f"{current_year}-{1 if semestre <= 6 else 2}"

                # 🔹 Crear o buscar curso
                curso, _ = CursoClinico.objects.get_or_create(
                    codigoCurso=str(row['CodigoCurso']),
                    defaults={
                        'nombreCurso': row.get('CursoNombre', 'Sin nombre'),
                        'semestre': int(row.get('Semestre', 1)),
                        'fechaDesde': '2025-01-01',
                        'fechaHasta': '2025-12-31',
                        'periodoAcademico': periodo,
                    }
                )

                # 🔹 Crear o buscar grupo
                grupo = None
                if pd.notna(row.get('GrupoCodigo')):
                    grupo, _ = Grupo.objects.get_or_create(
                        codigoGrupo=str(row['GrupoCodigo']),
                        defaults={
                            'idCurso': curso,
                            'semestre': int(row.get('Semestre', 1))
                        }
                    )

                # 🔹 Crear estudiante
                est, creado = Estudiante.objects.get_or_create(
                    codigoEstudiantil=str(row['CodigoEstudiantil']),
                    defaults={
                        'cedula': str(row['Cedula']),
                        'nombre1': row.get('Nombre1'),
                        'nombre2': row.get('Nombre2'),
                        'apell1': row.get('Apellido1'),
                        'apell2': row.get('Apellido2'),
                        'correo': row.get('Correo'),
                        'telefono1': str(row.get('Telefono1', '')),
                        'telefono2': str(row.get('Telefono2', '')) if pd.notna(row.get('Telefono2')) else None,
                        'semestreActual': semestre,
                        'idGrupo': grupo,
                        'fechaDesde': '2025-01-01',
                        'fechaHasta': '2025-12-31',
                        'activo': True,
                        'idFuncion': funcion_estudiante
                    }
                )

                if not creado:
                    # Actualizar datos si el estudiante ya existe
                    est.nombre1 = row.get('Nombre1', est.nombre1)
                    est.apell1 = row.get('Apellido1', est.apell1)
                    est.correo = row.get('Correo', est.correo)
                    est.telefono1 = str(row.get('Telefono1', est.telefono1))
                    est.semestreActual = semestre
                    est.idGrupo = grupo
                    est.save()

        except Exception as e:
                errores.append((i + 2, f"❌ Error en fila {i + 2}: {str(e)}"))

    print("\n--- IMPORTACIÓN FINALIZADA ---")
    print(f"Total registros: {len(df)}")
    print(f"Errores detectados: {len(errores)}")

    if errores:
        for err in errores:
            print(err)
    else:
        print("✅ Todos los registros se importaron correctamente.")

    return errores
