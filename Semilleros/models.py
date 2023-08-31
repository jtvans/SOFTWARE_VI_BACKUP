from django.db import models
from django.contrib.auth.models import User
from Users.models import Usuario_Estudiante
from Proyectos.models import Proyecto

from django.shortcuts import render, redirect
from django.core.validators import MaxValueValidator



# --------------------------------------------- SEMILLEROS ---------------------------------------------------

# SEMILLEROS
class Semillero(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #proyectos = models.ManyToManyField(Proyecto, blank=True)

    # INFORMACIÓN GENERAL DEL SEMILLERO
    fecha_inscripcion = models.DateField(auto_now_add=True)
    nombre_semillero = models.CharField(max_length=200)
    facultad = models.CharField(max_length=100)
    programa = models.CharField(max_length=100)
    grupo_investigacion = models.CharField(max_length=200)
    linea_investigacion = models.CharField(max_length=200)
    tematica_estudio = models.CharField(max_length=200)
    justificacion_semillero = models.CharField(max_length=500)

    # IDENTIFICACIÓN DEL DOCENTE COORDINADOR DEL SEMILLERO
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20)
    lugar_expedicion = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField(blank=True, null=True, default=None)
    lugar_nacimiento = models.CharField(max_length=40)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=300)
    correo = models.EmailField(max_length=100)
    nivel_formacion = models.CharField(max_length=100)

    NIVEL_INGLES = [
        ('bajo','Bajo'),
        ('medio','Medio'),
        ('alto','Alto'),
    ]

    nivel_ingles_habla = models.CharField(max_length=300, choices=NIVEL_INGLES)
    nivel_ingles_lee = models.CharField(max_length=300, choices=NIVEL_INGLES)
    nivel_ingles_entiende = models.CharField(max_length=300, choices=NIVEL_INGLES)
    nivel_ingles_escribe = models.CharField(max_length=300, choices=NIVEL_INGLES)

    # CURSOS DE FORMACIÓN EN INVESTIGACIÓN
    DOCENTE_INVESTIGADOR = (
        ('si', 'Sí'),
        ('no', 'No'),
    )
    docente_investigador = models.CharField(max_length=2, choices=DOCENTE_INVESTIGADOR, default='si')

    tematica = models.CharField(max_length=200, blank=True)
    institucion = models.CharField(max_length=200, blank=True)
    horas = models.CharField(max_length=200, blank=True)
    fecha = models.DateField(blank=True, null=True, default=None)
    tematica_2 = models.CharField(max_length=200, blank=True)
    institucion_2 = models.CharField(max_length=200, blank=True)
    horas_2 = models.CharField(max_length=200, blank=True)
    fecha_2 = models.DateField(blank=True, null=True, default=None)
    tematica_3 = models.CharField(max_length=200, blank=True)
    institucion_3 = models.CharField(max_length=200, blank=True)
    horas_3 = models.CharField(max_length=200, blank=True)
    fecha_3 = models.DateField(blank=True, null=True, default=None)

    # Experiencia en investigacion
    TIENE_CVLAC = (
        ('si', 'Sí'),
        ('no', 'No'),
    )
    tiene_cvlac = models.CharField(max_length=2, choices=TIENE_CVLAC, default='no')
    cvlac = models.URLField(blank=True)

    TIENE_PROYECTOS_CHOICES = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    tiene_proyectos = models.CharField(max_length=2, choices=TIENE_PROYECTOS_CHOICES, default='no')

    Se_nombre_proyecto = models.CharField(max_length=200, blank=True)
    Se_institucion = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion = models.CharField(max_length=200, blank=True)
    Se_fecha = models.DateField(blank=True, null=True, default=None)
    
    Se_nombre_proyecto_2 = models.CharField(max_length=200, blank=True)
    Se_institucion_2 = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion_2 = models.CharField(max_length=200, blank=True)
    Se_fecha_2 = models.DateField(blank=True, null=True, default=None)

    Se_nombre_proyecto_3 = models.CharField(max_length=200, blank=True)
    Se_institucion_3 = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion_3 = models.CharField(max_length=200, blank=True)
    Se_fecha_3 = models.DateField(blank=True, null=True, default=None)

    # ACTIVIDADES INTER E INTRA INSTITUCIONALES
    ACTIVIDADES = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    actividades = models.CharField(max_length=2, choices=ACTIVIDADES, default='no')
    nombre_grupo = models.CharField(max_length=200, blank=True)
    actividad_tema = models.CharField(max_length=200, blank=True)
    tipo_vinculacion = models.CharField(max_length=200, blank=True)
    fecha_actividad = models.DateField(blank=True, null=True, default=None)

    nombre_grupo_2 = models.CharField(max_length=200, blank=True)
    actividad_tema_2 = models.CharField(max_length=200, blank=True)
    tipo_vinculacion_2 = models.CharField(max_length=200, blank=True)
    fecha_actividad_2 = models.DateField(blank=True, null=True, default=None)

    nombre_grupo_3 = models.CharField(max_length=200, blank=True)
    actividad_tema_3 = models.CharField(max_length=200, blank=True)
    tipo_vinculacion_3 = models.CharField(max_length=200, blank=True)
    fecha_actividad_3 = models.DateField(blank=True, null=True, default=None)

    aprobacion = models.BooleanField(default=False)
    aprobacion_firma = models.CharField(max_length=200, blank=True)
    aprobado_fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    

# INSCRIPCION A SEMILLERO
class InscripcionSemillero(models.Model):
    semillero = models.ForeignKey(Semillero, on_delete=models.CASCADE)
    user_e = models.ForeignKey(Usuario_Estudiante, on_delete=models.CASCADE)

    TIPO_SOLICITANTE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('otro', 'Otro (indique cual)'),
    )
    tipo_solicitante = models.CharField(max_length=20, choices=TIPO_SOLICITANTE_CHOICES)
    tipo_solicitante_otro = models.CharField(max_length=100, blank=True)
    nombre_e = models.CharField(max_length=100)
    identificacion_e = models.CharField(max_length=20)
    telefono_e = models.CharField(max_length=20)
    correo_e = models.EmailField(max_length=100)
    programa_e = models.CharField(max_length=100, blank=True)

    lugar_expedicion_e = models.CharField(max_length=40)
    fecha_nacimiento_e = models.DateField(blank=True, null=True, default=None)
    lugar_nacimiento_e = models.CharField(max_length=40)
    direccion_e = models.CharField(max_length=40)

    fecha_inscripcion_e = models.DateTimeField(auto_now_add=True)
    estado_e = models.BooleanField(default=False)

    NIVEL_INGLES_E = [
        ('bajo','Bajo'),
        ('medio','Medio'),
        ('alto','Alto'),
    ]
    nivel_ingles_habla_e = models.CharField(max_length=300, choices=NIVEL_INGLES_E)
    nivel_ingles_lee_e = models.CharField(max_length=300, choices=NIVEL_INGLES_E)
    nivel_ingles_entiende_e = models.CharField(max_length=300, choices=NIVEL_INGLES_E)
    nivel_ingles_escribe_e = models.CharField(max_length=300, choices=NIVEL_INGLES_E)

    semestre_actual = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10)])
    año_ingreso = models.DateField(blank=True, null=True, default=None)
    fecha_grado = models.DateField(blank=True, null=True, default=None)

    CURSOS_INVES = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    cursos_inves = models.CharField(max_length=2, choices=CURSOS_INVES, default='no')

    tematica_e = models.CharField(max_length=200, blank=True)
    institucion_e = models.CharField(max_length=200, blank=True)
    horas_e = models.CharField(max_length=3, blank=True)
    fecha_e = models.DateField(blank=True, null=True, default=None)

    tematica_e_2 = models.CharField(max_length=200, blank=True)
    institucion_e_2 = models.CharField(max_length=200, blank=True)
    horas_e_2 = models.CharField(max_length=3, blank=True)
    fecha_e_2 = models.DateField(blank=True, null=True, default=None)

    TIENE_CVLAC_E = (
        ('si', 'Sí'),
        ('no', 'No'),
    )
    tiene_cvlac_e = models.CharField(max_length=2, choices=TIENE_CVLAC_E, default='no')
    cvlac_e = models.URLField(blank=True)

    PARTICIPA_PROYECTOS = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    participa_proyectos = models.CharField(max_length=2, choices=PARTICIPA_PROYECTOS, default='no')

    Se_nombre_proyecto_e = models.CharField(max_length=200, blank=True)
    Se_institucion_e = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion_e = models.CharField(max_length=200, blank=True)
    Se_fecha_e = models.DateField(blank=True, null=True, default=None)
    
    Se_nombre_proyecto_e_2 = models.CharField(max_length=200, blank=True)
    Se_institucion_e_2 = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion_e_2 = models.CharField(max_length=200, blank=True)
    Se_fecha_e_2 = models.DateField(blank=True, null=True, default=None)

    Se_nombre_proyecto_e_3 = models.CharField(max_length=200, blank=True)
    Se_institucion_e_3 = models.CharField(max_length=200, blank=True)
    Se_tipo_vinculacion_e_3 = models.CharField(max_length=200, blank=True)
    Se_fecha_e_3 = models.DateField(blank=True, null=True, default=None)

    ACTIVIDADES_E = (
        ('no', 'No'),
        ('si', 'Sí'),
    )
    actividades_e = models.CharField(max_length=2, choices=ACTIVIDADES_E, default='no')
    nombre_grupo_e = models.CharField(max_length=200, blank=True)
    actividad_tema_e = models.CharField(max_length=200, blank=True)
    tipo_vinculacion_e = models.CharField(max_length=200, blank=True)
    fecha_actividad_e = models.DateField(blank=True, null=True, default=None)

    nombre_grupo_e_2 = models.CharField(max_length=200, blank=True)
    actividad_tema_e_2 = models.CharField(max_length=200, blank=True)
    tipo_vinculacion_e_2 = models.CharField(max_length=200, blank=True)
    fecha_actividad_e_2 = models.DateField(blank=True, null=True, default=None)

    semillero_proyecto_interes = models.CharField(max_length=100, blank=True)
    proyecto_interes = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, blank=True, null=True)

    linea_sublinea = models.CharField(max_length=100, blank=True)
    horas_semanales = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(168)])
    TIPO_SEMILLERO = (
        ('unica','Fase Unica'),
    )
    tipo_semillero = models.CharField(max_length=20, choices=TIPO_SEMILLERO)


# ACTIVIDADES DEL SEMILLERO
class ActividadesSemillero(models.Model):
    user_e = models.ForeignKey(Usuario_Estudiante, on_delete=models.CASCADE)
    semillero = models.ForeignKey(Semillero, on_delete=models.CASCADE)
    inscripcion = models.ForeignKey(InscripcionSemillero, on_delete=models.CASCADE)

    nombre_estuidante_actividad_e = models.CharField(max_length=100)
    identificacion_estuidante_actividad_e = models.CharField(max_length=20)

    nombre_actividad_e = models.CharField(max_length=200, blank=True)
    descripcion_actividad_e = models.CharField(max_length=200, blank=True)
    fecha_actividad_inicio_e = models.DateField(blank=True, null=True, default=None)
    fecha_actividad_final_e = models.DateField(blank=True, null=True, default=None)
    lugar_actividad_e = models.CharField(max_length=200, blank=True)
    ciudad_actividad_e = models.CharField(max_length=200, blank=True)

    participantes_actividad_e = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    adjunto_actividad_e = models.FileField(upload_to ="Adjuntos_Actividades_E/", blank=True, null=True)


