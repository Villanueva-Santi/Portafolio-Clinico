# core/api/carga_masiva_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Importar las vistas base desde views/carga_masiva_views.py
from core.views.carga_masiva_views import (
    CargaMasivaEstudianteAPIView,   # 🟩
    CargaMasivaProfesorAPIView,  
    CargaMasivaGrupoAPIView # 🟩
)

# API que expone las rutas hacia las vistas de carga masiva

class CargaEstudiantesAPI(CargaMasivaEstudianteAPIView):   # 🟩
    """API para carga masiva de estudiantes"""
    pass   # 🟩

class CargaProfesoresAPI(CargaMasivaProfesorAPIView):      # 🟩
    """API para carga masiva de profesores"""
    pass   # 🟩

class CargaGruposAPI(CargaMasivaGrupoAPIView):             # 🟩
    """API para carga masiva de grupos"""
    pass   # 🟩
