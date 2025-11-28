# core/api/profesores_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Usuario, Profesor, Grupo, CursoClinico, Practica, Estudiante, EvaluacionDocente
from django.db.models import Count


class ProfesoresAPIView(APIView):
    """
    Endpoint para listar profesores clínicos con detalle completo:
    grupos, curso asignado y cantidad de estudiantes.
    Accesible por Director, Coordinadores de Práctica e Internado y Coordinadores de Curso.
    """

    def post(self, request):
        usuario = request.data.get("usuario")
        contrasena = request.data.get("contrasena")

        # Validar usuario
        try:
            u = Usuario.objects.select_related("idFuncion").get(usuario=usuario)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        rol = u.idFuncion.nombreFuncion

        # Validar permiso
        if rol not in ["Director del Programa", "Coordinador de Práctica e Internado", "Coordinador de Curso"]:
            return Response(
                {"error": "No tiene permisos para acceder a esta información."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Filtrado jerárquico
        profesores = Profesor.objects.filter(activo=True)

        if rol == "Coordinador de Curso":
            curso = CursoClinico.objects.filter(grupos__cedulaProfesor__isnull=False).first()
            if curso:
                profesores = profesores.filter(cursoAsignado=curso.nombreCurso).distinct()

        elif rol == "Coordinador de Práctica e Internado":
            practica = Practica.objects.filter(idCoordinadorPI__cedula=u.cedula).first()
            if practica:
                profesores = profesores.filter(grupos__idCurso__practica=practica).distinct()

        elif rol == "Director del Programa":
            # Puede ver todos los profesores
            pass

        # Agregar conteos globales
        profesores = profesores.annotate(
            total_grupos=Count("grupos", distinct=True),
            total_estudiantes=Count("grupos__estudiante", distinct=True),
            total_evaluaciones=Count("evaluaciondocente", distinct=True)
        )

        # Estructura de salida detallada
        data_profesores = []
        for p in profesores:
            grupos_detalle = []
            for g in Grupo.objects.filter(cedulaProfesor=p):
                grupos_detalle.append({
                    "codigoGrupo": g.codigoGrupo,
                    "curso": g.idCurso.nombreCurso if g.idCurso else None,
                    "semestre": g.semestre,
                    "estudiantes_en_grupo": Estudiante.objects.filter(idGrupo=g).count()
                })

            data_profesores.append({
                "cedula": p.cedula,
                "nombre_completo": f"{p.nombre1} {p.nombre2 or ''} {p.apell1} {p.apell2 or ''}".strip(),
                "correo": p.correo,
                "telefono1": p.telefono1,
                "telefono2": p.telefono2,
                "curso_asignado": p.cursoAsignado,
                "semestre_asignacion": p.semestreAsignacion,
                "fecha_desde": p.fechaDesde,
                "fecha_hasta": p.fechaHasta,
                "activo": p.activo,
                "total_grupos": p.total_grupos,
                "total_estudiantes": p.total_estudiantes,
                "total_evaluaciones": p.total_evaluaciones,
                "grupos_detalle": grupos_detalle
            })

        # Respuesta final
        data = {
            "usuario": u.usuario,
            "rol": rol,
            "total_profesores": profesores.count(),
            "permisos_profesor": {
                "puede_evaluar_estudiantes": True,
                "puede_registrar_observaciones": True,
                "puede_asignar_estudiantes": True,
                "puede_ver_sus_estudiantes": True
            },
            "profesores": data_profesores
        }

        return Response(data, status=status.HTTP_200_OK)
