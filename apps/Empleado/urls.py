from django.urls import path
from . import views

app_name = 'Empleado'

urlpatterns = [
    path('puestos/', views.puestos),
    path('tablaPuestos/', views.tablaPuestos),
    path('registrarPuesto/', views.registrarPuestos),
    path('editarPuestos/<int:idPuestoEmpleado>/', views.editar_puestos),
    path('areas/', views.areas),
    path('tablaAreas/', views.tablaAreas),
    path('registrarArea/', views.registrarAreas),
    path('editarAreas/<int:idArea>/', views.editar_areas),
    path('titulos/', views.titulos),
    path('tablaTitulos/', views.tablaTitulos),
    path('registrarTitulo/', views.registrarTitulo),
    path('editarTitulos/<int:idtitulo>/', views.editar_titulos),
    path('empleados/', views.empleados),
    
]