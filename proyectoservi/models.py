from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Perfil del usuario {}'.format(self.user.username)

class ServiceRequest(models.Model):
    tipo_servicio = models.CharField(max_length=100)
    modelo_vehiculo = models.CharField(max_length=100)
    descripcion_problema = models.TextField()
    patente = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Solicitud de Servicio {self.tipo_servicio} para {self.modelo_vehiculo}'