from django.db import models

# Create your models here.
class puestosEmpleado(models.Model):
    idPuestoEmpleado = models.AutoField(primary_key=True)
    nombrePuesto = models.CharField(max_length=50)

class areasEmpleados(models.Model):
    idArea = models.AutoField(primary_key=True)
    nombreArea = models.CharField(max_length=50)

class titulosAcademicos(models.Model):
    idTitulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    abreviatura = models.CharField(max_length=10)  
    
class empleados(models.Model):
    idEmpleado = models.AutoField(primary_key=True)    
    idPersona = models.ForeignKey('Persona.personas', on_delete=models.CASCADE)
    numeroEmpleado = models.CharField(max_length=15) 
    fechaAlta = models.DateField()
    idTitulo = models.ForeignKey('titulosAcademicos', on_delete=models.CASCADE)
    rfc = models.CharField(max_length=15) 
    idPuestoEmpleado = models.ForeignKey('puestosEmpleado', on_delete=models.CASCADE)
    estatus =models.IntegerField()
    idArea = models.ForeignKey('areasEmpleados', on_delete=models.CASCADE)
"""
class maestros(models.Model):
    idMaestro = models.AutoField(primary_key=True)    
    idPersona = models.ForeignKey('Persona.personas', on_delete=models.CASCADE)
    numeroEmpleado = models.CharField(max_length=15) 
    fechaAlta = models.DateField()
    idTitulo = models.ForeignKey('titulosAcademicos', on_delete=models.CASCADE)
    rfc = models.CharField(max_length=15) 
    idPuestoEmpleado = models.ForeignKey('puestosEmpleado', on_delete=models.CASCADE)
    estatus =models.IntegerField()
    idArea = models.ForeignKey('areasEmpleados', on_delete=models.CASCADE)"""

class documentosEmpleado(models.Model):
    idDocEmpleado = models.AutoField(primary_key=True) 
    idEmpleado = models.ForeignKey('empleados', on_delete=models.CASCADE)
    acta = models.CharField(max_length=20, null=True)
    domicilio = models.CharField(max_length=20, null=True)
    curp = models.CharField(max_length=20, null=True)
    credencial = models.CharField(max_length=20, null=True)
    cartilla = models.CharField(max_length=20, null=True)
    licencia = models.CharField(max_length=20, null=True)
    aPenales = models.CharField(max_length=20, null=True)
    aDisciplinarios = models.CharField(max_length=20, null=True)
    recomentacion1 = models.CharField(max_length=20, null=True)
    recomentacion2 = models.CharField(max_length=20, null=True)