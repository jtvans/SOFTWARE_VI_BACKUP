from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Usuario, Usuario_Administrador


# Define un InlineAdmin para tu modelo Usuario
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuario'

# Define una nueva clase de administrador de UserAdmin con tu modelo Usuario incluido
class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)

# Desregistra el modelo User predeterminado
admin.site.unregister(User)

# Registra el modelo User con tu administrador personalizado
admin.site.register(User, CustomUserAdmin)
