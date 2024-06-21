from django.urls import path
from . import views
#from Aspirante.views import *
app_name = 'Reportes'


urlpatterns = [
    path('registrarAspirante/reporte/<int:idAspirante>/', views.reporte_pdf, name='reporte'), #Ruta para el reporte de pre-registro de aspirantes TSU
    path('reporteDatosAspirantes/<int:idPeriodo>/<int:filtro>/', views.reporteDatosAspirantes, name='reporteDatosAspirantes'), #Ruta para el reporte de los datos del aspirante
    path('actualizaAspirante/reporte/<int:idAspirante>/', views.reporteAspirante, name='reinscripcionAspirante'),
    path('capacidadAtencion/reporte/<int:idAspirante>/', views.reporteCapacidadAtencion, name='reporteCapacidadAtencion')

]