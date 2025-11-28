# portafolio_clinico/backups/backup_utils.py
import os
import datetime
from django.core.management import call_command
from django.conf import settings

# 🟩 Función para crear backup automático
def crear_backup(nombre_evento):
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(settings.BASE_DIR, "portafolio_clinico", "backups")

    # Crear carpeta si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Nombre del archivo de backup
    filename = f"backup_{nombre_evento}_{fecha}.json"
    filepath = os.path.join(backup_dir, filename)

    # Ejecutar dumpdata
    with open(filepath, "w", encoding="utf-8") as f:
        call_command("dumpdata", indent=2, stdout=f)

    print(f"🟢 Backup creado: {filename}")
