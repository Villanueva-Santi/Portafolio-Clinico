from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.conf import settings

NIVELES_DREYFUS = [
    ('NOVATO', 'Novato'),
    ('PRINCIPIANTE_AVANZADO', 'Principiante Avanzado'),
    ('COMPETENTE', 'Competente'),
    ('PROFESIONAL', 'Profesional'),
    ('EXPERTO', 'Experto'),
]

TIPO_SIMULACION = [
    ('REAL', 'Real'),
    ('SIMULADO', 'Simulado'),
]

## POR DEFINIR ##
TIPO_PROCEDIMIENTO = [
    ('DIAGNOSTICO', 'Diagnostico'),
    ('TERAPEUTICO', 'Terapéutico'),
    ('PREVENTIVO', 'Preventivo'),
    ('REHABILITACION', 'Rehabilitación'),
]

SEMESTRES = [(i, f"{i}") for i in range(1, 13)]

TIPO_BACKUP = [
    ('COMPLETO', 'Completo'),
    ('INCREMENTAL', 'Incremental'),
    ('DIFERENCIAL', 'Diferencial'),  
]

# Create your models here.

class Funcion(models.Model):
    idFuncion = models.AutoField(primary_key=True)
    nombreFuncion = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombreFuncion

# ACTORES INSTITUCIONALES

class DirectorPrograma(models.Model):
    cedula = models.CharField(max_length=15, primary_key=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, null=True, blank=True)
    apell1 = models.CharField(max_length=50)
    apell2 = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombre1} {self.apell1}"


class CoordinadorPractica(models.Model):
    cedula = models.CharField(max_length=15, primary_key=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, null=True, blank=True)
    apell1 = models.CharField(max_length=50)
    apell2 = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    idDirectorPrograma = models.ForeignKey(DirectorPrograma, on_delete=models.SET_NULL, null=True)
    sitioAsignado = models.CharField(max_length=100)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombre1} {self.apell1}"


class CoordinadorCurso(models.Model):
    cedula = models.CharField(max_length=15, primary_key=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, null=True, blank=True)
    apell1 = models.CharField(max_length=50)
    apell2 = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    idCoordinadorPractica = models.ForeignKey(CoordinadorPractica, on_delete=models.SET_NULL, null=True)
    cursoAsignado = models.CharField(max_length=100)
    semestreAsignacion = models.CharField(max_length=10)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombre1} {self.apell1}"


class Profesor(models.Model):
    cedula = models.CharField(max_length=15, primary_key=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, null=True, blank=True)
    apell1 = models.CharField(max_length=50)
    apell2 = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    idCoordinadorCurso = models.ForeignKey(CoordinadorCurso, on_delete=models.SET_NULL, null=True)
    cursoAsignado = models.CharField(max_length=100)
    semestreAsignacion = models.CharField(max_length=10)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombre1} {self.apell1}"


class Grupo(models.Model):
    idGrupo = models.AutoField(primary_key=True)
    codigoGrupo = models.CharField(max_length=20, unique=True, validators=[RegexValidator(regex=r'^[A-Za-z0-9\s\-]+$', message='El código debe contener solo números.')])
    semestre = models.PositiveIntegerField(choices=SEMESTRES,
        default=1)
    activo = models.BooleanField(default=True)
    idCurso = models.ForeignKey('CursoClinico', on_delete=models.CASCADE, related_name='grupos')
    cedulaProfesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos')

    # Agregar estudiante
    def agregar_estudiante(self, estudiante):
        """Agrega un estudiante al grupo, siempre que no supere el límite de 6."""
        from core.models import Estudiante 

        LIMITE_ESTUDIANTES = 6
        cantidad_actual = Estudiante.objects.filter(idGrupo=self).count()

        # Verificar si el estudiante ya pertenece a este grupo
        if estudiante.idGrupo == self:
            raise ValidationError(
                f"El estudiante {estudiante.nombre1} {estudiante.apell1} ya pertenece al grupo '{self.codigoGrupo}'."
            )

        # Verificar límite máximo
        if cantidad_actual >= LIMITE_ESTUDIANTES:
            raise ValidationError(
                f"No se puede agregar al grupo '{self.codigoGrupo}', ya tiene el máximo de {LIMITE_ESTUDIANTES} estudiantes."
            )

        # Asignar el grupo y guardar
        estudiante.idGrupo = self
        estudiante.save()

    # Eliminar estudiante
    def eliminar_estudiante(self, estudiante):
        """Elimina un estudiante del grupo actual."""
        if estudiante.idGrupo != self:
            raise ValidationError(
                f"El estudiante {estudiante.nombre1} {estudiante.apell1} no pertenece al grupo '{self.codigoGrupo}'."
            )
        estudiante.idGrupo = None
        estudiante.save()

    # Validar máximo 2 grupos por profesor
    def save(self, *args, **kwargs):
        if self.cedulaProfesor:
            grupos_asignados = Grupo.objects.filter(cedulaProfesor=self.cedulaProfesor).exclude(pk=self.pk).count()
            if grupos_asignados >= 2:
                raise ValidationError(
                    f"El profesor '{self.cedulaProfesor}' ya tiene asignados 2 grupos como máximo."
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Grupo {self.codigoGrupo} - Semestre {self.semestre}"


class Estudiante(models.Model):
    cedula = models.CharField(max_length=15, primary_key=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, null=True, blank=True)
    apell1 = models.CharField(max_length=50)
    apell2 = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    codigoEstudiantil = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\d+$', message='El código debe contener solo números.')]
    )
    semestreActual = models.PositiveIntegerField(choices=SEMESTRES,
        default=1)
    idGrupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    usuario = models.OneToOneField(
    'core.Usuario',
    on_delete=models.CASCADE,
    related_name='estudiante',
    null=True,   
    blank=True    
)

    def __str__(self):
        return f"{self.cedula} - {self.nombre1} {self.apell1}"


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, unique=True)
    contrasenaHash = models.CharField(max_length=255)
    cedula = models.CharField(max_length=15, unique=True)
    idFuncion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    ultimoAcceso = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    def set_password(self, raw_password):
        """Permite cifrar la contraseña antes de guardarla."""
        self.contrasenaHash = make_password(raw_password)


    def check_password(self, raw_password):
        """Verifica contraseña."""
        
        # Método de verificación
        return check_password(raw_password, self.contrasenaHash)

    def __str__(self):
        nombre_funcion = getattr(self.idFuncion, "nombreFuncion", "")
        return f"{self.usuario} ({nombre_funcion})"

# ENTIDADES ACADÉMICAS Y CLÍNICAS

class CursoClinico(models.Model):
    idCurso = models.AutoField(primary_key=True)
    codigoCurso = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombreCurso = models.CharField(max_length=100)
    semestre = models.PositiveIntegerField(choices=SEMESTRES,
        default=1)
    periodoAcademico = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{4}-[1-2]$',
                message='El periodo académico debe tener el formato YYYY-1 o YYYY-2.'
            )
        ],
        help_text="Formato: YYYY-1 o YYYY-2 (Ejemplo: 2025-1, 2025-2)"
    )
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigoCurso} - {self.nombreCurso} ({self.periodoAcademico})"


class CompetenciaClinica(models.Model):
    idCompetencia = models.AutoField(primary_key=True)
    nombreCompetencia = models.CharField(max_length=100)
    descripcion = models.TextField(blank=False, null=False)
    nivelEsperado = models.CharField(max_length=50, choices=NIVELES_DREYFUS, null=False, blank=False)

    def __str__(self):
        return f"{self.nombreCompetencia} ({self.nivelEsperado})"


class ProcedimientoClinico(models.Model):
    idProcedimiento = models.AutoField(primary_key=True)
    idCompetencia = models.ForeignKey(CompetenciaClinica, on_delete=models.PROTECT)
    nombreProcedimiento = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_PROCEDIMIENTO)
    simulado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombreProcedimiento


class Practica(models.Model):
    idPractica = models.AutoField(primary_key=True)
    cedulaEstudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    idCurso = models.ForeignKey(CursoClinico, on_delete=models.PROTECT)
    cedulaCoordinadorPractica = models.ForeignKey(CoordinadorPractica, on_delete=models.PROTECT)
    idGrupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"Práctica {self.idPractica}"


class ProcedimientoRealizado(models.Model):
    idProcedimientoRealizado = models.AutoField(primary_key=True)
    idPractica = models.ForeignKey(Practica, on_delete=models.PROTECT)
    idProcedimiento = models.ForeignKey(ProcedimientoClinico, on_delete=models.PROTECT)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_SIMULACION)
    estado = models.CharField(max_length=20)
    resultadoEvaluacionProfesor = models.CharField(max_length=50, choices=NIVELES_DREYFUS)
    resultadoAutoevaluacionEstudiante = models.CharField(max_length=50, choices=NIVELES_DREYFUS)
    observaciones = models.TextField(blank=False, null=False)

    def __str__(self):
        # Usar guardas para evitar AttributeError si faltan relaciones
        estudiante = None
        try:
            estudiante = self.idPractica.cedulaEstudiante
            nombre = f"{estudiante.nombre1} {estudiante.apell1}"
        except Exception:
            nombre = "N/A"
        return f"ProcedimientoRealizado {self.idProcedimientoRealizado} - Estudiante {nombre}"

class EvaluacionDocente(models.Model):
    idEvaluacion = models.AutoField(primary_key=True)
    cedulaProfesor = models.ForeignKey(Profesor, on_delete=models.PROTECT)
    idProcedimientoRealizado = models.ForeignKey(ProcedimientoRealizado, on_delete=models.PROTECT)
    calificacion = models.DecimalField(
        max_digits=2,          
        decimal_places=1,      
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        help_text="Calificación numérica de 0.0 a 5.0"
    )
    nivelDreyfus = models.CharField(max_length=50, choices=NIVELES_DREYFUS)
    retroalimentacion = models.TextField(blank=False, null=False)
    fechaEvaluacion = models.DateField()

    # Retroalimentación
    comoSeSintio = models.TextField(verbose_name="¿Cómo se sintió el estudiante durante la sesión?", null=True, blank=True)
    principalesAprendizajes = models.TextField(verbose_name="¿Cuáles fueron los principales aprendizajes observados?", null=True, blank=True)
    retroalimentacionProfesor = models.TextField(verbose_name="Retroalimentación cualitativa del profesor", null=True, blank=True)

    def __str__(self):
        # Representación segura
        try:
            estudiante = self.idProcedimientoRealizado.idPractica.cedulaEstudiante
            profesor = self.cedulaProfesor
            return f"Evaluación de {estudiante.cedula} por {profesor.cedula} - {self.calificacion} - Nivel {self.nivelDreyfus}"
        except Exception:
            return f"Evaluacion {self.idEvaluacion} - {self.calificacion}"

class Autoevaluacion(models.Model):
    idAutoevaluacion = models.AutoField(primary_key=True)
    cedulaEstudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, max_length=50, null=True, blank=True) # Quitar blank y null true cuando deje de ser prototipo
    idProcedimientoRealizado = models.ForeignKey(ProcedimientoRealizado, on_delete=models.PROTECT, max_length=50, null=True, blank=True) # Quitar blank y null true cuando deje de ser prototipo
    nivelPercibido = models.CharField(max_length=50, choices=NIVELES_DREYFUS, null=False, blank=False)
    comentarios = models.TextField(blank=False, null=False)
    fechaAutoevaluacion = models.DateField()

    # Campos de reflexión cualitativa
    comoSeSintio = models.TextField(verbose_name="¿Cómo se sintió?", null=True, blank=True)
    principalesAprendizajes = models.TextField(verbose_name="¿Cuáles fueron tus principales aprendizajes de esta sesión?", null=True, blank=True)

    def __str__(self):
        return f"Autoevaluación de {self.cedulaEstudiante} - {self.idProcedimientoRealizado} Autoevaluación {self.idAutoevaluacion} - {self.nivelPercibido}"


class Retroalimentacion(models.Model):
    idRetroalimentacion = models.AutoField(primary_key=True)
    idEvaluacion = models.ForeignKey(EvaluacionDocente, on_delete=models.PROTECT, related_name="retroalimentaciones")
    cedulaProfesor = models.ForeignKey(Profesor, on_delete=models.PROTECT)
    comentarios = models.TextField(blank=False, null=False)
    fecha = models.DateField()

    def __str__(self):
        return f"Retroalimentación {self.idRetroalimentacion}"


class HistorialEvaluacion(models.Model):
    idHistorial = models.AutoField(primary_key=True)
    idEvaluacion = models.ForeignKey(EvaluacionDocente, on_delete=models.PROTECT)
    fechaCambio = models.DateTimeField()
    usuarioEditor = models.CharField(max_length=100)
    detalleCambio = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Historial {self.idHistorial}"


class Reporte(models.Model):
    idReporte = models.AutoField(primary_key=True)
    cedulaEstudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    tipoReporte = models.CharField(max_length=50)
    periodo = models.CharField(max_length=20)
    fechaGeneracion = models.DateField()
    contenido = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Reporte {self.idReporte}"


class BitacoraSistema(models.Model):
    idLog = models.AutoField(primary_key=True)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    accion = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    ip = models.GenericIPAddressField()
    detalle = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Log {self.idLog}"


class BackupLog(models.Model):
    idBackup = models.AutoField(primary_key=True)
    fechaBackup = models.DateTimeField()
    responsable = models.CharField(max_length=100)
    tipoBackup = models.CharField(max_length=20, choices=TIPO_BACKUP)
    resultado = models.CharField(max_length=20)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Backup {self.idBackup}"
    
# Notificaciones del sistema 
class Notificacion(models.Model):
    TIPOS = [
        ('evaluacion', 'Evaluación'),
        ('procedimiento', 'Procedimiento'),
        ('reporte', 'Reporte'),
        ('sistema', 'Sistema'),
    ]

    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='sistema')
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.idUsuario}"
