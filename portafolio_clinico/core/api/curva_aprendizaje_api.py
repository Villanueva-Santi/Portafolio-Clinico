# core/api/curva_aprendizaje_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count

from core.models import (
    Estudiante,
    EvaluacionDocente,
    Autoevaluacion,
    ProcedimientoClinico,
)
from core.permissions import user_in_group


class CurvaAprendizajePermission:
    """
    Permisos:
      - Director, Coordinador de Práctica o Curso → acceso completo
      - Profesor → acceso solo si ha evaluado al estudiante
      - Estudiante → solo su propia curva
    """
    @staticmethod
    def has_access(user, cedula_estudiante):
        if not getattr(user, "is_authenticated", False):
            return False

        # Director y Coordinadores tienen acceso total
        if user_in_group(user, "Director") or user_in_group(user, "CoordinadorPractica") or user_in_group(user, "CoordinadorCurso"):
            return True

        # Estudiante solo a su propio registro
        if user_in_group(user, "Estudiante"):
            return str(getattr(user, "cedula", "")) == str(cedula_estudiante)

        # Profesor: si ha evaluado al estudiante
        if user_in_group(user, "Profesor"):
            return EvaluacionDocente.objects.filter(
                cedulaProfesor__cedula=user.cedula,
                idProcedimientoRealizado__idPractica__cedulaEstudiante__cedula=cedula_estudiante
            ).exists()

        return False

# API: Curva de Aprendizaje por Estudiante
class CurvaAprendizajeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cedula):
        # Verificación de permisos
        if not CurvaAprendizajePermission.has_access(request.user, cedula):
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)

        try:
            estudiante = Estudiante.objects.get(cedula=cedula)
        except Estudiante.DoesNotExist:
            return Response({"detail": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Recuperar promedios de Evaluaciones y Autoevaluaciones
        # Promedio numérico de calificación docente y autoevaluación por procedimiento y semestre
        evaluaciones = (
            EvaluacionDocente.objects
            .filter(idProcedimientoRealizado__idPractica__cedulaEstudiante=estudiante)
            .values(
                "idProcedimientoRealizado__idProcedimiento__nombreProcedimiento",
                "idProcedimientoRealizado__idPractica__idCurso__semestre"
            )
            .annotate(promedio=Avg("calificacion"), total=Count("idEvaluacionDocente"))
        )

        autoevaluaciones = (
            Autoevaluacion.objects
            .filter(cedulaEstudiante=estudiante)
            .values(
                "idProcedimientoRealizado__idProcedimiento__nombreProcedimiento",
                "idProcedimientoRealizado__idPractica__idCurso__semestre"
            )
            .annotate(promedio=Avg("nivelAutoevaluacion"), total=Count("idAutoevaluacion"))
        )

        # Combinar datos por procedimiento y semestre
        data_dict = {}

        def agregar_datos(origen, tipo):
            for e in origen:
                procedimiento = e["idProcedimientoRealizado__idProcedimiento__nombreProcedimiento"]
                semestre = e["idProcedimientoRealizado__idPractica__idCurso__semestre"]
                clave = (procedimiento, semestre)
                if clave not in data_dict:
                    data_dict[clave] = {"procedimiento": procedimiento, "semestre": semestre, "evaluacion_docente": None, "autoevaluacion": None}

                data_dict[clave][tipo] = round(e["promedio"], 2) if e["promedio"] else None

        agregar_datos(evaluaciones, "evaluacion_docente")
        agregar_datos(autoevaluaciones, "autoevaluacion")

        # Convertir promedios numéricos a niveles Dreyfus
        def nivel_dreyfus(valor):
            if valor is None:
                return "Sin datos"
            if valor < 2.0:
                return "Novato"
            elif valor < 3.0:
                return "Principiante Avanzado"
            elif valor < 4.0:
                return "Competente"
            elif valor < 4.6:
                return "Proficiente"
            else:
                return "Experto"

        curvas = []
        for (procedimiento, semestre), valores in sorted(data_dict.items(), key=lambda x: x[0][1]):
            docente = valores["evaluacion_docente"]
            auto = valores["autoevaluacion"]
            promedio_final = None

            if docente and auto:
                promedio_final = round((docente + auto) / 2, 2)
            elif docente:
                promedio_final = docente
            elif auto:
                promedio_final = auto

            curvas.append({
                "procedimiento": procedimiento,
                "semestre": semestre,
                "nivel": nivel_dreyfus(promedio_final),
                "promedio_final": promedio_final
            })

        # Respuesta final
        respuesta = {
            "estudiante": {
                "cedula": estudiante.cedula,
                "nombre": f"{estudiante.nombre1} {estudiante.apell1}",
                "codigoEstudiantil": estudiante.codigoEstudiantil,
                "semestreActual": estudiante.semestreActual,
            },
            "curva_aprendizaje": curvas
        }

        return Response(respuesta, status=status.HTTP_200_OK)
