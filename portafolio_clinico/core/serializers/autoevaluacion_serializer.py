# core/serializers/autoevaluacion_serializer.py
from rest_framework import serializers
from core.models import Autoevaluacion

class AutoevaluacionSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    nivelDreyfus_display = serializers.SerializerMethodField()

    class Meta:
        model = Autoevaluacion
        fields = [
            'idAutoevaluacion',
            'cedulaEstudiante',
            'idProcedimientoRealizado',
            'nivelPercibido',              
            'nivelDreyfus_display',        
            'comoSeSintio',                
            'principalesAprendizajes',
            'fechaAutoevaluacion',
            'estudiante_nombre'
        ]

    # Campos calculados
    def get_estudiante_nombre(self, obj):
        if obj.cedulaEstudiante:
            return f"{obj.cedulaEstudiante.nombre1} {obj.cedulaEstudiante.apell1}"
        return None

    def get_nivelDreyfus_display(self, obj):
        niveles = {
            "NOVATO": "Novato",
            "PRINCIPANTE_AVANZADO": "Principiante Avanzado",
            "COMPETENTE": "Competente",
            "PROFICIENTE": "Proficiente",
            "EXPERTO": "Experto",
        }
        return niveles.get(obj.nivelPercibido, "Desconocido")

    # Validaciones
    def validate(self, data):
        if not data.get('comoSeSintio') or not data.get('principalesAprendizajes'):
            raise serializers.ValidationError("Las dos preguntas de reflexión son obligatorias.")
        return data