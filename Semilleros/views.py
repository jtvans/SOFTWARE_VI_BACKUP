from django.shortcuts import render
from .models import Semillero
from .forms import SemilleroForm
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


# CREAR SEMILLERO
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
    return render(request, 'crear_semillero.html', context={'form': form, 'proyectos': proyectos})


# LISTA DE SEMILLEROS
@login_required
def lista_semilleros(request):
    semilleros = Semillero.objects.filter(usuario=request.user)
    success_message = request.GET.get('message')

    context = {
        'semilleros': semilleros,
        'success_message': success_message
    }
    return render(request, 'lista_semilleros.html', context)