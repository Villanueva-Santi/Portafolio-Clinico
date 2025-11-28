# core/views/carga_masiva_views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions  # 🟩
from core.models import Estudiante, Profesor, Grupo
from django.db import transaction
from core.permissions import IsDirector, IsCoordinadorPractica, IsCoordinadorCurso  # 🟩

# Clase base para carga masiva de Estudiantes
class CargaMasivaEstudianteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector | IsCoordinadorPractica | IsCoordinadorCurso]  # 🟩

    def post(self, request):
        try:
            excel_file = request.FILES.get('file')
            if not excel_file:
                return Response({'error': 'No se ha proporcionado un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file)

            # Validar columnas necesarias
            columnas_requeridas = ['nombres', 'apellidos', 'correo', 'codigoEstudiantil', 'semestre']  # 🟩
            for columna in columnas_requeridas:
                if columna not in df.columns:
                    return Response({'error': f'Falta la columna requerida: {columna}'}, status=status.HTTP_400_BAD_REQUEST)

            # Registrar estudiantes
            with transaction.atomic():
                for _, fila in df.iterrows():
                    Estudiante.objects.create(
                        nombres=fila['nombres'],
                        apellidos=fila['apellidos'],
                        correo=fila['correo'],
                        codigoEstudiantil=fila['codigoEstudiantil'],
                        semestre=fila['semestre']
                    )

            return Response({'mensaje': 'Carga masiva de estudiantes completada exitosamente'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Clase base para carga masiva de Profesores

class CargaMasivaProfesorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector | IsCoordinadorPractica]  

    def post(self, request):
        try:
            excel_file = request.FILES.get('file')
            if not excel_file:
                return Response({'error': 'No se ha proporcionado un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file)

            columnas_requeridas = ['nombres', 'apellidos', 'correo', 'especialidad']  
            for columna in columnas_requeridas:
                if columna not in df.columns:
                    return Response({'error': f'Falta la columna requerida: {columna}'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                for _, fila in df.iterrows():
                    Profesor.objects.create(
                        nombres=fila['nombres'],
                        apellidos=fila['apellidos'],
                        correo=fila['correo'],
                        especialidad=fila['especialidad']
                    )

            return Response({'mensaje': 'Carga masiva de profesores completada exitosamente'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Carga masiva de Grupos 

class CargaMasivaGrupoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector | IsCoordinadorCurso | IsCoordinadorPractica]

    def post(self, request):
        try:
            excel_file = request.FILES.get('file')
            if not excel_file:
                return Response({'error': 'No se ha proporcionado un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file)

            # Coincide con el modelo Grupo
            columnas_requeridas = ['codigoGrupo', 'semestre', 'idCurso', 'cedulaProfesor']
            for columna in columnas_requeridas:
                if columna not in df.columns:
                    return Response({'error': f'Falta la columna requerida: {columna}'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                for _, fila in df.iterrows():
                    Grupo.objects.create(
                        codigoGrupo=fila['codigoGrupo'],
                        semestre=fila['semestre'],
                        idCurso_id=fila['idCurso'],              
                        cedulaProfesor_id=fila['cedulaProfesor'], 
                        activo=True                              
                    )

            return Response({'mensaje': 'Carga masiva de grupos completada exitosamente'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
