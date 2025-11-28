# core/serializers/evaluaciondocente_serializer.py
from rest_framework import serializers
from core.models import EvaluacionDocente

class EvaluacionDocenteSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()
    nivelDreyfus_display = serializers.SerializerMethodField()

    class Meta:
        model = EvaluacionDocente
        fields = [
            'idEvaluacion',
            'cedulaProfesor',
            'idProcedimientoRealizado',
            'calificacion',
            'nivelDreyfus',
            'nivelDreyfus_display',      
            'retroalimentacion',
            'comoSeSintio',
            'principalesAprendizajes',
            'retroalimentacionProfesor',
            'fechaEvaluacion',
            'estudiante_nombre',
            'profesor_nombre'
        ]
        extra_kwargs = {
            'cedulaEstudiante': {'required': False},
            'idProcedimientoRealizado': {'required': False},
        }

    # Campos calculados
    def get_estudiante_nombre(self, obj):
        """Obtiene el nombre del estudiante a través de ProcedimientoRealizado → Práctica → Estudiante."""
        try:
            estudiante = obj.idProcedimientoRealizado.idPractica.cedulaEstudiante
            return f"{estudiante.nombre1} {estudiante.apell1}"
        except AttributeError:
            return None

    def get_profesor_nombre(self, obj):
        """Devuelve el nombre completo del profesor evaluador."""
        if obj.cedulaProfesor:
            return f"{obj.cedulaProfesor.nombre1} {obj.cedulaProfesor.apell1}"
        return None

    def get_nivelDreyfus_display(self, obj):
        """Devuelve la representación legible del nivel Dreyfus."""
        if not obj.nivelDreyfus:
            return "Desconocido"

        niveles = {
            "NOVATO": "Novato",
            "PRINCIPIANTE AVANZADO": "Principiante Avanzado",
            "COMPETENTE": "Competente",
            "PROFICIENTE": "Proficiente",
            "EXPERTO": "Experto",
        }

        # Normaliza el texto
        clave = obj.nivelDreyfus.strip().upper()
        return niveles.get(clave, "Desconocido")

    # Validaciones
    def validate(self, data):
        """Valida los datos antes de crear o actualizar la evaluación."""
        if not data.get('retroalimentacion'):
            raise serializers.ValidationError("La retroalimentación es obligatoria.")
        
        nivel = data.get('nivelDreyfus', '').strip().upper()
        niveles_validos = ["NOVATO", "PRINCIPIANTE AVANZADO", "COMPETENTE", "PROFICIENTE", "EXPERTO"]

        if nivel not in niveles_validos:
            raise serializers.ValidationError("El nivel Dreyfus debe ser una de las categorías válidas.")
        
        return data
