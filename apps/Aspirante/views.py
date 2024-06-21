import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import aspirantes,  encuesta, universidades, documentos, escuelasProcedencia, procesosFichas, documentoCondicionado, subsistemas, detalleOtroDato, otrosDatos
from apps.Usuario.models import usuarios, tiposUsuarios
from apps.Persona.models import estados, municipios, paises, colonias, personas, carreras, datosMedicos
from apps.Alumno.models import periodo
from apps.Empleado.models import empleados
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import IntegerField
from urllib.parse import urlencode
from django.urls import reverse
from django.db.models import Prefetch
import urllib.parse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import OuterRef, Subquery, Max
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator


# rCreate your views here.

#View que carga el formulario de pre-registro
def preRegistro(request):
    lcarreras = carreras.objects.filter(estatus=1, nivel=1)
    return render (request, "aspirantes/preRegistro.html", {"lcarreras":lcarreras,})

def escuelasProcedencialist(request):
    return render (request, "aspirantes/escuelasProcedencia.html")

def tablaEdadNuevoIngreso(request):

    laspirantes = aspirantes.objects.all()

    edad_sexo_contadores = {
        17: {'f': 0, 'm': 0},
        18: {'f': 0, 'm': 0},
        19: {'f': 0, 'm': 0},
        20: {'f': 0, 'm': 0},
        21: {'f': 0, 'm': 0},
        27: {'f': 0, 'm': 0},
    }

    for aspirante in laspirantes:
        persona = aspirante.idPersona
        curp = persona.curp
        sexo = persona.sexo
        

        anio_nacimiento = int(curp[4:6])
        if anio_nacimiento<24:
            anio_nacimiento += 2000
        else:
            anio_nacimiento += 1900
        mes_nacimiento = int(curp[6:8])
        dia_nacimiento = int(curp[8:10])
        fecha_nacimiento = datetime.date(anio_nacimiento, mes_nacimiento, dia_nacimiento)

        hoy = datetime.date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if edad in edad_sexo_contadores:
            if sexo == 1:
                edad_sexo_contadores[edad]['f'] += 1
            elif sexo == 2:
                edad_sexo_contadores[edad]['m'] += 1

    contexto = {}
    for edad, contadores in edad_sexo_contadores.items():
        contexto[f'f{edad}'] = contadores['f']
        contexto[f'm{edad}'] = contadores['m']
        contexto[f't{edad}'] = contadores['f'] + contadores['m']

    return render(request, 'aspirantes/tablaEdadNuevoIngreso.html', contexto)

def menuAspirantes(request):
    return render (request, "aspirantes/menuAspirantes.html")

#View que consulta todos los datos de los aspirantes y sus relaciones por registrados y no registrados
def datosAspirantes(request): 
    lperiodos = periodo.objects.all()   
    periodoActivo = periodo.objects.filter(activo=1).first()
   # laspirantes = aspirantes.objects.all()
    laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo)

    for aspirante in laspirantes:
        if aspirante.estatus == 1:
            aspirante.estatus_view = 'No Registrado'
        elif aspirante.estatus >= 2:
            aspirante.estatus_view = 'Registrado'
   
    return render (request, "aspirantes/datosAspirantes.html", {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "periodoActivo" : periodoActivo
    })

#View que consulta todos los datos de los aspirantes y sus relaciones por registrados y no registrados con filtros depende el argumento enviado

def datosAspirantesFiltro(request):
    periodoS = request.GET.get('periodo')
    filtros = request.GET.get('filtro')
 
    lperiodos = periodo.objects.all()   
    periodoActivo = periodo.objects.filter(idPeriodo=periodoS).first()
   # laspirantes = aspirantes.objects.all()

    if filtros=='1':
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo, estatus=1)
    elif filtros=='2':
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo, estatus=2)
    else:        
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo)


    for aspirante in laspirantes:
        if aspirante.estatus == 1:
            aspirante.estatus_view = 'No Registrado'
        elif aspirante.estatus >= 2:
            aspirante.estatus_view = 'Registrado'

    return render (request, "aspirantes/datosAspirantes.html", {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "periodoActivo" : periodoActivo,
        "radios" : filtros
    })

#Esta view muestra los aspirantes con su especialidad de prepa registrados en el ultimo PeriodoInicioClases registrado
def aspirantesEspecialidad(request): 
    lperiodos = periodo.objects.order_by('-idPeriodo') 
    lcarreras = carreras.objects.all()
    periodoInicioClases = lperiodos.first()
    #laspirantes = aspirantes.objects.all()#esta es solo para pruebas
    lempleados = empleados.objects.filter(estatus=1)

    laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoInicioClases)
    
    max_id_subquery = laspirantes.values('idPersona__curp').annotate(max_id=Max('idAspirante')).values('max_id')
    
    # Filtrar los aspirantes para quedarte solo con los registros más recientes por curp y no se repi
    laspirantes = laspirantes.filter(idAspirante__in=Subquery(max_id_subquery))

    especialidades = {
    '1': 'Administración',
    '2': 'Administración de la Pequeña Empresa',
    '3': 'Administración en Sistemas<',
    '4': 'Biotecnología',
    '5': 'Ciencias Exactas y Naturales',
    '6': 'Ciencias Sociales',
    '7': 'Ciencias y Humanidades',
    '8': 'Computación Fiscal y Contable',
    '9': 'Computación y Sistemas de Administración',
    '10': 'Comunicación',
    '11': 'Dibujo Arquitectónico',
    '12': 'Económico-Administrativo',
    '13': 'Electromecánica',
    '14': 'Electrónica',
    '15': 'Físico-Químico',
    '16': 'Físico-Matemático',
    '17': 'Horticultura',
    '18': 'Humanidades',
    '19': 'Informática',
    '20': 'Informática Administrativa',
    '21': 'Instalaciones Hidráulicas y Eléctrica',
    '22': 'Laboratorio Químico',
    '23': 'Mantenimiento',
    '24': 'Máquinas de Combustión Interna',
    '25': 'Mecánica',
    '26': 'Mecánica Industrial',
    '27': 'Mecatrónica',
    '28': 'Nutrición',
    '29': 'Otro',
    '30': 'Práctica Docente',
    '31': 'Práctica Educativa',
    '32': 'Programador Analista',
    '33': 'Promotor Educativo',
    '34': 'Psicopedagógico',
    '35': 'Químico Biológico con Turismo',
    '36': 'Químico Biológico e Informática',
    '37': 'Químico Biólogo',
    '38': 'Químico Biólogo en el Área de Alimentos',
    '39': 'Químico Industrial',
    '40': 'Recursos Humanos',
    '41': 'Relaciones Humanas',
    '42': 'Secretaria Ejecutiva en Español',
    '43': 'Social Administrativo',
    '44': 'Técnica Agropecuaria',
    '45': 'Técnica en Computación',
    '46': 'Técnica en Informática Agropecuaria',
    '47': 'Técnico Agropecuario',
    '48': 'Técnico Electromecánico',
    '49': 'Técnico en Administración',
    '50': 'Técnico en Alimentos',
    '51': 'Técnico en Computación',
    '52': 'Técnico en Computación Fiscal Contable',
    '53': 'Técnico en Construcción Urbana',
    '54': 'Técnico en Contabilidad',
    '55': 'Técnico en Máquinas y Herramientas',
    '56': 'Técnico en Nutrición',
    '57': 'Técnico en Puericultura',
    '58': 'Técnico en Trabajo Social',
    '59': 'Técnico Laboratorista Clínico',
    '60': 'Tecnología de los Alimentos',
    '61': 'Tecnología en Alimentos',
    '62': 'Trabajadora Social',
    '63': 'TSU en Comercialización',
    '64': 'TSU en Informática',
    '65': 'TSU en Mantenimiento Industrial',
    '66': 'TSU en Mecánica',
    '67': 'TSU en Procesos Agroindustriales',
    '68': 'TSU en Tecnologías de la Información y Comunicación',
    '69': 'Turismo',
    '70': 'Viveros'
    }

    for aspirante in laspirantes:
        aspirante.especialidadPrepa_view = especialidades.get(aspirante.especialidadPrepa, 'Otro')

   
    return render (request, "aspirantes/aspirantesEspecialidad.html", {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "lempleados": lempleados,
        "lcarreras": lcarreras,
        "periodoInicioClases" : periodoInicioClases
    })

def aspirantesEspecialidadFiltro(request): 
    lperiodos = periodo.objects.order_by('-idPeriodo') 
    lcarreras = carreras.objects.all()
    periodoInicioClases = lperiodos.first()
    #laspirantes = aspirantes.objects.all()#esta es solo para pruebas
    laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoInicioClases)

    especialidades = {
    '1': 'Administración',
    '2': 'Administración de la Pequeña Empresa',
    '3': 'Administración en Sistemas<',
    '4': 'Biotecnología',
    '5': 'Ciencias Exactas y Naturales',
    '6': 'Ciencias Sociales',
    '7': 'Ciencias y Humanidades',
    '8': 'Computación Fiscal y Contable',
    '9': 'Computación y Sistemas de Administración',
    '10': 'Comunicación',
    '11': 'Dibujo Arquitectónico',
    '12': 'Económico-Administrativo',
    '13': 'Electromecánica',
    '14': 'Electrónica',
    '15': 'Físico-Químico',
    '16': 'Físico-Matemático',
    '17': 'Horticultura',
    '18': 'Humanidades',
    '19': 'Informática',
    '20': 'Informática Administrativa',
    '21': 'Instalaciones Hidráulicas y Eléctrica',
    '22': 'Laboratorio Químico',
    '23': 'Mantenimiento',
    '24': 'Máquinas de Combustión Interna',
    '25': 'Mecánica',
    '26': 'Mecánica Industrial',
    '27': 'Mecatrónica',
    '28': 'Nutrición',
    '29': 'Otro',
    '30': 'Práctica Docente',
    '31': 'Práctica Educativa',
    '32': 'Programador Analista',
    '33': 'Promotor Educativo',
    '34': 'Psicopedagógico',
    '35': 'Químico Biológico con Turismo',
    '36': 'Químico Biológico e Informática',
    '37': 'Químico Biólogo',
    '38': 'Químico Biólogo en el Área de Alimentos',
    '39': 'Químico Industrial',
    '40': 'Recursos Humanos',
    '41': 'Relaciones Humanas',
    '42': 'Secretaria Ejecutiva en Español',
    '43': 'Social Administrativo',
    '44': 'Técnica Agropecuaria',
    '45': 'Técnica en Computación',
    '46': 'Técnica en Informática Agropecuaria',
    '47': 'Técnico Agropecuario',
    '48': 'Técnico Electromecánico',
    '49': 'Técnico en Administración',
    '50': 'Técnico en Alimentos',
    '51': 'Técnico en Computación',
    '52': 'Técnico en Computación Fiscal Contable',
    '53': 'Técnico en Construcción Urbana',
    '54': 'Técnico en Contabilidad',
    '55': 'Técnico en Máquinas y Herramientas',
    '56': 'Técnico en Nutrición',
    '57': 'Técnico en Puericultura',
    '58': 'Técnico en Trabajo Social',
    '59': 'Técnico Laboratorista Clínico',
    '60': 'Tecnología de los Alimentos',
    '61': 'Tecnología en Alimentos',
    '62': 'Trabajadora Social',
    '63': 'TSU en Comercialización',
    '64': 'TSU en Informática',
    '65': 'TSU en Mantenimiento Industrial',
    '66': 'TSU en Mecánica',
    '67': 'TSU en Procesos Agroindustriales',
    '68': 'TSU en Tecnologías de la Información y Comunicación',
    '69': 'Turismo',
    '70': 'Viveros'
    }

    for aspirante in laspirantes:
        aspirante.especialidadPrepa_view = especialidades.get(aspirante.especialidadPrepa, 'Otro')

   
    return render (request, "aspirantes/aspirantesEspecialidad.html", {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "lcarreras": lcarreras,
        "periodoInicioClases" : periodoInicioClases
    })

def datosPersonalizados(request):    
    laspirantes = aspirantes.objects.all()
    return render (request, "aspirantes/datosAspirantes.html", {"laspirantes":laspirantes})

def aspirantesRegistrados(request):
    lfichas = procesosFichas.objects.all()  # Obtener todos los procesos de fichas existentes
    ultimaFicha = procesosFichas.objects.order_by('-idProcesoFicha').first()  # Obtener el último proceso de fichas registrado
    t=0
    # Obtener todas las carreras registradas que estén activas
    lcarreras = carreras.objects.filter(estatus=1)
    totalAspirantesR = aspirantes.objects.filter(estatus__gt=1, idProcesoFicha=ultimaFicha).count()
    
    if ultimaFicha:  # Verificar si hay una ficha registrada
        laspirantes = lcarreras.annotate(
            cm=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=2, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=ultimaFicha)), Value(0)),
            cf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=1, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=ultimaFicha)), Value(0)),
            nr=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus=1, carrera1__idAspirante__idProcesoFicha=ultimaFicha)), Value(0)),
            totalmf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=ultimaFicha)), Value(0)),
        ).annotate(
            ts=F('cm') + F('cf'),
            totalmf = F('totalmf') * 100.0 / totalAspirantesR
        ).values(
            'nombreCarrera', 'cm', 'cf', 'ts', 'nr', 'totalmf'
        )
        
        tm = sum(aspirante['cm'] for aspirante in laspirantes) #suma el total de hombres
        tf = sum(aspirante['cf'] for aspirante in laspirantes) #suma el total de mujeres
        totalRegistrados = tm + tf
        t = sum(aspirante['nr'] for aspirante in laspirantes) #suma los aspirantes que solo hicieron pre-registro y aun no se registran

    else:
        laspirantes = lcarreras.annotate(
            cm=Value(0, output_field=IntegerField()),
            cf=Value(0, output_field=IntegerField()),
            ts=Value(0, output_field=IntegerField())
        ).values(
            'nombreCarrera', 'cm', 'cf', 'ts', 'nr'
        )

    return render(request, "aspirantes/aspirantesRegistrados.html", {
        "lcarreras": lcarreras,
        "lfichas": lfichas,
        "ultimaFicha": ultimaFicha,
        "laspirantes": laspirantes,
        "totalRegistrados": totalRegistrados,
        "tm": tm,
        "tf": tf,
        "t": t,
        "cm": 0,
        "cf": 0
    })

def aspirantesRegistradosFiltro(request):
    lfichas = procesosFichas.objects.all()  # Obtener todos los procesos de fichas existentes
    totalRegistrados=''
    laspirantes=''
    fichaS = request.GET.get('ficha', None)
    fechaInicioS = request.GET.get('fechaInicio', '')
    fechaFinS = request.GET.get('fechaFin', '')
    #ultimaFicha = procesosFichas.objects.order_by('idProcesoFicha').first()  # Obtener el último proceso de fichas registrado
    t=tm=tf=0
    # Obtener todas las carreras registradas que estén activas
    lcarreras = carreras.objects.filter(estatus=1)
    if not fechaInicioS:

        totalAspirantesR = aspirantes.objects.filter(estatus__gt=1, idProcesoFicha=fichaS).count()
        
    # Verificar si hay una ficha registrada
        laspirantes = lcarreras.annotate(
            cm=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=2, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=fichaS)), Value(0)),
            cf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=1, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=fichaS)), Value(0)),
            nr=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus=1, carrera1__idAspirante__idProcesoFicha=fichaS)), Value(0)),
            totalmf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha=fichaS)), Value(0)),
        ).annotate(
            ts=F('cm') + F('cf'),
            totalmf = F('totalmf') * 100.0 / totalAspirantesR
        ).values(
            'nombreCarrera', 'cm', 'cf', 'ts', 'nr', 'totalmf'
        )
        
        tm = sum(aspirante['cm'] for aspirante in laspirantes) #suma el total de hombres
        tf = sum(aspirante['cf'] for aspirante in laspirantes) #suma el total de mujeres
        totalRegistrados = tm + tf
        t = sum(aspirante['nr'] for aspirante in laspirantes) #suma los aspirantes que solo hicieron pre-registro y aun no se registran

    else:
        fechaInicio = datetime.strptime(fechaInicioS, '%Y-%m-%d').date()
        fechaFin = datetime.strptime(fechaFinS, '%Y-%m-%d').date()

        procesosEnRango = procesosFichas.objects.filter(
            Q(fechaInicioFicha__range=[fechaInicio, fechaFin]) |
            Q(fechaFinFicha__range=[fechaInicio, fechaFin])
        ).values_list('idProcesoFicha', flat=True)

        # Filtrar los aspirantes por idProcesoFicha en procesosEnRango
        totalAspirantesR = aspirantes.objects.filter(
            estatus__gt=1,
            idProcesoFicha__in=procesosEnRango
        ).count()

        laspirantes = lcarreras.annotate(
        cm=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=2, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha__in=procesosEnRango)), Value(0)),
        cf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idPersona__sexo=1, carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha__in=procesosEnRango)), Value(0)),
        nr=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus=1, carrera1__idAspirante__idProcesoFicha__in=procesosEnRango)), Value(0)),
        totalmf=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__estatus__gt=1, carrera1__idAspirante__idProcesoFicha__in=procesosEnRango)), Value(0)),
        ).annotate(
            ts=F('cm') + F('cf'),
            totalmf=F('totalmf') * 100.0 / totalAspirantesR
        ).values(
            'nombreCarrera', 'cm', 'cf', 'ts', 'nr', 'totalmf'
        )

        tm = sum(aspirante['cm'] for aspirante in laspirantes)  # suma el total de hombres
        tf = sum(aspirante['cf'] for aspirante in laspirantes)  # suma el total de mujeres
        totalRegistrados = tm + tf
        t = sum(aspirante['nr'] for aspirante in laspirantes)

    
    fichaS= int(fichaS)
    

    return render(request, "aspirantes/aspirantesRegistrados.html", {
        "lcarreras": lcarreras,
        "lfichas": lfichas,
        "ultimaFicha": fichaS,
        "laspirantes": laspirantes,
        "totalRegistrados": totalRegistrados,
        "tm": tm,
        "tf": tf,
        "t": t,
        "cm": 0,
        "cf": 0
    })

def aspirantesInscritos(request): 
    lperiodos = periodo.objects.order_by('-idPeriodo') 
    lcarreras = carreras.objects.all()
    periodoInicioClases = lperiodos.first()
    #laspirantes = aspirantes.objects.all()#esta es solo para pruebas
    lempleados = empleados.objects.filter(estatus=1)

    laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoInicioClases)
    
    max_id_subquery = laspirantes.values('idPersona__curp').annotate(max_id=Max('idAspirante')).values('max_id')
    
    # Filtrar los aspirantes para quedarte solo con los registros más recientes por curp y no se repita
    laspirantes = laspirantes.filter(idAspirante__in=Subquery(max_id_subquery))

   
    return render (request, "aspirantes/aspirantesInscritos.html", {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "lempleados": lempleados,
        "lcarreras": lcarreras,
        "periodoInicioClases" : periodoInicioClases
    })

def get_paises(request):
    lpaises = list(paises.objects.values('idPais', 'nombre'))
    return JsonResponse(lpaises, safe=False)

def get_estados(request, idPais):
    lestados = list(estados.objects.filter(idPais=idPais).values('idEstado', 'nombreEstado'))
    return JsonResponse(lestados, safe=False)

def get_municipios(request, idEstado):
    lmunicipios = list(municipios.objects.filter(idEstado=idEstado).values('idMunicipio', 'nombreMunicipio'))
    return JsonResponse(lmunicipios, safe=False)

def get_colonias(request, idMunicipio):
    lcolonias = list(colonias.objects.filter(idMunicipio=idMunicipio).values('idColonia', 'nombreColonia'))
    return JsonResponse(lcolonias, safe=False)

def get_escuelaid(request, idEscuelaProcedencia):
    lescuelaid = list(escuelasProcedencia.objects.filter(idEscuelaProcedencia=idEscuelaProcedencia, estatus=1).values('idEscuelaProcedencia', 'nombreEscuela', 'claveEscuela', 'direccionEscuela', 'telefonoEscuela'))
    return JsonResponse(lescuelaid, safe=False)

def get_escuelas(request, idMunicipio):
    lescuelas = list(escuelasProcedencia.objects.filter(municipioEscuela=idMunicipio, estatus=1).values('idEscuelaProcedencia', 'nombreEscuela', 'claveEscuela', 'direccionEscuela', 'telefonoEscuela'))    
    return JsonResponse(lescuelas, safe=False)

def get_estados2(request):
    lestados = list(estados.objects.values('idEstado', 'nombreEstado'))
    return JsonResponse(lestados, safe=False)

def get_uni(request):
    lpaises = list(universidades.objects.values('idUniversidad', 'nombre'))
    return JsonResponse(lpaises, safe=False)

def preRegistro2(request):
    return render (request, "preRegistro2.html")

# Vista para el formulario de registrar Universidades
def Universidadades(request):
    return render (request, "universidades/Universidades.html")

#Vista Para la tabla de Universidades registradas
def tablaUniversidades(request):
    universidades_listado = universidades.objects.all()

    paginator = Paginator(universidades_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "universidades/tablaUniversidades.html", {"universidades": page_obj})


# View que registar los datos del formulario de Universidades
def registrarUniversidad(request):
    NOMUNIVERSIDAD = request.POST['universidad']
    SIGLAS = request.POST ['siglas']
    ESTADO = request.POST.get('estatus','0')
    RECTOR = request.POST['rector']
    MUNICIPIOUNI_ID = request.POST['mpioE']

    if universidades.objects.filter(nombre=NOMUNIVERSIDAD).exists():
        messages.warning(request, 'Error, ya existe una universidad con ese nombre')
        return redirect('/universidad/')
    else:

        MUNICIPIOUNI = municipios.objects.get(idMunicipio=MUNICIPIOUNI_ID)
        insUniversidad= universidades.objects.create(nombre=NOMUNIVERSIDAD, siglas=SIGLAS, estatus=ESTADO, nombreRector=RECTOR,  municipioUniversidad=MUNICIPIOUNI)
        messages.success(request, 'Universidad registrada correctamente.')
    return redirect('/tablaUniversidades/')


# View que edita los datos en la tabla de Universidades
def editar_universidad(request, idUniversidad):
    universidad = get_object_or_404(universidades, idUniversidad=idUniversidad)
    nombreUniversidad = request.GET.get('universidad', universidad.nombre)
    siglas = request.GET.get('siglas')
    nombreRector = request.GET.get('nombreRector')
    estatus = request.GET.get('estatus')

    universidad.nombre = nombreUniversidad
    universidad.siglas = siglas
    universidad.nombreRector = nombreRector
    universidad.estatus = estatus
    universidad.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaUniversidades/')

# View para el formulario de registrar Carreras
def Carreras(request):
    lEmpleados = empleados.objects.all()
    return render (request, "carreras/Carreras.html", {'lEmpleados': lEmpleados})

# View para los registros del formulario de carreras
def tablaCarreras(request):
    carreras_listado = carreras.objects.order_by('-estatus', 'nombreCarrera')
    for carrera in carreras_listado:
        if carrera.nivel==1:
            carrera.nivel_view='TSU'
        else:
            carrera.nivel_view='ING'

    paginator = Paginator(carreras_listado, 13)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'carreras/tablaCarreras.html', {'carreras': page_obj})


# View para registrar los datos del formulario de Carreras
def registrarCarrera(request):
    NOMCARRERA = request.POST['carrera']
    SIGLAS = request.POST ['siglas_carrera']
    ESTADO = request.POST.get('estatus','1')
    NIVEL = request.POST['nivel'] 
    CLAVE = request.POST['clave']
    MODALIDAD = request.POST['modalidad']
    AREA = request.POST['area']
    DIRECTOR = request.POST['director']
    
    objDirector = empleados.objects.get(idEmpleado=DIRECTOR)
    if carreras.objects.filter(nombreCarrera=NOMCARRERA).exists():
        messages.warning(request, 'Error, ya existe una carrera con ese nombre')
        return redirect('/carrera/')
    else:
        insCarrera = carreras.objects.create(nombreCarrera=NOMCARRERA, siglas=SIGLAS, estatus=ESTADO, nivel=NIVEL, clave=CLAVE, modalidad=MODALIDAD, area=AREA, idEmpleado=objDirector)
        messages.success(request, 'Carrera registrada correctamente.')
    return redirect('/tablaCarreras/') 

#  View para editar los datos en la tabla de Carreras
def editar_carrera(request, idCarrera):
    carrera = get_object_or_404(carreras, idCarrera=idCarrera)
    nombreCarrera = request.GET.get('carrera', carrera.nombreCarrera)
    siglas = request.GET.get('siglas')
    area = request.GET.get('area')
    director = request.GET.get('director')
    clave = request.GET.get('clave')
    nivel_view = request.GET.get('nivel')
    estatus = request.GET.get('estatus')
    nivel=0

    if nivel_view =='TSU':
        nivel=1
    elif nivel_view=='ING':
        nivel=2   
    else:
        messages.warning(request, 'Para el campo nivel solo puedes poner TSU o ING')
        return redirect('/tablaCarreras/')

    carrera.nombreCarrera = nombreCarrera
    carrera.siglas = siglas
    carrera.area = area
    carrera.clave = clave
    carrera.nivel = nivel
    carrera.estatus = estatus
    try:
        carrera.save()
        messages.success(request, 'Se guardaron los cambios')
    except Exception as e:
        messages.error(request, f'No se pudieron guardar los cambios: {e}')
    
    return redirect('/tablaCarreras/') 




# View para el formulario de registrar escuelas de procedencia
def escuela(request):
    return render (request, "escuelas/escuelas.html")

# View para la tabla de regitsros del formulario de Escuelas de procedencia
def tablaEscuelas(request):
    escuelas_listado = escuelasProcedencia.objects.all()

    paginator = Paginator(escuelas_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "escuelas/tablaEscuelas.html", {"escuelas": page_obj})


# View para registrar las escuelas de procedecia
def registrarEscuela(request):
    NOMESCUELA = request.POST['escuela']
    CLAVE = request.POST ['claveEscuela']
    DIRECCION = request.POST ['dirEscuela']
    TELEFONO = request.POST ['telEscuela']
    ESTADO = request.POST.get('estatus','0')
    MUNICIPIOESCUELA_ID = request.POST['mpioE']
    SUBSISTEMA_ID= request.POST ['subsistema']

    if escuelasProcedencia.objects.filter(nombreEscuela=NOMESCUELA).exists():
        messages.warning(request, 'Error, ya existe escuela con ese nombre')
        return redirect('/escuelas/')
    else:

        MUNICIPIOUNIESCUELA = municipios.objects.get(idMunicipio=MUNICIPIOESCUELA_ID)
        SUBSISTEMA = subsistemas.objects.get(idSubsistema=SUBSISTEMA_ID)
        insEscuela= escuelasProcedencia.objects.create(nombreEscuela=NOMESCUELA, claveEscuela=CLAVE, direccionEscuela= DIRECCION, telefonoEscuela= TELEFONO, estatus=ESTADO, municipioEscuela=MUNICIPIOUNIESCUELA, idSubsistema = SUBSISTEMA )
        messages.success(request, 'Escuela registrada correctamente.')
    return redirect('/tablaEscuelas/')


# View para editar los campos en la tabla de escuelas de procedencia
def editar_escuela(request, idEscuelaProcedencia):
    escuela = get_object_or_404(escuelasProcedencia, idEscuelaProcedencia=idEscuelaProcedencia)
    nombreEscuela = request.GET.get('escuela', escuela.nombreEscuela)
    claveEscuela = request.GET.get('claveEscuela')
    direccionEscuela = request.GET.get('direccionEscuela')
    telefonoEscuela = request.GET.get('telefonoEscuela')
    estatus = request.GET.get('estatus','0')

    escuela.nombreEscuela = nombreEscuela
    escuela.claveEscuela = claveEscuela
    escuela.direccionEscuela = direccionEscuela
    escuela.telefonoEscuela = telefonoEscuela
    escuela.estatus = estatus
    escuela.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaEscuelas/')

# View para el formulario de subsistemas
def subsistema(request):
    return render (request, "subsistemas/subsistemas.html")

# View para la tabla de los registros de subsistemas
def tablaSubsistemas(request):
    subsistemas_listado = subsistemas.objects.all()

    paginator = Paginator(subsistemas_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "subsistemas/tablaSubsistemas.html", {"subsistemas": page_obj})

# View para registrar los subsistemas
def registrarSusbsistema(request):
    SUBSISTEMA = request.POST['subsistema']
 
    if subsistemas.objects.filter(nombre=SUBSISTEMA).exists():
        messages.warning(request, 'Error, este susbsistema ya existe')
        return redirect('/subsistema/')
    else:
        insSubsistema = subsistemas.objects.create(nombre=SUBSISTEMA)
        messages.success(request, 'Subsistema registrado correctamente.')
    return redirect('/tablaSubsistemas/')

# View para cargar el combo de los registros de subsitemas en el formulario de escuelas de procedencia
def obtener_subsistemas(request):
    subsistemas_list = subsistemas.objects.all().values('idSubsistema', 'nombre')
    return JsonResponse(list(subsistemas_list), safe=False)

# View para editar los datos en la tabla de subsistemas
def editar_subsistema(request, idSubsistema):
    subsistema = get_object_or_404(subsistemas, idSubsistema=idSubsistema)
    nombreSubsistema = request.GET.get('nombre', subsistema.nombre)
   
    subsistema.nombre = nombreSubsistema
    subsistema.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaSubsistemas/')


#view para cargar el formulario de fichas
def fichas(request):
    fichas = procesosFichas.objects.all()
    periodos = periodo.objects.all() 
    
    return render(request, "Fichas/fichas.html", {'fichas': fichas, 'periodos': periodos})


# View para registrar los procesos de las fichas 
def registrarFicha(request):
    FECHAINICIO = request.POST['fechaInicio']
    FECHAFIN = request.POST ['fechaFin']
    FECHAEXANI = request.POST ['fechaExam']
    HOREXANI = request.POST ['horaExam']
    PERIODO_ID= request.POST.get('periodo')
    LUGAR = request.POST['lugar']
    

    fecha_inicio = datetime.strptime(FECHAINICIO, '%Y-%m-%d')
    fecha_fin = datetime.strptime(FECHAFIN, '%Y-%m-%d')

    if fecha_fin < fecha_inicio:
        messages.error(request, 'La fecha de finalizacion no puede ser anterior a la fecha de inicio.')
        return redirect('/fichas/')
    elif procesosFichas.objects.filter(fechaInicioFicha=FECHAINICIO).exists():
        messages.warning(request, 'Error, ya existe una ficha con esta fecha')
        return redirect('/fichas/')
    else:
        PERIODO = periodo.objects.get(idPeriodo=PERIODO_ID)
        insFicha= procesosFichas.objects.create(fechaInicioFicha=FECHAINICIO, fechaFinFicha=FECHAFIN, fechaExani= FECHAEXANI, horaExani= HOREXANI, PeriodoInicioClases=PERIODO, lugarAplicacion=LUGAR)
        messages.success(request, 'Ficha registrada correctamente.')
    return redirect('/tablaFichas/')



#view para cargar el formulario de fichas
def fichas(request):
    fichas = procesosFichas.objects.all()
    periodos = periodo.objects.all() 
    return render(request, "Fichas/fichas.html", {'fichas': fichas, 'periodos': periodos})

    
# View para la tabla de los registros de fichas
def tablaFichas(request):
    fichas_listado = procesosFichas.objects.all()

    paginator = Paginator(fichas_listado, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "Fichas/tablaFichas.html", {"fichas": page_obj})


# View para editar los datos en la tabla de fichas
def editar_ficha(request, idProcesoFicha):
    ficha = get_object_or_404(procesosFichas, idProcesoFicha=idProcesoFicha)
    fechaInicioFicha = request.GET.get('fechaInicio', ficha.fechaInicioFicha)
    fechaFinFicha = request.GET.get('fechaFin')
    fechaExani = request.GET.get('fechaExam')
    horaExani = request.GET.get('horaExam')
    lugarAplicacion = request.GET.get('lugar')

   
    ficha.fechaInicioFicha = fechaInicioFicha
    ficha.fechaFinFicha = fechaFinFicha
    ficha.fechaExani = fechaExani
    ficha.horaExani = horaExani
    ficha.lugarAplicacion = lugarAplicacion
    ficha.save()
    messages.success(request, 'Se guardaron los cambios')
    return redirect('/tablaFichas/')




#View que obtiene y compara la curp del aspirafichas la fecha de registro
def get_curp(request):
    curpAct = request.POST.get('curp', None)
    if curpAct:
        response_data = {}
        personas_con_curp = personas.objects.filter(curp=curpAct).order_by('-aspirantes__fechaRegistro')
        if personas_con_curp.exists():

            objPersona = personas_con_curp[0]
            objAspirante = aspirantes.objects.get(idPersona=objPersona)
            fecha_registro = objAspirante.fechaRegistro
            fecha_actual = timezone.now().date()
            diferencia_meses = (fecha_actual.year - fecha_registro.year) * 12 + fecha_actual.month - fecha_registro.month
            if diferencia_meses < 1:
                response_data['error'] = 'No te puedes regisrar más de una vez por mes'
            """else:
                print('Te puedes reinscribir')
        else:
            print('Curp no registrada')
    else:
        print('Sin datos')"""
    return JsonResponse(response_data,safe=False)


#View que recopila los datos del formulario de pre-registro y realiza las inserciones en la BD
def guardaAsp(request):
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
        INDIGENA = request.POST.get('indigena', 0)
        AFROAMERICANO = request.POST.get('afroamericano', 0)     
        MIGRANTE = request.POST.get('migrante',0)
        NACIONALIDAD = request.POST['nacionalidad']
        ESTADONAC = request.POST['estadoNacimiento']
        MPIONAC = request.POST['mpioNacimiento']
        CALLE = request.POST['calle']
        NUM = request.POST['numero']
        CP = request.POST['cp']
        ZONA = request.POST['zona']
        ESTADO = request.POST['estado']
        MPIO = request.POST['mpio']
        COLONIA = request.POST['colonia']
        ESCUELAPROC = request.POST['escuelaProcedencia']
        INGRESO = request.POST['ingreso']
        EGRESO = request.POST['egreso']
        PROM = request.POST['prom']
        ESCUELAESP = request.POST['escuelaEspecialidad']
        PESO = request.POST['peso']
        ESTATURA = request.POST['estatura']
        TIPOSANGRE = request.POST['tipoSangre']
        HIPERTENSOS = request.POST.get('hipertensos', 0)
        DIABETICOS = request.POST.get('diabeticos', 0) 
        CARDIACOS = request.POST.get('cardiacos', 0)
        ENTERARSE = request.POST['enterarse']
        ENTERARSEFICHAS = request.POST['enterarseFichas']
        PORQUEUTSOE = request.POST['porqueutsoe']
        try:
            CUALUNI = request.POST['cualuni']
        except KeyError:
            CUALUNI = 0
        NOMBRET = request.POST['nombreTutor']
        APE1T = request.POST['ape1Tutor']
        APE2T = request.POST['ape2Tutor']
        CARRERA1 = request.POST['carrera1']
        CARRERA2 = request.POST['carrera2']
        ACTA = request.FILES['acta']
        CURPDOC = request.FILES['curpDoc']
        CERTIFICADO = request.FILES.get('certificado')
        CONSTANCIA = request.FILES.get('constancia')
        FOTO = request.FILES['foto']
        NOMBREUSER = request.POST['nombreUser']
        PASS1 = request.POST['pass1']
        FECHA_ACTUAL = datetime.now()
        DOCS = []
        #normalizar datos
        NOMBRE = NOMBRE.capitalize()
        APE1 = APE1.capitalize()
        APE2 = APE2.capitalize()
        CORREO = CORREO.lower()
        CALLE = CALLE.capitalize()
        print(NOMBRE + " " + APE1 + " " + APE2 + " " + CORREO + " " + CALLE)
        #instancias
        IDTIPOUSUARIO = tiposUsuarios.objects.get(idTipoUsuario=5)
        COLONIA = colonias.objects.get(idColonia=COLONIA)
        MPIO = municipios.objects.get(idMunicipio=MPIO)
        ESCUELAPROC = escuelasProcedencia.objects.get(idEscuelaProcedencia=ESCUELAPROC)
        IDPROCESOFICHA = procesosFichas.objects.get(idProcesoFicha=1)
        IDUSUARIOREGISTRA = usuarios.objects.get(idUsuario=1)
        CARRERA1 = carreras.objects.get(idCarrera=CARRERA1)
        CARRERA2 = carreras.objects.get(idCarrera = CARRERA2)
        #Registros en la BD
        insUsuario = usuarios.objects.create(usuario=NOMBREUSER, contraseña=PASS1, fechaAlta=FECHA_ACTUAL, idTipoUsuario=IDTIPOUSUARIO)
        if APE2 != 0:
            insPersona = personas.objects.create(curp=CURP, nombre=NOMBRE, ape1=APE1, ape2=APE2, calle=CALLE, numero=NUM, zona=ZONA, cp=CP, idColonia=COLONIA, idMunicipioNacimiento=MPIO, nacionalidad=NACIONALIDAD, sexo=SEXO, estatus=1, telCasa=TEL, telCelular=CEL, estadoCivil=ESTADOCIV, hijos=HIJOS, correo=CORREO, idUsuario=insUsuario)
        else:
            insPersona = personas.objects.create(curp=CURP, nombre=NOMBRE, ape1=APE1, calle=CALLE, numero=NUM, zona=ZONA, cp=CP, idColonia=COLONIA, idMunicipioNacimiento=MPIO, nacionalidad=NACIONALIDAD, sexo=SEXO, estatus=1, telCasa=TEL, telCelular=CEL, estadoCivil=ESTADOCIV, hijos=HIJOS, correo=CORREO, idUsuario=insUsuario)
        insAspirantes = aspirantes.objects.create(idPersona=insPersona, añoIngresoPrepa=INGRESO, añoEgresoPrepa=EGRESO, promedioPrepa=PROM, especialidadPrepa=ESCUELAESP, idEscuelaProcedencia=ESCUELAPROC, nombreTutor=NOMBRET, ape1Tutor=APE1T, ape2Tutor=APE2T, folioCeneval=0, folioPagoFicha=0, fechaRegistro=FECHA_ACTUAL, idProcesoFicha=IDPROCESOFICHA, idUsuarioRegistra=IDUSUARIOREGISTRA, nivel=1, estatus=1)
        insdatosM = datosMedicos.objects.create(idPersona=insPersona, peso=PESO, estatura=ESTATURA, famDiabeticos=DIABETICOS, famHipertensos=HIPERTENSOS, famCardiacos=CARDIACOS, tipoSangre=TIPOSANGRE)
        insEncuesta = encuesta.objects.create(idAspirante=insAspirantes, enterarUniversidad=ENTERARSE, medioEntregaFicha=ENTERARSEFICHAS, razonInscripcion=PORQUEUTSOE, otraUniversidad=CUALUNI, idCarrera=CARRERA1, idCarrera2=CARRERA2)   
        if INDIGENA == '1':
            objDato = otrosDatos.objects.get(idDato = 1)
            insDetalleOtroDato = detalleOtroDato.objects.create(idAspirante = insAspirantes, idDato = objDato)
        if AFROAMERICANO == '1':
            objDato = otrosDatos.objects.get(idDato = 2)
            insDetalleOtroDato = detalleOtroDato.objects.create(idAspirante = insAspirantes, idDato = objDato)
        if MIGRANTE == '1':
            objDato = otrosDatos.objects.get(idDato = 3)
            insDetalleOtroDato = detalleOtroDato.objects.create(idAspirante = insAspirantes, idDato = objDato)
        
        # Carpeta donde se guardarán los archivos
        nuevaRuta = os.path.join(settings.BASE_DIR, 'apps', 'Aspirante', 'Docs')
        #En caso de no cargar certificado
        if CERTIFICADO is None:
            for file_field in ['acta', 'curpDoc', 'constancia', 'foto']:
                uploaded_file = request.FILES.get(file_field)
                if uploaded_file:
                    # Renombrar el archivo
                    new_filename = f"{CURP}_{file_field}{os.path.splitext(uploaded_file.name)[1]}"
                    file_path = os.path.join(nuevaRuta, new_filename)
                
                    #Guardar el nombre del archivo renombrado en la lista
                    DOCS.append(new_filename)

                    # Guardar el archivo en el directorio especificado
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                           
            insDocumentos = documentos.objects.create(idAspirante=insAspirantes, acta=DOCS[0], curp=DOCS[1], constancia=DOCS[2], foto=DOCS[3])
            DOCUMENTOCONDICIONADO=  insDocumentos.pk
            DOCUMENTOCONDICIONADO= documentos.objects.get(idDocumento=DOCUMENTOCONDICIONADO) 
            #FECHAENTREGA = FECHA_ACTUAL + timedelta(days=60)
            insCondicionado = documentoCondicionado.objects.create(fechaEntrega=FECHAENTREGA, estatus=0, idDocumento=DOCUMENTOCONDICIONADO)
            
        else: #En caso de cargar certificado
            for file_field in ['acta', 'curpDoc', 'certificado', 'foto']:
                uploaded_file = request.FILES.get(file_field)
                if uploaded_file:
                    # Renombrar el archivo
                    new_filename = f"{CURP}_{file_field}{os.path.splitext(uploaded_file.name)[1]}" 
                    file_path = os.path.join(nuevaRuta, new_filename)
                
                    #Guardar el nombre del archivo renombrado en la lista
                    DOCS.append(new_filename)

                    # Guardar el archivo en el directorio especificado
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
            insDocumentos = documentos.objects.create(idAspirante=insAspirantes, acta=DOCS[0], curp=DOCS[1], certificadoBachillerato=DOCS[2], foto=DOCS[3])                
        
        messages.success(request, 'Has realizado tu Pre Registro con éxito')
        return redirect('reporte/{}'.format(insAspirantes.pk))
        #return redirect('reporte/{}'.format(insAspirantes.pk))
        #return redirect('reporte/', idAspirante=insAspirantes.pk)
    else:
        messages.warning(request, 'Ha ocurrido un error durante tu Pre Registro, intenta de nuevo por favor')
        return render(request, 'aspirantes/preRegistro.html')

#View que maqueta el reporte de pre-registro
def reportePreR(request):
    return render(request, 'reportes/reportePreRegistro.html')

#View que carga el formulario de busqueda de aspirantes
def buscarAspirate(request):
    return render (request, "aspirantes/buscaAspirantes.html")

#View que devuelve los datos del aspirante
def get_aspirante(request):
    filters = {}
    if request.method == 'POST':
        try:
            folio = request.POST['folioBusca']
        except:
            folio = 0
        try:
            nombreP = request.POST['nombreBusca']
            #filters['nombre__in'] = [nombreP]
        except:
            nombreP = None
        try:
            ape1P = request.POST['ape1Busca']
            #filters['ape1__in'] = [ape1P]
        except:
            ape1P = None
        try:
            ape2P = request.POST['ape2Busca']
            #filters['ape2__in'] = [ape2P]
        except:
            ape2P = None


        print(ape1P)
        print(ape2P)
        print(nombreP)

        if folio != 0 and folio != '.':
            try:
                objPersona = personas.objects.filter(idPersona = folio).order_by('-aspirantes__fechaRegistro').first()
                messages.success(request, 'Aspirante encontrado.')
                print("folio")
                return redirect('/editaAspirante/{}'.format(objPersona.pk))
            except:
                messages.warning(request, 'Aspirante no encontrado.')
                print("folio ex")
                return redirect('/aspirantes/')
        else:
            if ape1P is not None and ape2P!='':
                try:
                    objPersona = personas.objects.filter(nombre = nombreP, ape1 = ape1P, ape2 = ape2P).order_by('-aspirantes__fechaRegistro').first()
                    messages.success(request, 'Aspirante encontrado.')
                    print("completo")
                    return redirect('/editaAspirante/{}'.format(objPersona.pk))
                except:
                    print("completo ex")
                    messages.warning(request, 'Aspirante no encontrado.')
                    return redirect('/aspirantes/')
            else:
                try:
                    objPersona = personas.objects.filter(nombre = nombreP, ape1 = ape1P).order_by('-aspirantes__fechaRegistro').first()
                    messages.success(request, 'Aspirante encontrado.')
                    print("1 PELLIDO")
                    return redirect('/editaAspirante/{}'.format(objPersona.pk))
                except:
                    print("1 PELLIDO ex")
                    messages.warning(request, 'Aspirante no encontrado.')
                    return redirect('/aspirantes/')
    else:
        messages.warning(request, 'No se han enviado datos.')
        return redirect('/aspirantes/')

#View para editar datos del aspirante
def editarAspirante(request, id):
    #Instancias
    objPersona = personas.objects.get(pk = id)
    objAspirante = aspirantes.objects.get(idPersona = objPersona.pk)
    objEncuesta = encuesta.objects.get(idAspirante = objAspirante.pk)
    objDocumento = documentos.objects.get(idAspirante = objAspirante.pk)
    objCarreras = carreras.objects.filter(estatus=1, nivel=1)
    #Calculo de edad 
    curp = objPersona.curp
    
    anio_nacimiento = int(curp[4:6])
    if anio_nacimiento<24:
        anio_nacimiento += 2000
    else:
        anio_nacimiento += 1900
   
    mes_nacimiento = int(curp[6:8])
    dia_nacimiento = int(curp[8:10])
    fecha_nacimiento = datetime(anio_nacimiento, mes_nacimiento, dia_nacimiento)

    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    
    datos = {
        "persona": objPersona,
        "aspirante": objAspirante,
        "encuesta": objEncuesta,
        "documentos": objDocumento,
        "carreras": objCarreras,
        "edad": edad
    }
    return render(request, 'aspirantes/editarAsp.html', datos)

#View para dar de alta a los aspirantes
def actualizarAspirante(request):
    if request.method=='POST':
        ASPIRANTE = request.POST['aspirante']
        CURP = request.POST['curp']
        NOMBRE = request.POST['nombre']
        APE1 = request.POST['ape1']
        APE2 = request.POST['ape2']
        TELEFONO = request.POST['tel']
        SEXO = request.POST['sexo']
        CORREO = request.POST['correo']
        ESTADOCIV = request.POST['estadoCivil']
        HIJOS = request.POST['hijos']
        CALLE = request.POST['calle']
        NUMERO = request.POST['numero']
        INGRESO = request.POST['ingreso']
        EGRESO = request.POST['egreso']
        PROM = request.POST['prom']
        CARRERA = request.POST['carrera1']
        CENEVAL = request.POST['folioCeneval']
        FICHA = request.POST['folioFicha']
        ACTA = request.POST['acta']
        CURPDOC = request.POST['curpDoc']
        try:
            CERTIFICADO = request.POST['certificado']
        except:
            CERTIFICADO = None
        try:
            CONSTANCIA = request.POST['constancia']
        except:
            CONSTANCIA = None
        FOTO = request.POST['foto']

        #Instancias
        objAspirante = aspirantes.objects.get(pk = ASPIRANTE)
        objPersona = personas.objects.get(idPersona = objAspirante.idPersona_id)
        objDocumento = documentos.objects.get(idAspirante = objAspirante.pk)
        objEncuesta = encuesta.objects.get(idAspirante = objAspirante.pk)
        CARRERA = carreras.objects.get(idCarrera = CARRERA)
        #Actualizar Personas
        objPersona.curp = CURP
        objPersona.nombre = NOMBRE
        objPersona.ape1 = APE1
        objPersona.ape2 = APE2
        objPersona.calle = CALLE
        objPersona.numero = NUMERO
        objPersona.estadoCivil = ESTADOCIV
        objPersona.telCasa = TELEFONO
        objPersona.correo = CORREO
        objPersona.hijos = HIJOS
        objPersona.sexo = SEXO
        
        try:
            objPersona.save()
        except (ValidationError, IntegrityError) as e:  
            messages.warning(request, 'Persona errror.')
            return redirect('/aspirantes/') 
        #Actualizar Aspirante
        objAspirante.añoIngresoPrepa = INGRESO
        objAspirante.añoEgresoPrepa = EGRESO
        objAspirante.promedioPrepa = PROM
        objAspirante.folioCeneval = CENEVAL
        objAspirante.folioPagoFicha = FICHA
        objAspirante.estatus = 2
        try:
            objAspirante.save()
        except (ValidationError, IntegrityError) as e:  
            messages.warning(request, 'Aspirante error.')
            return redirect('/aspirantes/') 
        #Actualizar Documentos
        objDocumento.actaF = ACTA
        objDocumento.curpF = CURPDOC
        objDocumento.certificadoBachilleratoF = CERTIFICADO
        objDocumento.constanciaF = CONSTANCIA
        objDocumento.fotoF = FOTO
        try:
            objDocumento.save()
        except (ValidationError, IntegrityError) as e:  
            messages.warning(request, 'Documentos error.')
            return redirect('/aspirantes/')        
        #Actualizar Encuesta        
        objEncuesta.idCarrera = CARRERA
        try:
            objEncuesta.save()
            return redirect('reporte/{}'.format(objAspirante.pk))
        except (ValidationError, IntegrityError) as e:  
            messages.warning(request, 'Encuesta error.')
            return redirect('/aspirantes/') 
    else:
        messages.warning(request, 'No se ha seleccionado ningun aspirante')
        return redirect('/aspirantes/')
    
#View que carga la tabla de aspirantes y los filtra
def mostrarAspirantes(request):
    laspirantes = aspirantes.objects.filter(estatus=2)
    return render(request, 'aspirantes/tablaAspirantes.html', {"laspirantes": laspirantes})

def editarAspiranteAcp(request, id):
    #instancias
    objPersona = personas.objects.get(pk = id)
    objAspirante = aspirantes.objects.get(idPersona = objPersona.pk)
    objEncuesta = encuesta.objects.get(idAspirante = objAspirante.pk)
    objCarreras = carreras.objects.all()
    #Calculo de edad 
    curp = objPersona.curp
    
    anio_nacimiento = int(curp[4:6])
    if anio_nacimiento<24:
        anio_nacimiento += 2000
    else:
        anio_nacimiento += 1900
   
    mes_nacimiento = int(curp[6:8])
    dia_nacimiento = int(curp[8:10])
    fecha_nacimiento = datetime(anio_nacimiento, mes_nacimiento, dia_nacimiento)

    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    
    datos = {
        "persona": objPersona,
        "aspirante": objAspirante,
        "encuesta": objEncuesta,
        "carreras": objCarreras,
        "edad": edad
    }
    return render(request, 'aspirantes/editarAspiranteAcp.html', datos)

#View para actualizar los datos de los aspirantes aceptados
def actualizarAspiranteAcp(request):
    if request.method=='POST':
        #Instancias
        objAspirante = aspirantes.objects.get(pk = ASPIRANTE)
        objPersona = personas.objects.get(idPersona = objAspirante.idPersona_id)
        objDocumento = documentos.objects.get(idAspirante = objAspirante.pk)
        CARRERA = carreras.objects.get(idCarrera = CARRERA)
        #Obtener datos
        ASPIRANTE = request.POST['aspirante']
        CARRERA = request.POST['carrera']
        PLANESTUDIO = request.POST['planEstudios']
        PERIODO = request.POST['periodo']
        GRUPO = request.POST['grupo']
        CARRERA = request.POST['carrera1']
        CENEVAL = request.POST['folioCeneval']
        FICHA = request.POST['folioFichaPago']
        ACTA = request.POST['acta']
        CURPDOC = request.POST['curpDoc']
        FOTO = request.POST['foto']
        ANALISIS = request.POST['analisisMedico']
        try:
            CONSTANCIA = request.POST['constancia']
        except:
            CONSTANCIA = None
        try:
            FECHACONDICIONADO = request.POST['fechaCondicinado']
        except:
            FECHACONDICIONADO = None
        try:
            CONDICIONADO = request.POST['condicionado']
            objCondicionado = documentoCondicionado.objects.get(idDocumento = objDocumento.pk)
        except:
            CONDICIONADO = None
        #Actualizar Documentos
        objDocumento.actaF = 2
        objDocumento.curpF = 2
        objDocumento.fotoF = 2
        objDocumento.analisisSanguineoF = 2
        if CONDICIONADO == None:
            objDocumento.certificadoBachilleratoF = 0
            objCondicionado.fechaEntrega = FECHACONDICIONADO
        else:
            objDocumento.certificadoBachilleratoF = 2

        #Actualizar pago queda pendiente 

        #Actualizar carrera, periodo, grupo queda pendiente y redirigir al reporte


    else:
        messages.warning(request, 'No se ha seleccionado ningun aspirante')
        return redirect('/tablaAspirantes/')