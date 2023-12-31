from django.urls import path
from . import views

app_name = 'Semilleros'

urlpatterns = [
    # DOCENTE
    path('crear/', views.crear_semillero, name='crear_semillero'),
    path('semilleros/', views.lista_semilleros, name='lista_semilleros'),
    path('semilleros/<int:semillero_id>/', views.opciones_semillero, name='opciones_semillero'),
    path('<int:semillero_id>/', views.detalle_semillero, name='detalle_semillero'),
    path('ver_perfil_solicitante/<int:semillero_id>/<int:estudiante_id>/', views.ver_perfil_solicitante, name='ver_perfil_solicitante'),
    path('generar_aval/<int:semillero_id>/<int:estudiante_id>/', views.generar_aval, name='generar_aval'),
    path('actividades/', views.ver_actividades_semillero, name='ver_actividades_semillero'),
    path('detalle-actividad/<int:actividad_id>/', views.ver_detalle_actividad_semillero, name='ver_detalle_actividad_semillero'),


    # ESTUDIANTE
    path('ver-semilleros/', views.ver_semilleros_estudiante, name='ver_semilleros_estudiante'),
    path('detalle-semillero/<int:semillero_id>/', views.detalle_semillero_estudiante, name='detalle_semillero_estudiante'),
    path('inscribirse-semillero/<int:semillero_id>/', views.formulario_inscripcion_semillero, name='formulario_inscripcion_semillero'),
    path('mis-semilleros/', views.ver_mis_semilleros, name='ver_mis_semilleros'),

    # ADMIN
    path('ver-semilleros-admin/', views.ver_semilleros_admin, name='ver_semilleros_admin'),
    path('detalle-semillero-admin/<int:semillero_id>/', views.detalle_semillero_admin, name='detalle_semillero_admin'),
    path('aprobar-semillero/<int:semillero_id>/', views.aprobar_semillero, name='aprobar_semillero'),
    path('generar_aval_admin_semi/<int:semillero_id>/<int:estudiante_id>/', views.generar_aval_admin_semi, name='generar_aval_admin_semi'),
    path('informes_semi/', views.informes_semi, name='informes_semi'),
    path('informes_facultad/', views.informes_facultad, name='informes_facultad'),
    
]