from django.db import models 
#from Persona.models import personas

# Create your models here.






class procesosFichas(models.Model):
    idProcesoFicha = models.AutoField(primary_key=True)
    fechaInicioFicha = models.DateField()
    fechaFinFicha = models.DateField()
    fechaExani = models.DateField()
    horaExani = models.TimeField()
    PeriodoInicioClases = models.ForeignKey('Alumno.periodo', on_delete=models.CASCADE)
    lugarAplicacion = models.CharField(max_length=50)

class subsistemas(models.Model):
    idSubsistema = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)


class escuelasProcedencia(models.Model):
    idEscuelaProcedencia = models.AutoField(primary_key=True)
    claveEscuela = models.CharField(max_length=30)
    nombreEscuela = models.CharField(max_length=100)
    direccionEscuela = models.CharField(max_length=100)
    telefonoEscuela = models.CharField(max_length=12)
    estatus = models.IntegerField()
    municipioEscuela = models.ForeignKey('Persona.municipios', on_delete=models.CASCADE)
    idSubsistema = models.ForeignKey('subsistemas', on_delete=models.CASCADE)

class aspirantes(models.Model):
    idAspirante = models.AutoField(primary_key=True)
    idPersona = models.ForeignKey('Persona.personas', on_delete=models.CASCADE)
    añoIngresoPrepa = models.CharField(max_length=5)
    añoEgresoPrepa = models.CharField(max_length=5)
    promedioPrepa = models.CharField(max_length=5)
    especialidadPrepa = models.CharField(max_length=30)
    idEscuelaProcedencia = models.ForeignKey('escuelasProcedencia', on_delete=models.CASCADE)
    nombreTutor = models.CharField(max_length=30)
    ape1Tutor = models.CharField(max_length=30)
    ape2Tutor = models.CharField(max_length=30, null=True)
    folioCeneval = models.CharField(max_length=30)
    folioPagoFicha = models.CharField(max_length=30)
    fechaRegistro = models.DateField()
    idProcesoFicha = models.ForeignKey('procesosFichas', on_delete=models.CASCADE)
    idUsuarioRegistra = models.ForeignKey('Usuario.usuarios', on_delete=models.CASCADE)
    nivel = models.IntegerField()
    estatus = models.IntegerField()

class otrosDatos(models.Model):
    idDato = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=20)
    tipo = models.IntegerField()

class detalleOtroDato(models.Model):
    idDetDato = models.AutoField(primary_key=True) 
    idAspirante = models.ForeignKey('aspirantes', on_delete=models.CASCADE)
    idDato = models.ForeignKey('otrosDatos', on_delete=models.CASCADE)



class documentos(models.Model):
    idDocumento = models.AutoField(primary_key=True)
    idAspirante = models.ForeignKey('aspirantes', on_delete=models.CASCADE)
    acta = models.CharField(max_length=20)
    actaF = models.IntegerField(null=True)
    curp = models.CharField(max_length=20)
    curpF = models.IntegerField(null=True)
    foto = models.CharField(max_length=20)
    fotoF = models.IntegerField(null=True)
    certificadoBachillerato = models.CharField(max_length=20, null=True)
    certificadoBachilleratoF = models.IntegerField(null=True)
    constancia = models.CharField(max_length=20, null=True)
    constanciaF = models.IntegerField(null=True)
    analisisSanguineo = models.CharField(max_length=20, null=True)
    analisisSanguineoF = models.IntegerField(null=True)

class documentoCondicionado(models.Model):
    idDocumentoCondicionado = models.AutoField(primary_key=True)
    idDocumento = models.ForeignKey('documentos', on_delete=models.CASCADE)
    fechaEntrega = models.DateField()
    estatus = models.IntegerField()
    

class encuesta(models.Model):
    idEncuesta = models.AutoField(primary_key=True)
    idAspirante = models.ForeignKey('aspirantes', on_delete=models.CASCADE)
    enterarUniversidad = models.IntegerField()
    medioEntregaFicha = models.IntegerField()
    razonInscripcion = models.IntegerField()
    otraUniversidad = models.IntegerField(null=True) 
    idCarrera = models.ForeignKey('Persona.carreras', on_delete=models.CASCADE, related_name='carrera1')
    idCarrera2 = models.ForeignKey('Persona.carreras', on_delete=models.CASCADE, related_name='carrera2')

class universidades(models.Model):
    idUniversidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10, null=True)
    estatus = models.IntegerField()
    nombreRector = models.CharField(max_length=100, null=True)
    municipioUniversidad = models.ForeignKey('Persona.municipios', on_delete=models.CASCADE)







