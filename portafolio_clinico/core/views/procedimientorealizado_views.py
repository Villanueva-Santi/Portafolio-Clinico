# core/views/procedimientorealizado_viewset.py

from rest_framework import viewsets, permissions
from core.models import ProcedimientoRealizado
from core.serializers.procedimientorealizado_serializer import ProcedimientoRealizadoSerializer
from core.permissions import IsDirector, IsCoordinadorPractica, IsProfesor, IsEstudiante, IsReadOnly

class ProcedimientoRealizadoViewSet(viewsets.ModelViewSet):
    queryset = ProcedimientoRealizado.objects.all().select_related(
        'idPractica', 'idProcedimiento'
    )
    serializer_class = ProcedimientoRealizadoSerializer

    def get_permissions(self):
        """
        Controla los permisos por rol:
        - Director y Coordinador pueden ver y editar todos.
        - Profesor puede listar y crear solo los suyos.
        - Estudiante puede ver solo los que le pertenecen.
        """
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [IsReadOnly]
        elif self.request.user.groups.filter(name__in=['Director', 'CoordinadorPractica']).exists():
            permission_classes = [IsDirector | IsCoordinadorPractica]
        elif self.request.user.groups.filter(name='Profesor').exists():
            permission_classes = [IsProfesor]
        else:
            permission_classes = [IsEstudiante]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        """
        Filtra los procedimientos según el rol.
        """
        user = self.request.user

        # Director / Coordinador ven todo
        if user.groups.filter(name__in=['Director', 'CoordinadorPractica']).exists():
            return ProcedimientoRealizado.objects.all()

        # Profesor: Ver procedimientos de sus estudiantes
        if user.groups.filter(name='Profesor').exists():
            return ProcedimientoRealizado.objects.filter(
                idPractica__idGrupo__cedulaProfesor__usuario=user
            )

        # Estudiante: Ver solo los suyos
        if user.groups.filter(name='Estudiante').exists():
            return ProcedimientoRealizado.objects.filter(
                idPractica__cedulaEstudiante__usuario=user
            )

        return ProcedimientoRealizado.objects.none()
