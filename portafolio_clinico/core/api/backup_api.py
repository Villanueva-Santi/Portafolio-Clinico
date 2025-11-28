# core/api/backup_api.py
import os
import subprocess
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from core.models import BackupLog, Usuario
from core.permissions import IsDirector, IsCoordinadorPractica
from core.signals import registrar_bitacora


class GenerarBackupAPIView(APIView):
    """
    Permite generar un respaldo manual de la base de datos PostgreSQL.
    Solo accesible para Director o Coordinador de Práctica.
    """
    permission_classes = [permissions.IsAuthenticated, (IsDirector | IsCoordinadorPractica)]

    def post(self, request):
        usuario = request.user
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ruta destino del backup
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_filename = f"backup_portafolio_{fecha}.sql"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Datos conexión
        db = settings.DATABASES['default']
        db_name = db['NAME']
        db_user = db['USER']
        db_pass = db['PASSWORD']
        db_host = db.get('HOST', 'localhost')
        db_port = db.get('PORT', '5432')

        # Comando pg_dump
        comando = [
            "pg_dump",
            f"--dbname=postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
            "-f", backup_path
        ]

        try:
            subprocess.run(comando, check=True)
            estado = "Éxito"
            mensaje = f"Respaldo creado correctamente: {backup_filename}"

        except subprocess.CalledProcessError as e:
            estado = "Error"
            mensaje = f"Error al crear respaldo: {str(e)}"

        # Registrar en BackupLog
        BackupLog.objects.create(
            idUsuario=usuario,
            fecha=datetime.now(),
            nombreArchivo=backup_filename,
            estado=estado,
        )

        # Registrar en Bitácora
        registrar_bitacora(usuario, "BACKUP", mensaje)

        return Response({"mensaje": mensaje, "estado": estado}, status=status.HTTP_200_OK)
