# core/serializers/procedimientorealizado_serializer.py
from rest_framework import serializers
from core.models import ProcedimientoRealizado

class ProcedimientoRealizadoSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    procedimiento_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ProcedimientoRealizado
        fields = [
            'idProcedimientoRealizado',
            'idPractica',
            'idProcedimiento',
            'fecha',
            'tipo',
            'estado',
            'resultadoEvaluacionProfesor',
            'resultadoAutoevaluacionEstudiante',
            'observaciones',
            'estudiante_nombre',
            'procedimiento_nombre',
        ]

    def get_estudiante_nombre(self, obj):
        """Devuelve el nombre completo del estudiante relacionado."""
        try:
            estudiante = obj.idPractica.cedulaEstudiante
            return f"{estudiante.nombre1} {estudiante.apell1}"
        except Exception:
            return None

    def get_procedimiento_nombre(self, obj):
        """Devuelve el nombre del procedimiento clínico."""
        try:
            # Asegurar que el campo correcto sea accedido
            procedimiento = obj.idProcedimiento
            if hasattr(procedimiento, 'nombre'):
                return procedimiento.nombre
            elif hasattr(procedimiento, 'nombreProcedimiento'):
                return procedimiento.nombreProcedimiento
            elif hasattr(procedimiento, 'descripcion'):
                return procedimiento.descripcion
            else:
                return str(procedimiento)
        except Exception:
            return None

    def validate(self, data):
        """Validaciones básicas de negocio."""
        if not data.get('observaciones'):
            raise serializers.ValidationError("Las observaciones son obligatorias.")
        if not data.get('resultadoAutoevaluacionEstudiante') and not data.get('resultadoEvaluacionProfesor'):
            raise serializers.ValidationError("Debe registrar al menos un resultado de evaluación.")
        return data
