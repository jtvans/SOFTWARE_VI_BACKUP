from django.contrib import admin
from .models import Proyecto, Actividad, Producto, Portafolio

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'usuario', 'fecha_inscripcion', 'facultad', 'programa',
        'porcentaje_cumplimiento_total', 'aprobado'
    )
    list_filter = ('fecha_inscripcion', 'facultad', 'programa', 'aprobado')
    search_fields = ('titulo', 'usuario__username', 'usuario__email')
    ordering = ('-fecha_inscripcion',)
    
    # Agrega ambos campos readonly en una sola línea
    readonly_fields = ('porcentaje_cumplimiento_total', 'aprobado_fecha')

    fieldsets = (
        ('Información General', {
            'fields': (
                'usuario', 'titulo', 'palabras_clave', 'facultad', 'programa',
                'grupo_investigacion', 'linea_investigacion', 'semillero_investigacion',
                'imagen'
            ),
        }),
        ('Investigadores Participantes', {
            'fields': (
                'nombre', 'identificacion', 'telefono', 'correo', 'cvlac'
            ),
        }),
        ('Co-Investigadores', {
            'fields': (
                'co_investigador_1_nombre', 'co_investigador_1_identificacion',
                'co_investigador_1_telefono', 'co_investigador_1_correo',
                'co_investigador_1_formacion', 'co_investigador_1_institucion',
                'co_investigador_1_cvlac'
            ),
        }),
        ('Duración del Proyecto', {
            'fields': ('fecha_inicio', 'fecha_finalizacion'),
        }),
        ('Descripción del Proyecto', {
            'fields': (
                'problema_pregunta', 'justificacion', 'objetivo_general',
                'objetivos_especificos', 'metodologia_propuesta', 'estado_arte',
                'impactos_esperados'
            ),
        }),
        ('Ética y Aprobación', {
            'fields': (
                'comite_etica', 'archivo_adjunto', 'aprobado', 'aprobado_nombre',
                'aprobado_fecha', 'aprobado_adjunto'
            ),
        }),
        ('Porcentaje de Cumplimiento', {
            'fields': ('porcentaje_cumplimiento_total',),
        }),
    )


#Actividades-proyecto
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proyecto', 'duracion', 'tipo_duracion')
    list_filter = ('proyecto', 'tipo_duracion')
    search_fields = ('nombre', 'proyecto__titulo')
    ordering = ('nombre',)


#Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('tipo_producto', 'proyecto', 'categoria', 'cantidad')
    list_filter = ('proyecto', 'categoria')
    search_fields = ('tipo_producto', 'proyecto__titulo')
    ordering = ('tipo_producto',)


#Portafolio
@admin.register(Portafolio)
class PortafolioAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'producto', 'avance_1_estado', 'avance_2_estado', 'avance_3_estado')
    list_filter = ('proyecto', 'producto', 'avance_1_estado', 'avance_2_estado', 'avance_3_estado')
    search_fields = ('proyecto__titulo', 'producto__tipo_producto')
    ordering = ('proyecto', 'producto')
