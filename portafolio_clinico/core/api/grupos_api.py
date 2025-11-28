# core/api/grupos_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsProfesor, IsReadOnly  
from core.models import (
    Usuario, DirectorPrograma, CoordinadorPractica, CoordinadorCurso,
    Profesor, Estudiante, Grupo
)
from django.core.exceptions import ValidationError


class GruposAPIView(APIView):
    """
    API que permite consultar y gestionar grupos clínicos según el rol del usuario.
    - Director del Programa: ve todos los grupos.
    - Coordinador de Práctica e Internado: ve grupos bajo su coordinación.
    - Coordinador de Curso: ve grupos asociados a su curso.
    - Profesor: ve y gestiona sus grupos (puede agregar/eliminar estudiantes).
    - Estudiante: ve su grupo actual.
    """

    # Solo autenticados; solo profesores pueden escribir
    permission_classes = [IsAuthenticated & (IsProfesor | IsReadOnly)]

    def post(self, request):
        usuario = request.data.get("usuario")
        accion = request.data.get("accion")

        if not usuario:
            return Response(
                {"error": "Debe proporcionar un nombre de usuario."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            u = Usuario.objects.select_related("idFuncion").get(usuario=usuario)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        rol = u.idFuncion.nombreFuncion
        data = {"usuario": usuario, "rol": rol}

        # ACCIONES RESTRINGIDAS A PROFESORES
        if accion in ["agregar_estudiante", "eliminar_estudiante"]:
            # Verificamos si el usuario actual tiene permiso de profesor
            if not request.user.groups.filter(name='Profesor').exists():
                return Response(
                    {"error": "Solo los profesores pueden modificar grupos."},
                    status=status.HTTP_403_FORBIDDEN
                )

            try:
                profesor = Profesor.objects.get(cedula=u.cedula)
            except Profesor.DoesNotExist:
                return Response({"error": "No se encontró el registro del profesor."}, status=status.HTTP_404_NOT_FOUND)

            codigo_grupo = request.data.get("codigo_grupo")
            cedula_estudiante = request.data.get("cedula_estudiante")

            if not codigo_grupo or not cedula_estudiante:
                return Response({"error": "Debe indicar 'codigo_grupo' y 'cedula_estudiante'."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                grupo = Grupo.objects.get(codigoGrupo=codigo_grupo)
            except Grupo.DoesNotExist:
                return Response({"error": "No se encontró el grupo especificado."}, status=status.HTTP_404_NOT_FOUND)

            # validamos que el grupo pertenezca al profesor
            if grupo.cedulaProfesor is None or grupo.cedulaProfesor.pk != profesor.pk:
                return Response({"error": "No tiene permiso sobre este grupo."}, status=status.HTTP_403_FORBIDDEN)

            try:
                estudiante = Estudiante.objects.get(cedula=cedula_estudiante)
            except Estudiante.DoesNotExist:
                return Response({"error": "No se encontró el estudiante especificado."}, status=status.HTTP_404_NOT_FOUND)

            if accion == "agregar_estudiante":
                try:
                    grupo.agregar_estudiante(estudiante)
                    return Response(
                        {"mensaje": f"✅ Estudiante {estudiante.nombre1} {estudiante.apell1} agregado exitosamente al grupo {grupo.codigoGrupo}."},
                        status=status.HTTP_200_OK
                    )
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            elif accion == "eliminar_estudiante":
                try:
                    grupo.eliminar_estudiante(estudiante)
                    return Response(
                        {"mensaje": f"✅ Estudiante {estudiante.nombre1} {estudiante.apell1} eliminado exitosamente del grupo {grupo.codigoGrupo}."},
                        status=status.HTTP_200_OK
                    )
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # CONSULTAS
        return Response(data, status=status.HTTP_200_OK)
