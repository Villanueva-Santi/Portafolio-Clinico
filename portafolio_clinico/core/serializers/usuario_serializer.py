# core/serializers/usuario_serializer.py

from rest_framework import serializers
from core.models import Usuario, Funcion


class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcion
        fields = ['id', 'nombreFuncion']


class UsuarioSerializer(serializers.ModelSerializer):
    idFuncion = FuncionSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'idUsuario',
            'usuario',
            'cedula',
            'idFuncion',
            'ultimoAcceso',
            'estado',
        ]
