# core/utils/auth_utils.py
from django.contrib.auth.hashers import check_password, make_password
from core.models import Usuario

def autenticar_usuario(usuario_input, contrasena_input):
    """
    Autentica un usuario según su nombre y contraseña.
    Retorna el objeto Usuario si las credenciales son correctas, o None si no.
    """
    try:
        usuario = Usuario.objects.get(usuario=usuario_input, estado=True)
        if check_password(contrasena_input, usuario.contrasenaHash):
            return usuario
        else:
            return None
    except Usuario.DoesNotExist:
        return None

def crear_contrasena_segura(contrasena_plana):
    """
    Genera un hash seguro para almacenar contraseñas.
    """
    return make_password(contrasena_plana)

def cambiar_contrasena(usuario, contrasena_actual, contrasena_nueva):
    """
    Cambia la contraseña de un usuario si la contraseña actual es correcta.
    Retorna True si se cambió correctamente, False si falló la verificación.
    """
    if check_password(contrasena_actual, usuario.contrasenaHash):
        usuario.contrasenaHash = make_password(contrasena_nueva)
        usuario.save()
        return True
    else:
        return False

def resetear_contrasena(usuario, nueva_contrasena):
    """
    Permite resetear la contraseña sin validar la anterior (solo para administradores o coordinadores).
    """
    usuario.contrasenaHash = make_password(nueva_contrasena)
    usuario.save()
    return True

