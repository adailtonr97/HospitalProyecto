from django.db import models
from django.utils import timezone

class Paciente(models.Model):
        nombre_paciente = models.CharField(max_length=200)
        direccion_paciente = models.CharField(max_length=200)
        telefono_paciente = models.CharField(max_length=200)
        correo_paciente = models.EmailField(max_length=200)
        sintomas_paciente = models.TextField()
        fecha_creacion = models.DateTimeField(
                default=timezone.now)
        fecha_publicacion = models.DateTimeField(
                blank=True, null=True)

        def publish(self):
            self.fecha_publicacion = timezone.now()
            self.save()

        def __str__(self):
            return self.nombre_paciente

class Doctor(models.Model):
        nombre_doctor = models.CharField(max_length=200)
        direccion_doctor = models.CharField(max_length=200)
        telefono_doctor = models.CharField(max_length=200)
        correo_doctor = models.EmailField(max_length=200)
        colegiado_doctor = models.CharField(max_length=200)
        especialidad_doctor = models.CharField(max_length=200)
        fecha_creacion2 = models.DateTimeField(
                default=timezone.now)
        fecha_publicacion2 = models.DateTimeField(
                blank=True, null=True)

        def publish(self):
            self.fecha_publicacion2 = timezone.now()
            self.save()

        def __str__(self):
            return self.nombre_paciente
