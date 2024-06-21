from django.db import models

# Create your models here.
class periodo(models.Model):
    idPeriodo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    activo = models.IntegerField(null=True, blank=True)
    genTSU =models.IntegerField()
    genING =models.IntegerField()


class grupos(models.Model):
    idGrupo = models.AutoField(primary_key=True)
    grado = models.SmallIntegerField()
    grupo = models.CharField(max_length=1)
    turno = models.SmallIntegerField()
    idMaestro = models.ForeignKey('Empleado.empleados', on_delete=models.CASCADE)
    idCarrera = models.ForeignKey('Persona.carreras', on_delete=models.CASCADE)
    idPeriodo = models.ForeignKey('periodo', on_delete=models.CASCADE)

class estatusAlumnos(models.Model):
    idEstatusAlumno = models.AutoField(primary_key=True)
    nombreEstatus = models.CharField(max_length=50)

class alumnos(models.Model):
    idGrupo = models.AutoField(primary_key=True)
    idPersona=models.ForeignKey('Persona.personas', on_delete=models.CASCADE)
    matricula = models.CharField(max_length=10)
    nivel = models.SmallIntegerField() 
    idEstatusAlumno = models.ForeignKey('estatusAlumnos', on_delete=models.CASCADE)
    fechaAlta = models.DateField()
    idGrupo = models.ForeignKey('grupos', on_delete=models.CASCADE)
    periodoInicio=models.ForeignKey('periodo', on_delete=models.CASCADE)
    idUsuarioInscribe = models.ForeignKey('Usuario.usuarios', on_delete=models.CASCADE)

    