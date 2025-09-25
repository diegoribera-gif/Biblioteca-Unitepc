from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Libro(models.Model):
    titulo = models.CharField(max_length=200, default="Sin título")
    editorial = models.CharField(max_length=200, default="Sin editorial")
    autor = models.CharField(max_length=200, default="Sin autor")
    cantidad = models.PositiveIntegerField(default=1)
    categoria = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.titulo



class Prestamo(models.Model):
    codigo_estudiante = models.CharField(max_length=20, default="0000") 
    nombre_estudiante = models.CharField(max_length=100, default="Desconocido")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} - {self.nombre_estudiante}"


class Devolucion(models.Model):
    codigo_estudiante = models.CharField(max_length=20, default="0000") 
    nombre_estudiante = models.CharField(max_length=100, default="Desconocido")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_devolucion = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=100, default="Bueno")

    def __str__(self):
        return f"{self.libro.titulo} devuelto por {self.nombre_estudiante}"
    
    
class Notificacion(models.Model):
    codigo_estudiante = models.CharField(max_length=20, default="0000")
    nombre_estudiante = models.CharField(max_length=100, default="Desconocido")
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje