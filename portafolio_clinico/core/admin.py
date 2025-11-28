from django.contrib import admin

from .models import (
    Funcion, DirectorPrograma, CoordinadorPractica, CoordinadorCurso,
    Profesor, Estudiante, Usuario, CursoClinico, Grupo, Practica,
    CompetenciaClinica, ProcedimientoClinico, ProcedimientoRealizado,
    EvaluacionDocente, Autoevaluacion, Retroalimentacion, HistorialEvaluacion,
    Reporte, BitacoraSistema, BackupLog
)

# Admins simples y útiles

@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = ('idFuncion', 'nombreFuncion', 'descripcion')
    search_fields = ('nombreFuncion',)


@admin.register(DirectorPrograma)
class DirectorProgramaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'activo')
    search_fields = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2')
    list_filter = ('activo',)


@admin.register(CoordinadorPractica)
class CoordinadorPracticaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'sitioAsignado', 'activo')
    search_fields = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'sitioAsignado')
    list_filter = ('activo',)


@admin.register(CoordinadorCurso)
class CoordinadorCursoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'cursoAsignado', 'semestreAsignacion', 'activo')
    search_fields = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'cursoAsignado')
    list_filter = ('semestreAsignacion','activo')


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'cursoAsignado', 'semestreAsignacion', 'activo')
    search_fields = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'cursoAsignado')
    list_filter = ('cursoAsignado','activo')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'codigoEstudiantil', 'semestreActual', 'activo', 'idGrupo')
    search_fields = ('cedula', 'nombre1', 'nombre2','apell1', 'apell2', 'correo', 'telefono1', 'telefono2', 'codigoEstudiantil')
    list_filter = ('semestreActual','activo')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('idUsuario', 'usuario', 'cedula', 'idFuncion', 'estado', 'ultimoAcceso')
    search_fields = ('usuario', 'cedula')
    list_filter = ('idFuncion','estado')


@admin.register(CursoClinico)
class CursoClinicoAdmin(admin.ModelAdmin):
    list_display = ('idCurso','codigoCurso','nombreCurso','semestre','periodoAcademico','fechaDesde','fechaHasta','estado')
    search_fields = ('nombreCurso','periodoAcademico')
    list_filter = ('semestre','estado', 'periodoAcademico')


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('idGrupo','codigoGrupo','semestre','idCurso', 'cedulaProfesor','activo')
    search_fields = ('codigoGrupo',)
    list_filter = ('semestre','activo')


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ('idPractica','idCurso','cedulaEstudiante','idGrupo','cedulaCoordinadorPractica','fechaInicio','fechaFin','estado')
    search_fields = ('idPractica','cedulaEstudiante__cedula')
    list_filter = ('estado',)


@admin.register(CompetenciaClinica)
class CompetenciaClinicaAdmin(admin.ModelAdmin):
    list_display = ('idCompetencia','nombreCompetencia','nivelEsperado')
    search_fields = ('nombreCompetencia',)


@admin.register(ProcedimientoClinico)
class ProcedimientoClinicoAdmin(admin.ModelAdmin):
    list_display = ('idProcedimiento','nombreProcedimiento','idCompetencia','tipo','simulado')
    search_fields = ('nombreProcedimiento',)
    list_filter = ('simulado','tipo')


@admin.register(ProcedimientoRealizado)
class ProcedimientoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('idProcedimientoRealizado','idPractica','idProcedimiento','fecha','tipo','estado','resultadoEvaluacionProfesor','resultadoAutoevaluacionEstudiante')
    search_fields = ('idProcedimientoRealizado','idPractica__idPractica')
    list_filter = ('tipo','estado')


@admin.register(EvaluacionDocente)
class EvaluacionDocenteAdmin(admin.ModelAdmin):
    list_display = ('idEvaluacion','cedulaProfesor','idProcedimientoRealizado','calificacion','nivelDreyfus','fechaEvaluacion')
    search_fields = ('idEvaluacion','cedulaProfesor__cedula')
    list_filter = ('nivelDreyfus',)


@admin.register(Autoevaluacion)
class AutoevaluacionAdmin(admin.ModelAdmin):
    list_display = ('idAutoevaluacion','cedulaEstudiante','idProcedimientoRealizado','nivelPercibido','fechaAutoevaluacion')
    search_fields = ('idAutoevaluacion','cedulaEstudiante__cedula')
    list_filter = ('nivelPercibido',)


@admin.register(Retroalimentacion)
class RetroalimentacionAdmin(admin.ModelAdmin):
    list_display = ('idRetroalimentacion','idEvaluacion','cedulaProfesor','fecha')
    search_fields = ('idRetroalimentacion','cedulaProfesor__cedula')


@admin.register(HistorialEvaluacion)
class HistorialEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('idHistorial','idEvaluacion','fechaCambio','usuarioEditor')
    search_fields = ('idHistorial','usuarioEditor')


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('idReporte','cedulaEstudiante','tipoReporte','periodo','fechaGeneracion')
    search_fields = ('tipoReporte','periodo')
    list_filter = ('tipoReporte',)


@admin.register(BitacoraSistema)
class BitacoraSistemaAdmin(admin.ModelAdmin):
    list_display = ('idLog','idUsuario','accion','fecha','ip')
    search_fields = ('accion','idUsuario__usuario')
    list_filter = ('fecha',)


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ('idBackup','fechaBackup','responsable','tipoBackup','resultado')
    search_fields = ('responsable','tipoBackup')
    list_filter = ('tipoBackup','resultado')