from django.urls import path
from . import views  # Importa las vistas de la app

urlpatterns = [
    path('register/',views.register, name="register"),
]
