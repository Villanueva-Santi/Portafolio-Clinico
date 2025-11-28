# core/serializers/notificacion_serializer.py
from rest_framework import serializers
from core.models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'fecha', 'leida']
