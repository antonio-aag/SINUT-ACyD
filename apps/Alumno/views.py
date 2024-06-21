from django.shortcuts import render, redirect, get_object_or_404
from .models import periodo
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import ListView

# Create your views here.

# View para el formulario de registrar Periodos
def Periodos(request):
    return render (request, "periodos/Periodos.html")


# View para registrar los datos del formulario de Periodos
def registrarPeriodo(request):
    FECHAINICIO = request.POST['fechaInicio']
    FECHAFIN = request.POST ['fechaFin']
    ACTIVO = 0
    GENTSU = request.POST['GenTSU'] 
    GENING = request.POST['GenING']
   
    insPeriodo = periodo.objects.create(fechaInicio=FECHAINICIO, fechaFin=FECHAFIN, activo=ACTIVO, genTSU=GENTSU, genING=GENING)
    messages.success(request, 'Periodo registrado correctamente.')
    return redirect('/tablaPeriodos/') 

# View para la tabla de los registros del formulario de Periodos
def tablaPeriodos(request):
    periodos_listado = periodo.objects.all()

    paginator = Paginator(periodos_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'periodos/tablaPeriodos.html', {'periodos': page_obj})

# View para editar los campos de Periodos
def editar_periodo(request, idPeriodo):
    periodo_obj = get_object_or_404(periodo, idPeriodo=idPeriodo)
    fechaInicio = request.GET.get('fechaInicio', periodo_obj.fechaInicio)
    fechaFin = request.GET.get('fechaFin')
    genTSU = request.GET.get('GenTSU')
    genING = request.GET.get('GenING')
    activo = request.GET.get('estatus')

   
    if activo == '1':
        periodo.objects.exclude(idPeriodo=periodo_obj.idPeriodo).update(activo=0)

    periodo_obj.fechaInicio = fechaInicio
    periodo_obj.fechaFin = fechaFin
    periodo_obj.genTSU = genTSU
    periodo_obj.genING = genING
    periodo_obj.activo = activo
    periodo_obj.save()

    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaPeriodos/')

