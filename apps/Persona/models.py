from django.db import models 
#from Usuario.models import usuarios

class carreras(models.Model):
    idCarrera = models.AutoField(primary_key=True)
    nombreCarrera = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10)
    estatus = models.IntegerField()
    nivel = models.IntegerField()
    area = models.CharField(max_length=10)
    clave = models.CharField(max_length=10)
    modalidad = models.IntegerField()
    idEmpleado = models.ForeignKey('Empleado.empleados', on_delete=models.CASCADE)



class capacidadAtencion(models.Model):
    idCapacidad = models.AutoField(primary_key=True)
    idCarrera = models.ForeignKey('carreras', on_delete=models.CASCADE)
    capacidadAtencion = models.IntegerField()
    proyeccionFichas = models.IntegerField()
    grupos = models.IntegerField()
    ciclo = models.CharField(max_length=9)

# Create your models here.
class paises(models.Model):
    idPais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

class estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombreEstado = models.CharField(max_length=20)
    idPais = models.ForeignKey('paises', on_delete=models.CASCADE)

class municipios(models.Model):
    idMunicipio = models.AutoField(primary_key=True)
    nombreMunicipio = models.CharField(max_length=20)
    idEstado = models.ForeignKey('estados', on_delete=models.CASCADE)

class colonias(models.Model):
    idColonia = models.AutoField(primary_key=True)
    nombreColonia= models.CharField(max_length=20)
    idMunicipio = models.ForeignKey('municipios', on_delete=models.CASCADE)
    cp = models.CharField(max_length=5)


class personas(models.Model):
    idPersona = models.AutoField(primary_key=True)
    curp = models.CharField(max_length=18)
    nombre = models.CharField(max_length=40)
    ape1 = models.CharField(max_length=30)
    ape2 = models.CharField(max_length=30, null=True)
    calle = models.CharField(max_length=30)
    numero = models.CharField(max_length=5)
    zona = models.IntegerField()
    cp = models.CharField(max_length=5)
    idColonia = models.ForeignKey('colonias', on_delete=models.CASCADE)
    idMunicipioNacimiento = models.ForeignKey('municipios', on_delete=models.CASCADE)
    nacionalidad = models.IntegerField()
    sexo = models.IntegerField()
    estatus = models.IntegerField()
    telCasa = models.CharField(max_length=10, null=True)
    telCelular = models.CharField(max_length=10, null=True)
    estadoCivil = models.IntegerField()
    hijos = models.IntegerField()
    correo = models.CharField(max_length=80)
    idUsuario = models.ForeignKey('Usuario.usuarios', on_delete=models.CASCADE)
   

class datosMedicos(models.Model):
    idDatosMedicos = models.AutoField(primary_key=True)
    idPersona = models.ForeignKey('personas', on_delete=models.CASCADE)
    peso = models.FloatField()
    estatura = models.IntegerField()
    famDiabeticos = models.IntegerField(null=True)
    famHipertensos = models.IntegerField(null=True)
    famCardiacos = models.IntegerField(null=True)
    tipoSangre = models.IntegerField()