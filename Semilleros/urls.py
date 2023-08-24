from django.urls import path
from . import views

app_name = 'Semilleros'

urlpatterns = [
    path('crear/', views.crear_semillero, name='crear_semillero'),
    path('semilleros/', views.lista_semilleros, name='lista_semilleros'),
]