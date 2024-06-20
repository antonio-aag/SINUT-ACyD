from django.urls import path
from . import views


app_name = 'Alumno'

urlpatterns = [
    path('periodos/', views.Periodos),
    path('registrarPeriodo/', views.registrarPeriodo),
    path('tablaPeriodos/', views.tablaPeriodos),
    path('editarPeriodo/<int:idPeriodo>/', views.editar_periodo),
    ]
