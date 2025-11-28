# core/api/notificaciones_api.py
from rest_framework import generics, permissions
from core.models import Notificacion
from core.serializers.notificacion_serializer import NotificacionSerializer

class NotificacionesUsuarioAPIView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Notificacion.objects.filter(idUsuario=usuario).order_by('-fecha')
