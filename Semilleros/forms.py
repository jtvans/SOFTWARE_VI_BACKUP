from django import forms
from .models import Semillero
from Users.models import Usuario
from django.forms import DateInput


class SemilleroForm(forms.ModelForm):
    grupo_investigacion = forms.ChoiceField(choices=Usuario.GRUPOS_INVESTIGACION)
    linea_investigacion = forms.ChoiceField(choices=[])
    tematica_estudio = forms.CharField(max_length=100)
    justificacion_semillero = forms.CharField(widget=forms.Textarea, required=True)
    nivel_formacion = forms.CharField(max_length=200)

    NIVEL_INGLES = (
        ('bajo','Bajo'),
        ('medio','Medio'),
        ('alto','Alto'),
    )
    nivel_ingles_habla = forms.ChoiceField(choices=NIVEL_INGLES)
    nivel_ingles_lee = forms.ChoiceField(choices=NIVEL_INGLES)
    nivel_ingles_entiende = forms.ChoiceField(choices=NIVEL_INGLES)
    nivel_ingles_escribe = forms.ChoiceField(choices=NIVEL_INGLES)

    DOCENTE_INVESTIGADOR = (
        ('--', '--'),
        ('si', 'Sí'),
        ('no', 'No'),
    )
    docente_investigador = forms.ChoiceField(choices=DOCENTE_INVESTIGADOR)
    tematica = forms.CharField(max_length=200, required=False)
    institucion = forms.CharField(max_length=200, required=False)
    horas = forms.CharField(max_length=200, required=False)
    fecha = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    tematica_2 = forms.CharField(max_length=200, required=False)
    institucion_2 = forms.CharField(max_length=200, required=False)
    horas_2 = forms.CharField(max_length=200, required=False)
    fecha_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    tematica_3 = forms.CharField(max_length=200, required=False)
    institucion_3 = forms.CharField(max_length=200, required=False)
    horas_3 = forms.CharField(max_length=200, required=False)
    fecha_3 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    TIENE_CVLAC = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_cvlac = forms.ChoiceField(choices=TIENE_CVLAC)

    TIENE_PROYECTOS_CHOICES = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_proyectos = forms.ChoiceField(choices=TIENE_PROYECTOS_CHOICES)

    class Meta:
        model = Semillero
        fields = ['nombre_semillero', 'facultad', 'programa', 'grupo_investigacion', 'linea_investigacion', 'tematica_estudio', 'justificacion_semillero', 'nombre', 'identificacion', 'telefono', 'correo', 'cvlac', 'nivel_formacion','nivel_ingles_habla', 'nivel_ingles_lee', 'nivel_ingles_entiende', 'nivel_ingles_escribe', 'tiene_cvlac','docente_investigador','tematica','institucion','horas','fecha','tematica_2','institucion_2','horas_2','fecha_2','tematica_3','institucion_3','horas_3','fecha_3', 'tiene_proyectos']

    # GRUPOS - LINEAS INVESTIGACION
    #-------------------------------------------------------------------------------------------------------------
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
    #-------------------------------------------------------------------------------------------------------------

