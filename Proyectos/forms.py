from django import forms
from .models import Proyecto, Actividad, Producto #, PlanTrabajo, CategoriaProducto, TipoProducto
from Users.models import Usuario
from django.forms import DateInput

#----------------- // ----------------- PROYECTO ----------------- \\ -----------------

class ProyectoForm(forms.ModelForm):
    grupo_investigacion = forms.ChoiceField(choices=Usuario.GRUPOS_INVESTIGACION)
    linea_investigacion = forms.ChoiceField(choices=[])

    fecha_inicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_finalizacion = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    problema_pregunta = forms.CharField(widget=forms.Textarea, required=True)
    justificacion = forms.CharField(widget=forms.Textarea, required=True)
    objetivo_general = forms.CharField(widget=forms.Textarea, required=True)
    objetivos_especificos = forms.CharField(widget=forms.Textarea, required=True)
    metodologia_propuesta = forms.CharField(widget=forms.Textarea, required=True)
    estado_arte = forms.CharField(widget=forms.Textarea, required=True)
    impactos_esperados = forms.CharField(widget=forms.Textarea, required=True)
    archivo_adjunto = forms.FileField(required=False)

    class Meta:
        model = Proyecto
        fields = ['titulo', 'palabras_clave', 'facultad', 'programa', 'grupo_investigacion', 'linea_investigacion', 'semillero_investigacion', 'nombre', 'identificacion', 'telefono', 'correo', 'cvlac', 'co_investigador_1_nombre', 'co_investigador_1_identificacion', 'co_investigador_1_telefono', 'co_investigador_1_correo', 'co_investigador_1_formacion', 'co_investigador_1_institucion', 'co_investigador_1_cvlac', 'fecha_inicio', 'fecha_finalizacion', 'problema_pregunta', 'justificacion', 'objetivo_general', 'objetivos_especificos', 'metodologia_propuesta', 'estado_arte', 'impactos_esperados','comite_etica','archivo_adjunto']

    
    # GRUPOS - LINEAS INVESTIGACION
    #-------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'grupo_investigacion' in self.data:
            grupo = self.data.get('grupo_investigacion')
            self.fields['linea_investigacion'].choices = self.get_lineas_investigacion_choices(grupo)
        elif self.instance.pk:
            grupo = self.instance.grupo_investigacion
            self.fields['linea_investigacion'].choices = self.get_lineas_investigacion_choices(grupo)

    def get_lineas_investigacion_choices(self, grupo_investigacion):
        if grupo_investigacion == 'Aglalia':
            return [
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Nuevas tecnologías e inteligencia artificial', 'Nuevas tecnologías e inteligencia artificial'),
                ('Sistemas de información e ingeniería de software', 'Sistemas de información e ingeniería de software'),
            ]
        elif grupo_investigacion == 'ProCont':
            return [
                ('Contabilidad social y ambiental', 'Contabilidad social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif grupo_investigacion == 'DehJüs':
            return [
                ('Conflictos instituciones jurídicas y nuevas tendencias del derecho privado', 'Conflictos instituciones jurídicas y nuevas tendencias del derecho privado'),
                ('Derecho público y justicia', 'Derecho público y justicia'),
                ('Desarrollo humano salud mental y psicología forense', 'Desarrollo humano salud mental y psicología forense'),
                ('Género sociedad y derechos humanos', 'Género sociedad y derechos humanos'),
            ]
        elif grupo_investigacion == 'TES':
            return [
                ('Bilinguismo', 'Bilinguismo'),
                ('Infancia y desarrollo social', 'Infancia y desarrollo social'),
                ('Neuropsicologia comportamiento y aprendizaje', 'Neuropsicologia comportamiento y aprendizaje'),
                ('Practica pedagógica investigativa', 'Practica pedagógica investigativa'),
                ('Psicologia educativa y evolutiva', 'Psicologia educativa y evolutiva'),
                ('Psicologia social y comunitaria', 'Psicologia social y comunitaria'),
            ]
        elif grupo_investigacion == 'GECAES':
            return [
                ('Capital social y ambiental', 'Capital social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif grupo_investigacion == 'Gestion e Innovacion':
            return [
                ('Gestión e innovación', 'Gestión e innovación'),
                ('Innovación y gestión turística', 'Innovación y gestión turística'),
            ]
        elif grupo_investigacion == 'IC':
            return [
                ('Ciudadanía genero y sociedad', 'Ciudadanía genero y sociedad'),
                ('Innovaciones sociales', 'Innovaciones sociales'),
            ]
        elif grupo_investigacion == 'LyS':
            return [
                ('Derecho y gestión de políticas publicas', 'Derecho y gestión de políticas publicas'),
                ('Derecho y sociedad', 'Derecho y sociedad'),
                ('Derecho y sujetos de especial protección constitucional', 'Derecho y sujetos de especial protección constitucional')
            ]
        elif grupo_investigacion == 'Gisela':
            return [
                ('Gestión organizacional, desarrollo y sociedad', 'Gestión organizacional, desarrollo y sociedad'),
                ('Competitividad e innovacion en pymes', 'Competitividad e innovacion en pymes'),
            ]
        elif grupo_investigacion == 'LAW':
            return [
                ('Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación', 'Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación'),
                ('Propiedad intelectual', 'Propiedad intelectual'),
                ('Práctica jurídica', 'Práctica jurídica'),
                ('Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías', 'Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías'),
            ]
        elif grupo_investigacion == 'Business Intelligence':
            return [
                ('Comercio y negocios internacionales', 'Comercio y negocios internacionales'),
                ('Logistica nacional e internacional', 'Logistica nacional e internacional'),
            ]
        elif grupo_investigacion == 'Americana Emprendedora':
            return [
                ('Emprendimiento ecosistemas de emprendimiento e innovación', 'Emprendimiento ecosistemas de emprendimiento e innovación'),
                ('Emprendimiento de mujeres y comunidades', 'Emprendimiento de mujeres y comunidades'),
            ]
        elif grupo_investigacion == 'PSI Context':
            return [
                ('Desarrollo humano y problemáticas sociales', 'Desarrollo humano y problemáticas sociales'),
                ('Salud y bienestar', 'Salud y bienestar'),
            ]
        elif grupo_investigacion == 'Engineeri':
            return [
                ('Diseño y gestión de Sistemas productivos y logísticos', 'Diseño y gestión de Sistemas productivos y logísticos'),
                ('Innovación y gestión tecnológica', 'Innovación y gestión tecnológica'),
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Sistemas integrados de procesos y gestión', 'Sistemas integrados de procesos y gestión'),
            ]
        elif grupo_investigacion == 'SeHaT':
            return [
                ('Emprendimiento e innovación', 'Emprendimiento e innovación'),
                ('Salud Ocupacional', 'Salud Ocupacional'),
                ('Seguridad Industrial', 'Seguridad Industrial'),
            ]
        else:
            return []
    #-------------------------------------------------------------------

class ActividadForm(forms.ModelForm):
    DURACION_CHOICES = (
        ('semanas', 'Por Semanas'),
        ('meses', 'Por Meses'),
    )
    tipo_duracion = forms.ChoiceField(choices=DURACION_CHOICES)
    duracion = forms.IntegerField()
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'duracion', 'tipo_duracion']

#----------------- // ----------------- PRODUCTO ----------------- \\ -----------------

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'tipo_producto']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'id_categoria'}),
            'tipo_producto': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_producto'}),
        }


#----------------- // ----------------- PORTAFOLIO - AVANCES ----------------- \\ -----------------

class AvanceEstado0Form(forms.Form):
    avance_justificacion = forms.CharField(widget=forms.Textarea)


class AvanceEstado1Form(forms.Form):
    avance_nombre = forms.CharField(max_length=100)
    avance_descripcion = forms.CharField(widget=forms.Textarea)
    avance_link = forms.URLField(required=False)
    avance_adjunto = forms.FileField(required=False)
    avance_correcciones_realizadas = forms.BooleanField(required=False, initial=False)


class AvanceEstado2Form(forms.Form):
    avance_descripcion = forms.CharField(widget=forms.Textarea)
    avance_link = forms.URLField(required=False)
    avance_adjunto = forms.FileField(required=False)
    avance_correcciones_realizadas = forms.BooleanField(required=False, initial=False)


class AvanceEstado3Form(forms.Form):
    avance_descripcion = forms.CharField(widget=forms.Textarea)
    avance_link = forms.URLField(required=False)
    avance_adjunto = forms.FileField(required=False)
    avance_correcciones_realizadas = forms.BooleanField(required=False, initial=False)