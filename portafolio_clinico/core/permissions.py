from rest_framework.permissions import BasePermission, SAFE_METHODS

# Función auxiliar para verificar grupo (más robusta frente a usuarios anónimos)
def user_in_group(user, group_name):
    if not user:
        return False
    # user.is_authenticated cubre AnonymousUser
    return getattr(user, "is_authenticated", False) and user.groups.filter(name=group_name).exists()


# Director del Programa
class IsDirector(BasePermission):
    """
    El Director tiene control total sobre todos los módulos del sistema.
    """
    def has_permission(self, request, view):
        # Defensiva: request.user puede ser None en contextos extraños
        return user_in_group(getattr(request, "user", None), 'Director')


# Coordinador de Prácticas e Internado
class IsCoordinadorPractica(BasePermission):
    """
    Puede gestionar lugares de práctica, profesores y procedimientos,
    previa validación del Director.
    """
    def has_permission(self, request, view):
        return user_in_group(getattr(request, "user", None), 'CoordinadorPractica')


# Coordinador de Curso
class IsCoordinadorCurso(BasePermission):
    """
    Puede gestionar profesores, estudiantes y procedimientos de su curso.
    """
    def has_permission(self, request, view):
        return user_in_group(getattr(request, "user", None), 'CoordinadorCurso')


# Profesor
class IsProfesor(BasePermission):
    """
    Puede evaluar a los estudiantes de su curso.
    No puede modificar otros módulos.
    """
    def has_permission(self, request, view):
        return user_in_group(getattr(request, "user", None), 'Profesor')


# Estudiante
class IsEstudiante(BasePermission):
    """
    Puede ver y registrar solo sus propias autoevaluaciones y procedimientos.
    """
    def has_permission(self, request, view):
        return user_in_group(getattr(request, "user", None), 'Estudiante')


# Lectura segura (GET, HEAD, OPTIONS) para usuarios autenticados
class IsReadOnly(BasePermission):
    """
    Permite operaciones de solo lectura a cualquier usuario autenticado.
    """
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return request.method in SAFE_METHODS and getattr(user, "is_authenticated", False)


# Permiso combinado (Útil para vistas accesibles a más de un rol)
class HasAnyRole(BasePermission):
    """
    Permite acceso si el usuario pertenece a uno de los roles listados.
    Uso: permission_classes = [HasAnyRole(['Director', 'CoordinadorCurso'])]
    Esta clase se puede instanciar con la lista de roles deseada.
    """
    def __init__(self, roles):
        # roles debe ser iterable de strings
        if roles is None:
            roles = []
        self.roles = list(roles)

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return False
        # Retornará True si pertenece a cualquiera de los roles
        return any(user_in_group(user, role) for role in self.roles)


# Permiso para verificar solo autenticación 
class IsAuthenticatedUser(BasePermission):
    """Permite acceso solo a usuarios autenticados."""
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        # usar is_authenticated 
        return bool(getattr(user, "is_authenticated", False))
