from django.urls import path
from . import views


urlpatterns = [
    path('usuarios/', views.tipoUsuario),
    path('registrarUsuario/', views.registrarUsuario),
    path('tablaTipoUsuario/', views.tablaTipoUsuario),
    path('editarUsuario/<int:idTipoUsuario>/', views.editar_usuario),
    #path('reporte_tiposUsuarios', views.reporte_tiposUsuarios)
    
    
]