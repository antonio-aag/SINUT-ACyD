from django.shortcuts import render, redirect, get_object_or_404
from .models import tiposUsuarios, usuarios
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import json

#Se importan para los reportes weasyprint, HttpResponse y render_to_string


# Create your views here.

# Vista para el formulario tipo de usuarios
def tipoUsuario(request):
    return render (request, "usuarios/tipoUsuarios.html")

# vista para la tabla de tipos de usuarios
def tablaTipoUsuario(request):
    tiposUsuariosListado = tiposUsuarios.objects.order_by('nombre')
    
    paginator = Paginator(tiposUsuariosListado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "usuarios/tablaTipoUsuarios.html", {"usuarios": page_obj})




# Vista para registrar nuevos usuarios
def registrarUsuario(request):
    USUARIO = request.POST['user']
    ESTADO = request.POST.get('estatus','0')
 
    if tiposUsuarios.objects.filter(nombre=USUARIO).exists():
        messages.warning(request, 'Error, ese tipo de usuario ya existe')
        return redirect('/usuarios/')
    else:
        insTiposUsuarios = tiposUsuarios.objects.create(nombre=USUARIO, estatus=ESTADO)
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('/tablaTipoUsuario/')

# Vista Para editar en la tabla los tipos de usuarios
def editar_usuario(request, idTipoUsuario):
    usuario = get_object_or_404(tiposUsuarios, idTipoUsuario=idTipoUsuario)
    nombre = request.GET.get('nombre', usuario.nombre)
    estatus = request.GET.get('estatus')
 
    usuario.nombre = nombre
    usuario.estatus = estatus
    usuario.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaTipoUsuario/')
    
      

