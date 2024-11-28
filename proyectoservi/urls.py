from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('user/', views.user_index, name="user_index"),
    path('employee/', views.employee_index, name="employee_index"),
    path('employee/all_service/', views.view_all_services, name="all_employee_service"),
    path('employee/all_service/complete/<int:id>/', views.complete_service, name="complete_service"),
    path('employee/all_service/delete/<int:id>/', views.employee_delete_service, name="delete"),
    path('employee/reports/', views.generar_reporte, name="generar_reporte"),
    path('superuser/', views.superuser_index, name="superuser_index"),
    path('superuser/completed_services/', views.completed_services, name="completed_services"),
    path('logout/', views.logout_view, name="logout"),
    path('user/service/', views.service_view, name="service_view"),
    path('productos/', views.vista_productos, name='vista_productos'),
    path('user/service/request/', views.service_request, name="service_request"),
    path('user/service/request/invoice/', views.invoice_request, name="invoice_request"),
    path('user/service/request/view/', views.view_request, name="view_request"),
    path('user/service/request/view/delete/<int:id>/', views.delete_service, name="delete_service"),

]
