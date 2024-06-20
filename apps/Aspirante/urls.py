from django.urls import path
from . import views
#from Aspirante.views import *
app_name = 'Aspirante'

urlpatterns = [
    #Rutas para pais, estado, municipio y colonia
    path('get_paises/', views.get_paises, name='get_paises'),
    path('get_estados2/', views.get_estados2, name='get_estados2'),
    path('get_estados/<int:idPais>/', views.get_estados, name='get_estados'),
    path('get_municipios/<int:idEstado>/', views.get_municipios, name='get_municipios'),
    path('get_colonias/<int:idMunicipio>/', views.get_colonias, name='get_colonias'),
    path('get_escuelas/<int:idMunicipio>/', views.get_escuelas, name='get_escuelas'),
    path('get_uni/', views.get_uni, name='get_uni'),
    path('get_escuelaid/<int:idEscuelaProcedencia>/', views.get_escuelaid, name='get_escuelaid'),
    path('get_subsistemas/', views.obtener_subsistemas, name='get_subsistemas'),
    path('get_curp/', views.get_curp, name='get_curp'),

    path('carrera/', views.Carreras),
    path('tablaCarreras/', views.tablaCarreras),
    path('registrarCarrera/', views.registrarCarrera),
    path('editarCarrera/<int:idCarrera>/', views.editar_carrera),
    path('subsistema/', views.subsistema),
    path('tablaSubsistemas/', views.tablaSubsistemas),
    path('registrarSubsistema/', views.registrarSusbsistema),
    path('editarSubsistema/<int:idSubsistema>/', views.editar_subsistema),
    path('escuela/', views.escuela),
    path('tablaEscuelas/', views.tablaEscuelas),
    path('registrarEscuela/', views.registrarEscuela),
    path('editarEscuela/<int:idEscuelaProcedencia>/', views.editar_escuela),
    path('universidad/', views.Universidadades),
    path('tablaUniversidades/', views.tablaUniversidades),
    path('registrarUniversidad/', views.registrarUniversidad),
    path('editarUniversidad/<int:idUniversidad>/', views.editar_universidad),
    path('fichas/', views.fichas),
    path('registrarFicha/', views.registrarFicha),
    path('tablaFichas/', views.tablaFichas),
    path('editarFicha/<int:idProcesoFicha>/', views.editar_ficha),
    path('registrarAspirante/', views.guardaAsp),
    path('menuAspirantes/', views.menuAspirantes),
    path('datosPersonalizados/', views.datosPersonalizados),
    
    path('tablaEdadNuevoIngreso/', views.tablaEdadNuevoIngreso),
    
    #Ruta para generar reporte de pre-registro
    path('reportePreR/', views.reportePreR),

    #Rutas para dar de alta aspirantes
    path('aspirantes/', views.buscarAspirate),
    path('get_aspirante/', views.get_aspirante, name='get_aspirante'),
    path('editaAspirante/<int:id>/', views.editarAspirante, name='editaAspirante'),
    path('actualizaAspirante/', views.actualizarAspirante, name='actualizaAspirante'),
    path('tablaAspirantes/', views.mostrarAspirantes, name='tablaAspirantes'),    

    #Rutas para la tabla de datos aspirantes
    path('datosAspirantes/', views.datosAspirantes),
    path('datosAspirantesFiltro/', views.datosAspirantesFiltro, name='datosAspirantesFiltro'),

    #Rutas para la tabla de aspirantes registrados con % de avance por carrera
    path('aspirantesRegistrados/', views.aspirantesRegistrados),
    path('aspirantesRegistradosFiltro/', views.aspirantesRegistradosFiltro, name='aspirantesRegistradosFiltro'),

    #Rutas para la tabla de aspirantes por especialidad y director
    path('aspirantesEspecialidad/', views.aspirantesEspecialidad),
    path('aspirantesEspecialidadFiltro/', views.aspirantesEspecialidadFiltro, name='aspirantesEspecialidadFiltro'),

     path('aspirantesInscritos/', views.aspirantesInscritos),
     path('editarAspiranteAceptado/<int:id>/', views.editarAspiranteAcp, name='editarAspiranteAceptado'),
    #Rutapath('probando/', views.verReporteAsp, name="probarReporte"),
    
    #path('descargareportePreR/', views.generarReportePreR),
    #path('estados/', get_estados2, name='get_estados2'),
    #path('estados/<int:idPais>/', get_estados, name='get_estados'),
    #path('municipios/<int:idEstado>/', get_municipios, name='get_municipios'),
    #path('colonias/<int:idMunicipio>/', get_colonias, name='get_colonias'),
     
    
] 