from django.shortcuts import render
from django.template.loader import get_template
from django.http import  HttpResponse



def menu(request):
    return render (request, "menu.html")

def login(request):
    return render (request, "login.html")
    
#views alumnos
def indexalumno(request):
    return render (request, "alumnos/indexalumno.html")
def procesosalumno(request):
    return render (request, "alumnos/procesosalumno.html")
def reportesalumno(request):
    return render (request, "alumnos/reportesalumno.html")

#views procesos alumnos
def pagosalumno(request):
    return render (request, "alumnos/procesos/pagos.html")
def cambiopass(request):
    return render (request, "alumnos/procesos/cambiopass.html")
def editdatosalumno(request):
    return render (request, "alumnos/procesos/editdatosalumno.html")
def reinscripcionlinea(request):
    return render (request, "alumnos/procesos/reinscripcionlinea.html")

#views reportes alumnos
def adeudosalumno(request):
    return render (request, "alumnos/reportes/adeudosalumno.html")
def boletas(request):
    return render (request, "alumnos/reportes/boletas.html")
def documentacionelec(request):
    return render (request, "alumnos/reportes/documentacionelec.html")
def historialpagos(request):
    return render (request, "alumnos/reportes/historialpagos.html")



#views reportes alumnos

