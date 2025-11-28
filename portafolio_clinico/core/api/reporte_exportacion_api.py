# core/api/reporte_exportacion_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import HttpResponse
from datetime import datetime
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from core.models import (
    Estudiante,
    Profesor,
    EvaluacionDocente,
    Autoevaluacion,
    ProcedimientoRealizado,
    CursoClinico,
)
from core.permissions import (
    IsDirector,
    IsCoordinadorPractica,
    IsCoordinadorCurso,
    IsProfesor,
    IsEstudiante,
)

# Clase base de permisos combinados
class PermisoReporteMixin:
    """Control de permisos por rol."""
    permission_classes = [
        IsDirector | IsCoordinadorPractica | IsCoordinadorCurso | IsProfesor | IsEstudiante
    ]

# Reporte Excel
class ExportarReporteExcelAPIView(PermisoReporteMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Parámetros de filtrado
            cedula_estudiante = request.query_params.get("cedula_estudiante")
            semestre = request.query_params.get("semestre")
            curso = request.query_params.get("curso")
            fecha_desde = request.query_params.get("fecha_desde")
            fecha_hasta = request.query_params.get("fecha_hasta")

            # Query base
            queryset = EvaluacionDocente.objects.select_related(
                "cedulaProfesor",
                "idProcedimientoRealizado__idPractica__cedulaEstudiante",
                "idProcedimientoRealizado__idProcedimiento__idCompetencia",
                "idProcedimientoRealizado__idPractica__idCurso",
            )

            # Filtros dinámicos
            if cedula_estudiante:
                queryset = queryset.filter(idProcedimientoRealizado__idPractica__cedulaEstudiante__cedula=cedula_estudiante)
            if semestre:
                queryset = queryset.filter(idProcedimientoRealizado__idPractica__cedulaEstudiante__semestreActual=semestre)
            if curso:
                queryset = queryset.filter(idProcedimientoRealizado__idPractica__idCurso__nombreCurso__icontains=curso)
            if fecha_desde and fecha_hasta:
                queryset = queryset.filter(fechaEvaluacion__range=[fecha_desde, fecha_hasta])

            # Construcción del DataFrame
            data = []
            for eval in queryset:
                estudiante = eval.idProcedimientoRealizado.idPractica.cedulaEstudiante
                profesor = eval.cedulaProfesor
                procedimiento = eval.idProcedimientoRealizado.idProcedimiento
                competencia = procedimiento.idCompetencia
                curso_obj = eval.idProcedimientoRealizado.idPractica.idCurso

                data.append({
                    "Cédula Estudiante": estudiante.cedula,
                    "Nombre Estudiante": f"{estudiante.nombre1} {estudiante.apell1}",
                    "Semestre": estudiante.semestreActual,
                    "Curso": curso_obj.nombreCurso,
                    "Procedimiento": procedimiento.nombreProcedimiento,
                    "Competencia": competencia.nombreCompetencia,
                    "Profesor": f"{profesor.nombre1} {profesor.apell1}",
                    "Nivel Dreyfus": eval.nivelDreyfus,
                    "Calificación": eval.calificacion,
                    "Retroalimentación": eval.retroalimentacion,
                    "Fecha Evaluación": eval.fechaEvaluacion,
                })

            if not data:
                return Response({"detalle": "No se encontraron registros."}, status=status.HTTP_204_NO_CONTENT)

            df = pd.DataFrame(data)

            # Generar archivo Excel en memoria
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="Reporte Clínico")
            buffer.seek(0)

            # Respuesta HTTP
            response = HttpResponse(
                buffer,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            filename = f"reporte_portafolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Reporte PDF
class ExportarReportePDFAPIView(PermisoReporteMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            cedula_estudiante = request.query_params.get("cedula_estudiante")
            semestre = request.query_params.get("semestre")

            queryset = EvaluacionDocente.objects.select_related(
                "cedulaProfesor",
                "idProcedimientoRealizado__idPractica__cedulaEstudiante",
                "idProcedimientoRealizado__idProcedimiento__idCompetencia",
                "idProcedimientoRealizado__idPractica__idCurso",
            )

            if cedula_estudiante:
                queryset = queryset.filter(idProcedimientoRealizado__idPractica__cedulaEstudiante__cedula=cedula_estudiante)
            if semestre:
                queryset = queryset.filter(idProcedimientoRealizado__idPractica__cedulaEstudiante__semestreActual=semestre)

            # Crear PDF en memoria
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            p.setFont("Helvetica-Bold", 14)
            p.drawString(1 * inch, height - 1 * inch, "Reporte Clínico - Evaluaciones Docentes")
            p.setFont("Helvetica", 10)
            p.drawString(1 * inch, height - 1.2 * inch, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            y = height - 1.5 * inch
            for eval in queryset:
                estudiante = eval.idProcedimientoRealizado.idPractica.cedulaEstudiante
                profesor = eval.cedulaProfesor
                procedimiento = eval.idProcedimientoRealizado.idProcedimiento

                if y < 1 * inch:
                    p.showPage()
                    y = height - 1 * inch
                    p.setFont("Helvetica", 10)

                p.drawString(1 * inch, y, f"Estudiante: {estudiante.nombre1} {estudiante.apell1} ({estudiante.cedula})")
                y -= 12
                p.drawString(1 * inch, y, f"Procedimiento: {procedimiento.nombreProcedimiento}")
                y -= 12
                p.drawString(1 * inch, y, f"Profesor: {profesor.nombre1} {profesor.apell1}")
                y -= 12
                p.drawString(1 * inch, y, f"Nivel Dreyfus: {eval.nivelDreyfus} | Calificación: {eval.calificacion}")
                y -= 12
                p.drawString(1 * inch, y, f"Fecha: {eval.fechaEvaluacion}")
                y -= 12
                p.drawString(1 * inch, y, f"Retroalimentación: {eval.retroalimentacion[:100]}...")
                y -= 20

            p.save()
            buffer.seek(0)

            response = HttpResponse(buffer, content_type="application/pdf")
            filename = f"reporte_portafolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Curva Dreyfus en PDF 
class ExportarCurvaPDFAPIView(PermisoReporteMixin, APIView):
    def get(self, request, cedula_estudiante, *args, **kwargs):
        try:
            estudiante = Estudiante.objects.get(cedula=cedula_estudiante)
            evaluaciones = EvaluacionDocente.objects.filter(
                idProcedimientoRealizado__idPractica__cedulaEstudiante=estudiante
            ).select_related(
                "cedulaProfesor",
                "idProcedimientoRealizado__idProcedimiento__idCompetencia",
            )

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            p.setFont("Helvetica-Bold", 14)
            p.drawString(1 * inch, height - 1 * inch, f"Curva Dreyfus - {estudiante.nombre1} {estudiante.apell1}")
            p.setFont("Helvetica", 10)
            p.drawString(1 * inch, height - 1.2 * inch, f"Cédula: {estudiante.cedula} | Semestre: {estudiante.semestreActual}")

            y = height - 1.5 * inch
            for eval in evaluaciones:
                procedimiento = eval.idProcedimientoRealizado.idProcedimiento
                profesor = eval.cedulaProfesor
                competencia = procedimiento.idCompetencia

                if y < 1 * inch:
                    p.showPage()
                    y = height - 1 * inch
                    p.setFont("Helvetica", 10)

                p.drawString(1 * inch, y, f"Procedimiento: {procedimiento.nombreProcedimiento}")
                y -= 12
                p.drawString(1 * inch, y, f"Competencia: {competencia.nombreCompetencia}")
                y -= 12
                p.drawString(1 * inch, y, f"Profesor: {profesor.nombre1} {profesor.apell1}")
                y -= 12
                p.drawString(1 * inch, y, f"Nivel Dreyfus: {eval.nivelDreyfus} | Calificación: {eval.calificacion}")
                y -= 20

            p.save()
            buffer.seek(0)

            response = HttpResponse(buffer, content_type="application/pdf")
            filename = f"curva_dreyfus_{estudiante.cedula}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Reportes seguros
class PermisoReporteSeguroMixin:
    """Solo Director y Coordinadores pueden acceder a estos reportes."""
    permission_classes = [IsDirector | IsCoordinadorPractica | IsCoordinadorCurso]

# Exportar Reporte Seguro Excel
class ExportarReporteSeguroExcelAPIView(PermisoReporteSeguroMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = EvaluacionDocente.objects.select_related(
                "cedulaProfesor",
                "idProcedimientoRealizado__idPractica__cedulaEstudiante",
                "idProcedimientoRealizado__idProcedimiento__idCompetencia",
                "idProcedimientoRealizado__idPractica__idCurso",
            )

            data = []
            for eval in queryset:
                estudiante = eval.idProcedimientoRealizado.idPractica.cedulaEstudiante
                profesor = eval.cedulaProfesor
                procedimiento = eval.idProcedimientoRealizado.idProcedimiento
                competencia = procedimiento.idCompetencia
                curso_obj = eval.idProcedimientoRealizado.idPractica.idCurso

                data.append({
                    "Cédula": estudiante.cedula,
                    "Estudiante": f"{estudiante.nombre1} {estudiante.apell1}",
                    "Curso": curso_obj.nombreCurso,
                    "Procedimiento": procedimiento.nombreProcedimiento,
                    "Competencia": competencia.nombreCompetencia,
                    "Profesor": f"{profesor.nombre1} {profesor.apell1}",
                    "Nivel Dreyfus": eval.nivelDreyfus,
                    "Calificación": eval.calificacion,
                    "Fecha Evaluación": eval.fechaEvaluacion,
                })

            df = pd.DataFrame(data)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="Reporte Seguro")
            buffer.seek(0)

            response = HttpResponse(
                buffer,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            filename = f"reporte_seguro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Exportar Curva Segura PDF
class ExportarCurvaSeguraPDFAPIView(PermisoReporteSeguroMixin, APIView):
    def get(self, request, cedula_estudiante):
        try:
            estudiante = Estudiante.objects.get(cedula=cedula_estudiante)
            evaluaciones = EvaluacionDocente.objects.filter(
                idProcedimientoRealizado__idPractica__cedulaEstudiante=estudiante
            ).order_by("fechaEvaluacion")

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            p.setFont("Helvetica-Bold", 14)
            p.drawString(1 * inch, height - 1 * inch, f"Curva de Aprendizaje - {estudiante.nombre1} {estudiante.apell1}")
            p.setFont("Helvetica", 10)
            p.drawString(1 * inch, height - 1.2 * inch, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            y = height - 1.6 * inch
            for eval in evaluaciones:
                if y < 1 * inch:
                    p.showPage()
                    y = height - 1 * inch
                    p.setFont("Helvetica", 10)
                p.drawString(1 * inch, y, f"{eval.fechaEvaluacion} - {eval.idProcedimientoRealizado.idProcedimiento.nombreProcedimiento}")
                y -= 12
                p.drawString(1 * inch, y, f"Nivel Dreyfus: {eval.nivelDreyfus} | Calificación: {eval.calificacion}")
                y -= 16

            p.save()
            buffer.seek(0)

            response = HttpResponse(buffer, content_type="application/pdf")
            filename = f"curva_segura_{estudiante.cedula}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
