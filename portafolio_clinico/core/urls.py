# core/urls.py
from django.urls import path, include
from core import views  
from core.views.autoevaluaciones_views import AutoevaluacionViewSet
from core.views.evaluaciondocente_views import EvaluacionDocenteViewSet
from rest_framework.routers import DefaultRouter
from core.views.procedimientorealizado_views import ProcedimientoRealizadoViewSet

router = DefaultRouter()
router.register(r'autoevaluaciones', AutoevaluacionViewSet, basename='autoevaluaciones')
router.register(r'evaluaciones-docentes', EvaluacionDocenteViewSet, basename='evaluaciones_docentes')
router.register(r'procedimientos-realizados', ProcedimientoRealizadoViewSet, basename='procedimientorealizado')

urlpatterns = [
    path('', include(router.urls)),          # Endpoints de autoevaluaciones y evaluaciones docentes
    path('', include('core.api.urls')),  # Endpoints adicionales (grupos, login, etc.)
]

