# core/scripts/import_profesores.py
import pandas as pd
from django.db import transaction
from core.models import Profesor, Funcion, CoordinadorCurso

def procesar_excel_profesores(path):
    """
    Procesa un archivo Excel para importar profesores.
    Cada fila debe tener las columnas:
    Cedula, Nombre1, Nombre2, Apell1, Apell2, Correo, Telefono1, Telefono2,
    CursoAsignado, SemestreAsignacion, FechaDesde, FechaHasta
    """
    df = pd.read_excel(path)
    errores = []

    try:
        funcion_profesor = Funcion.objects.get(nombreFuncion__iexact="Profesor")
    except Funcion.DoesNotExist:
        raise ValueError("❌ No existe una función llamada 'Profesor' en la tabla Funcion. Por favor créala primero.")

    for i, row in df.iterrows():
        try:
            with transaction.atomic():
                # Asignar coordinador si se quiere (opcional)
                coordinador = None
                if 'CedulaCoordinador' in df.columns and pd.notna(row.get('CedulaCoordinador')):
                    coordinador = CoordinadorCurso.objects.filter(cedula=str(row['CedulaCoordinador'])).first()

                profesor, creado = Profesor.objects.get_or_create(
                    cedula=str(row['Cedula']),
                    defaults={
                        'nombre1': row.get('Nombre1', '').strip(),
                        'nombre2': row.get('Nombre2', None),
                        'apell1': row.get('Apell1', '').strip(),
                        'apell2': row.get('Apell2', None),
                        'correo': row.get('Correo', '').strip(),
                        'telefono1': str(row.get('Telefono1', '')),
                        'telefono2': str(row.get('Telefono2', '')) if pd.notna(row.get('Telefono2')) else None,
                        'idFuncion': funcion_profesor,
                        'idCoordinadorCurso': coordinador,
                        'cursoAsignado': row.get('CursoAsignado', 'No asignado'),
                        'semestreAsignacion': str(row.get('SemestreAsignacion', '1')),
                        'fechaDesde': pd.to_datetime(row.get('FechaDesde', '2025-01-01')).date(),
                        'fechaHasta': pd.to_datetime(row.get('FechaHasta', '2025-12-31')).date() if pd.notna(row.get('FechaHasta')) else None,
                        'activo': True
                    }
                )

                if not creado:
                    # Actualiza datos si el profesor ya existe
                    profesor.nombre1 = row.get('Nombre1', profesor.nombre1)
                    profesor.apell1 = row.get('Apell1', profesor.apell1)
                    profesor.correo = row.get('Correo', profesor.correo)
                    profesor.cursoAsignado = row.get('CursoAsignado', profesor.cursoAsignado)
                    profesor.semestreAsignacion = str(row.get('SemestreAsignacion', profesor.semestreAsignacion))
                    profesor.save()

        except Exception as e:
            errores.append((i + 2, str(e)))  # +2 porque pandas empieza en 0 y Excel en 2 visualmente

    print("\n--- IMPORTACIÓN DE PROFESORES FINALIZADA ---")
    print(f"Total registros procesados: {len(df)}")
    print(f"Errores detectados: {len(errores)}")
    if errores:
        for fila, err in errores:
            print(f"❌ Error en fila {fila}: {err}")
    else:
        print("✅ Todos los profesores fueron importados correctamente.")

    return errores
