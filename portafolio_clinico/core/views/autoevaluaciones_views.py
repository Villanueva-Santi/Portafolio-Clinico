# core/views/autoevaluaciones_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from core.models import Autoevaluacion
from core.serializers.autoevaluacion_serializer import AutoevaluacionSerializer
from core.permissions import IsEstudiante, IsProfesor, IsReadOnly

class AutoevaluacionViewSet(viewsets.ModelViewSet):
    queryset = Autoevaluacion.objects.all()
    serializer_class = AutoevaluacionSerializer
    permission_classes = [IsEstudiante | IsProfesor | IsReadOnly]

    def create(self, request, *args, **kwargs):

        es_estudiante = request.user.groups.filter(name='Estudiante').exists()
        es_profesor = request.user.groups.filter(name='Profesor').exists()

        if not (es_estudiante or es_profesor):
            return Response(
                {"error": "Solo estudiantes o profesores pueden registrar autoevaluaciones."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()

        # Si el frontend no envía fecha, se llena con hoy
        if not data.get("fechaAutoevaluacion"):
            data["fechaAutoevaluacion"] = timezone.now().date()  # #

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "✅ Autoevaluación registrada correctamente.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({"errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def por_estudiante(self, request):
        cedula = request.query_params.get('cedula')
        if not cedula:
            return Response(
                {"error": "Debe enviar la cédula del estudiante."},
                status=status.HTTP_400_BAD_REQUEST
            )

        evaluaciones = Autoevaluacion.objects.filter(cedulaEstudiante__cedula=cedula)
        serializer = self.get_serializer(evaluaciones, many=True)
        return Response(serializer.data)
