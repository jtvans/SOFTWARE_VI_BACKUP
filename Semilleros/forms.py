from django import forms
from .models import Semillero, InscripcionSemillero, ActividadesSemillero
from Users.models import Usuario
from django.forms import DateInput
import datetime
from django.core.validators import MaxValueValidator




class SemilleroForm(forms.ModelForm):
    nombre_semillero = forms.CharField(max_length=200)
    grupo_investigacion = forms.ChoiceField(choices=Usuario.GRUPOS_INVESTIGACION)
    linea_investigacion = forms.ChoiceField(choices=[])
    tematica_estudio = forms.CharField(max_length=100)
    justificacion_semillero = forms.CharField(widget=forms.Textarea, required=True)
    nivel_formacion = forms.CharField(max_length=200)

    lugar_expedicion = forms.CharField(max_length=40)
    fecha_nacimiento = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    lugar_nacimiento = forms.CharField(max_length=40)
    direccion = forms.CharField(max_length=40)

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
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_cvlac = forms.ChoiceField(choices=TIENE_CVLAC)

    TIENE_PROYECTOS_CHOICES = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_proyectos = forms.ChoiceField(choices=TIENE_PROYECTOS_CHOICES)

    Se_nombre_proyecto = forms.CharField(max_length=200, required=False)
    Se_institucion = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion = forms.CharField(max_length=200, required=False)
    Se_fecha = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    
    Se_nombre_proyecto_2 = forms.CharField(max_length=200, required=False)
    Se_institucion_2 = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion_2 = forms.CharField(max_length=200, required=False)
    Se_fecha_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    Se_nombre_proyecto_3 = forms.CharField(max_length=200, required=False)
    Se_institucion_3 = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion_3 = forms.CharField(max_length=200, required=False)
    Se_fecha_3 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    ACTIVIDADES = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    actividades = forms.ChoiceField(choices=ACTIVIDADES)
    nombre_grupo = forms.CharField(max_length=200, required=False)
    actividad_tema = forms.CharField(max_length=200, required=False)
    tipo_vinculacion = forms.CharField(max_length=200, required=False)
    fecha_actividad = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    nombre_grupo_2 = forms.CharField(max_length=200, required=False)
    actividad_tema_2 = forms.CharField(max_length=200, required=False)
    tipo_vinculacion_2 = forms.CharField(max_length=200, required=False)
    fecha_actividad_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    nombre_grupo_3 = forms.CharField(max_length=200, required=False)
    actividad_tema_3 = forms.CharField(max_length=200, required=False)
    tipo_vinculacion_3 = forms.CharField(max_length=200, required=False)
    fecha_actividad_3 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)



    class Meta:
        model = Semillero
        fields = ['nombre_semillero', 'facultad', 'programa', 'grupo_investigacion', 'linea_investigacion', 'tematica_estudio', 'justificacion_semillero', 'nombre', 'identificacion', 'lugar_expedicion', 'fecha_nacimiento', 'lugar_nacimiento', 'direccion','telefono', 'correo', 'cvlac', 'nivel_formacion','nivel_ingles_habla', 'nivel_ingles_lee', 'nivel_ingles_entiende', 'nivel_ingles_escribe', 'tiene_cvlac','docente_investigador','tematica','institucion','horas','fecha','tematica_2','institucion_2','horas_2','fecha_2','tematica_3','institucion_3','horas_3','fecha_3', 'tiene_proyectos','actividades','nombre_grupo','actividad_tema','tipo_vinculacion','fecha_actividad', 'nombre_grupo_2','actividad_tema_2','tipo_vinculacion_2','fecha_actividad_2', 'nombre_grupo_3','actividad_tema_3','tipo_vinculacion_3','fecha_actividad_3','Se_nombre_proyecto','Se_institucion','Se_tipo_vinculacion','Se_fecha', 'Se_nombre_proyecto_2','Se_institucion_2','Se_tipo_vinculacion_2','Se_fecha_2', 'Se_nombre_proyecto_3','Se_institucion_3','Se_tipo_vinculacion_3','Se_fecha_3']

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


# FORM INSCRIPCION A SEMILLERO - ESTUDIANTE
class InscripcionSemilleroForm(forms.Form):
    nombre_e = forms.CharField(max_length=100)
    identificacion_e = forms.CharField(max_length=20)
    telefono_e = forms.CharField(max_length=20)
    correo_e = forms.EmailField(max_length=100)
    programa_e = forms.CharField(max_length=100)

    lugar_expedicion_e = forms.CharField(max_length=40)
    fecha_nacimiento_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    lugar_nacimiento_e = forms.CharField(max_length=40)
    direccion_e = forms.CharField(max_length=40)

    TIPO_SOLICITANTE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('otro', 'Otro (indique cual)'),
    )
    tipo_solicitante = forms.ChoiceField(choices=TIPO_SOLICITANTE_CHOICES)
    tipo_solicitante_otro = forms.CharField(max_length=100, required=False)

    NIVEL_INGLES_E = (
        ('bajo','Bajo'),
        ('medio','Medio'),
        ('alto','Alto'),
    )
    nivel_ingles_habla_e = forms.ChoiceField(choices=NIVEL_INGLES_E)
    nivel_ingles_lee_e = forms.ChoiceField(choices=NIVEL_INGLES_E)
    nivel_ingles_entiende_e = forms.ChoiceField(choices=NIVEL_INGLES_E)
    nivel_ingles_escribe_e = forms.ChoiceField(choices=NIVEL_INGLES_E)

    semestre_actual = forms.IntegerField(max_value=10, min_value=1)
    año_ingreso = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    fecha_grado = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    CURSOS_INVES = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    cursos_inves = forms.ChoiceField(choices=CURSOS_INVES)

    tematica_e = forms.CharField(max_length=200, required=False)
    institucion_e = forms.CharField(max_length=200, required=False)
    horas_e = forms.CharField(max_length=3, required=False)
    fecha_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    tematica_e_2 = forms.CharField(max_length=200, required=False)
    institucion_e_2 = forms.CharField(max_length=200, required=False)
    horas_e_2 = forms.CharField(max_length=3, required=False)
    fecha_e_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    TIENE_CVLAC_E = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_cvlac_e = forms.ChoiceField(choices=TIENE_CVLAC_E)
    cvlac_e = forms.URLField(required=False)
    
    PARTICIPA_PROYECTOS = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    participa_proyectos = forms.ChoiceField(choices=PARTICIPA_PROYECTOS)

    Se_nombre_proyecto_e = forms.CharField(max_length=200, required=False)
    Se_institucion_e = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion_e = forms.CharField(max_length=200, required=False)
    Se_fecha_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    
    Se_nombre_proyecto_e_2 = forms.CharField(max_length=200, required=False)
    Se_institucion_e_2 = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion_e_2 = forms.CharField(max_length=200, required=False)
    Se_fecha_e_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    Se_nombre_proyecto_e_3 = forms.CharField(max_length=200, required=False)
    Se_institucion_e_3 = forms.CharField(max_length=200, required=False)
    Se_tipo_vinculacion_e_3 = forms.CharField(max_length=200, required=False)
    Se_fecha_e_3 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)


    ACTIVIDADES_E = (
        ('--', '--'),
        ('no', 'No'),
        ('si', 'Sí'),
    )
    actividades_e = forms.ChoiceField(choices=ACTIVIDADES_E)
    nombre_grupo_e = forms.CharField(max_length=200, required=False)
    actividad_tema_e = forms.CharField(max_length=200, required=False)
    tipo_vinculacion_e = forms.CharField(max_length=200, required=False)
    fecha_actividad_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    nombre_grupo_e_2 = forms.CharField(max_length=200, required=False)
    actividad_tema_e_2 = forms.CharField(max_length=200, required=False)
    tipo_vinculacion_e_2 = forms.CharField(max_length=200, required=False)
    fecha_actividad_e_2 = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    semillero_proyecto_interes = forms.CharField(max_length=200, required=False)
    proyecto_interes = forms.CharField(max_length=200, required=False)

    linea_sublinea = forms.CharField(max_length=200, required=False)
    horas_semanales = forms.IntegerField(max_value=168, min_value=1)
    
    TIPO_SEMILLERO = (
        ('unica','Fase Unica'),
    )
    tipo_semillero = forms.ChoiceField(choices=TIPO_SEMILLERO)


# FORM ACTIVIDADES SEMILLERO - ESTUDIANTE
class ActividadesSemilleroForm(forms.ModelForm):
    nombre_estuidante_actividad_e = forms.CharField(max_length=100)
    identificacion_estuidante_actividad_e = forms.CharField(max_length=20)

    nombre_actividad_e = forms.CharField(max_length=100)
    descripcion_actividad_e = forms.CharField(max_length=200)
    fecha_actividad_inicio_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    fecha_actividad_final_e = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    lugar_actividad_e = forms.CharField(max_length=100)
    ciudad_actividad_e = forms.CharField(max_length=100)

    participantes_actividad_e = forms.IntegerField(max_value=10, min_value=0)
    adjunto_actividad_e = forms.FileField(required=False, label='Adjuntar Evidencia')

    class Meta:
        model = ActividadesSemillero
        fields = ['nombre_estuidante_actividad_e', 'identificacion_estuidante_actividad_e', 'nombre_actividad_e', 'descripcion_actividad_e', 'fecha_actividad_inicio_e', 'fecha_actividad_final_e', 'lugar_actividad_e', 'ciudad_actividad_e', 'participantes_actividad_e', 'adjunto_actividad_e']

# FORM ACTIVIDADES SEMILLERO [PARTICIPANTES] - ESTUDIANTE
class BuscarEstudianteForm(forms.Form):
    cedula_estudiante = forms.CharField(max_length=20, label='Cédula del Estudiante')