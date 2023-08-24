"""
URL configuration for SW_Investigation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Principal - Base
    path('admin/', admin.site.urls),
    path('', views.Pagina_Principal, name='Pagina_Principal'),
    path('Pagina_Principal_About', views.Pagina_Principal_About, name='Pagina_Principal_About'),
    path('Pagina_Principal_Contact', views.Pagina_Principal_Contact, name='Pagina_Principal_Contact'),
    

    path('users/', include('Users.urls')),
    path('proyectos/', include('Proyectos.urls')),
    path('semilleros/', include('Semilleros.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
