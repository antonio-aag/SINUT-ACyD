"""sinut2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from sinut2.views import menu, indexalumno, procesosalumno, reportesalumno, pagosalumno , login
from sinut2.views import reinscripcionlinea, editdatosalumno, cambiopass
from sinut2.views import adeudosalumno, boletas, documentacionelec, historialpagos
from apps.Aspirante.views import *
from apps.Persona.views import *
from apps.Usuario.views import *
from . import views

#Importaciones para los archivos
from django.conf import settings
from django.conf.urls.static import static


#from apps.Persona.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu),
    path('pre', preRegistro),
    
  
    path('login', login),
    path('', include('apps.Aspirante.urls')),
    path('', include('apps.Persona.urls')),
    path('', include('apps.Usuario.urls')),
    path('', include('apps.Reportes.urls')),
    path('', include('apps.Alumno.urls')),
    path('', include('apps.Empleado.urls')),
    
    
    
   
   

    #views alumnos
    path('indexalumno', indexalumno),
    path('procesosalum', procesosalumno),
    path('reportesalum', reportesalumno),
    
    #views procesos alumnos
    path('pagos', pagosalumno),
    path('reinscripcion', reinscripcionlinea),
    path('editardatosalumno', editdatosalumno),
    path('cambiarcontrasena', cambiopass),
    
    #views reportes alumnos
    path('adeudos', adeudosalumno),
    path('boletas', boletas),
    path('documentacion', documentacionelec),
    path('hpagos', historialpagos),



    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
