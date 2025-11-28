# core/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import logging

from core.models import (
    BitacoraSistema,
    ProcedimientoRealizado,
    EvaluacionDocente,
    Autoevaluacion,
    Retroalimentacion,
    Usuario,
    Notificacion,
)

from portafolio_clinico.backups.backup_utils import crear_backup  

logger = logging.getLogger(__name__)

# FUNCIONES AUXILIARES

def get_usuario_contexto(instance):
    """Identifica el usuario relacionado con el cambio.
    Intenta resolver Usuario por relaciones conocidas (Estudiante / Profesor / Practica).
    Si no encuentra, devuelve el primer Usuario (fallback) o None.
    """
    try:
        if hasattr(instance, "cedulaEstudiante") and instance.cedulaEstudiante:
            # instance.cedulaEstudiante es un objeto Estudiante
            return Usuario.objects.filter(cedula=instance.cedulaEstudiante.cedula).first()
        if hasattr(instance, "cedulaProfesor") and instance.cedulaProfesor:
            return Usuario.objects.filter(cedula=instance.cedulaProfesor.cedula).first()
        # El objeto puede tener idPractica -> idPractica.cedulaEstudiante
        if hasattr(instance, "idPractica") and getattr(instance.idPractica, "cedulaEstudiante", None):
            return Usuario.objects.filter(cedula=instance.idPractica.cedulaEstudiante.cedula).first()
    except Exception as e:
        logger.exception("Error al resolver usuario contexto: %s", e)
    # Fallback seguro: Devuelve None en vez de un usuario genérico para evitar escribir bitácoras con usuario incorrecto
    return Usuario.objects.first() if Usuario.objects.exists() else None  # Preferible None si no hay usuarios

def registrar_bitacora(usuario, accion, detalle, ip="127.0.0.1"):
    """Crea un registro en la Bitácora del sistema."""
    try:
        if not isinstance(usuario, Usuario):
            # Si vino None, usar el primer usuario disponible (Fallback)
            usuario = Usuario.objects.first()
        if usuario is None:
            logger.warning("No hay usuario disponible para bitácora. Detalle: %s", detalle)
            return
        BitacoraSistema.objects.create(
            idUsuario=usuario,
            accion=accion,
            fecha=timezone.now(),
            ip=ip,
            detalle=detalle,
        )
    except Exception as e:
        logger.exception("Error al crear bitácora: %s", e)

# FUNCIÓN AUXILIAR DE NOTIFICACIÓN
def crear_notificacion(usuario, titulo, mensaje, tipo="sistema"):
    """Crea una notificación asociada a un usuario."""
    try:
        if usuario is None:
            logger.warning("crear_notificacion: usuario es None; notificación no creada. Título: %s", titulo)
            return
        Notificacion.objects.create(
            idUsuario=usuario,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            fecha=timezone.now()
        )
    except Exception as e:
        logger.exception("Error al crear notificación: %s", e)

# SEÑAL UNIFICADA: Creación / Actualización (ProcedimientoRealizado, EvaluacionDocente, Autoevaluacion, Retroalimentacion) 
@receiver(post_save, sender=ProcedimientoRealizado)
@receiver(post_save, sender=EvaluacionDocente)
@receiver(post_save, sender=Autoevaluacion)
@receiver(post_save, sender=Retroalimentacion)
def señal_creacion_actualizacion_unificada(sender, instance, created, **kwargs):
    """
    Registra bitácora, crea notificación y (opcional) lanza backup cuando se crean/actualizan registros relevantes.
    CAMBIO: función unificada para evitar duplicidad.
    """
    try:
        usuario = get_usuario_contexto(instance)
        accion = "CREACIÓN" if created else "ACTUALIZACIÓN"
        detalle = f"{sender.__name__} (ID {getattr(instance, 'pk', 'N/A')}) {'creado' if created else 'modificado'}."
        registrar_bitacora(usuario, accion, detalle)

        # Crear notificación para el usuario relevante 
        titulo = f"{sender.__name__} - {'Nuevo' if created else 'Actualizado'}"
        mensaje = f"Se ha {'creado' if created else 'actualizado'} un registro de tipo {sender.__name__} con ID {getattr(instance, 'pk', 'N/A')}."
        # Tipo por sender
        tipo_map = {
            'EvaluacionDocente': 'evaluacion',
            'ProcedimientoRealizado': 'procedimiento',
            'Autoevaluacion': 'autoevaluacion',
            'Retroalimentacion': 'retroalimentacion',
        }
        tipo = tipo_map.get(sender.__name__, 'sistema')
        crear_notificacion(usuario, titulo, mensaje, tipo=tipo)

        # Generar backup para ciertos eventos (Si tu utilidad manejará estos tipos)
        try:
            if sender is EvaluacionDocente:
                crear_backup("evaluacion")
            elif sender is ProcedimientoRealizado:
                crear_backup("procedimiento")
        except Exception as e:
            logger.exception("Error al ejecutar crear_backup: %s", e)

    except Exception as e:
        logger.exception("Error en señal_creacion_actualizacion_unificada: %s", e)

# SEÑAL UNIFICADA: Eliminación
@receiver(post_delete, sender=ProcedimientoRealizado)
@receiver(post_delete, sender=EvaluacionDocente)
@receiver(post_delete, sender=Autoevaluacion)
@receiver(post_delete, sender=Retroalimentacion)
def señal_eliminacion_unificada(sender, instance, **kwargs):
    """Registra eliminación en la bitácora y crea notificación informativa."""
    try:
        usuario = get_usuario_contexto(instance)
        detalle = f"{sender.__name__} (ID {getattr(instance, 'pk', 'N/A')}) eliminado."
        registrar_bitacora(usuario, "ELIMINACIÓN", detalle)

        titulo = f"{sender.__name__} - Eliminado"
        mensaje = f"Se ha eliminado un registro de tipo {sender.__name__} con ID {getattr(instance, 'pk', 'N/A')}."
        crear_notificacion(usuario, titulo, mensaje, tipo='sistema')
    except Exception as e:
        logger.exception("Error en señal_eliminacion_unificada: %s", e)