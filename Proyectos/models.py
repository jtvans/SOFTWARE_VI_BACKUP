# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# from django.core.validators import MinValueValidator
from django.db import models

# --------------------------------------------- PROYECTOS ---------------------------------------------------
User = get_user_model()


# PROYECTOS
class Proyecto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # INSCRIPCION PROYECTO
    fecha_inscripcion = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=200)
    palabras_clave = models.CharField(max_length=200)
    facultad = models.CharField(max_length=100)
    programa = models.CharField(max_length=100)
    grupo_investigacion = models.CharField(max_length=200)
    linea_investigacion = models.CharField(max_length=200)
    semillero_investigacion = models.CharField(max_length=200)
    imagen = models.CharField(max_length=200)

    # INVESTIGADORES PARTICIPANTES ---- Datos del investigador
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20)
    telefono = models.CharField(max_length=300)
    correo = models.EmailField(max_length=100)
    cvlac = models.URLField(blank=True)

    # CO-INVESTIGADORES
    co_investigador_1_nombre = models.CharField(max_length=100, blank=True)
    co_investigador_1_identificacion = models.CharField(
        max_length=20,
        blank=True,
    )
    co_investigador_1_telefono = models.CharField(max_length=300, blank=True)
    co_investigador_1_correo = models.EmailField(max_length=100, blank=True)
    co_investigador_1_formacion = models.CharField(max_length=100, blank=True)
    co_investigador_1_institucion = models.CharField(
        max_length=200,
        blank=True,
    )
    co_investigador_1_cvlac = models.URLField(blank=True)

    # Duración del proyecto
    fecha_inicio = models.DateField(blank=True)
    fecha_finalizacion = models.DateField(blank=True)

    # DESCRIPCIÓN DEL PROYECTO
    problema_pregunta = models.TextField(blank=True)
    justificacion = models.TextField(blank=True)
    objetivo_general = models.TextField(blank=True)
    objetivos_especificos = models.TextField(blank=True)
    metodologia_propuesta = models.TextField(blank=True)
    estado_arte = models.TextField(blank=True)
    impactos_esperados = models.TextField(blank=True)

    COMITE_ETICA_CHOICES = (
        ("si", "Sí"),
        ("no", "No"),
    )
    comite_etica = models.CharField(
        max_length=2, choices=COMITE_ETICA_CHOICES, default="no"
    )
    archivo_adjunto = models.FileField(
        upload_to="adjuntos_comite_etica/", blank=True, null=True
    )

    aprobado = models.BooleanField(default=False)
    aprobado_nombre = models.CharField(max_length=100)
    aprobado_fecha = models.DateField(auto_now_add=True)
    aprobado_adjunto = models.FileField(
        upload_to="adjuntos_aprobado/", blank=True, null=True
    )

    porcentaje_cumplimiento_total = models.FloatField(default=0)


# PROYECTO - Actividades
class Actividad(models.Model):
    DURACION_CHOICES = (
        ("semanas", "Fecha de Semanas"),
        ("meses", "Fecha por Meses"),
    )
    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="actividades"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.IntegerField()
    tipo_duracion = models.CharField(max_length=10, choices=DURACION_CHOICES)

    def __str__(self):
        return self.nombre


# --------------------------------------------- PRODUCTOS DERIVADOS ---------
class EstadoProducto(models.Model):
    """Model definition for EstadoProducto."""

    # TODO: Define fields here
    codigo = models.CharField(max_length=50, unique=True, help_text="00 - ESTADO 00")
    descripcion = models.CharField(
        "Descripcion",
        max_length=200,
        help_text="Descripcion de los estados de los productos",
    )

    class Meta:
        """Meta definition for EstadoProducto."""

        verbose_name = "Estado Producto"
        verbose_name_plural = "Estados Productos"

    def __str__(self):
        """Unicode representation of EstadoProducto."""
        return self.descripcion


# PRODUCTOS
class Producto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    CATEGORIAS = [
        ("Generación de Nuevo Conocimiento", "Generación de Nuevo Conocimiento"),
        ("Desarrollo Tecnológico e Innovación", "Desarrollo Tecnológico e Innovación"),
        ("Apropiación Social del Conocimiento", "Apropiación Social del Conocimiento"),
        ("Formación del Recurso Humano CteI", "Formación del Recurso Humano CteI"),
        ("Gestión de semillero", "Gestión de semillero"),
        ("Otros encargos", "Otros encargos"),
    ]
    categoria = models.CharField(max_length=300, choices=CATEGORIAS)
    tipo_producto = models.CharField(max_length=300)
    cantidad = models.IntegerField(default=1)
    estado_0 = models.CharField(max_length=300, default="No Iniciado")
    estado_0_justificado = models.CharField(max_length=300, default="")
    estado_1 = models.CharField(max_length=300, default="")
    estado_2 = models.CharField(max_length=300, default="")
    estado_3 = models.CharField(max_length=300, default="")
    estado_producto = models.ForeignKey(
        EstadoProducto, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.tipo_producto


# --------------------------------------------- PORTAFOLIO ACTIVIDADES ------------------------------------------


class Portafolio(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    avance_0_justificacion = models.TextField()
    avance_0_fecha = models.DateField(blank=True, null=True)

    avance_1_nombre = models.CharField(max_length=300)
    avance_1_descripcion = models.TextField(max_length=500)
    avance_1_link = models.URLField(blank=True, max_length=300)
    avance_1_adjunto = models.FileField(
        upload_to="Adjuntos_avance/", blank=True, null=True
    )
    avance_1_fecha = models.DateField(blank=True, null=True)
    avance_1_estado = models.CharField(max_length=300, default="No Revisado")
    avance_1_observacion = models.CharField(max_length=300)
    avance_1_correcciones_realizadas = models.BooleanField(default=False)
    porcentaje_avance_1 = models.FloatField(default=0)

    avance_2_descripcion = models.TextField(max_length=500)
    avance_2_link = models.URLField(blank=True, max_length=300)
    avance_2_adjunto = models.FileField(
        upload_to="adjuntos_avance/", blank=True, null=True
    )
    avance_2_fecha = models.DateField(blank=True, null=True)
    avance_2_estado = models.CharField(max_length=300, default="No Revisado")
    avance_2_observacion = models.CharField(max_length=300)
    avance_2_correcciones_realizadas = models.BooleanField(default=False)
    porcentaje_avance_2 = models.FloatField(default=0)

    avance_3_descripcion = models.TextField(max_length=500)
    avance_3_link = models.URLField(blank=True, max_length=300)
    avance_3_adjunto = models.FileField(
        upload_to="adjuntos_avance/", blank=True, null=True
    )
    avance_3_fecha = models.DateField(blank=True, null=True)
    avance_3_estado = models.CharField(max_length=300, default="No Revisado")
    avance_3_observacion = models.CharField(max_length=300)
    avance_3_correcciones_realizadas = models.BooleanField(default=False)
    porcentaje_avance_3 = models.FloatField(default=0)

    def __str__(self):
        return self.proyecto
