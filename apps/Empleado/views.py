from django.shortcuts import render, redirect, get_object_or_404
from .models import empleados, puestosEmpleado, areasEmpleados, titulosAcademicos
from apps.Persona.models import estados, municipios, paises, colonias, personas, carreras
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.

# View para el formulario de puestos
def puestos(request):
    return render (request, "empleados/puestos.html")

# View para la tabla de los registros de puestos
def tablaPuestos(request):
    puestos_listado = puestosEmpleado.objects.all()

    paginator = Paginator(puestos_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, "empleados/tablaPuestos.html", {"puestos": page_obj})

# View para registrar los puestos
def registrarPuestos(request):
    PUESTO = request.POST['puesto']
 
    if puestosEmpleado.objects.filter(nombrePuesto=PUESTO).exists():
        messages.warning(request, 'Error, puesto ya existe')
        return redirect('/puestos/')
    else:
        insPuestos = puestosEmpleado.objects.create(nombre=PUESTO)
        messages.success(request, 'Puesto registrado correctamente.')
    return redirect('/tablaPuestos/')


# View para editar los datos en la tabla de puestos
def editar_puestos(request, idPuestoEmpleado):
    puesto = get_object_or_404(puestosEmpleado, idPuestoEmpleado=idPuestoEmpleado)
    nombrePuesto = request.GET.get('puesto', puestosEmpleado.nombrePuesto)
   
    puesto.nombrePuesto = nombrePuesto
    puesto.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaPuestos/')


# View para el formulario de areas
def areas(request):
    return render (request, "empleados/areas.html")

# View para la tabla de los registros de areas
def tablaAreas(request):
    areas_listado = areasEmpleados.objects.all()

    paginator = Paginator(areas_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, "empleados/tablaAreas.html", {"areas": page_obj})

# View para registrar las areas
def registrarAreas(request):
    AREA = request.POST['area']
 
    if areasEmpleados.objects.filter(nombreArea=AREA).exists():
        messages.warning(request, 'Error, esta area ya existe')
        return redirect('/areas/')
    else:
        insAreas = areasEmpleados.objects.create(nombreArea=AREA)
        messages.success(request, 'Area registrado correctamente.')
    return redirect('/tablaAreas/')


# View para editar los datos en la tabla de Areas
def editar_areas(request, idArea):
    area = get_object_or_404(areasEmpleados, idArea=idArea)
    nombreArea = request.GET.get('area', areasEmpleados.nombreArea)
   
    area.nombreArea = nombreArea
    area.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaAreas/')


# View para el formulario de titulos
def titulos(request):
    return render(request, "empleados/titulos.html")

def tablaTitulos(request):
    titulos_listado = titulosAcademicos.objects.all()

    paginator = Paginator(titulos_listado, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "empleados/tablaTitulos.html", {"titulos": page_obj})

def registrarTitulo(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        abreviatura = request.POST['abreviatura']
 
        if titulosAcademicos.objects.filter(nombre=titulo).exists():
            messages.warning(request, 'Error, este título ya existe')
            return redirect('/titulos/')
        else:
            insTitulos = titulosAcademicos.objects.create(nombre=titulo, abreviatura=abreviatura)
            messages.success(request, 'Título registrado correctamente.')
            return redirect('/tablaTitulos/')
    else:
        return redirect('/titulos/')



def editar_titulos(request, idtitulo):
    titulos = get_object_or_404(titulosAcademicos, idtitulo=idtitulo)
    nombre = request.GET.get('titulo', titulos.nombre)
    abreviatura = request.GET.get('abreviatura')
   
    titulos.nombre = nombre
    titulos.abreviatura = abreviatura
    titulos.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaTitulos/')




# View para el formulario de empleados
def empleados(request):
    persona = personas.objects.all()
    puestos = puestosEmpleado.objects.all()
    areas = areasEmpleados.objects.all()
    titulos = titulosAcademicos.objects.all()
    return render(request, "empleados/empleados.html", {'puestos': puestos, 'areas': areas, 'titulos': titulos, 'persona': persona })


#View que recopila los datos del formulario de pre-registro y realiza las inserciones en la BD
def guardaEmpleado(request):
    #recibir parámetros
    if request.method == 'POST' and request.FILES:
        CURP = request.POST['curp']
        NOMBRE = request.POST['nombre']
        APE1 = request.POST['ape1']
        APE2 = request.POST['ape2']
        TEL = request.POST['tel']
        CEL = request.POST['cel']
        CORREO = request.POST['correo']
        SEXO = request.POST['sexo']
        ESTADOCIV = request.POST['estadoCivil']
        HIJOS = request.POST['hijos']
        NACIONALIDAD = request.POST['nacionalidad']
        ESTADONAC = request.POST['estadoNacimiento']
        MPIONAC = request.POST['mpioNacimiento']
        CALLE = request.POST['calle']
        NUM = request.POST['numero']
        CP = request.POST['cp']
        ZONA = request.POST['zona']
        ESTADO = request.POST.get('estatus','1')
        NUMEMPLEADO = request.POST['nombre']
        FECHADEALTA = request.POST['nombre']
        ID_TITULO = request.POST['nombre']
        RFC = request.POST['nombre']
        IDPUESTO = request.POST['nombre']
        IDAREA = request.POST['nombre']

        
       
       
        #insEmpleado= personas.objects.create(curp=CURP, nombre=NOMBRE, ape1=APE1, ape2=APE2, calle=CALLE, numero=NUM, zona=ZONA, cp=CP, estadoNacimiento=ESTADONAC, mpioNacimiento=MPIONAC, nacionalidad=NACIONALIDAD, sexo=SEXO, estatus=1, telCasa=TEL, telCelular=CEL, estadoCivil=ESTADOCIV, hijos=HIJOS, correo=CORREO, estatus=ESTADO)
        messages.success(request, 'Ficha registrada correctamente.')
    return redirect('/tablaEmpleados/')