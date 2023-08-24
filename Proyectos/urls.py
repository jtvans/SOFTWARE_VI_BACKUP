from django.urls import path
from . import views

app_name = 'Proyectos'

urlpatterns = [
    # Proyecto
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/<int:proyecto_id>/', views.opciones_proyecto, name='opciones_proyecto'),
    

    # Productos
    path('proyectos/<int:proyecto_id>/crear_plan_trabajo/', views.crear_plan_trabajo, name='crear_plan_trabajo'),
    path('plan_trabajo_creado/<int:proyecto_id>/', views.plan_trabajo_creado, name='plan_trabajo_creado'),
    path('eliminar_proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),

    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('descargar_pdf/<int:proyecto_id>/', views.descargar_pdf, name='descargar_pdf'),
    path('ver_plan_trabajo/<int:proyecto_id>/', views.ver_plan_trabajo, name='ver_plan_trabajo'),


    # Portafolio
    path('portafolio_actividades/<int:proyecto_id>/', views.portafolio_actividades, name='portafolio_actividades'),

    path('avance_estado_0/<int:proyecto_id>/<int:producto_id>/', views.avance_estado_0, name='avance_estado_0'),
    path('ver_evidencias_0/<int:proyecto_id>/<int:producto_id>/', views.ver_evidencias_0, name='ver_evidencias_0'),


    path('avance_estado_1/<int:proyecto_id>/<int:producto_id>/', views.avance_estado_1, name='avance_estado_1'),
    path('ver_evidencias_1/<int:proyecto_id>/<int:producto_id>/', views.ver_evidencias_1, name='ver_evidencias_1'),
    path('avance_estado_1_editar/<int:proyecto_id>/<int:producto_id>/<int:evidencia_id>/', views.avance_estado_1_editar, name='avance_estado_1_editar'),


    path('avance_estado_2/<int:proyecto_id>/<int:producto_id>/', views.avance_estado_2, name='avance_estado_2'),
    path('ver_evidencias_2/<int:proyecto_id>/<int:producto_id>/', views.ver_evidencias_2, name='ver_evidencias_2'),
    path('avance_estado_2_editar/<int:proyecto_id>/<int:producto_id>/<int:evidencia_id>/', views.avance_estado_2_editar, name='avance_estado_2_editar'),


    path('avance_estado_3/<int:proyecto_id>/<int:producto_id>/', views.avance_estado_3, name='avance_estado_3'),
    path('ver_evidencias_3/<int:proyecto_id>/<int:producto_id>/', views.ver_evidencias_3, name='ver_evidencias_3'),
    path('avance_estado_3_editar/<int:proyecto_id>/<int:producto_id>/<int:evidencia_id>/', views.avance_estado_3_editar, name='avance_estado_3_editar'),


]
