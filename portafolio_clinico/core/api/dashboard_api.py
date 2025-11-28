# core/api/dashboard_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from core.models import (
    Usuario,
    Estudiante,
    Profesor,
    CursoClinico,
    Grupo,
    ProcedimientoRealizado,
    EvaluacionDocente
)

class DashboardDataAPIView(APIView):
    """
    Devuelve datos consolidados para el dashboard según rol.
    """
    def post(self, request):
        usuario = request.data.get("usuario")
        if not usuario:
            return Response({"error": "Debe especificar el nombre de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        u = get_object_or_404(Usuario.objects.select_related("idFuncion"), usuario=usuario)
        rol = u.idFuncion.nombreFuncion if getattr(u, "idFuncion", None) else None

        data = {
            "usuario": u.usuario,
            "rol": rol,
            "timestamp": timezone.now(),
        }

        # Roles con resúmenes
        if rol == "Director del Programa":
            data["dashboard"] = {
                "titulo": "Panel del Director del Programa",
                "resumen": {
                    "total_estudiantes": Estudiante.objects.count(),
                    "total_profesores": Profesor.objects.count(),
                    "total_cursos": CursoClinico.objects.count(),
                    "total_procedimientos": ProcedimientoRealizado.objects.count(),
                    "evaluaciones_registradas": EvaluacionDocente.objects.count()
                }
            }
        elif rol == "Profesor":
            data["dashboard"] = {
                "titulo": "Panel del Profesor Clínico",
                "resumen": {
                    "grupos_asignados": Grupo.objects.filter(cedulaProfesor=u.cedula).count(),
                    "estudiantes_asignados": Estudiante.objects.filter(idGrupo__cedulaProfesor=u.cedula).count(),
                    "evaluaciones_realizadas": EvaluacionDocente.objects.filter(cedulaProfesor__cedula=u.cedula).count(),
                }
            }
        elif rol == "Estudiante":
            data["dashboard"] = {
                "titulo": "Panel del Estudiante",
                "resumen": {
                    "procedimientos_realizados": ProcedimientoRealizado.objects.filter(idPractica__cedulaEstudiante__cedula=u.cedula).count(),
                    "evaluaciones_realizadas": EvaluacionDocente.objects.filter(idProcedimientoRealizado__idPractica__cedulaEstudiante__cedula=u.cedula).count(),
                }
            }
        else:
            data["dashboard"] = {"mensaje": "Rol no reconocido."}

        return Response(data, status=status.HTTP_200_OK)
