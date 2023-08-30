from .models import Semillero, InscripcionSemillero, ActividadesSemillero
from .forms import SemilleroForm, InscripcionSemilleroForm, ActividadesSemilleroForm
from Users.models import User
from Users.models import Usuario_Estudiante
from Proyectos.models import Proyecto


import os
import random
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from reportlab.pdfgen import canvas
#from django.shortcuts import reverse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import date
from django.db.models import Count
from django.contrib import messages


#----------------- // ----------------- SEMILLERO - DOCENTE ----------------- \\ -----------------

# CREAR SEMILLERO
@login_required
def crear_semillero(request):
    usuario_actual = request.user.usuario
    proyectos = Proyecto.objects.filter(usuario=request.user)

    # Verificar datos perfil.
    if not usuario_actual.telefono or not usuario_actual.facultad or not usuario_actual.Programa:
        messages.error(request, "Se requiere completar los datos de tu perfil.")
        return redirect('Users:Users_editar_perfil')
    
    # Verificar Grupos y lineas.
    if (not usuario_actual.grupo_investigacion and not usuario_actual.grupo_investigacion_2 and not usuario_actual.grupo_investigacion_3) or not usuario_actual.lineas_investigacion:
        messages.error(request, "Se requiere especificar minimo un Grupo y una Linea de investigacion")
        return redirect('Users:Users_editar_grupos_investigacion')
    
    if request.method == 'POST':
        form = SemilleroForm(request.POST)
        if form.is_valid():
            semillero = form.save(commit=False)
            semillero.usuario = usuario_actual.user
            semillero.save()
            return redirect('Semilleros:lista_semilleros')
    else:
        context = {
            'proyectos': proyectos,
        }
        perfil_usuario = usuario_actual
        facultad = perfil_usuario.facultad
        programa = perfil_usuario.Programa
        grupo_investigacion = perfil_usuario.grupo_investigacion
        linea_investigacion = perfil_usuario.lineas_investigacion.first().nombre if perfil_usuario.lineas_investigacion.exists() else None
        nombre = perfil_usuario.nombre
        identificacion = perfil_usuario.identificacion
        telefono = perfil_usuario.telefono
        correo = perfil_usuario.correo
        cvlac = perfil_usuario.cvlac

        initial_data = {
            'facultad': facultad,
            'programa': programa,
            'grupo_investigacion': grupo_investigacion,
            'linea_investigacion': linea_investigacion,
            'nombre': nombre,
            'identificacion': identificacion,
            'telefono': telefono,
            'correo': correo,
            'cvlac': cvlac
        }

        form = SemilleroForm(initial=initial_data)
    return render(request, 'Docentes/crear_semillero.html', context={'form': form, 'proyectos': proyectos})


# LISTA DE SEMILLEROS
@login_required
def lista_semilleros(request):
    semilleros = Semillero.objects.filter(usuario=request.user)
    success_message = request.GET.get('message')

    context = {
        'semilleros': semilleros,
        'success_message': success_message
    }
    return render(request, 'Docentes/lista_semilleros.html', context)


# OPCIONES DE SEMILLEROS
@login_required
def opciones_semillero(request, semillero_id):
    try:
        semillero = Semillero.objects.get(pk=semillero_id, usuario=request.user)
    except Semillero.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    context = {
        'semillero': semillero,
    }
    return render(request, 'Docentes/opciones_semillero.html', context)


# DETALLE SEMILLERO
@login_required
def detalle_semillero(request, semillero_id):
    try:
        semillero = Semillero.objects.get(pk=semillero_id, usuario=request.user)
    except Semillero.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    proyectos = Proyecto.objects.filter(usuario=request.user)
    estudiantes_inscritos = InscripcionSemillero.objects.filter(semillero=semillero)
    
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        estudiante = InscripcionSemillero.objects.get(pk=estudiante_id)
        estudiante.estado_e = not estudiante.estado_e
        estudiante.save()
    
    return render(request, 'Docentes/detalle_semillero.html', {'semillero': semillero, 'proyectos': proyectos, 'estudiantes_inscritos': estudiantes_inscritos})


# VER PERFIL ESTUDIANTE
def ver_perfil_solicitante(request, estudiante_id, semillero_id):
    try:
        semillero = Semillero.objects.get(pk=semillero_id, usuario=request.user)
    except Semillero.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    estudiante = InscripcionSemillero.objects.get(id=estudiante_id)
    return render(request, 'Docentes/ver_perfil_solicitante.html', {'estudiante': estudiante, 'semillero': semillero})


# GENERAR AVAL PDF
@login_required
def generar_aval(request, estudiante_id, semillero_id):
    try:
        semillero = Semillero.objects.get(pk=semillero_id, usuario=request.user)
    except Semillero.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    estudiante = InscripcionSemillero.objects.get(id=estudiante_id)

    html = render_to_string('Docentes/generar_aval_pdf.html', {'semillero': semillero, 'estudiante': estudiante})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Carta Aval Semillero - Estudiante.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


# ACTIVIDADES DE SEMILLERO
@login_required
def ver_actividades_semillero(request):
    actividades = ActividadesSemillero.objects.all()
    return render(request, 'Docentes/ver_actividades_semillero.html', {'actividades': actividades})


# DETALLES ACTIVIDADES DE SEMILLERO
@login_required
def ver_detalle_actividad_semillero(request, actividad_id):
    try:
        actividad = get_object_or_404(ActividadesSemillero, pk=actividad_id)
    except Semillero.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    
    return render(request, 'Docentes/ver_detalle_actividad_semillero.html', {'actividad': actividad} )


#----------------- // ----------------- SEMILLERO - ESTUDIANTES ----------------- \\ -----------------

# VER SEMILLEROS
@login_required
def ver_semilleros_estudiante(request):
    usuario_e = request.user.usuario_estudiante
    semilleros_disponibles = Semillero.objects.all()

    return render(request, 'Estudiantes/ver_semilleros_estudiante.html', {'semilleros_disponibles': semilleros_disponibles, 'usuario_e': usuario_e})


# VER SEMILLEROS INSCRITOS
@login_required
def ver_mis_semilleros(request):
    usuario_e = request.user.usuario_estudiante
    inscripciones = InscripcionSemillero.objects.filter(user_e=usuario_e)
    semilleros_inscritos = [inscripcion.semillero for inscripcion in inscripciones]
    
    return render(request, 'Estudiantes/ver_mis_semilleros.html', {'usuario_e': usuario_e, 'semilleros_inscritos': semilleros_inscritos})


# DETALLES DEL SEMIERRO - ESTUDIANTE
@login_required
def detalle_semillero_estudiante(request, semillero_id):
    semillero = get_object_or_404(Semillero, pk=semillero_id)
    usuario_estudiante = request.user.usuario_estudiante
    existe_inscripcion = InscripcionSemillero.objects.filter(semillero=semillero, user_e=usuario_estudiante).exists()

    if existe_inscripcion:
        datos_e = InscripcionSemillero.objects.get(semillero=semillero, user_e=usuario_estudiante)
        actividades_permiso = datos_e.estado_e

        if request.method == 'POST':
            actividades_form = ActividadesSemilleroForm(request.POST)
            if actividades_form.is_valid():
                nueva_actividad = actividades_form.save(commit=False)
                nueva_actividad.user_e = usuario_estudiante
                nueva_actividad.semillero = semillero
                nueva_actividad.inscripcion = datos_e
                nueva_actividad.save()

                if 'adjunto_actividad_e' in request.FILES:
                    nueva_actividad.adjunto_actividad_e = request.FILES['adjunto_actividad_e']
                    nueva_actividad.save()
                return redirect('Semilleros:detalle_semillero_estudiante', semillero_id=semillero.id)

        else:
            nombre_estuidante_actividad_e = usuario_estudiante.nombre
            identificacion_estuidante_actividad_e = usuario_estudiante.identificacion

            initial_data = {
                'nombre_estuidante_actividad_e': nombre_estuidante_actividad_e,
                'identificacion_estuidante_actividad_e': identificacion_estuidante_actividad_e,
            }
            actividades_form = ActividadesSemilleroForm(initial=initial_data)

            return render(request, 'Estudiantes/detalle_semillero_estudiante.html', {
                'semillero': semillero,
                'existe_inscripcion': existe_inscripcion,
                'datos_e': datos_e,
                'actividades_permiso': actividades_permiso,
                'actividades_form': actividades_form
            })

    else:
        datos_e = None
        actividades_permiso = False
        actividades_form = None

    return render(request, 'Estudiantes/detalle_semillero_estudiante.html', {
        'semillero': semillero,
        'existe_inscripcion': existe_inscripcion,
        'datos_e': datos_e,
        'actividades_permiso': actividades_permiso,
    })


# INSCRIBIRSE A UN SEMILLERO (formulario_inscripcion_semillero)
@login_required
def formulario_inscripcion_semillero(request, semillero_id):
    semillero = Semillero.objects.get(pk=semillero_id)
    usuario_estudiante = request.user.usuario_estudiante

    if request.method == 'POST':
        form = InscripcionSemilleroForm(request.POST)
        if form.is_valid():
            tipo_solicitante = form.cleaned_data['tipo_solicitante']
            tipo_solicitante_otro = form.cleaned_data['tipo_solicitante_otro'] if tipo_solicitante == 'otro' else ''

            InscripcionSemillero.objects.create(
                semillero = semillero,
                user_e = usuario_estudiante,
                tipo_solicitante = tipo_solicitante,
                tipo_solicitante_otro = tipo_solicitante_otro,
                nombre_e = usuario_estudiante.nombre,
                identificacion_e = usuario_estudiante.identificacion,
                telefono_e = usuario_estudiante.telefono,
                correo_e = usuario_estudiante.correo,
                programa_e = usuario_estudiante.programa,

                #
                nivel_ingles_habla_e = form.cleaned_data['nivel_ingles_habla_e'],
                nivel_ingles_lee_e = form.cleaned_data['nivel_ingles_lee_e'],
                nivel_ingles_entiende_e = form.cleaned_data['nivel_ingles_entiende_e'],
                nivel_ingles_escribe_e = form.cleaned_data['nivel_ingles_escribe_e'],

                #
                semestre_actual = form.cleaned_data['semestre_actual'],
                año_ingreso = form.cleaned_data['año_ingreso'],
                fecha_grado = form.cleaned_data['fecha_grado'],

                #
                cursos_inves = form.cleaned_data['cursos_inves'],
                tematica_e = form.cleaned_data['tematica_e'],
                institucion_e = form.cleaned_data['institucion_e'],
                horas_e = form.cleaned_data['horas_e'],
                fecha_e = form.cleaned_data['fecha_e'],

                #
                tematica_e_2 = form.cleaned_data['tematica_e_2'],
                institucion_e_2 = form.cleaned_data['institucion_e_2'],
                horas_e_2 = form.cleaned_data['horas_e_2'],
                fecha_e_2 = form.cleaned_data['fecha_e_2'],
                tiene_cvlac_e = form.cleaned_data['tiene_cvlac_e'],
                cvlac_e = form.cleaned_data['cvlac_e'],

                #
                participa_proyectos = form.cleaned_data['participa_proyectos'],
                Se_nombre_proyecto_e = form.cleaned_data['Se_nombre_proyecto_e'],
                Se_institucion_e = form.cleaned_data['Se_institucion_e'],
                Se_tipo_vinculacion_e = form.cleaned_data['Se_tipo_vinculacion_e'],
                Se_fecha_e = form.cleaned_data['Se_fecha_e'],
                Se_nombre_proyecto_e_2 = form.cleaned_data['Se_nombre_proyecto_e_2'],
                Se_institucion_e_2 = form.cleaned_data['Se_institucion_e_2'],
                Se_tipo_vinculacion_e_2 = form.cleaned_data['Se_tipo_vinculacion_e_2'],
                Se_fecha_e_2 = form.cleaned_data['Se_fecha_e_2'],
                Se_nombre_proyecto_e_3 = form.cleaned_data['Se_nombre_proyecto_e_3'],
                Se_institucion_e_3 = form.cleaned_data['Se_institucion_e_3'],
                Se_tipo_vinculacion_e_3 = form.cleaned_data['Se_tipo_vinculacion_e_3'],
                Se_fecha_e_3 = form.cleaned_data['Se_fecha_e_3'],

                #
                actividades_e = form.cleaned_data['actividades_e'],
                nombre_grupo_e = form.cleaned_data['nombre_grupo_e'],
                actividad_tema_e = form.cleaned_data['actividad_tema_e'],
                tipo_vinculacion_e = form.cleaned_data['tipo_vinculacion_e'],
                fecha_actividad_e = form.cleaned_data['fecha_actividad_e'],

                nombre_grupo_e_2 = form.cleaned_data['nombre_grupo_e_2'],
                actividad_tema_e_2 = form.cleaned_data['actividad_tema_e_2'],
                tipo_vinculacion_e_2 = form.cleaned_data['tipo_vinculacion_e_2'],
                fecha_actividad_e_2 = form.cleaned_data['fecha_actividad_e_2'],

                #
                semillero_proyecto_interes = semillero.nombre_semillero,
                linea_sublinea = semillero.linea_investigacion,
                horas_semanales = form.cleaned_data['horas_semanales'],
                tipo_semillero = form.cleaned_data['tipo_semillero'],

                #
                lugar_expedicion_e = form.cleaned_data['lugar_expedicion_e'],
                fecha_nacimiento_e = form.cleaned_data['fecha_nacimiento_e'],
                lugar_nacimiento_e = form.cleaned_data['lugar_nacimiento_e'],
                direccion_e = form.cleaned_data['direccion_e'],

            )
            return redirect('Semilleros:ver_semilleros_estudiante')

    else:
        initial_data = {
            'nombre_e': usuario_estudiante.nombre,
            'identificacion_e': usuario_estudiante.identificacion,
            'telefono_e': usuario_estudiante.telefono,
            'correo_e': usuario_estudiante.correo,
            'programa_e': usuario_estudiante.programa,
        }
        form = InscripcionSemilleroForm(initial=initial_data)

    return render(request, 'Estudiantes/formulario_inscripcion_semillero.html', {'semillero': semillero, 'form': form})


#
