# core/serializers/carga_masiva_serializer.py
from rest_framework import serializers
from core.models import Profesor, Estudiante, Funcion, CoordinadorCurso, Grupo

class ProfesorCargaSerializer(serializers.ModelSerializer):
    idFuncion = serializers.PrimaryKeyRelatedField(queryset=Funcion.objects.all())
    idCoordinadorCurso = serializers.PrimaryKeyRelatedField(
        queryset=CoordinadorCurso.objects.all(), allow_null=True
    )

    class Meta:
        model = Profesor
        fields = [
            'cedula', 'nombre1', 'nombre2', 'apell1', 'apell2',
            'correo', 'telefono1', 'telefono2',
            'idFuncion', 'idCoordinadorCurso',
            'cursoAsignado', 'semestreAsignacion',
            'fechaDesde', 'fechaHasta', 'activo'
        ]


class EstudianteCargaSerializer(serializers.ModelSerializer):
    idFuncion = serializers.PrimaryKeyRelatedField(queryset=Funcion.objects.all())
    idGrupo = serializers.PrimaryKeyRelatedField(queryset=Grupo.objects.all(), allow_null=True)

    class Meta:
        model = Estudiante
        fields = [
            'cedula', 'nombre1', 'nombre2', 'apell1', 'apell2',
            'correo', 'telefono1', 'telefono2',
            'idFuncion', 'codigoEstudiantil', 'semestreActual',
            'idGrupo', 'fechaDesde', 'fechaHasta', 'activo'
        ]
