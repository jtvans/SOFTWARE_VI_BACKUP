from django.db import models
from django.contrib.auth.models import User
from Proyectos.models import Proyecto

# --------------------------------------------- SEMILLEROS ---------------------------------------------------

# SEMILLEROS
class Semillero(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

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
    proyectos = models.ManyToManyField(Proyecto, blank=True)

    def __str__(self):
        return self.nombre