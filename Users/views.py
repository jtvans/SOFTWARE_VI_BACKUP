# Modelos
from .models import Usuario, Usuario_Administrador, Usuario_Estudiante, Usuario_Adminin_Semi, LineaInvestigacion, LineaInvestigacion_2, LineaInvestigacion_3
from Proyectos.models import Proyecto, Producto, Portafolio
from Semilleros.models import Semillero, InscripcionSemillero, ActividadesSemillero

#Componentes 1
import requests
from datetime import date
from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, JsonResponse

# Componentes 2
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, FloatField, Sum


import json
from django.template.loader import render_to_string
import pdfkit
#----------------- // ----------------- // ----------------- // ----------------- PAGINA PRINCIPAL ----------------- \\ ----------------- \\ ----------------- \\ -----------------

# PAGINA PRINCIPAL
def Pagina_Principal(request):
    return render(request, 'Pagina_Principal.html')


def Pagina_Principal_About(request):
    return render(request, 'Pagina_Principal_About.html')


def Pagina_Principal_Contact(request):
    return render(request, 'Pagina_Principal_Contact.html')


def Pagina_Principal_Portafolio(request):
    return render(request, 'Pagina_Principal_Portfolio.html')


def Pagina_Principal_Service(request):
    return render(request, 'Pagina_Principal_Service.html')




#----------------- // ----------------- USUARIO DOCENTE  ----------------- \\ -----------------


# CONSULTAR PERFIL Y EXTRAER DATOS
def Users_consultar_identificacion(request):
    if request.method == 'POST':

        identificacion = request.POST.get('identificacion')

        # Si existe en BD
        if Usuario.objects.filter(identificacion=identificacion).exists():
            message = "Ya cuentas con un usuario registrado. Inicia sesión."
            query_params = QueryDict(mutable=True)
            query_params['message'] = message
            return HttpResponseRedirect(f"/users/Users_login/?{query_params.urlencode()}")
        else:
            # Api_Perfil
            api_perfil = f'http://190.60.75.134/searches/consultar_perfil.json?periodos={identificacion}'
            response_perfil = requests.get(api_perfil)

            if response_perfil.status_code == 200:
                data_pefil = response_perfil.json()

                if (data_pefil) and (data_pefil[0][3] == 'Docente' or data_pefil[0][3] == 'DOCENTE'):
                    nombre = data_pefil[0][0]
                    identificacion = data_pefil[0][1]

                    # Api_Datos_Estudiantes
                    api_datos = f'http://190.60.75.134/searches/votaciones_docentes_cdirectivo.json?periodos={identificacion}'
                    response_datos = requests.get(api_datos)
                    if response_datos.status_code == 200:
                        data_datos = response_datos.json()
                        correo = data_datos[0][8]

                        # Redirigir a la vista de registro de usuario con datos precargados
                        return redirect('Users:Users_registro_usuario', nombre=nombre, identificacion=identificacion, correo=correo)
                    
    return render(request, 'Docentes/Users_consultar_identificacion.html')


# CREAR USUARIO
def Users_registro_usuario(request, nombre, identificacion, correo):
    if request.method == 'POST':
        clave = request.POST.get('clave')
        confirmar_clave = request.POST.get('confirmar_clave')

        # Coincidir Contraseñas
        if clave == confirmar_clave:
            # Crear un nuevo usuario utilizando el modelo User de Django
            user = User.objects.create_user(username=identificacion.lower(), password=clave)
            
            # Guardar los otros datos en el perfil del usuario
            usuario = Usuario(user=user, nombre=nombre, identificacion=identificacion, correo=correo.lower(), clave=clave)
            usuario.save()
            
            # Iniciar sesión después del registro
            user = authenticate(username=identificacion.lower(), password=clave)
            if user is not None:
                login(request, user)
                return redirect('Users:Users_registro_exitoso')
            else:
                return HttpResponse('Error al iniciar sesión')

        else:
            error_message = "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            return render(request, 'Docentes/Users_registro_usuario.html', {'nombre': nombre, 'identificacion': identificacion, 'error_message': error_message})

    return render(request, 'Docentes/Users_registro_usuario.html', {'nombre': nombre, 'identificacion': identificacion})


# USUARIO CREADO
def Users_registro_exitoso(request):
    return render(request, 'Docentes/Users_registro_exitoso.html')



# PAGINA HOME
@login_required
def Users_home(request):
    usuario = request.user.usuario

    proyectos = Proyecto.objects.filter(usuario=request.user)
    semilleristas = InscripcionSemillero.objects.filter(semillero__usuario=request.user, estado_e=True)
    postulantes = InscripcionSemillero.objects.filter(semillero__usuario=request.user, estado_e=False)

    correcciones = Portafolio.objects.filter(proyecto__usuario=request.user)
    notificacion_correcciones = False
    for correccion in correcciones:
        if (
            (correccion.avance_1_observacion and not correccion.avance_1_correcciones_realizadas) or
            (correccion.avance_2_observacion and not correccion.avance_2_correcciones_realizadas) or
            (correccion.avance_3_observacion and not correccion.avance_3_correcciones_realizadas)
        ):
            notificacion_correcciones = True
            break


    cant_proyectos = proyectos.count()
    cant_productos = Producto.objects.filter(proyecto__in=proyectos).count()

    cant_evidencias = Portafolio.objects.filter(
        proyecto__usuario=request.user
    ).exclude(
        Q(avance_1_nombre='') & Q(avance_2_descripcion='') & Q(avance_3_descripcion='')
    ).count()

    cant_productos_completados = Portafolio.objects.filter(
        proyecto__usuario=request.user,
        avance_3_estado="Aceptado"
    ).count()

    cant_semilleros_aprobados = Semillero.objects.filter(usuario=request.user, aprobacion=True).count()
    cant_estudiantes_aprobados = InscripcionSemillero.objects.filter(semillero__usuario=request.user, estado_e=True).count()
    cant_estudiantes_inscritos = InscripcionSemillero.objects.filter(semillero__usuario=request.user).count()
    cant_actividades_semillero = ActividadesSemillero.objects.filter(semillero__usuario=request.user).count()

    acti_semilleros = ActividadesSemillero.objects.filter(semillero__usuario=request.user)

    notificacion_semillero = False
    for act_sem in acti_semilleros:
        if act_sem.nombre_actividad_e:
            notificacion_semillero = True
            break


    context = {
        'usuario': usuario,
        'proyectos': proyectos,
        'semilleristas': semilleristas,
        'postulantes': postulantes,
        'acti_semilleros': acti_semilleros,
        'correcciones': correcciones,

        'notificacion_correcciones': notificacion_correcciones,
        'notificacion_semillero': notificacion_semillero,
        'cant_proyectos': cant_proyectos,
        'cant_productos': cant_productos,
        'cant_evidencias': cant_evidencias,
        'cant_productos_completados': cant_productos_completados,
        'cant_semilleros_aprobados': cant_semilleros_aprobados,
        'cant_estudiantes_inscritos': cant_estudiantes_inscritos,
        'cant_estudiantes_aprobados': cant_estudiantes_aprobados,
        'cant_actividades_semillero': cant_actividades_semillero,
    }
    return render(request, 'Docentes/Users_home.html', context)




# LOGIN - INICIAR SESION
def Users_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Users:Users_home')
        else:
            error_message = "Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo."
            return render(request, 'Docentes/Users_login.html', {'error_message': error_message})
    else:
        message = request.GET.get('message')
        return render(request, 'Docentes/Users_login.html', {'message': message, 'error_message': None})
    
    
# LOGIN - CERRAR SESION
@login_required
def cerrar_sesion (request):
    logout(request)
    return render(request, 'Docentes/Users_login.html')
  

# VER PERFIL
@login_required
def Users_ver_perfil(request):
    usuario = request.user.usuario
    facultad = usuario.facultad

    grupo_imagenes = {
        "Aglalia": "images_groups/G1.png",
        "ProCont": "images_groups/G2.png",
        "DehJüs": "images_groups/G3.png",
        "TES": "images_groups/G4.png",
        "GECAES": "images_groups/G5.png",
        "Gestion e Innovacion": "images_groups/G6.png",
        "IC": "images_groups/G7.png",
        "LyS": "images_groups/G8.png",
        "Gisela": "images_groups/G9.png",
        "LAW": "images_groups/G10.png",
        "Business Intelligence": "images_groups/G11.png",
        "Americana Emprendedora": "images_groups/G12.png",
        "PSI Context": "images_groups/G13.png",
        "Engineeri": "images_groups/G14.png",
        "SeHaT": "images_groups/G15.png",
    }
    if usuario.grupo_investigacion in grupo_imagenes:
        imagen_grupo_1 = grupo_imagenes[usuario.grupo_investigacion]
    else:
        imagen_grupo_1 = None

    if usuario.grupo_investigacion_2 in grupo_imagenes:
        imagen_grupo_2 = grupo_imagenes[usuario.grupo_investigacion_2]
    else:
        imagen_grupo_2 = None

    if usuario.grupo_investigacion_3 in grupo_imagenes:
        imagen_grupo_3 = grupo_imagenes[usuario.grupo_investigacion_3]
    else:
        imagen_grupo_3 = None

    if facultad == 'Ciencias_Admin':
        facultad_personalizada = 'CIENCIAS ADMINISTRATIVAS, ECONOMICAS Y CONTABLES'
    elif facultad == 'Humanidades':
        facultad_personalizada = 'HUMANIDADES Y CIENCIAS SOCIALES'
    elif facultad == 'Ingenieria':
        facultad_personalizada = 'INGENIERIA'
    elif facultad == 'Educacion':
        facultad_personalizada = 'EDUCACION'
    else:
        facultad_personalizada = facultad

    context = {
        'usuario': usuario,
        'facultad_personalizada': facultad_personalizada,
        'imagen_grupo_1': imagen_grupo_1,
        'imagen_grupo_2': imagen_grupo_2,
        'imagen_grupo_3': imagen_grupo_3,
    }
    return render(request, 'Docentes/Users_ver_perfil.html', context)


# EDITAR PERFIL
@login_required
def Users_editar_perfil(request):
    usuario = request.user.usuario
    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        
        facultad = request.POST.get('facultad')
        Programa = request.POST.get('Programa')

        cvlac = request.POST.get('cvlac')
        orcid = request.POST.get('orcid')
        google_scholar = request.POST.get('google_scholar')
        categoria = request.POST.get('categoria')

        usuario.telefono = telefono
        usuario.facultad = facultad
        usuario.Programa = Programa
        usuario.cvlac = cvlac
        usuario.orcid = orcid
        usuario.google_scholar = google_scholar
        usuario.categoria = categoria

        usuario.save()
        return redirect('Users:Users_ver_perfil')
    return render(request, 'Docentes/Users_editar_perfil.html', {'usuario': usuario})


# VER GRUPOS INVESTIGACION 
@login_required
def Users_ver_grupos(request):
    usuario = request.user.usuario

    grupo_imagenes = {
        "Aglalia": "images_groups/G1.png",
        "ProCont": "images_groups/G2.png",
        "DehJüs": "images_groups/G3.png",
        "TES": "images_groups/G4.png",
        "GECAES": "images_groups/G5.png",
        "Gestion e Innovacion": "images_groups/G6.png",
        "IC": "images_groups/G7.png",
        "LyS": "images_groups/G8.png",
        "Gisela": "images_groups/G9.png",
        "LAW": "images_groups/G10.png",
        "Business Intelligence": "images_groups/G11.png",
        "Americana Emprendedora": "images_groups/G12.png",
        "PSI Context": "images_groups/G13.png",
        "Engineeri": "images_groups/G14.png",
        "SeHaT": "images_groups/G15.png",
    }

    if usuario.grupo_investigacion in grupo_imagenes:
        imagen_grupo_1 = grupo_imagenes[usuario.grupo_investigacion]
    else:
        imagen_grupo_1 = None

    if usuario.grupo_investigacion_2 in grupo_imagenes:
        imagen_grupo_2 = grupo_imagenes[usuario.grupo_investigacion_2]
    else:
        imagen_grupo_2 = None

    if usuario.grupo_investigacion_3 in grupo_imagenes:
        imagen_grupo_3 = grupo_imagenes[usuario.grupo_investigacion_3]
    else:
        imagen_grupo_3 = None

    context = {
        'usuario': usuario,
        'imagen_grupo_1': imagen_grupo_1,
        'imagen_grupo_2': imagen_grupo_2,
        'imagen_grupo_3': imagen_grupo_3,
    }

    return render(request, 'Docentes/Users_ver_grupos.html', context)


# EDITAR/AGREGAR GRUPOS INVESTIGACION 
@login_required
def Users_editar_grupos_investigacion(request):
    usuario = request.user.usuario
    if request.method == 'POST':

        grupo_investigacion = request.POST.get('grupo_investigacion')
        lineas_investigacion = request.POST.getlist('linea_investigacion')

        grupo_investigacion_2 = request.POST.get('grupo_investigacion_2')
        lineas_investigacion_2 = request.POST.getlist('linea_investigacion_2')

        grupo_investigacion_3 = request.POST.get('grupo_investigacion_3')
        lineas_investigacion_3 = request.POST.getlist('linea_investigacion_3')

        usuario.grupo_investigacion = grupo_investigacion
        usuario.grupo_investigacion_2 = grupo_investigacion_2
        usuario.grupo_investigacion_3 = grupo_investigacion_3

        usuario.lineas_investigacion.clear()
        usuario.lineas_investigacion_2.clear()
        usuario.lineas_investigacion_3.clear()

        # Eliminar todas las líneas de investigación existentes
        for linea in lineas_investigacion:
            linea_obj, created = LineaInvestigacion.objects.get_or_create(nombre=linea)
            usuario.lineas_investigacion.add(linea_obj)

        # 
        for linea in lineas_investigacion_2:
            linea_obj, created = LineaInvestigacion_2.objects.get_or_create(nombre=linea)
            usuario.lineas_investigacion_2.add(linea_obj)

        # 
        for linea in lineas_investigacion_3:
            linea_obj, created = LineaInvestigacion_3.objects.get_or_create(nombre=linea)
            usuario.lineas_investigacion_3.add(linea_obj)
        
        usuario.save()
        return redirect('Users:Users_ver_grupos')
    return render(request, 'Docentes/Users_editar_grupos_investigacion.html', {'usuario': usuario})


# EDITAR PERFIL - Grupo Investigacion 1
@login_required
def eliminar_grupo_investigacion(request):
    usuario = request.user.usuario

    if usuario.grupo_investigacion:
        lineas_investigacion = usuario.lineas_investigacion.all()
        usuario.grupo_investigacion = None
        usuario.save()
        usuario.lineas_investigacion.remove(*lineas_investigacion)

    return redirect('Users:Users_editar_grupos_investigacion')


# EDITAR PERFIL - Grupo Investigacion 2
@login_required
def eliminar_grupo_investigacion_2(request):
    usuario = request.user.usuario

    if usuario.grupo_investigacion_2:
        lineas_investigacion_2 = usuario.lineas_investigacion_2.all()
        usuario.grupo_investigacion_2 = None
        usuario.save()
        usuario.lineas_investigacion_2.remove(*lineas_investigacion_2)

    return redirect('Users:Users_editar_grupos_investigacion')


# EDITAR PERFIL - Grupo Investigacion 3
@login_required
def eliminar_grupo_investigacion_3(request):
    usuario = request.user.usuario
    if usuario.grupo_investigacion_3:
        lineas_investigacion_3 = usuario.lineas_investigacion_3.all()
        usuario.grupo_investigacion_3 = None
        usuario.save()
        usuario.lineas_investigacion_3.remove(*lineas_investigacion_3)

    return redirect('Users:Users_editar_grupos_investigacion')


#----------------- // ----------------- USUARIO ADMINISTRADOR ----------------- \\ -----------------

# PAGINA HOME
@login_required
def Admin_home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        print(messages)
        return redirect('Pagina_Principal')
    
    return render(request, 'Vicerrectoria_Admin/Admin_Home.html')


# ADMINISTRADOR - CREAR USUARIO 
CONTRASENA_ADMIN = "1450064"
def Admin_registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        identificacion = request.POST.get('identificacion')
        correo = request.POST.get('correo')
        clave = request.POST.get('clave')
        confirmar_clave = request.POST.get('confirmar_clave')

        if Usuario_Administrador.objects.filter(identificacion=identificacion).exists():
            message = "Ya cuentas con un usuario registrado. Inicia sesión."
            query_params = QueryDict(mutable=True)
            query_params['message'] = message
            return HttpResponseRedirect(f"/users/Admin_login/?{query_params.urlencode()}")
        

        if clave == confirmar_clave and clave == CONTRASENA_ADMIN:
            user_admin = User.objects.create_user(username=identificacion.lower(), password=clave)

            usuario_administrador = Usuario_Administrador(user_admin=user_admin, nombre=nombre, identificacion=identificacion, correo=correo.lower(), clave=clave)
            usuario_administrador.save()

            # Iniciar sesión después del registro
            user_admin = authenticate(username=identificacion.lower(), password=clave)
            if user_admin is not None:
                login(request, user_admin)
                return redirect('Users:Admin_registro_exitoso')
            else:
                return HttpResponse('Error al iniciar sesión')
        else:
            error_message = "Contraseña incorrecta o las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            return render(request, 'Vicerrectoria_Admin/Admin_registro_usuario.html', {'error_message': error_message})
    
    return render(request, 'Vicerrectoria_Admin/Admin_registro_usuario.html')


# ADMINISTRADOR - USUARIO CREADO
def Admin_registro_exitoso(request):
    return render(request, 'Vicerrectoria_Admin/Admin_registro_exitoso.html')


# ADMINISTRADOR - LOGIN - INICIAR SESION
def Admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_admin = authenticate(request, username=username, password=password)
        if user_admin is not None:
            login(request, user_admin)
            return redirect('Users:Admin_home')  # Redirige a la página principal del administrador
        else:
            error_message = "Credenciales Administrador Incorrectas, inténtalo de nuevo."
            return render(request, 'Vicerrectoria_Admin/Admin_login.html', {'error_message': error_message})

    return render(request, 'Vicerrectoria_Admin/Admin_login.html')


# ADMINISTRADOR - LOGIN - CERRAR SESION
@login_required
def Admin_cerrar_sesion (request):
    logout(request)
    return render(request, 'Vicerrectoria_Admin/Admin_Pagina_Principal.html')


#------------------------------------------------------------------------------------------------------

# VER LOS USUARIOS.
@login_required
def Admin_lista_usuarios(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        print([message.message for message in messages.get_messages(request)])
        return redirect('Pagina_Principal')
    
    usuarios = Usuario.objects.all()
    return render(request, 'Vicerrectoria_Admin/Admin_lista_usuarios.html', {'usuarios': usuarios})


# VER INFO DE USUARIO.
@login_required
def Admin_ver_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    proyectos = Proyecto.objects.filter(usuario=usuario.user)
    return render(request, 'Vicerrectoria_Admin/Admin_ver_usuario.html', {'usuario': usuario, 'proyectos': proyectos})


# OPCIONES DEL PROYECTO PROYECTO DE USUARIO
@login_required
def Admin_menu_opciones(request, proyecto_id, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    return render(request, 'Vicerrectoria_Admin/Admin_menu_opciones.html', {'usuario': usuario, 'proyecto': proyecto})


# APROBAR PROYECTO
@login_required
def Admin_aprobar_proyecto(request, proyecto_id, usuario_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        proyecto.aprobado = True
        aprobado_nombre = request.user.usuario_administrador.nombre
        print("Nombre del usuario administrador:", aprobado_nombre)  # Agregar mensaje de depuración
        proyecto.aprobado_nombre = aprobado_nombre
        proyecto.aprobado_fecha = date.today()
        proyecto.aprobado_adjunto = request.FILES.get('aprobado_adjunto')
        proyecto.save()
        messages.success(request, 'Proyecto aprobado exitosamente.')
        return redirect('Users:Admin_menu_opciones', proyecto_id=proyecto_id, usuario_id=usuario_id)
    return render(request, 'Vicerrectoria_Admin/Admin_aprobar_proyecto.html', {'proyecto': proyecto, 'usuario': usuario})


# PRODUCTOS DEL PROYECTO DE USUARIO
@login_required
def Admin_ver_productos(request, proyecto_id, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    productos = Producto.objects.filter(proyecto=proyecto)
    context = {
        'proyecto': proyecto,
        'productos': productos,
        'usuario': usuario,
    }
    return render(request, 'Vicerrectoria_Admin/Admin_ver_productos.html', context)


# PORTAFOLIO DEL PROYECTO DE USUARIO
@login_required
def Admin_ver_portafolio(request, proyecto_id, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    portafolios = Portafolio.objects.filter(proyecto=proyecto)
    productos = Producto.objects.filter(proyecto=proyecto)
    
    context = {
        'proyecto': proyecto,
        'productos': productos,
        'portafolios': portafolios,
        'usuario': usuario,
    }
    return render(request, 'Vicerrectoria_Admin/Admin_ver_portafolio.html', context)


# ACEPTAR EVIDENCIA.
@login_required
def aceptar_estado(request, portafolio_id, avance_numero):
    portafolio = get_object_or_404(Portafolio, id=portafolio_id)
    proyecto = portafolio.proyecto
    usuario = proyecto.usuario  
    productos = Producto.objects.filter(proyecto=proyecto)
    portafolios = Portafolio.objects.filter(proyecto=proyecto)

    if str(avance_numero) == '1':
        portafolio.avance_1_estado = 'Aceptado'
        portafolio.avance_1_observacion = ""
        messages.success(request, "La evidencia fue aceptada exitosamente.")

    elif str(avance_numero) == '2':
        portafolio.avance_2_estado = 'Aceptado'
        portafolio.avance_2_observacion = ""
        messages.success(request, "La evidencia fue aceptada exitosamente.")
        
    elif str(avance_numero) == '3':
        portafolio.avance_3_estado = 'Aceptado'
        portafolio.avance_3_observacion = ""
        messages.success(request, "La evidencia fue aceptada exitosamente.")
        
    portafolio.save()

    context = {
        'tipo_mensaje': 'aceptar',
        'proyecto': proyecto,
        'productos': productos,
        'portafolios': portafolios,
        'usuario': usuario,
    }

    return render(request, 'Vicerrectoria_Admin/Admin_ver_portafolio.html', context)


# ENVIAR CORRECIONES OBSERVACIONES
@login_required
def enviar_correcciones(request, portafolio_id, avance_numero):
    if request.method == 'POST':
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        corrections_message = request.POST.get('corrections_message')
        
        if str(avance_numero) == '1':
            portafolio.avance_1_observacion = corrections_message
            portafolio.avance_1_estado = 'Correcciones Requeridas'

        if str(avance_numero) == '2':
            portafolio.avance_2_observacion = corrections_message
            portafolio.avance_2_estado = 'Correcciones Requeridas'

        if str(avance_numero) == '3':
            portafolio.avance_3_observacion = corrections_message
            portafolio.avance_3_estado = 'Correcciones Requeridas'

        portafolio.save()
        
    return redirect('Users:Admin_ver_portafolio', proyecto_id=portafolio.proyecto.id, usuario_id=portafolio.proyecto.usuario.id)


# ELIMINAR (ESTADO) EVIDENCIA.
@login_required
def eliminar_estado(request, portafolio_id, avance_numero):
    portafolio = get_object_or_404(Portafolio, id=portafolio_id)
    proyecto = portafolio.proyecto
    usuario = proyecto.usuario  
    productos = Producto.objects.filter(proyecto=proyecto)
    portafolios = Portafolio.objects.filter(proyecto=proyecto)

    if str(avance_numero) == '1':
        portafolio.avance_1_estado = 'No Revisado'
        portafolio.avance_1_observacion = ""
        messages.warning(request, "Se eliminó la revisión de la Evidencia 1")

    elif str(avance_numero) == '2':
        portafolio.avance_2_estado = 'No Revisado'
        portafolio.avance_2_observacion = ""
        messages.warning(request, "Se eliminó la revisión de la Evidencia 2")
        
    elif str(avance_numero) == '3':
        portafolio.avance_3_estado = 'No Revisado'
        portafolio.avance_3_observacion = ""
        messages.warning(request, "Se eliminó la revisión de la Evidencia 3")
        
    portafolio.save()

    context = {
        'tipo_mensaje': 'eliminar',
        'proyecto': proyecto,
        'productos': productos,
        'portafolios': portafolios,
        'usuario': usuario,
    }

    return render(request, 'Vicerrectoria_Admin/Admin_ver_portafolio.html', context)


# PORCENTAJE DE CUMPLIMIENTO - DOCENTE
@login_required
def Admin_porcentaje_cumplimiento(request, usuario_id, proyecto_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    productos = Producto.objects.filter(proyecto=proyecto)
    portafolios = Portafolio.objects.filter(proyecto=proyecto)

    total_productos = len(productos)
    pesos_productos = 1 / total_productos if total_productos > 0 else 0
    print("Peso Productos: ", pesos_productos)
    avances_por_producto = {}  # Diccionario para almacenar los avances por producto

    for portafolio in portafolios:
        producto_id = portafolio.producto_id
        if producto_id not in avances_por_producto:
            avances_por_producto[producto_id] = []
        avances_por_producto[producto_id].append(portafolio)

    tabla_avances = []

    productos_completados_total = 0
    porcentaje_cumplimiento = 0


    for producto in productos:
        producto_id = producto.id
        avances = avances_por_producto.get(producto_id, [])

        productos_completados = 0
        for avance in avances:
            if avance.avance_3_estado == "Aceptado":
                productos_completados += pesos_productos

        porcentaje_cumplimiento = round(productos_completados * 100, 2)
        productos_completados_total += productos_completados

        tabla_avances.append({
            'producto': producto,
            'avances': avances,
            'porcentaje_cumplimiento': porcentaje_cumplimiento
        })

    print("Productos Completados Total:", productos_completados_total)
    print("Total Productos:", total_productos)

    porcentaje_cumplimiento_total = round(productos_completados_total * 100, 2)

    # Guardar el porcentaje de cumplimiento total en el proyecto
    proyecto.porcentaje_cumplimiento_total = porcentaje_cumplimiento_total
    proyecto.save()

    peso_formulario = round(porcentaje_cumplimiento / 100, 3)
    print("Peso Formulario: ", pesos_productos)

    print("Porcentaje Cumplimiento Total:", porcentaje_cumplimiento_total)

    return render(request, 'Vicerrectoria_Admin/Admin_porcentaje_cumplimiento.html', {
        'usuario': usuario,
        'proyecto': proyecto,
        'tabla_avances': tabla_avances,
        'porcentaje_cumplimiento_total': porcentaje_cumplimiento_total,
        'peso_formulario': peso_formulario,
        'pesos_productos': pesos_productos
    })


# PORCENTAJE DE CUMPLIMIENTO GENERAL
@login_required
def Admin_porcentaje_general(request):
    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()
    portafolios = Portafolio.objects.all()
    
    porcentaje_general_malo = 0
    porcentaje_general_medio = 0
    porcentaje_general_aceptable = 0
    porcentaje_general_bueno = 0

    porcentaje_cumplimiento_total = sum(proyecto.porcentaje_cumplimiento_total for proyecto in proyectos)
    cantidad_proyectos = proyectos.count()

    if cantidad_proyectos > 0:
        porcentaje_general = porcentaje_cumplimiento_total / cantidad_proyectos
    else:
        porcentaje_general = 0

    print("porcentaje_cumplimiento_total", porcentaje_cumplimiento_total)
    print("porcentaje_general", porcentaje_general)

    if porcentaje_general >= 0 and porcentaje_general <= 25.99:
        porcentaje_general_malo = porcentaje_general
    elif porcentaje_general >= 26 and porcentaje_general <= 50.99:
        porcentaje_general_medio = porcentaje_general
    elif porcentaje_general >= 51 and porcentaje_general <= 75.99:
        porcentaje_general_aceptable = porcentaje_general
    elif porcentaje_general >= 76 and porcentaje_general <= 100:
        porcentaje_general_bueno = porcentaje_general
    
    if request.method == 'POST':
        for usuario in usuarios:
            # Obtener los datos del formulario
            usuario_id = usuario.id
            proyecto_id = request.POST.get(f'proyecto_id_{usuario_id}')

            # Llamar a la función para actualizar el porcentaje de cumplimiento del usuario
            Admin_porcentaje_cumplimiento(request, usuario_id, proyecto_id)

    
    return render(request, 'Vicerrectoria_Admin/Admin_porcentaje_general.html', {'porcentaje_general': porcentaje_general,'usuarios': usuarios, 'proyectos': proyectos, 'porcentaje_general_malo': porcentaje_general_malo, 'porcentaje_general_medio': porcentaje_general_medio, 'porcentaje_general_aceptable': porcentaje_general_aceptable, 'porcentaje_general_bueno': porcentaje_general_bueno})


#----------------- //  INFORMES  \\ -----------------
@login_required
def Admin_informes(request):
     return render(request, 'Vicerrectoria_Admin/Admin_informes.html')

@login_required
def Admin_informe_facultad_programa(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        facultad_seleccionada = request.GET.get('facultad')
        programa_seleccionado = request.GET.get('programa')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        identificacion = request.GET.get('identificacion')

        usuarios = User.objects.filter(usuario__facultad=facultad_seleccionada)

        # Filtrar por Programa
        if programa_seleccionado:
            usuarios = usuarios.filter(usuario__Programa=programa_seleccionado)

        # Filtrar por Fecha
        if fecha_inicio and fecha_fin:
            proyectos = Proyecto.objects.filter(
                usuario__in=usuarios,
                fecha_inscripcion__range=[fecha_inicio, fecha_fin]
            )
        else:
            proyectos = Proyecto.objects.filter(usuario__in=usuarios)

        # Filtrar por Identificacion
        if identificacion:
            usuarios = usuarios.filter(usuario__identificacion=identificacion)

        data = []
        for usuario in usuarios:
            usuario_info = {'nombre': usuario.usuario.nombre, 'identificacion': usuario.usuario.identificacion}

            proyectos_usuario = proyectos.filter(usuario=usuario)
            proyectos_info = []

            for proyecto in proyectos_usuario:
                proyecto_info = {'titulo': proyecto.titulo}
                productos_proyecto = Producto.objects.filter(proyecto=proyecto)

                categorias = set()
                tipos = set()
                for producto in productos_proyecto:
                    categorias.add(producto.categoria)
                    tipos.add(producto.tipo_producto)

                proyecto_info['categorias'] = list(categorias)
                proyecto_info['tipos'] = list(tipos)

                proyectos_info.append(proyecto_info)

            data.append({'usuario': usuario_info, 'proyectos': proyectos_info})

        response_data = {
            'data': data,
        }
        return JsonResponse(response_data)
    else:
        cont_users_Ing = User.objects.filter(usuario__facultad='Ingenieria').count()
        cont_users_Hum = User.objects.filter(usuario__facultad='Humanidades').count()
        cont_users_Adm = User.objects.filter(usuario__facultad='Ciencias_Admin').count()
        cont_users_Edu = User.objects.filter(usuario__facultad='Educacion').count()
        cont_total_users =  cont_users_Ing + cont_users_Hum + cont_users_Adm + cont_users_Edu
        
        Cont_Users_Facultad = {
            'cont_users_Ing': cont_users_Ing,
            'cont_users_Hum': cont_users_Hum,
            'cont_users_Adm': cont_users_Adm,
            'cont_users_Edu': cont_users_Edu,
            'cont_total_users': cont_total_users,
        }

        return render(request, 'Vicerrectoria_Admin/Admin_informe_facultad_programa.html', Cont_Users_Facultad)


""" #BACKUP 1
# Informe Admin_informe_categoria_producto
@login_required
def Admin_informe_categoria_producto(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        categoria_seleccionada = request.GET.get('categoria')

        productos = Producto.objects.filter(categoria=categoria_seleccionada)

        productos_por_usuario = {}
        tipos_por_usuario = {}

        for producto in productos:
            usuario = producto.proyecto.usuario
            if usuario in productos_por_usuario:
                productos_por_usuario[usuario] += 1
                tipos_por_usuario[usuario].append(producto.tipo_producto)
            else:
                productos_por_usuario[usuario] = 1
                tipos_por_usuario[usuario] = [producto.tipo_producto]

        resultados = []
        for usuario, cantidad_productos in productos_por_usuario.items():
            resultados.append({
                'nombre': usuario.usuario.nombre,
                'identificacion': usuario.usuario.identificacion,
                'cantidad_productos': cantidad_productos,
                'tipos_productos': ', '.join(tipos_por_usuario[usuario]),
            })

        response_data = {
            'data': resultados,
        }

        return JsonResponse(response_data)
    else:
        return render(request, 'Vicerrectoria_Admin/Admin_informe_categoria_producto.html')
"""


""" BACUP 2 - ESTADOS
@login_required
def Admin_informe_categoria_producto(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        categoria_seleccionada = request.GET.get('categoria')

        productos = Producto.objects.filter(categoria=categoria_seleccionada)

        # Crear una lista de tipos de productos según el estado
        tipos_no_iniciados = []
        tipos_justificados = []
        tipos_iniciados = []
        tipos_en_progreso = []
        tipos_completados = []

        for producto in productos:
            if producto.estado_3 == "Completado":
                tipos_completados.append(producto.tipo_producto)
            elif producto.estado_2 == "En progreso":
                tipos_en_progreso.append(producto.tipo_producto)
            elif producto.estado_1 == "Iniciado":
                tipos_iniciados.append(producto.tipo_producto)
            elif producto.estado_0_justificado == "Justificado":
                tipos_justificados.append(producto.tipo_producto)
            else:
                tipos_no_iniciados.append(producto.tipo_producto)

        # Crear una lista de resultados
        resultados = []
        for producto in productos:
            resultado = {
                "nombre": producto.tipo_producto,
                "No Iniciado": "X" if producto.estado_0 == "No Iniciado" else "",
                "Justificado": "X" if producto.estado_0_justificado == "Justificado" else "",
                "Iniciado": "X" if producto.estado_1 == "Iniciado" else "",
                "En Progreso": "X" if producto.estado_2 == "En Progreso" else "",
                "Completado": "X" if producto.estado_3 == "Completado" else "",
            }
            resultados.append(resultado)

        response_data = {
            'data': resultados,
        }


        return JsonResponse(response_data)
    else:
        return render(request, 'Vicerrectoria_Admin/Admin_informe_categoria_producto.html')
"""


# Informe Admin_informe_categoria_producto
@login_required
def Admin_informe_categoria_producto(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        categoria_seleccionada = request.GET.get('categoria')

        if categoria_seleccionada == 'General':
            # Obtener todos los productos sin importar la categoría
            productos = Producto.objects.all()
        else:
            productos = Producto.objects.filter(categoria=categoria_seleccionada)

        productos_por_usuario = {}
        tipos_por_usuario = {}
        no_iniciados_por_usuario = {}
        #cant_no_iniciados_por_usuario = {}

        for producto in productos:
            usuario = producto.proyecto.usuario
            if usuario in productos_por_usuario:
                productos_por_usuario[usuario] += 1
                tipos_por_usuario[usuario].append(producto.tipo_producto)
                if producto.estado_0 == "No Iniciado":
                    no_iniciados_por_usuario[usuario].append(producto.tipo_producto)
                    #cant_no_iniciados_por_usuario[usuario] += 1
            else:
                productos_por_usuario[usuario] = 1
                tipos_por_usuario[usuario] = [producto.tipo_producto]
                no_iniciados_por_usuario[usuario] = []
                #if producto.estado_0 == "No Iniciado":
                    #cant_no_iniciados_por_usuario[usuario] = 1

        resultados = []
        for usuario, cantidad_productos in productos_por_usuario.items():
            resultados.append({
                'nombre': usuario.usuario.nombre,
                'identificacion': usuario.usuario.identificacion,
                'cantidad_productos': cantidad_productos,
                'tipos_productos': ', '.join(tipos_por_usuario[usuario]),
                'no_iniciados': ', '.join(no_iniciados_por_usuario[usuario]),
                #'cant_no_iniciados': cant_no_iniciados_por_usuario.get(usuario, 0),
            })

        response_data = {
            'data': resultados,
        }

        return JsonResponse(response_data)
    else:
        return render(request, 'Vicerrectoria_Admin/Admin_informe_categoria_producto.html')





#----------------- // ----------------- USUARIO ESTUDIANTE  ----------------- \\ -----------------

# CONSULTAR PERFIL Y EXTRAER DATOS - ESTUDIANTE
def Users_E_consultar_identificacion(request):
    if request.method == 'POST':

        identificacion = request.POST.get('identificacion')

        if Usuario_Estudiante.objects.filter(identificacion=identificacion).exists():
            message = "Ya cuentas con un usuario registrado. Inicia sesión."
            query_params = QueryDict(mutable=True)
            query_params['message'] = message
            return HttpResponseRedirect(f"/users/Users_E_login/?{query_params.urlencode()}")
        else:
            # Api_Perfil
            api_perfil = f'http://190.60.75.134/searches/consultar_perfil.json?periodos={identificacion}'
            response_perfil = requests.get(api_perfil)

            if response_perfil.status_code == 200:
                data_pefil = response_perfil.json()

                if (data_pefil) and (data_pefil[0][3] == 'Alumno' or data_pefil[0][3] == 'ALUMNO'):
                    nombre = data_pefil[0][0]
                    identificacion = data_pefil[0][1]

                    # Api_Datos_Estudiantes
                    api_datos = f'http://190.60.75.134/searches/datos_estudiante.json?periodos={identificacion}'
                    response_datos = requests.get(api_datos)
                    if response_datos.status_code == 200:
                        data_datos = response_datos.json()
                        telefono = data_datos[0][2]
                        correo = data_datos[0][4]
                        programa = data_datos[0][8]

                        # Redirigir a la vista de registro de usuario con datos precargados
                        return redirect('Users:Users_E_registro_usuario', nombre=nombre, identificacion=identificacion, correo=correo,programa=programa,telefono=telefono)
    return render(request, 'Estudiantes/Users_E_consultar_identificacion.html')


# CREAR USUARIO - ESTUDIANTE
def Users_E_registro_usuario(request, nombre, identificacion, correo, programa, telefono):
    if request.method == 'POST':
        clave = request.POST.get('clave')
        confirmar_clave = request.POST.get('confirmar_clave')

        # Coincidir Contraseñas
        if clave == confirmar_clave:
            # Crear un nuevo usuario utilizando el modelo User de Django
            user_e = User.objects.create_user(username=identificacion.lower(), password=clave)
            
            # Guardar los otros datos en el perfil del usuario
            usuario_e = Usuario_Estudiante(user_e=user_e, nombre=nombre, identificacion=identificacion, correo=correo.lower(), clave=clave, programa=programa,telefono=telefono)
            usuario_e.save()
            
            # Iniciar sesión después del registro
            user_e = authenticate(username=identificacion.lower(), password=clave)
            if user_e is not None:
                login(request, user_e)
                return redirect('Users:Users_E_registro_exitoso')
            else:
                return HttpResponse('Error al iniciar sesión')

        else:
            error_message = "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            return render(request, 'Estudiantes/Users_E_registro_usuario.html', {'nombre': nombre, 'identificacion': identificacion, 'error_message': error_message})

    return render(request, 'Estudiantes/Users_E_registro_usuario.html', {'nombre': nombre, 'identificacion': identificacion})


# USUARIO CREADO - ESTUDIANTES
def Users_E_registro_exitoso(request):
    return render(request, 'Estudiantes/Users_E_registro_exitoso.html')


# LOGIN - INICIAR SESION
def Users_E_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_e = authenticate(request, username=username, password=password)
        if user_e is not None:
            login(request, user_e)
            return redirect('Users:Users_E_home')
        else:
            error_message = "Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo."
            return render(request, 'Estudiantes/Users_E_login.html', {'error_message': error_message})
    else:
        message = request.GET.get('message')
        return render(request, 'Estudiantes/Users_E_login.html', {'message': message, 'error_message': None})


# PAGINA HOME
@login_required
def Users_E_home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        print(messages)
        return redirect('Pagina_Principal')
    
    return render(request, 'Estudiantes/Users_E_home.html')


# LOGIN - CERRAR SESION
@login_required
def Users_E_cerrar_sesion (request):
    logout(request)
    return render(request, 'Estudiantes/Users_E_login.html')



#----------------- // ----------------- USUARIO ADMINISTRADOR SEMILLERO  ----------------- \\ -----------------

# PAGINA HOME
@login_required
def Admin_Semi_home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        print(messages)
        return redirect('Pagina_Principal')
    
    return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_Home.html')


# ADMINISTRADOR SEMILLERO - CREAR USUARIO 
CONTRASENA_ADMIN_SEMI = "1450065"
def Admin_Semi_registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        identificacion = request.POST.get('identificacion')
        correo = request.POST.get('correo')
        clave = request.POST.get('clave')
        confirmar_clave = request.POST.get('confirmar_clave')

        if Usuario_Adminin_Semi.objects.filter(identificacion=identificacion).exists():
            message = "Ya cuentas con un usuario registrado. Inicia sesión."
            query_params = QueryDict(mutable=True)
            query_params['message'] = message
            return HttpResponseRedirect(f"/users/Admin_Semi_login/?{query_params.urlencode()}")
        

        if clave == confirmar_clave and clave == CONTRASENA_ADMIN_SEMI:
            user_admin_s = User.objects.create_user(username=identificacion.lower(), password=clave)

            user_admin_s = Usuario_Adminin_Semi(user_admin_s=user_admin_s, nombre=nombre, identificacion=identificacion, correo=correo.lower(), clave=clave)
            user_admin_s.save()

            # Iniciar sesión después del registro
            user_admin_s = authenticate(username=identificacion.lower(), password=clave)
            if user_admin_s is not None:
                login(request, user_admin_s)
                return redirect('Users:Admin_Semi_registro_exitoso')
            else:
                return HttpResponse('Error al iniciar sesión')
        else:
            error_message = "Contraseña incorrecta o las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_registro_usuario.html', {'error_message': error_message})
    
    return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_registro_usuario.html')


# ADMINISTRADOR SEMILLERO - USUARIO CREADO
def Admin_Semi_registro_exitoso(request):
    return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_registro_exitoso.html')


# ADMINISTRADOR SEMILLERO - LOGIN - INICIAR SESION
def Admin_Semi_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario_admin_semi = authenticate(request, username=username, password=password)
        if usuario_admin_semi is not None:
            login(request, usuario_admin_semi)
            return redirect('Users:Admin_Semi_home')
        else:
            error_message = "Credenciales Administrador Incorrectas, inténtalo de nuevo."
            return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_login.html', {'error_message': error_message})

    return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_login.html')


# ADMINISTRADOR SEMILLERO - LOGIN - CERRAR SESION
@login_required
def Admin_Semi_cerrar_sesion(request):
    logout(request)
    return render(request, 'Vicerrectoria_Admin_Semi/Admin_Semi_login.html')

