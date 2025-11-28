# core/api/reportes_api.py
# core/api/reporte_curva_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Avg, Count
from datetime import datetime

from core.models import EvaluacionDocente, Autoevaluacion, Estudiante, CursoClinico
from core.permissions import IsDirector, IsCoordinadorPractica, IsCoordinadorCurso, IsProfesor, IsEstudiante

# API: Curva de Aprendizaje (Estudiante y Profesor)
class CurvaDreyfusAPIView(APIView):
    """
    Devuelve los datos combinados de evaluaciones (profesor y estudiante)
    para graficar la curva de aprendizaje según el modelo Dreyfus.
    """

    permission_classes = [permissions.IsAuthenticated & (IsDirector | IsCoordinadorPractica | IsCoordinadorCurso | IsProfesor | IsEstudiante)]

    def get(self, request, cedula_estudiante):
        try:
            estudiante = Estudiante.objects.get(cedula=cedula_estudiante)

            # Filtrar evaluaciones y autoevaluaciones
            evaluaciones = EvaluacionDocente.objects.filter(
                idProcedimientoRealizado__idPractica__cedulaEstudiante=estudiante
            ).select_related("idProcedimientoRealizado")

            autoevaluaciones = Autoevaluacion.objects.filter(
                cedulaEstudiante=estudiante
            ).select_related("idProcedimientoRealizado")

            # Diccionario nivel → valor numérico (Para graficar)
            niveles_valor = {
                "NOVATO": 1,
                "PRINCIPIANTE_AVANZADO": 2,
                "COMPETENTE": 3,
                "PROFESIONAL": 4,
                "EXPERTO": 5,
            }

            # Promediar niveles por semestre
            datos_profesor = {}
            datos_estudiante = {}

            for ev in evaluaciones:
                semestre = ev.idProcedimientoRealizado.idPractica.idCurso.semestre
                valor = niveles_valor.get(ev.nivelDreyfus, 0)
                datos_profesor.setdefault(semestre, []).append(valor)

            for auto in autoevaluaciones:
                semestre = auto.idProcedimientoRealizado.idPractica.idCurso.semestre
                valor = niveles_valor.get(auto.nivelPercibido, 0)
                datos_estudiante.setdefault(semestre, []).append(valor)

            # Calcular promedios
            semestres = sorted(set(list(datos_profesor.keys()) + list(datos_estudiante.keys())))
            curva_profesor = [
                {"semestre": s, "nivelPromedio": sum(datos_profesor[s]) / len(datos_profesor[s])} if s in datos_profesor else {"semestre": s, "nivelPromedio": 0}
                for s in semestres
            ]
            curva_estudiante = [
                {"semestre": s, "nivelPromedio": sum(datos_estudiante[s]) / len(datos_estudiante[s])} if s in datos_estudiante else {"semestre": s, "nivelPromedio": 0}
                for s in semestres
            ]

            return Response({
                "estudiante": f"{estudiante.nombre1} {estudiante.apell1}",
                "curva_profesor": curva_profesor,
                "curva_estudiante": curva_estudiante,
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, status=status.HTTP_200_OK)

        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
