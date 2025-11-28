# core/tests/test_grupos_api.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Usuario, Funcion, Profesor, Estudiante, Grupo, CursoClinico
from django.core.exceptions import ValidationError
from datetime import date

class GruposAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear funciones
        self.funcion_profesor = Funcion.objects.create(nombreFuncion="Profesor")
        self.funcion_estudiante = Funcion.objects.create(nombreFuncion="Estudiante")

        # Crear curso clínico
        self.curso = CursoClinico.objects.create(
            codigoCurso="CC1",
            nombreCurso="Curso Clínico I",
            semestre=2,
            periodoAcademico="2025-2",
            fechaDesde="2025-08-01",
            fechaHasta="2025-12-01"
        )

        # Crear profesor y usuario
        self.profesor = Profesor.objects.create(
            cedula="123456789",
            nombre1="Carlos",
            apell1="Rojas",
            correo="carlos@example.com",
            telefono1="3001234567",
            fechaDesde=date.today(),
            idFuncion=self.funcion_profesor
        )
        self.usuario_profesor = Usuario.objects.create(
            usuario="profesor1",
            contrasenaHash="test123",
            cedula=self.profesor.cedula,
            idFuncion=self.funcion_profesor
        )

        # Crear grupo
        self.grupo = Grupo.objects.create(
            codigoGrupo="G2",
            semestre=2,
            idCurso=self.curso,
            cedulaProfesor=self.profesor
        )

        # Crear estudiante y usuario
        self.estudiante = Estudiante.objects.create(
            cedula="123456",
            nombre1="Ana",
            apell1="Pérez",
            correo="ana@example.com",
            telefono1="3104567890",
            idFuncion=self.funcion_estudiante,
            codigoEstudiantil="202501",
            semestreActual=2,
            fechaDesde="2025-08-01"
        )
        self.usuario_estudiante = Usuario.objects.create(
            usuario="ana123",
            contrasenaHash="test123",
            cedula=self.estudiante.cedula,
            idFuncion=self.funcion_estudiante
        )

        self.url = "/api/grupos/"

    def test_agregar_estudiante_a_grupo(self):
        """✅ El profesor puede agregar un estudiante a su grupo"""
        data = {
            "usuario": "profesor1",
            "accion": "agregar_estudiante",
            "codigo_grupo": "G2",
            "cedula_estudiante": "123456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("agregado exitosamente", response.data["mensaje"])

    def test_agregar_estudiante_a_grupo_no_pertenece_profesor(self):
        """❌ El profesor no puede agregar estudiante a un grupo que no es suyo"""
        otro_prof = Profesor.objects.create(
            cedula="987654321",
            nombre1="Laura",
            apell1="Gómez",
            correo="laura@example.com",
            telefono1="3204561234",
            fechaDesde=date.today(),  # ✅ agregado
            idFuncion=self.funcion_profesor
        )
        otro_grupo = Grupo.objects.create(
            codigoGrupo="G3",
            semestre=3,
            idCurso=self.curso,
            cedulaProfesor=otro_prof
        )

        data = {
            "usuario": "profesor1",
            "accion": "agregar_estudiante",
            "codigo_grupo": "G3",
            "cedula_estudiante": "123456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("no pertenece al profesor", response.data["error"])

    def test_limite_maximo_estudiantes_en_grupo(self):
        """❌ No se puede agregar más de 6 estudiantes al mismo grupo"""
        for i in range(6):
            Estudiante.objects.create(
        cedula=f"1000{i}",
        nombre1=f"Est{i}",
        apell1="Prueba",
        correo=f"est{i}@example.com",
        telefono1="300111222",
        codigoEstudiantil=f"20251{i}",  # ✅ empieza en 202510, no choca con 202501
        semestreActual=2,
        idGrupo=self.grupo,
        idFuncion=self.funcion_estudiante,
        fechaDesde="2025-08-01"
    )


        nuevo_estudiante = Estudiante.objects.create(
            cedula="999999",
            nombre1="Extra",
            apell1="Estudiante",
            correo="extra@mail.com",
            telefono1="3200000000",
            idFuncion=self.funcion_estudiante,
            codigoEstudiantil="999999",
            semestreActual=2,
            fechaDesde="2025-08-01"
        )

        data = {
            "usuario": "profesor1",
            "accion": "agregar_estudiante",
            "codigo_grupo": "G2",
            "cedula_estudiante": "999999"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("máximo de 6 estudiantes", response.data["error"])

    def test_consulta_por_rol_profesor(self):
        """✅ El profesor puede ver sus grupos"""
        data = {"usuario": "profesor1"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rol"], "Profesor")
        self.assertEqual(response.data["total_grupos"], 1)
