from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# 1
class LineaInvestigacion(models.Model):
    nombre = models.CharField(max_length=500)
    def __str__(self):
        return self.nombre
    
# 2
class LineaInvestigacion_2(models.Model):
    nombre = models.CharField(max_length=500)
    def __str__(self):
        return self.nombre

# 3
class LineaInvestigacion_3(models.Model):
    nombre = models.CharField(max_length=500)
    def __str__(self):
        return self.nombre
    

# USUARIO
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)
    clave = models.CharField(max_length=100)
    cvlac = models.URLField(blank=True)
    orcid = models.URLField(blank=True)
    google_scholar = models.URLField(blank=True)

    # CATEGORIAS -------
    CATEGORIAS = [
        ('Junior', 'Junior'),
        ('Asociado', 'Asociado'),
        ('Emerito', 'Emerito'),
        ('No_Reconocido', 'No_Reconocido'),
    ]
    categoria = models.CharField(max_length=100, choices=CATEGORIAS, default='No_Reconocido')

    # FACULTAD ------- PROGRAMA
    FACTULTAD = [
        ('Humanidades','Humanidades'),
        ('Ciencias_Admin','Ciencias_Admin'),
        ('Ingenieria','Ingenieria'),
        ('Educacion','Educacion'),
    ]
    facultad = models.CharField(max_length=200, choices=FACTULTAD, blank=True)
    Programa = models.CharField(max_length=100, blank=True)

    # GRUPOS INVESTIGACION ------- LINEAS INVESTIGACION
    GRUPOS_INVESTIGACION = [
        ('Aglalia', 'Aglalia'),
        ('ProCont', 'ProCont'),
        ('DehJüs', 'DehJüs'),
        ('TES', 'TES'),
        ('GECAES', 'GECAES'),
        ('Gestion e Innovacion', 'Gestion e Innovacion'),
        ('IC', 'IC'),
        ('LyS', 'LyS'),
        ('Gisela', 'Gisela'),
        ('LAW', 'LAW'),
        ('Business Intelligence', 'Business Intelligence'),
        ('Americana Emprendedora', 'Americana Emprendedora'),
        ('PSI Context', 'PSI Context'),
        ('Engineeri', 'Engineeri'),
        ('SeHaT', 'SeHaT'),
    ]
    # 1
    #grupo_investigacion = models.CharField(max_length=100, choices=GRUPOS_INVESTIGACION, blank=True)
    grupo_investigacion = models.CharField(max_length=200, choices=GRUPOS_INVESTIGACION, blank=True, null=True)

    def get_lineas_investigacion_choices(self):
        if self.grupo_investigacion == 'Aglalia':
            return [
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Nuevas tecnologías e inteligencia artificial', 'Nuevas tecnologías e inteligencia artificial'),
                ('Sistemas de información e ingeniería de software', 'Sistemas de información e ingeniería de software'),
            ]
        elif self.grupo_investigacion == 'ProCont':
            return [
                ('Contabilidad social y ambiental', 'Contabilidad social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion == 'DehJüs':
            return [
                ('Conflictos instituciones jurídicas y nuevas tendencias del derecho privado', 'Conflictos instituciones jurídicas y nuevas tendencias del derecho privado'),
                ('Derecho público y justicia', 'Derecho público y justicia'),
                ('Desarrollo humano salud mental y psicología forense', 'Desarrollo humano salud mental y psicología forense'),
                ('Genero sociedad y derechos humanos', 'Genero sociedad y derechos humanos'),
            ]
        elif self.grupo_investigacion =='TES':
            return [
                 ('Bilinguismo', 'Bilinguismo'),
                ('Infancia y desarrollo social', 'Infancia y desarrollo social'),
                ('Neuropsicologia comportamiento y aprendizaje', 'Neuropsicologia comportamiento y aprendizaje'),
                ('Practica pedagógica investigativa', 'Practica pedagógica investigativa'),
                ('Psicologia educativa y evolutiva', 'Psicologia educativa y evolutiva'),
                ('Psicologia social y comunitaria', 'Psicologia social y comunitaria'),
            ]
        elif self.grupo_investigacion == 'GECAES':
            return [
                ('Capital social y ambiental', 'Capital social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion == 'Gestion_e_Innovacion':
            return [
                ('Gestión e innovación', 'Gestión e innovación'),
                ('Innovación y gestión turística', 'Innovación y gestión turística'),
            ]
        elif self.grupo_investigacion == 'IC':
            return [
                ('Ciudadanía genero y sociedad', 'Ciudadanía genero y sociedad'),
                ('Innovaciones sociales', 'Innovaciones sociales'),
            ]
        elif self.grupo_investigacion == 'LyS':
            return [
                ('Derecho y gestión de políticas publicas', 'Derecho y gestión de políticas publicas'),
                ('Derecho y sociedad', 'Derecho y sociedad'),
                ('Derecho y sujetos de especial protección constituciona', 'Derecho y sujetos de especial protección constituciona')
            ]
        elif self.grupo_investigacion == 'Gisela':
            return [
                ('Gestión organizacional, desarrollo y sociedad', 'Gestión organizacional, desarrollo y sociedad'),
                ('Competitividad e innovacion en pymes', 'Competitividad e innovacion en pymes'),
            ]
        elif self.grupo_investigacion == 'LAW':
            return [
                ('Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación', 'Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación'),
                ('Propiedad intelectual', 'Propiedad intelectual'),
                ('Práctica jurídica', 'Práctica jurídica'),
                ('Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías', 'Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías'),
            ]
        elif self.grupo_investigacion == 'Business_Intelligence':
            return [
                ('Comercio y neogcios internacionales', 'Comercio y neogcios internacionales'),
                ('Logistica nacional e internacional', 'Logistica nacional e internacional'),
            ]
        elif self.grupo_investigacion == 'Americana_Emprendedora':
            return [
                ('Emprendimiento ecosistemas de emprendimiento e innovación', 'Emprendimiento ecosistemas de emprendimiento e innovación'),
                ('Emprendimiento de mujeres y comunidades', 'Emprendimiento de mujeres y comunidades'),
            ]
        elif self.grupo_investigacion == 'PSI_Context':
            return [
                ('Desarrollo humano y problemáticas sociales', 'Desarrollo humano y problemáticas sociales'),
                ('Salud y bienestar', 'Salud y bienestar'),
            ]
        elif self.grupo_investigacion == 'Engineeri':
            return [
                ('Diseño y gestión de Sistemas productivos y logísticos', 'Diseño y gestión de Sistemas productivos y logísticos'),
                ('Innovación y gestión tecnológica', 'Innovación y gestión tecnológica'),
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Sistemas integrados de procesos y gestión', 'Sistemas integrados de procesos y gestión'),
            ]
        elif self.grupo_investigacion == 'SeHaT':
            return [
                ('Emprendimiento e innovación', 'Emprendimiento e innovación'),
                ('Salud Ocupacional', 'Salud Ocupacional'),
                ('Seguridad Industrial', 'Seguridad Industrial'),
            ]
        else:
            return []
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion, blank=True)

    """"""
    # 2
    grupo_investigacion_2 = models.CharField(max_length=200, choices=GRUPOS_INVESTIGACION, blank=True, null=True)
    def get_lineas_investigacion_choices_2(self):
        if self.grupo_investigacion_2 == 'Aglalia':
            return [
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Nuevas tecnologías e inteligencia artificial', 'Nuevas tecnologías e inteligencia artificial'),
                ('Sistemas de información e ingeniería de software', 'Sistemas de información e ingeniería de software'),
            ]
        elif self.grupo_investigacion_2 == 'ProCont':
            return [
                ('Contabilidad social y ambiental', 'Contabilidad social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion_2 == 'DehJüs':
            return [
                ('Conflictos instituciones jurídicas y nuevas tendencias del derecho privado', 'Conflictos instituciones jurídicas y nuevas tendencias del derecho privado'),
                ('Derecho público y justicia', 'Derecho público y justicia'),
                ('Desarrollo humano salud mental y psicología forense', 'Desarrollo humano salud mental y psicología forense'),
                ('Genero sociedad y derechos humanos', 'Genero sociedad y derechos humanos'),
            ]
        elif self.grupo_investigacion_2 =='TES':
            return [
                 ('Bilinguismo', 'Bilinguismo'),
                ('Infancia y desarrollo social', 'Infancia y desarrollo social'),
                ('Neuropsicologia comportamiento y aprendizaje', 'Neuropsicologia comportamiento y aprendizaje'),
                ('Practica pedagógica investigativa', 'Practica pedagógica investigativa'),
                ('Psicologia educativa y evolutiva', 'Psicologia educativa y evolutiva'),
                ('Psicologia social y comunitaria', 'Psicologia social y comunitaria'),
            ]
        elif self.grupo_investigacion_2 == 'GECAES':
            return [
                ('Capital social y ambiental', 'Capital social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion_2 == 'Gestion_e_Innovacion':
            return [
                ('Gestión e innovación', 'Gestión e innovación'),
                ('Innovación y gestión turística', 'Innovación y gestión turística'),
            ]
        elif self.grupo_investigacion_2 == 'IC':
            return [
                ('Ciudadanía genero y sociedad', 'Ciudadanía genero y sociedad'),
                ('Innovaciones sociales', 'Innovaciones sociales'),
            ]
        elif self.grupo_investigacion_2 == 'LyS':
            return [
                ('Derecho y gestión de políticas publicas', 'Derecho y gestión de políticas publicas'),
                ('Derecho y sociedad', 'Derecho y sociedad'),
                ('Derecho y sujetos de especial protección constituciona', 'Derecho y sujetos de especial protección constituciona')
            ]
        elif self.grupo_investigacion_2 == 'Gisela':
            return [
                ('Gestión organizacional, desarrollo y sociedad', 'Gestión organizacional, desarrollo y sociedad'),
                ('Competitividad e innovacion en pymes', 'Competitividad e innovacion en pymes'),
            ]
        elif self.grupo_investigacion_2 == 'LAW':
            return [
                ('Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación', 'Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación'),
                ('Propiedad intelectual', 'Propiedad intelectual'),
                ('Práctica jurídica', 'Práctica jurídica'),
                ('Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías', 'Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías'),
            ]
        elif self.grupo_investigacion_2 == 'Business_Intelligence':
            return [
                ('Comercio y neogcios internacionales', 'Comercio y neogcios internacionales'),
                ('Logistica nacional e internacional', 'Logistica nacional e internacional'),
            ]
        elif self.grupo_investigacion_2 == 'Americana_Emprendedora':
            return [
                ('Emprendimiento ecosistemas de emprendimiento e innovación', 'Emprendimiento ecosistemas de emprendimiento e innovación'),
                ('Emprendimiento de mujeres y comunidades', 'Emprendimiento de mujeres y comunidades'),
            ]
        elif self.grupo_investigacion_2 == 'PSI_Context':
            return [
                ('Desarrollo humano y problemáticas sociales', 'Desarrollo humano y problemáticas sociales'),
                ('Salud y bienestar', 'Salud y bienestar'),
            ]
        elif self.grupo_investigacion_2 == 'Engineeri':
            return [
                ('Diseño y gestión de Sistemas productivos y logísticos', 'Diseño y gestión de Sistemas productivos y logísticos'),
                ('Innovación y gestión tecnológica', 'Innovación y gestión tecnológica'),
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Sistemas integrados de procesos y gestión', 'Sistemas integrados de procesos y gestión'),
            ]
        elif self.grupo_investigacion_2 == 'SeHaT':
            return [
                ('Emprendimiento e innovación', 'Emprendimiento e innovación'),
                ('Salud Ocupacional', 'Salud Ocupacional'),
                ('Seguridad Industrial', 'Seguridad Industrial'),
            ]
        else:
            return []
    lineas_investigacion_2 = models.ManyToManyField(LineaInvestigacion_2, blank=True)


    """"""
    # 3
    grupo_investigacion_3 = models.CharField(max_length=200, choices=GRUPOS_INVESTIGACION, blank=True, null=True)
    def get_lineas_investigacion_choices_3(self):
        if self.grupo_investigacion_3 == 'Aglalia':
            return [
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Nuevas tecnologías e inteligencia artificial', 'Nuevas tecnologías e inteligencia artificial'),
                ('Sistemas de información e ingeniería de software', 'Sistemas de información e ingeniería de software'),
            ]
        elif self.grupo_investigacion_3 == 'ProCont':
            return [
                ('Contabilidad social y ambiental', 'Contabilidad social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion_3 == 'DehJüs':
            return [
                ('Conflictos instituciones jurídicas y nuevas tendencias del derecho privado', 'Conflictos instituciones jurídicas y nuevas tendencias del derecho privado'),
                ('Derecho público y justicia', 'Derecho público y justicia'),
                ('Desarrollo humano salud mental y psicología forense', 'Desarrollo humano salud mental y psicología forense'),
                ('Genero sociedad y derechos humanos', 'Genero sociedad y derechos humanos'),
            ]
        elif self.grupo_investigacion_3 =='TES':
            return [
                 ('Bilinguismo', 'Bilinguismo'),
                ('Infancia y desarrollo social', 'Infancia y desarrollo social'),
                ('Neuropsicologia comportamiento y aprendizaje', 'Neuropsicologia comportamiento y aprendizaje'),
                ('Practica pedagógica investigativa', 'Practica pedagógica investigativa'),
                ('Psicologia educativa y evolutiva', 'Psicologia educativa y evolutiva'),
                ('Psicologia social y comunitaria', 'Psicologia social y comunitaria'),
            ]
        elif self.grupo_investigacion_3 == 'GECAES':
            return [
                ('Capital social y ambiental', 'Capital social y ambiental'),
                ('Contabilidad y gestión financiera', 'Contabilidad y gestión financiera'),
                ('Estudios fiscales y gestión tributaria', 'Estudios fiscales y gestión tributaria'),
            ]
        elif self.grupo_investigacion_3 == 'Gestion_e_Innovacion':
            return [
                ('Gestión e innovación', 'Gestión e innovación'),
                ('Innovación y gestión turística', 'Innovación y gestión turística'),
            ]
        elif self.grupo_investigacion_3 == 'IC':
            return [
                ('Ciudadanía genero y sociedad', 'Ciudadanía genero y sociedad'),
                ('Innovaciones sociales', 'Innovaciones sociales'),
            ]
        elif self.grupo_investigacion_3 == 'LyS':
            return [
                ('Derecho y gestión de políticas publicas', 'Derecho y gestión de políticas publicas'),
                ('Derecho y sociedad', 'Derecho y sociedad'),
                ('Derecho y sujetos de especial protección constituciona', 'Derecho y sujetos de especial protección constituciona')
            ]
        elif self.grupo_investigacion_3 == 'Gisela':
            return [
                ('Gestión organizacional, desarrollo y sociedad', 'Gestión organizacional, desarrollo y sociedad'),
                ('Competitividad e innovacion en pymes', 'Competitividad e innovacion en pymes'),
            ]
        elif self.grupo_investigacion_3 == 'LAW':
            return [
                ('Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación', 'Mecanismos alternativos de solución de conflictos en particular la mediación interdisciplinaria y la conciliación'),
                ('Propiedad intelectual', 'Propiedad intelectual'),
                ('Práctica jurídica', 'Práctica jurídica'),
                ('Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías', 'Línea de investigación en educación inclusiva e interdisciplinar y de las nuevas tecnologías'),
            ]
        elif self.grupo_investigacion_3 == 'Business_Intelligence':
            return [
                ('Comercio y neogcios internacionales', 'Comercio y neogcios internacionales'),
                ('Logistica nacional e internacional', 'Logistica nacional e internacional'),
            ]
        elif self.grupo_investigacion_3 == 'Americana_Emprendedora':
            return [
                ('Emprendimiento ecosistemas de emprendimiento e innovación', 'Emprendimiento ecosistemas de emprendimiento e innovación'),
                ('Emprendimiento de mujeres y comunidades', 'Emprendimiento de mujeres y comunidades'),
            ]
        elif self.grupo_investigacion_3 == 'PSI_Context':
            return [
                ('Desarrollo humano y problemáticas sociales', 'Desarrollo humano y problemáticas sociales'),
                ('Salud y bienestar', 'Salud y bienestar'),
            ]
        elif self.grupo_investigacion_3 == 'Engineeri':
            return [
                ('Diseño y gestión de Sistemas productivos y logísticos', 'Diseño y gestión de Sistemas productivos y logísticos'),
                ('Innovación y gestión tecnológica', 'Innovación y gestión tecnológica'),
                ('Modelado y simulación', 'Modelado y simulación'),
                ('Sistemas integrados de procesos y gestión', 'Sistemas integrados de procesos y gestión'),
            ]
        elif self.grupo_investigacion_3 == 'SeHaT':
            return [
                ('Emprendimiento e innovación', 'Emprendimiento e innovación'),
                ('Salud Ocupacional', 'Salud Ocupacional'),
                ('Seguridad Industrial', 'Seguridad Industrial'),
            ]
        else:
            return []
    lineas_investigacion_3 = models.ManyToManyField(LineaInvestigacion_3, blank=True)


    def __str__(self):
        return self.nombre


#--------------------------------------- USUER ADMIN ---------------------------------------

# Usuario Administrador
class Usuario_Administrador(models.Model):
    user_admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_administrador')
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    es_administrador = models.BooleanField(default=True)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    clave = models.CharField(max_length=100)

    # Agrega el argumento related_name a las relaciones groups y user_permissions
    groups = models.ManyToManyField(Group, verbose_name='grupos', blank=True, related_name='administradores')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='permisos de usuario', blank=True, related_name='administradores'
    )
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_active = True
        self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    

#--------------------------------------- USUER ESTUDIANTE ---------------------------------------


# USUARIO ESTUDIANTE
class Usuario_Estudiante(models.Model):
    user_e = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_estudiante')
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)
    clave = models.CharField(max_length=100)
    programa = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

    
#--------------------------------------- USUER ADMIN SEMILELRO ---------------------------------------

# USUARIO ADMIN SEMILELRO
class Usuario_Adminin_Semi(models.Model):
    user_e = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_admin_semi')
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return self.nombre

