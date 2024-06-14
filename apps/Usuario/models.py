from django.db import models

class tiposUsuarios(models.Model):
    idTipoUsuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    estatus = models.IntegerField()

class usuarios(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=20)
    fechaAlta = models.DateTimeField()
    idTipoUsuario = models.ForeignKey('tiposUsuarios', on_delete=models.CASCADE)
