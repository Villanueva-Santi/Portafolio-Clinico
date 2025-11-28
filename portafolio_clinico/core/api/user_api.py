# core/api/user_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers.usuario_serializer import UsuarioSerializer
from core.models import Usuario
from django.utils.timezone import now

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Devuelve la información del usuario autenticado."""
        try:
            usuario = Usuario.objects.get(usuario=request.user.username)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    def put(self, request):
        """Permite actualizar parcialmente los datos del usuario."""
        try:
            usuario = Usuario.objects.get(usuario=request.user.username)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UpdateLastAccessAPIView(APIView):
    """Actualiza la fecha del último acceso."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            usuario = Usuario.objects.get(usuario=request.user.username)
            usuario.ultimoAcceso = now()
            usuario.save(update_fields=["ultimoAcceso"])
            return Response({"message": "Último acceso actualizado correctamente."})
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)
