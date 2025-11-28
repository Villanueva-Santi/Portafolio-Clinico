# core/scripts/validar_usuarios.py
import os
import django
import sys

# 🔹 Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 🔹 Configurar correctamente el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_clinico.settings')
django.setup()

from core.models import Usuario

def validar_usuarios():
    print("\n--- VALIDACIÓN DE USUARIOS ---\n")
    usuarios = Usuario.objects.all()
    total = usuarios.count()

    if total == 0:
        print("⚠️ No hay usuarios registrados.")
        return

    print(f"Total de usuarios encontrados: {total}\n")

    errores = []
    for user in usuarios:
        if not user.idFuncion:
            errores.append((user, "❌ No tiene función asignada"))
        if not user.estado:
            errores.append((user, "⚠️ Usuario inactivo"))
        if not user.contrasenaHash:
            errores.append((user, "⚠️ No tiene contraseña configurada"))

    if errores:
        print("🔎 Inconsistencias detectadas:")
        for u, err in errores:
            print(f"- {u.usuario} ({u.idFuncion}) → {err}")
    else:
        print("✅ Todos los usuarios están correctos y activos.")

    print("\n--- VALIDACIÓN FINALIZADA ---")

if __name__ == "__main__":
    validar_usuarios()
