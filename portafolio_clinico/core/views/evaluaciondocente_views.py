# core/views/evaluaciondocente_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import EvaluacionDocente
from core.serializers.evaluaciondocente_serializer import EvaluacionDocenteSerializer
from core.permissions import IsProfesor, IsReadOnly  # Permisos

class EvaluacionDocenteViewSet(viewsets.ModelViewSet):
    """
    API para registrar y consultar evaluaciones realizadas por los profesores.
    Incluye observaciones y reflexiones sobre la sesión.
    """
    queryset = EvaluacionDocente.objects.all()
    serializer_class = EvaluacionDocenteSerializer
    permission_classes = [IsProfesor | IsReadOnly]  

    def create(self, request, *args, **kwargs):
        
        # Validación de rol: Solo profesor puede crear
        if not request.user.groups.filter(name='Profesor').exists():
            return Response({"error": "Solo los profesores pueden registrar evaluaciones docentes."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "✅ Evaluación docente registrada correctamente.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def por_profesor(self, request):
        """Listar evaluaciones realizadas por un profesor"""
        cedula = request.query_params.get('cedula')
        if not cedula:
            return Response({"error": "Debe enviar la cédula del profesor."}, status=status.HTTP_400_BAD_REQUEST)

        evaluaciones = EvaluacionDocente.objects.filter(cedulaProfesor__cedula=cedula)
        serializer = self.get_serializer(evaluaciones, many=True)
        return Response(serializer.data)
