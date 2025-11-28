# core/scripts/import_usuarios.py
import pandas as pd
from django.db import transaction
from django.contrib.auth.hashers import make_password
from core.models import Usuario, Funcion

def procesar_excel_usuarios(path):
    """
    Carga masivamente usuarios al sistema desde un Excel.
    Columnas requeridas:
    Usuario, Cedula, Contrasena, Funcion
    """
    df = pd.read_excel(path)
    errores = []

    for i, row in df.iterrows():
        try:
            with transaction.atomic():
                funcion = Funcion.objects.get(nombreFuncion__iexact=row['Funcion'])
                Usuario.objects.update_or_create(
                    usuario=row['Usuario'],
                    defaults={
                        'cedula': str(row['Cedula']),
                        'idFuncion': funcion,
                        'contrasenaHash': make_password(str(row['Contrasena'])),
                        'estado': True
                    }
                )
        except Exception as e:
            errores.append((i, str(e)))

    print("\n--- IMPORTACIÓN FINALIZADA ---")
    print(f"Total registros: {len(df)}")
    print(f"Errores detectados: {len(errores)}")
    if errores:
        for err in errores:
            print(err)
    else:
        print("✅ Todos los usuarios fueron importados correctamente.")

    return errores
