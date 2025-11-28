# core/utils/excel_utils.py
import pandas as pd
from core.models import Estudiante, Profesor, Grupo

# 🟩 Columnas mínimas requeridas (según tus modelos)
COLUMNAS_ESTUDIANTES_REQUERIDAS = ['cedula', 'nombre1', 'apell1', 'codigoestudiantil', 'semestreactual']
COLUMNAS_PROFESORES_REQUERIDAS = ['cedula', 'nombre1', 'apell1', 'correo']
COLUMNAS_GRUPOS_REQUERIDAS = ['codigogrupo', 'cedulaprofesor', 'semestre', 'idcurso']

def leer_excel(file):
    """Lee un archivo Excel y devuelve un DataFrame limpio."""
    df = pd.read_excel(file)
    df.columns = df.columns.str.lower().str.strip()
    return df

def validar_columnas(df, columnas_requeridas):
    """Valida que el Excel tenga al menos las columnas mínimas requeridas."""
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Columnas faltantes: {', '.join(faltantes)}")
    return True

def limpiar_datos(df, columnas_validas):
    """Retorna solo las columnas relevantes (ignora las demás)."""
    return df[[c for c in columnas_validas if c in df.columns]]

# ============================
# CARGA DE ESTUDIANTES
# ============================
def cargar_estudiantes_desde_excel(file):
    df = leer_excel(file)
    validar_columnas(df, COLUMNAS_ESTUDIANTES_REQUERIDAS)
    df = limpiar_datos(df, COLUMNAS_ESTUDIANTES_REQUERIDAS)

    registros_creados = 0
    for _, row in df.iterrows():
        Estudiante.objects.update_or_create(
            cedula=row['cedula'],
            defaults={
                'nombre1': row['nombre1'],
                'apell1': row['apell1'],
                'codigoEstudiantil': row['codigoestudiantil'],
                'semestreActual': row['semestreactual'],
                'activo': True
            }
        )
        registros_creados += 1
    return f"{registros_creados} estudiantes cargados correctamente."


# ============================
# CARGA DE PROFESORES
# ============================
def cargar_profesores_desde_excel(file):
    df = leer_excel(file)
    validar_columnas(df, COLUMNAS_PROFESORES_REQUERIDAS)
    df = limpiar_datos(df, COLUMNAS_PROFESORES_REQUERIDAS)

    registros_creados = 0
    for _, row in df.iterrows():
        Profesor.objects.update_or_create(
            cedula=row['cedula'],
            defaults={
                'nombre1': row['nombre1'],
                'apell1': row['apell1'],
                'correo': row['correo'],
                'activo': True
            }
        )
        registros_creados += 1
    return f"{registros_creados} profesores cargados correctamente."


# ============================
# CARGA DE GRUPOS
# ============================
def cargar_grupos_desde_excel(file):
    df = leer_excel(file)
    validar_columnas(df, COLUMNAS_GRUPOS_REQUERIDAS)
    df = limpiar_datos(df, COLUMNAS_GRUPOS_REQUERIDAS)

    registros_creados = 0
    for _, row in df.iterrows():
        profesor = Profesor.objects.filter(cedula=row['cedulaprofesor']).first()
        if profesor:
            Grupo.objects.update_or_create(
                codigoGrupo=row['codigogrupo'],
                defaults={
                    'cedulaProfesor': profesor,
                    'semestre': row['semestre'],
                    'idCurso_id': row['idcurso'],
                    'activo': True
                }
            )
            registros_creados += 1
    return f"{registros_creados} grupos cargados correctamente."
