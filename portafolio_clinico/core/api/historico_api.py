# core/api/historico_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from core.models import (
    Estudiante,
    Practica,
    ProcedimientoRealizado,
    EvaluacionDocente,
    Autoevaluacion,
    Profesor,
    Usuario,
)
from core.permissions import user_in_group 

# Serializers 
from core.serializers.procedimientorealizado_serializer import ProcedimientoRealizadoSerializer
from core.serializers.evaluaciondocente_serializer import EvaluacionDocenteSerializer
from core.serializers.autoevaluacion_serializer import AutoevaluacionSerializer


class HistoricoPermission:
    """
    Permiso custom (no hereda BasePermission porque hacemos lógica combinada en la vista).
    Reglas:
      - DIRECTOR o COORDINADOR PRACTICA o COORDINADOR CURSO: acceso completo.
      - PROFESOR: acceso si el profesor corresponde al estudiante (mismo curso/grupo) o si es profesor
                 de algún Practica relacionada al estudiante.
      - ESTUDIANTE: acceso sólo a su propio histórico (cedula debe coincidir).
      - En caso de no poder resolver roles, se niega.
    """
    @staticmethod
    def has_access(request_user, cedula_estudiante):
        if not getattr(request_user, "is_authenticated", False):
            return False

        # Se amplían los nombres de grupos para incluir variantes
        if (
            user_in_group(request_user, "Director") or
            user_in_group(request_user, "Director del Programa") or  
            user_in_group(request_user, "CoordinadorPractica") or
            user_in_group(request_user, "Coordinador de Práctica") or  
            user_in_group(request_user, "CoordinadorCurso") or
            user_in_group(request_user, "Coordinador de Curso")  
        ):
            return True

        # Estudiante: Sólo a su propio histórico
        if user_in_group(request_user, "Estudiante"):
            try:
                return str(getattr(request_user, "cedula", "")).strip() == str(cedula_estudiante).strip()
            except Exception:
                return False

        # Profesor: Permitir si el profesor (por su cedula) tiene relación con el estudiante
        if user_in_group(request_user, "Profesor"):
            try:
                user_cedula = getattr(request_user, "cedula", None)
                if not user_cedula:
                    return False
                profesor = Profesor.objects.filter(cedula=user_cedula).first()
                if not profesor:
                    return False

                # Comprobar si el profesor es responsable de algún Grupo / Curso del estudiante
                practicas_est = Practica.objects.filter(cedulaEstudiante__cedula=cedula_estudiante).select_related('idCurso', 'idGrupo')
                for p in practicas_est:
                    if getattr(p, "idGrupo", None) and getattr(p.idGrupo, "cedulaProfesor", None):
                        if p.idGrupo.cedulaProfesor and p.idGrupo.cedulaProfesor.cedula == profesor.cedula:
                            return True
                    if getattr(p, "idCurso", None):
                        curso = p.idCurso
                        if profesor.cursoAsignado and (profesor.cursoAsignado == curso.nombreCurso or profesor.cursoAsignado == getattr(curso, "codigoCurso", None)):
                            return True

                # Permitir si el profesor ha hecho evaluaciones sobre el estudiante
                existe_eval = EvaluacionDocente.objects.filter(
                    cedulaProfesor__cedula=profesor.cedula,
                    idProcedimientoRealizado__idPractica__cedulaEstudiante__cedula=cedula_estudiante
                ).exists()
                if existe_eval:
                    return True

                return False
            except Exception:
                return False

        # por defecto negar
        return False


class HistoricoEstudianteAPIView(APIView):
    """
    GET /api/historico/estudiante/<cedula>/?semestre=<sem>
    Devuelve histórico de procedimientos, evaluaciones y autoevaluaciones agrupadas por semestre/periodo.
    Permisos:
      - Director, CoordinadorPractica, CoordinadorCurso: acceso
      - Profesor: según lógica en HistoricoPermission.has_access
      - Estudiante: sólo su propio histórico
    """
    permission_classes = [IsAuthenticated]  # Verificación básica; acceso final por HistoricoPermission

    def get(self, request, cedula):
        if not HistoricoPermission.has_access(request.user, cedula):
            return Response({"detail": "No autorizado para ver este histórico."}, status=status.HTTP_403_FORBIDDEN)

        try:
            estudiante = Estudiante.objects.get(cedula=cedula)
        except Estudiante.DoesNotExist:
            return Response({"detail": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        filtro_semestre = request.query_params.get("semestre", None)
        practicas = Practica.objects.filter(cedulaEstudiante=estudiante).select_related('idCurso', 'idGrupo')

        procedimientos_qs = ProcedimientoRealizado.objects.filter(
            idPractica__in=practicas
        ).select_related('idProcedimiento', 'idPractica__idCurso').order_by('fecha')

        evaluaciones_qs = EvaluacionDocente.objects.filter(
            idProcedimientoRealizado__idPractica__in=practicas
        ).select_related('cedulaProfesor', 'idProcedimientoRealizado__idPractica').order_by('fechaEvaluacion')

        autoevaluaciones_qs = Autoevaluacion.objects.filter(
            cedulaEstudiante=estudiante
        ).select_related('idProcedimientoRealizado__idPractica').order_by('fechaAutoevaluacion')

        if filtro_semestre:
            if filtro_semestre.isdigit():
                procedimientos_qs = procedimientos_qs.filter(idPractica__idCurso__semestre=int(filtro_semestre))
                evaluaciones_qs = evaluaciones_qs.filter(idProcedimientoRealizado__idPractica__idCurso__semestre=int(filtro_semestre))
                autoevaluaciones_qs = autoevaluaciones_qs.filter(idProcedimientoRealizado__idPractica__idCurso__semestre=int(filtro_semestre))
            else:
                procedimientos_qs = procedimientos_qs.filter(idPractica__idCurso__periodoAcademico__icontains=filtro_semestre)
                evaluaciones_qs = evaluaciones_qs.filter(idProcedimientoRealizado__idPractica__idCurso__periodoAcademico__icontains=filtro_semestre)
                autoevaluaciones_qs = autoevaluaciones_qs.filter(idProcedimientoRealizado__idPractica__idCurso__periodoAcademico__icontains=filtro_semestre)

        historico = {}

        for proc in procedimientos_qs:
            try:
                curso = proc.idPractica.idCurso
                clave = curso.periodoAcademico or f"Sem-{curso.semestre}"
            except Exception:
                clave = f"Sem-{getattr(proc.idPractica, 'semestre', 'N/A')}"
            historico.setdefault(clave, {"procedimientos": [], "evaluaciones": [], "autoevaluaciones": []})
            historico[clave]["procedimientos"].append(ProcedimientoRealizadoSerializer(proc).data)

        for ev in evaluaciones_qs:
            try:
                curso = ev.idProcedimientoRealizado.idPractica.idCurso
                clave = curso.periodoAcademico or f"Sem-{curso.semestre}"
            except Exception:
                clave = "SinPeriodo"
            historico.setdefault(clave, {"procedimientos": [], "evaluaciones": [], "autoevaluaciones": []})
            historico[clave]["evaluaciones"].append(EvaluacionDocenteSerializer(ev).data)

        for auto in autoevaluaciones_qs:
            try:
                curso = auto.idProcedimientoRealizado.idPractica.idCurso
                clave = curso.periodoAcademico or f"Sem-{curso.semestre}"
            except Exception:
                clave = "SinPeriodo"
            historico.setdefault(clave, {"procedimientos": [], "evaluaciones": [], "autoevaluaciones": []})
            historico[clave]["autoevaluaciones"].append(AutoevaluacionSerializer(auto).data)

        semestres = []
        for clave, datos in sorted(historico.items(), key=lambda x: x[0]):
            semestres.append({
                "periodo": clave,
                "procedimientos": datos["procedimientos"],
                "evaluaciones": datos["evaluaciones"],
                "autoevaluaciones": datos["autoevaluaciones"],
            })

        resp = {
            "estudiante": {
                "cedula": estudiante.cedula,
                "nombre": f"{estudiante.nombre1} {estudiante.apell1}",
                "codigoEstudiantil": getattr(estudiante, "codigoEstudiantil", None),
                "semestreActual": estudiante.semestreActual,
            },
            "historico_por_periodo": semestres
        }

        return Response(resp, status=status.HTTP_200_OK)
