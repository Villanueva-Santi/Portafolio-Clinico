# core/management/commands/cargar_datos_base.py
from django.core.management.base import BaseCommand
from core.models import Funcion, Profesor, Grupo, Estudiante, CursoClinico
from datetime import date


class Command(BaseCommand):
    help = "Carga datos base iniciales para pruebas del Portafolio Clínico"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("🚀 Iniciando carga de datos base...")

            # ============================================================
            # 1️⃣ FUNCIONES
            # ============================================================
            func_est, _ = Funcion.objects.get_or_create(nombreFuncion="Estudiante")
            func_prof, _ = Funcion.objects.get_or_create(nombreFuncion="Profesor")
            self.stdout.write("✔️ Funciones creadas o verificadas.")

            # ============================================================
            # 2️⃣ CURSO CLÍNICO
            # ============================================================
            curso, _ = CursoClinico.objects.get_or_create(
                codigoCurso="CC101",
                defaults=dict(
                    nombreCurso="Semiología Médica",
                    semestre=6,
                    periodoAcademico="2025-2",
                    fechaDesde=date(2025, 8, 1),
                    fechaHasta=date(2025, 12, 15),
                    estado=True,
                ),
            )
            self.stdout.write("✔️ Curso clínico creado o verificado.")

            # ============================================================
            # 3️⃣ PROFESORES
            # ============================================================
            prof1, _ = Profesor.objects.get_or_create(
                cedula="123456789",
                defaults=dict(
                    nombre1="Ana",
                    apell1="López",
                    correo="ana.lopez@uni.edu",
                    telefono1="3102223344",
                    idFuncion=func_prof,
                    cursoAsignado="Semiología Médica",
                    semestreAsignacion="6",
                    fechaDesde=date(2025, 8, 1),
                    fechaHasta=date(2025, 12, 15),
                    activo=True,
                ),
            )

            prof2, _ = Profesor.objects.get_or_create(
                cedula="987654321",
                defaults=dict(
                    nombre1="Carlos",
                    apell1="Pérez",
                    correo="carlos.perez@uni.edu",
                    telefono1="3201112233",
                    idFuncion=func_prof,
                    cursoAsignado="Semiología Médica",
                    semestreAsignacion="6",
                    fechaDesde=date(2025, 8, 1),
                    fechaHasta=date(2025, 12, 15),
                    activo=True,
                ),
            )
            self.stdout.write("✔️ Profesores creados o actualizados.")

            # ============================================================
            # 4️⃣ GRUPOS
            # ============================================================
            grupo1, _ = Grupo.objects.get_or_create(
                codigoGrupo="G601",
                defaults=dict(
                    semestre=6,
                    activo=True,
                    idCurso=curso,
                    cedulaProfesor=prof1,
                ),
            )

            grupo2, _ = Grupo.objects.get_or_create(
                codigoGrupo="G602",
                defaults=dict(
                    semestre=6,
                    activo=True,
                    idCurso=curso,
                    cedulaProfesor=prof2,
                ),
            )

            self.stdout.write("✔️ Grupos creados o verificados.")

            # ============================================================
            # 5️⃣ ESTUDIANTES
            # ============================================================
            estudiantes_data = [
                ("1001", "Felipe", "Mora", "202501", grupo1),
                ("1002", "Laura", "Díaz", "202502", grupo1),
                ("1003", "Andrés", "Ruiz", "202503", grupo1),
                ("1004", "Sofía", "Gómez", "202504", grupo2),
                ("1005", "Mateo", "Hernández", "202505", grupo2),
                ("1006", "Camila", "Torres", "202506", grupo2),
            ]

            for cedula, nombre, apellido, codigo, grupo in estudiantes_data:
                Estudiante.objects.get_or_create(
                    cedula=cedula,
                    defaults=dict(
                        nombre1=nombre,
                        apell1=apellido,
                        correo=f"{nombre.lower()}.{apellido.lower()}@uni.edu",
                        telefono1="3100000000",
                        idFuncion=func_est,
                        codigoEstudiantil=codigo,
                        semestreActual=6,
                        idGrupo=grupo,
                        fechaDesde=date(2025, 8, 1),
                        activo=True,
                    ),
                )

            self.stdout.write("✔️ Estudiantes creados o verificados.")

            # ============================================================
            # ✅ FINALIZACIÓN
            # ============================================================
            self.stdout.write(self.style.SUCCESS("🎉 Carga de datos base completada exitosamente."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error durante la carga de datos: {e}"))
