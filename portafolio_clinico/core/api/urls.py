# core/api/urls.py
from django.urls import path
from core.api.auth_api import LoginAPIView, LogoutAPIView
from core.api.dashboard_api import DashboardDataAPIView
from core.api.estudiantes_api import EstudiantesAPIView
from core.api.profesores_api import ProfesoresAPIView
from core.api.grupos_api import GruposAPIView

from core.api.carga_masiva_api import (   
    CargaEstudiantesAPI,
    CargaProfesoresAPI,
    CargaGruposAPI,
)
from core.api.reportes_api import CurvaDreyfusAPIView

from core.api.reporte_exportacion_api import (
    ExportarReporteExcelAPIView,
    ExportarReportePDFAPIView,  
    ExportarCurvaPDFAPIView,
    ExportarReporteSeguroExcelAPIView,
    ExportarCurvaSeguraPDFAPIView,
)

from core.api.notificaciones_api import NotificacionesUsuarioAPIView
from core.api.backup_api import GenerarBackupAPIView  
from core.api.historico_api import HistoricoEstudianteAPIView  
from core.api.curva_aprendizaje_api import CurvaAprendizajeAPIView
from core.api.user_api import UserProfileAPIView, UpdateLastAccessAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('dashboard/', DashboardDataAPIView.as_view(), name='api_dashboard'),
    path('estudiantes/', EstudiantesAPIView.as_view(), name='api_estudiantes'),
    path('profesores/', ProfesoresAPIView.as_view(), name='api_profesores'),
    path('grupos/', GruposAPIView.as_view(), name='api_grupos'),
    path('notificaciones/', NotificacionesUsuarioAPIView.as_view(), name='api_notificaciones'),  
    
    path('historico/estudiante/<str:cedula>/', HistoricoEstudianteAPIView.as_view(), name='historico_estudiante'),  

    path('api/curva_aprendizaje/<str:cedula>/', CurvaAprendizajeAPIView.as_view(), name='curva_aprendizaje'),
    
    path('user/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user/last-access/', UpdateLastAccessAPIView.as_view(), name='update-last-access'),
    
    # Ruta para generar respaldo
    path('backup/generar/', GenerarBackupAPIView.as_view(), name='api_backup_generar'),
    
     # Nuevas rutas para carga masiva
    path('carga/estudiantes/', CargaEstudiantesAPI.as_view(), name='carga-estudiantes'),  
    path('carga/profesores/', CargaProfesoresAPI.as_view(), name='carga-profesores'),    
    path('carga/grupos/', CargaGruposAPI.as_view(), name='carga-grupos'),

    path('api/curva/<str:cedula_estudiante>/', CurvaDreyfusAPIView.as_view(), name='curva_dreyfus'),

    # EXPORTACIÓN GENERAL
    path('exportar/excel/', ExportarReporteExcelAPIView.as_view(), name='exportar_excel'),
    path('exportar/pdf/', ExportarReportePDFAPIView.as_view(), name='exportar_pdf'), 

    # EXPORTACIÓN DE CURVA Y SEGURIDAD
    path('exportar/curva/<str:cedula_estudiante>/', ExportarCurvaPDFAPIView.as_view(), name='exportar_curva'),
    path('exportar/seguro/excel/', ExportarReporteSeguroExcelAPIView.as_view(), name='exportar_excel_seguro'),
    path('exportar/seguro/curva/<str:cedula_estudiante>/', ExportarCurvaSeguraPDFAPIView.as_view(), name='exportar_curva_segura'),
]
