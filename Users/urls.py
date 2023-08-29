from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    # Usuario -----------------------------------------------------------------------------------
    path('Users_home', views.Users_home, name='Users_home'),
    path('Users_consultar_identificacion/', views.Users_consultar_identificacion, name='Users_consultar_identificacion'),
    path('Users_registro_usuario/<str:nombre>/<str:identificacion>/<str:correo>/', views.Users_registro_usuario, name='Users_registro_usuario'),
    path('Users_registro_exitoso/', views.Users_registro_exitoso, name='Users_registro_exitoso'),
    path('Users_login/', views.Users_login, name='Users_login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.Users_ver_perfil, name='Users_ver_perfil'),
    path('perfil/editar/', views.Users_editar_perfil, name='Users_editar_perfil'),
    path('Users_ver_grupos', views.Users_ver_grupos, name='Users_ver_grupos'),
    path('Users_editar_grupos_investigacion', views.Users_editar_grupos_investigacion, name='Users_editar_grupos_investigacion'),
    path('eliminar_grupo_investigacion/', views.eliminar_grupo_investigacion, name='eliminar_grupo_investigacion'),
    path('eliminar_grupo_investigacion_2/', views.eliminar_grupo_investigacion_2, name='eliminar_grupo_investigacion_2'),
    path('eliminar_grupo_investigacion_3/', views.eliminar_grupo_investigacion_3, name='eliminar_grupo_investigacion_3'),

    # Administrador -----------------------------------------------------------------------------------
    path('Admin_home', views.Admin_home, name='Admin_home'),
    path('Admin_registro_usuario/', views.Admin_registro_usuario, name='Admin_registro_usuario'),
    path('Admin_registro_exitoso/', views.Admin_registro_exitoso, name='Admin_registro_exitoso'),
    path('Admin_login/', views.Admin_login_view, name='Admin_login'),
    path('Admin_logout/', views.Admin_cerrar_sesion, name='Admin_logout'),

    #Acciones Administrador
    path('Admin_lista_usuarios/', views.Admin_lista_usuarios, name='Admin_lista_usuarios'),
    path('Admin_ver_usuario/<int:usuario_id>/', views.Admin_ver_usuario, name='Admin_ver_usuario'),
    path('Admin_menu_opciones/<int:usuario_id>/<int:proyecto_id>/', views.Admin_menu_opciones, name='Admin_menu_opciones'),
    path('Admin_ver_productos/<int:usuario_id>/<int:proyecto_id>/', views.Admin_ver_productos, name='Admin_ver_productos'),
    path('Admin_ver_portafolio/<int:usuario_id>/<int:proyecto_id>/', views.Admin_ver_portafolio, name='Admin_ver_portafolio'),
    path('aceptar_estado/<int:portafolio_id>/<int:avance_numero>/', views.aceptar_estado, name='aceptar_estado'),
    path('eliminar_estado/<int:portafolio_id>/<int:avance_numero>/', views.eliminar_estado, name='eliminar_estado'),
    path('enviar_correcciones/<int:portafolio_id>/<int:avance_numero>/', views.enviar_correcciones, name='enviar_correcciones'),
    path('Admin_porcentaje_cumplimiento/<int:usuario_id>/<int:proyecto_id>/', views.Admin_porcentaje_cumplimiento, name='Admin_porcentaje_cumplimiento'),
    path('Admin_porcentaje_general/', views.Admin_porcentaje_general, name='Admin_porcentaje_general'),
    path('Admin_aprobar_proyecto/<int:proyecto_id>/<int:usuario_id>/', views.Admin_aprobar_proyecto, name='Admin_aprobar_proyecto'),

    # Usuario -----------------------------------------------------------------------------------
    path('Users_E_consultar_identificacion/', views.Users_E_consultar_identificacion, name='Users_E_consultar_identificacion'),
    path('Users_E_registro_usuario/<str:nombre>/<str:identificacion>/<str:correo>/<str:programa>/<str:telefono>/', views.Users_E_registro_usuario, name='Users_E_registro_usuario'),
    path('Users_E_registro_exitoso/', views.Users_E_registro_exitoso, name='Users_E_registro_exitoso'),
    path('Users_E_login/', views.Users_E_login, name='Users_E_login'),
    path('Users_E_home', views.Users_E_home, name='Users_E_home'),
    path('Users_E_cerrar_sesion/', views.Users_E_cerrar_sesion, name='Users_E_cerrar_sesion'),
]
