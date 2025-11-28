# core/api/estudiantes_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Estudiante
from core.utils.auth_utils import autenticar_usuario

class EstudiantesAPIView(APIView):
    """
    Endpoint para listar estudiantes (Solo accesible por director o coordinadores).
    """
    def post(self, request):
        usuario = request.data.get("usuario")
        contrasena = request.data.get("contrasena")

        u = autenticar_usuario(usuario, contrasena)
        if not u:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        rol = u.idFuncion.nombreFuncion  

        if rol not in ["Director del Programa", "Coordinador de Práctica e Internado", "Coordinador de Curso"]:
            return Response({"error": "No autorizado para consultar estudiantes."}, status=status.HTTP_403_FORBIDDEN)

        # Consultar todos los estudiantes
        estudiantes = Estudiante.objects.all().values(
            "codigoEstudiantil", "cedula", "nombre1", "nombre2", "apell1", "apell2", "correo", 
            "telefono1", "telefono2", "semestreActual", "fechaDesde", "fechaHasta"
        )

        return Response({
            "usuario": u.usuario,
            "rol": rol,
            "total_estudiantes": len(estudiantes),
            "estudiantes": list(estudiantes)
        }, status=status.HTTP_200_OK)
