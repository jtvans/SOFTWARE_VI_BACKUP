# Models
from .models import Proyecto, Actividad, Producto, Portafolio
# Forms
from .forms import ProyectoForm, ActividadForm, ProductoForm, AvanceEstado0Form, AvanceEstado1Form, AvanceEstado2Form, AvanceEstado3Form
# Components
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





#----------------- // ----------------- PROYECTO - PLAN TRABAJO ----------------- \\ -----------------


# CREAR PROYECTO - PLAN TRABAJO
@login_required
def crear_proyecto(request):
    usuario_actual = request.user.usuario

    # Verificar datos perfil.
    if not usuario_actual.telefono or not usuario_actual.facultad or not usuario_actual.Programa:
        messages.error(request, "Se requiere completar los datos de tu perfil.")
        return redirect('Users:Users_editar_perfil')
    
    # Verificar Grupos y lineas.
    if (not usuario_actual.grupo_investigacion and not usuario_actual.grupo_investigacion_2 and not usuario_actual.grupo_investigacion_3) or not usuario_actual.lineas_investigacion:
        messages.error(request, "Se requiere especificar minimo un Grupo y una Linea de investigacion")
        return redirect('Users:Users_editar_grupos_investigacion')
    

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        ActividadFormSet = inlineformset_factory(Proyecto, Actividad, form=ActividadForm, extra=1)
        actividad_formset = ActividadFormSet(request.POST)

        if form.is_valid() and actividad_formset.is_valid():
            proyecto = form.save(commit=False)
            proyecto.usuario = usuario_actual.user
            
            image_folder = 'static/images_list_proyect'
            image_files = os.listdir(image_folder)
            random_index = random.randint(0, len(image_files) - 1)
            random_image = image_files[random_index]
            proyecto.imagen = random_image
            proyecto.save()

            actividad_formset.instance = proyecto
            actividad_formset.save()

            if 'archivo_adjunto' in request.FILES:
                proyecto.archivo_adjunto = request.FILES['archivo_adjunto']
                proyecto.save()
            return redirect('Proyectos:lista_proyectos')
    else:
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
        ActividadFormSet = inlineformset_factory(Proyecto, Actividad, form=ActividadForm, extra=1)
        form = ProyectoForm(initial=initial_data)
        actividad_formset = ActividadFormSet()

    return render(request, 'Proyectos/crear_proyecto.html', {'form': form, 'actividad_formset': actividad_formset})


# OPCIONES DE PROYECTO
@login_required
def opciones_proyecto(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    context = {
        'proyecto': proyecto,
    }
    return render(request, 'Proyectos/opciones_proyecto.html', context)


# DETALLES PROYECTO
@login_required
def detalle_proyecto(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    actividades = proyecto.actividades.all()
    productos = Producto.objects.filter(proyecto__usuario=request.user, proyecto=proyecto)
    categorias = [choice[1] for choice in Producto.CATEGORIAS]
    portafolios = Portafolio.objects.filter(proyecto=proyecto).order_by('id')

    return render(request, 'Proyectos/detalle_proyecto.html', {'proyecto': proyecto, 'actividades': actividades, 'productos': productos, 'categorias': categorias, 'portafolios': portafolios})


# ELIMINAR PROYECTO - PLAN TRABAJO
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        proyecto.delete()
        return redirect('Proyectos:lista_proyectos')
    context = {
        'proyecto': proyecto,
    }
    return render(request, 'Proyectos/lista_proyectos.html', context)



# LISTA DE PROYECTOS
@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    image_folder = 'static/images_list_proyect'  # Ruta carpeta de imágenes
    success_message = request.GET.get('message')
    for proyecto in proyectos:
        image_files = os.listdir(image_folder)
        random_index = random.randint(0, len(image_files) - 1)
        proyecto.random_image = image_files[random_index]

    context = {
        'proyectos': proyectos,
        'success_message': success_message
    }
    return render(request, 'Proyectos/lista_proyectos.html', context)


#----------------- // ----------------- PLAN TRABAJO - PRODUCTOS ----------------- \\ -----------------


# CREAR PLAN DE TRABAJO - AÑADIR TIPOS DE PRODUCTOS
@login_required
def crear_plan_trabajo(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    productos = Producto.objects.filter(proyecto__usuario=request.user, proyecto=proyecto)
    
    eliminar_producto_url = reverse('Proyectos:eliminar_producto', kwargs={'producto_id': 0})
    eliminar_producto_url = eliminar_producto_url.replace('0', '{}')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            plan_trabajo = form.save(commit=False)
            plan_trabajo.proyecto = proyecto
            plan_trabajo.cantidad = 1
            plan_trabajo.save()
            return redirect(request.path)
    else:
        form = ProductoForm()
    
    context = {
        'proyecto': proyecto,
        'form': form,
        'productos': productos,
        'categorias': [choice[1] for choice in Producto.CATEGORIAS],
        'eliminar_producto_url': eliminar_producto_url,
    }

    return render(request, 'Proyectos/crear_plan_trabajo.html', context)


# PLAN TRABAJO CREADO
def plan_trabajo_creado(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    return render(request, 'Proyectos/plan_trabajo_creado.html', {'proyecto': proyecto, 'proyecto_id': proyecto_id})


# ELIMINAR/ELIMINAR PRODUCTO
@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, proyecto__usuario=request.user)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'El producto ha sido eliminado exitosamente.')
        return JsonResponse({'success': True, 'url': reverse('Proyectos:crear_plan_trabajo', args=[producto.proyecto.id])})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})


# VER PLAN DE TRABAJO
@login_required
def ver_plan_trabajo(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    productos = Producto.objects.filter(proyecto__usuario=request.user, proyecto=proyecto)
    categorias = [choice[1] for choice in Producto.CATEGORIAS]

    return render(request, 'Proyectos/ver_plan_trabajo.html', {'proyecto': proyecto, 'productos': productos, 'categorias': categorias})


# DESCARGAR PDF DE PROYECTO.
@login_required
def descargar_pdf(request, proyecto_id):
    # Obtener los datos del proyecto y productos
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    productos = Producto.objects.filter(proyecto=proyecto)
    actividades = proyecto.actividades.all()
    portafolios = Portafolio.objects.filter(proyecto=proyecto).order_by('id')

    # Renderizar la vista HTML con los datos del proyecto y productos
    html = render_to_string('Proyectos/detalle_proyecto_pdf.html', {'proyecto': proyecto, 'productos': productos, 'actividades': actividades, 'portafolios':portafolios})

    # Crear el objeto HttpResponse con el tipo de contenido apropiado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Formato Inscripcion Proyecto Investigacion.pdf"'

    # Convertir la página HTML en un archivo PDF y adjuntarlo a la respuesta
    pisa.CreatePDF(html, dest=response)

    return response


#------------ // ------------ // ------------ PORTAFOLIO DE ACTIVIDADES ------------ \\ ------------ \\ ------------


# PORTAFOLIO
@login_required
def portafolio_actividades(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    actividades = proyecto.actividades.all()
    productos = Producto.objects.filter(proyecto__usuario=request.user, proyecto=proyecto)
    categorias = [choice[1] for choice in Producto.CATEGORIAS]
    portafolio = Portafolio.objects.filter(proyecto=proyecto)
    
    #---------- Porcentaje cumplimiento --------------#
    total_productos = len(productos)

    pesos_productos = 1 / total_productos if total_productos > 0 else 0

    avances_por_producto = {}

    for porta in portafolio:
        producto_id = porta.producto_id
        if producto_id not in avances_por_producto:
            avances_por_producto[producto_id] = []
        avances_por_producto[producto_id].append(porta)

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

    porcentaje_cumplimiento_total = round(productos_completados_total * 100, 2)
    proyecto.porcentaje_cumplimiento_total = porcentaje_cumplimiento_total
    proyecto.save()
    peso_formulario = round(porcentaje_cumplimiento / 100, 3)
    #--------------------------------------------------#
    
    return render(request, 'Proyectos/portafolio_actividades.html', 
        {'proyecto': proyecto,
         'actividades': actividades,
         'productos': productos,
         'categorias': categorias,
         'portafolio': portafolio,
         'tabla_avances': tabla_avances,
         'porcentaje_cumplimiento_total': porcentaje_cumplimiento_total,
         'peso_formulario': peso_formulario,
         'pesos_productos': pesos_productos
         })


# PORTAFOLIO ESTADO 0
@login_required
def avance_estado_0(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)

    if request.method == 'POST':
        form = AvanceEstado0Form(request.POST, request.FILES)
        if form.is_valid():
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_justificacion = form.cleaned_data['avance_justificacion']
            
            Portafolio.objects.create(
                proyecto = proyecto,
                producto = producto,
                avance_0_justificacion = avance_justificacion,
                avance_0_fecha = fecha_avance
            )

            # Cambiar el estado a "Iniciado"                       
            producto.estado_0 = "No Iniciado"
            producto.estado_0_justificado = "Justificado"
            producto.save()

            return redirect('Proyectos:portafolio_actividades', proyecto_id=proyecto_id)
    else:
        form = AvanceEstado0Form()

    return render(request, 'Proyectos/avance_estado_0.html', {'form': form, 'proyecto': proyecto, 'producto': producto})


# PORTAFOLIO ESTADO 1
@login_required
def avance_estado_1(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)

    if request.method == 'POST':
        form = AvanceEstado1Form(request.POST, request.FILES)
        if form.is_valid():
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_nombre = form.cleaned_data['avance_nombre']
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']


            Portafolio.objects.create(
                proyecto=proyecto,
                producto=producto,
                avance_1_nombre=avance_nombre,
                avance_1_descripcion=avance_descripcion,
                avance_1_link=avance_link,
                avance_1_adjunto=avance_adjunto,
                avance_1_fecha=fecha_avance,
                avance_1_estado = "No Revisado", 
            )

            # Cambiar el estado
            producto.estado_0 = "Iniciado"
            producto.estado_1 = "Iniciado"
            producto.save()

            return redirect('Proyectos:portafolio_actividades', proyecto_id=proyecto_id)
    else:
        form = AvanceEstado1Form()

    return render(request, 'Proyectos/avance_estado_1.html', {'form': form, 'proyecto': proyecto, 'producto': producto})

# EDITAR - PORTAFOLIO ESTADO 1 
@login_required
def avance_estado_1_editar(request, proyecto_id, producto_id, evidencia_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencia = get_object_or_404(Portafolio, id=evidencia_id, proyecto=proyecto, producto=producto)

    if request.method == 'POST':
        form = AvanceEstado1Form(request.POST, request.FILES)
        if form.is_valid():
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_nombre = form.cleaned_data['avance_nombre']
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']
            avance_correcciones_realizadas = form.cleaned_data['avance_correcciones_realizadas']

            # Actualizar los campos en el objeto Portafolio
            evidencia.avance_1_nombre = avance_nombre
            evidencia.avance_1_descripcion = avance_descripcion
            evidencia.avance_1_link = avance_link
            evidencia.avance_1_correcciones_realizadas = avance_correcciones_realizadas

            if avance_adjunto:
                evidencia.avance_1_adjunto = avance_adjunto
            evidencia.avance_1_fecha = fecha_avance
            evidencia.save()

            return redirect('Proyectos:ver_evidencias_1', proyecto_id=proyecto_id, producto_id=producto_id)
    else:
        # Rellenar el formulario con los datos existentes de la evidencia
        form = AvanceEstado1Form(initial={
            'avance_nombre': evidencia.avance_1_nombre,
            'avance_descripcion': evidencia.avance_1_descripcion,
            'avance_link': evidencia.avance_1_link,
            'avance_correcciones_realizadas': evidencia.avance_1_correcciones_realizadas
        })

    return render(request, 'Proyectos/avance_estado_1_editar.html', {'form': form, 'proyecto': proyecto, 'producto': producto, 'evidencia_id': evidencia_id})


# PORTAFOLIO ESTADO 2
@login_required
def avance_estado_2(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
    
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)

    if request.method == 'POST':
        form = AvanceEstado2Form(request.POST, request.FILES)
        if form.is_valid():
            
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']

            Portafolio.objects.create(
                proyecto=proyecto,
                producto=producto,
                avance_2_descripcion=avance_descripcion,
                avance_2_link=avance_link,
                avance_2_adjunto=avance_adjunto,
                avance_2_fecha=fecha_avance,
                avance_2_estado = "No Revisado"
            )

            # Cambiar el estado a "En Progreso"
            producto.estado_2 = "En Progreso"
            producto.save()

            return redirect('Proyectos:portafolio_actividades', proyecto_id=proyecto_id)
    else:
        form = AvanceEstado2Form()

    return render(request, 'Proyectos/avance_estado_2.html', {'form': form, 'proyecto': proyecto, 'producto': producto})

# EDITAR - PORTAFOLIO ESTADO 2 
@login_required
def avance_estado_2_editar(request, proyecto_id, producto_id, evidencia_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencia = get_object_or_404(Portafolio, id=evidencia_id, proyecto=proyecto, producto=producto)

    if request.method == 'POST':
        form = AvanceEstado2Form(request.POST, request.FILES)
        if form.is_valid():
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']
            avance_correcciones_realizadas = form.cleaned_data['avance_correcciones_realizadas']

            # Actualizar los campos en el objeto Portafolio
            evidencia.avance_2_descripcion = avance_descripcion
            evidencia.avance_2_link = avance_link
            evidencia.avance_2_correcciones_realizadas=avance_correcciones_realizadas

            if avance_adjunto:
                evidencia.avance_2_adjunto = avance_adjunto
            evidencia.avance_2_fecha = fecha_avance
            evidencia.save()

            return redirect('Proyectos:ver_evidencias_2', proyecto_id=proyecto_id, producto_id=producto_id)
    else:
        # Rellenar el formulario con los datos existentes de la evidencia
        form = AvanceEstado2Form(initial={
            'avance_descripcion': evidencia.avance_2_descripcion,
            'avance_link': evidencia.avance_2_link,
            'avance_correcciones_realizadas': evidencia.avance_2_correcciones_realizadas
        })

    return render(request, 'Proyectos/avance_estado_2_editar.html', {'form': form, 'proyecto': proyecto, 'producto': producto, 'evidencia_id': evidencia_id})


# PORTAFOLIO ESTADO 3
@login_required
def avance_estado_3(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)

    if request.method == 'POST':
        form = AvanceEstado3Form(request.POST, request.FILES)
        if form.is_valid():

            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']

            Portafolio.objects.create(
                proyecto=proyecto,
                producto=producto,
                avance_3_descripcion=avance_descripcion,
                avance_3_link=avance_link,
                avance_3_adjunto=avance_adjunto,
                avance_3_fecha=fecha_avance,
                avance_3_estado = "No Revisado"
            )

            # Cambiar el estado a "En Progreso"
            producto.estado_3 = "Completado"
            producto.save()

            return redirect('Proyectos:portafolio_actividades', proyecto_id=proyecto_id)
    else:
        form = AvanceEstado2Form()

    return render(request, 'Proyectos/avance_estado_3.html', {'form': form, 'proyecto': proyecto, 'producto': producto})

# EDITAR - PORTAFOLIO ESTADO 3 
@login_required
def avance_estado_3_editar(request, proyecto_id, producto_id, evidencia_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencia = get_object_or_404(Portafolio, id=evidencia_id, proyecto=proyecto, producto=producto)

    if request.method == 'POST':
        form = AvanceEstado3Form(request.POST, request.FILES)
        if form.is_valid():
            # Obtener la fecha actual
            fecha_avance = date.today()

            # Procesar los datos del formulario según tus requisitos
            avance_descripcion = form.cleaned_data['avance_descripcion']
            avance_link = form.cleaned_data['avance_link']
            avance_adjunto = form.cleaned_data['avance_adjunto']
            avance_correcciones_realizadas = form.cleaned_data['avance_correcciones_realizadas']

            # Actualizar los campos en el objeto Portafolio
            evidencia.avance_3_descripcion = avance_descripcion
            evidencia.avance_3_link = avance_link
            evidencia.avance_1_correcciones_realizadas = avance_correcciones_realizadas

            if avance_adjunto:
                evidencia.avance_3_adjunto = avance_adjunto
            evidencia.avance_3_fecha = fecha_avance
            evidencia.save()

            return redirect('Proyectos:ver_evidencias_3', proyecto_id=proyecto_id, producto_id=producto_id)
    else:
        # Rellenar el formulario con los datos existentes de la evidencia
        form = AvanceEstado3Form(initial={
            'avance_descripcion': evidencia.avance_3_descripcion,
            'avance_link': evidencia.avance_3_link,
            'avance_correcciones_realizadas': evidencia.avance_1_correcciones_realizadas
        })

    return render(request, 'Proyectos/avance_estado_3_editar.html', {'form': form, 'proyecto': proyecto, 'producto': producto, 'evidencia_id': evidencia_id})


# VER EVIDENCIA 0
@login_required
def ver_evidencias_0(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencias = Portafolio.objects.filter(producto=producto)
    return render(request, 'Proyectos/ver_evidencias_0.html', {'evidencias': evidencias, 'proyecto': proyecto})

# VER EVIDENCIA 1
@login_required
def ver_evidencias_1(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencias = Portafolio.objects.filter(
        proyecto=producto.proyecto,
        producto=producto,
        avance_1_nombre__isnull=False,
        avance_1_descripcion__isnull=False,
        avance_1_link__isnull=False,
        avance_1_adjunto__isnull=False,
        avance_1_fecha__isnull=False,
        avance_1_estado__isnull=False,
        avance_1_correcciones_realizadas__isnull=False,
    )
    return render(request, 'Proyectos/ver_evidencias_1.html', {'evidencias': evidencias, 'proyecto': proyecto})

# VER EVIDENCIA 2
@login_required
def ver_evidencias_2(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencias = Portafolio.objects.filter(
        proyecto=producto.proyecto,
        producto=producto,
        avance_2_descripcion__isnull=False,
        avance_2_link__isnull=False,
        avance_2_adjunto__isnull=False,
        avance_2_fecha__isnull=False,
        avance_1_estado__isnull=False,
        avance_1_correcciones_realizadas__isnull=False,
    )
    return render(request, 'Proyectos/ver_evidencias_2.html', {'evidencias': evidencias, 'proyecto': proyecto})

# VER EVIDENCIA 3
@login_required
def ver_evidencias_3(request, proyecto_id, producto_id):
    try:
        proyecto = Proyecto.objects.get(pk=proyecto_id, usuario=request.user)
    except Proyecto.DoesNotExist:
        return render(request, 'error_pages/Users_Pagina_Error.html', status=404)
        
    producto = get_object_or_404(Producto, id=producto_id, proyecto=proyecto)
    evidencias = Portafolio.objects.filter(
        proyecto=producto.proyecto,
        producto=producto,
        avance_3_descripcion__isnull=False,
        avance_3_link__isnull=False,
        avance_3_adjunto__isnull=False,
        avance_3_fecha__isnull=False,
        avance_1_estado__isnull=False,
        avance_1_correcciones_realizadas__isnull=False,
    )
    return render(request, 'Proyectos/ver_evidencias_3.html', {'evidencias': evidencias, 'proyecto': proyecto})

