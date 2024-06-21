from django.shortcuts import render, redirect, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
import os
from django.conf import settings
from apps.Aspirante.models import aspirantes, encuesta,  documentos
from apps.Usuario.models import usuarios
from apps.Persona.models import personas, carreras
from apps.Alumno.models import periodo
from django.utils import timezone
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Coalesce


#Esta función permite trabajar con archivos estáticos en los reportes PDF
def link_callback(uri, rel):

    s_url = settings.STATIC_URL  
    s_root = settings.STATICFILES_DIRS[0]  

    if uri.startswith(s_url):
        path = os.path.join(s_root, uri.replace(s_url, ""))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        return uri

    # Revisar que el archivo existe
    if not os.path.isfile(path):
        raise Exception(f"Archivo no encontrado: {path}")

    return path

#View que genera el reporte de pre-registro de aspirantes
def reporte_pdf(request, idAspirante):
    # Genarar los datos para el reporte
    objAspirante = aspirantes.objects.get(pk = idAspirante)
    objEncuesta = encuesta.objects.get(idAspirante = objAspirante)
    carrera1 = objEncuesta.idCarrera_id
    carrera1 = carreras.objects.get(idCarrera = carrera1)
    carrera2 = objEncuesta.idCarrera2_id
    carrera2 = carreras.objects.get(idCarrera = carrera2)
    persona = objAspirante.idPersona_id
    objPersona = personas.objects.get(idPersona = persona)
    usuario = usuarios.objects.get(idUsuario = objPersona.idUsuario_id)
    datos = {}
    for field in objAspirante._meta.fields:
        datos[field.name] = getattr(objAspirante, field.name)
    

    # Renderiza la plantilla HTML con los datos
    html = render_to_string('reportes/reportePreRegistro.html', {
        'datos': datos,
        'usuario':usuario,
        'carrera1': carrera1,
        'carrera2': carrera2,
        'static_url': settings.STATIC_URL,
        })

    # Crea una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    # Crear un buffer temporal para el PDF
    buffer = BytesIO()

    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(
        src=html,  # el contenido HTML a convertir
        dest=buffer,  # el buffer en memoria
        link_callback=link_callback  # llamada para resolver las rutas de los archivos estáticos
    )

    # Verifica si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)

    # Volver al principio del buffer
    buffer.seek(0)

    # Lee el contenido del buffer y escribe en la respuesta
    response.write(buffer.read())
    buffer.close()

    return response


def reporteDatosAspirantes(request, idPeriodo, filtro):

    periodoS = idPeriodo
    filtros = filtro

    lperiodos = periodo.objects.all()   
    periodoActivo = periodo.objects.filter(idPeriodo=periodoS).first()
   # laspirantes = aspirantes.objects.all()

    if filtros==1:
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo, estatus=1)
    elif filtros==2:
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo, estatus=2)
    else:        
        laspirantes = aspirantes.objects.filter(idProcesoFicha__PeriodoInicioClases=periodoActivo)


    for aspirante in laspirantes:
        if aspirante.estatus == 1:
            aspirante.estatus_view = 'No Registrado'
        elif aspirante.estatus >= 2:
            aspirante.estatus_view = 'Registrado'
    # Obtén los datos para el reporte

    #datos = ['Marcos', 'Jose', 'Miguel']

    # Renderiza la plantilla HTML con los datos
    html = render_to_string('reportes/reporteDatosAspirantes.html', {
        "laspirantes":laspirantes, 
        "lperiodos": lperiodos,
        "periodoActivo" : periodoActivo,
        "radios" : filtros,
        'static_url': settings.STATIC_URL,
        })

    # Crea una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    # Crear un buffer temporal para el PDF
    buffer = BytesIO()

    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(
        src=html,  # el contenido HTML a convertir
        dest=buffer,  # el buffer en memoria
        link_callback=link_callback  # llamada para resolver las rutas de los archivos estáticos
    )

    # Verifica si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)

    # Volver al principio del buffer
    buffer.seek(0)

    # Lee el contenido del buffer y escribe en la respuesta
    response.write(buffer.read())
    buffer.close()

    return response

#View que genera el reporte de preinscripción aspirantes
def reporteAspirante(request, idAspirante):
    # Genarar los datos para el reporte
    objAspirante = aspirantes.objects.get(idAspirante = idAspirante)
    objEncuesta = encuesta.objects.get(idAspirante = objAspirante)
    carrera1 = objEncuesta.idCarrera_id
    carrera1 = carreras.objects.get(idCarrera = carrera1)
    carrera2 = objEncuesta.idCarrera2_id
    carrera2 = carreras.objects.get(idCarrera = carrera2)
    fechaAct = timezone.now()
    fechaAct = fechaAct.strftime("%d/%m/%Y")
    objUsuario = objAspirante.idUsuarioRegistra_id
    objUsuario = personas.objects.get(idUsuario = objUsuario)
    objDocumentos = documentos.objects.get(idAspirante = objAspirante.pk)
    datos = {}
    for field in objAspirante._meta.fields:
        datos[field.name] = getattr(objAspirante, field.name)
    docs = {}
    for field in objDocumentos._meta.fields:
        docs[field.name] = getattr(objDocumentos, field.name)

    # Renderiza la plantilla HTML con los datos
    html = render_to_string('reportes/reportePreinscripcionAsp.html', {
        'datos': datos,
        'docs': docs,
        'usuario': objUsuario,
        'fecha': fechaAct,
        'carrera1': carrera1,
        'carrera2': carrera2,
        'static_url': settings.STATIC_URL,
        })

    # Crea una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    # Crear un buffer temporal para el PDF
    buffer = BytesIO()

    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(
        src=html,  # el contenido HTML a convertir
        dest=buffer,  # el buffer en memoria
        link_callback=link_callback  # llamada para resolver las rutas de los archivos estáticos
    )

    # Verifica si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)

    # Volver al principio del buffer
    buffer.seek(0)

    # Lee el contenido del buffer y escribe en la respuesta
    response.write(buffer.read())
    buffer.close()

    return response

#View que genera el reporte de inscripción a TSU
def reporteNuevoTSU(request, idAspirante):
    # Genarar los datos para el reporte
    objAspirante = aspirantes.objects.get(idAspirante = idAspirante)
    objEncuesta = encuesta.objects.get(idAspirante = objAspirante)
    carrera1 = objEncuesta.idCarrera_id
    carrera1 = carreras.objects.get(idCarrera = carrera1)
    fechaAct = timezone.now()
    fechaAct = fechaAct.strftime("%d/%m/%Y")
    objUsuario = objAspirante.idUsuarioRegistra_id
    objUsuario = personas.objects.get(idUsuario = objUsuario)
    objDocumentos = documentos.objects.get(idAspirante = objAspirante.pk)
    datos = {}
    for field in objAspirante._meta.fields:
        datos[field.name] = getattr(objAspirante, field.name)
    docs = {}
    for field in objDocumentos._meta.fields:
        docs[field.name] = getattr(objDocumentos, field.name)

    # Renderiza la plantilla HTML con los datos
    html = render_to_string('reportes/reportePreinscripcionAsp.html', {
        'datos': datos,
        'docs': docs,
        'usuario': objUsuario,
        'fecha': fechaAct,
        'carrera1': carrera1,
        'static_url': settings.STATIC_URL,
        })

    # Crea una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    # Crear un buffer temporal para el PDF
    buffer = BytesIO()

    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(
        src=html,  # el contenido HTML a convertir
        dest=buffer,  # el buffer en memoria
        link_callback=link_callback  # llamada para resolver las rutas de los archivos estáticos
    )

    # Verifica si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)

    # Volver al principio del buffer
    buffer.seek(0)

    # Lee el contenido del buffer y escribe en la respuesta
    response.write(buffer.read())
    buffer.close()

    return response

def reporteCapacidadAtencion(request, idAspirante):

    lcarreras = carreras.objects.filter(estatus=1)

    laspirantes = lcarreras.annotate(
            sol=Coalesce(Count('carrera1__idAspirante', filter=Q(carrera1__idAspirante__idProcesoFicha=11)), Value(0)),
            
    ).values(
        'sol', 'clave'
    )


    # Renderiza la plantilla HTML con los datos
    html = render_to_string('reportes/capacidadAtencion.html', {
        'laspirantes': laspirantes,
        'lcarreras': lcarreras,
        'static_url': settings.STATIC_URL,
        })

    # Crea una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    # Crear un buffer temporal para el PDF
    buffer = BytesIO()

    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(
        src=html,  # el contenido HTML a convertir
        dest=buffer,  # el buffer en memoria
        link_callback=link_callback  # llamada para resolver las rutas de los archivos estáticos
    )

    # Verifica si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)

    # Volver al principio del buffer
    buffer.seek(0)

    # Lee el contenido del buffer y escribe en la respuesta
    response.write(buffer.read())
    buffer.close()

    return response


# Create your views here.
