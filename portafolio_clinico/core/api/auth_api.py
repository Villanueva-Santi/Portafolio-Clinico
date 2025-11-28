# core/api/auth_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import check_password  
from core.models import Usuario
from core.utils.auth_utils import autenticar_usuario  

class LoginAPIView(APIView):
    """
    Endpoint de autenticación: /api/login/
    Recibe JSON: { "usuario": "...", "contrasena": "..." }
    Devuelve token asociado a un User espejo de Django.
    """
    permission_classes = []  # Permite login sin autenticación previa

    def post(self, request):
        username = request.data.get("usuario")
        password = request.data.get("contrasena")

        if not username or not password:
            return Response(
                {"error": "Debe ingresar usuario y contraseña."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verificar existencia del usuario
        usuario = Usuario.objects.filter(usuario=username).select_related("idFuncion").first()
        if not usuario:
            return Response(
                {"error": "Usuario o contraseña incorrectos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Usar check_password si hay contraseñas hashadas
        if hasattr(usuario, "contrasenaHash"):
            if not check_password(password, usuario.contrasenaHash):
                return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if usuario.contrasena != password:
                return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        # Actualiza último acceso
        usuario.ultimoAcceso = timezone.now()
        usuario.save(update_fields=["ultimoAcceso"])

        # Crear/obtener User espejo
        django_user, created = User.objects.get_or_create(
            username=usuario.usuario,
            defaults={
                "email": getattr(usuario, "correo", "") if hasattr(usuario, "correo") else "",
                "is_active": True,
            },
        )
        if created:
            django_user.set_unusable_password()
            django_user.save()

        token, _ = Token.objects.get_or_create(user=django_user)

        return Response(
            {
                "mensaje": "Autenticación exitosa",
                "usuario": usuario.usuario,
                "rol": usuario.idFuncion.nombreFuncion if getattr(usuario, "idFuncion", None) else None,
                "ultimoAcceso": usuario.ultimoAcceso,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )

class LogoutAPIView(APIView):
    """Cierre de sesión (requiere autenticación por token)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)
