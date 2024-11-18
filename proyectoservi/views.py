from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, ServiceRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission

def create_employee_role():
    group, created = Group.objects.get_or_create(name='empleado')
    if created:
        permissions = Permission.objects.all()
        group.permissions.set(permissions)
        print('Employee role created successfully')
    else:
        print('Employee role already exists')
create_employee_role()

def register_page(request):
    if request.method == "POST":
        # User fields
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        try:
            # Create user
            user = User.objects.create_user(username=username, password=password)

            # Create profile
            Profile.objects.create(user=user, phone=phone, address=address)

            # Redirect to login page
            return redirect("login")
        except Exception as e:
            return render(request, "register.html", {"error": str(e)})

    return render(request, "register.html")

def login_page(request):
    if request.method == "POST":
        # User fields
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            # Login
            login(request, user)

            # Debugging: Print user groups
            print(f"User groups: {user.groups.all()}")

            # Redirect based on user type
            if user.is_superuser:
                return redirect("superuser_index")
            elif user.groups.filter(name='empleado').exists():
                print("User is an employee")
                return redirect("employee_index")
            else:
                print("User is not an employee")
                return redirect("user_index")
        else:
            # Show error message
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

@login_required
def user_index(request):
    return render(request, "user_index.html")

@login_required
def employee_index(request):
    return render(request, "employee_index.html")

@login_required
def superuser_index(request):
    return render(request, "superuser_index.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def service_view(request):
    if request.method == "POST":
        # Service fields
        tipo_servicio = request.POST.get("tipo_servicio")
        modelo_vehiculo = request.POST.get("modelo_vehiculo")
        descripcion_problema = request.POST.get("descripcion_problema")
        patente = request.POST.get("patente")

        # Create service request
        user = request.user
        ServiceRequest.objects.create(
            tipo_servicio=tipo_servicio,
            modelo_vehiculo=modelo_vehiculo,
            descripcion_problema=descripcion_problema,
            patente=patente,
            user=user
        )

        return render(request, "confirmacion_servicio.html")

    return render(request, "service.html")

@login_required
def service_request(request):
    return render(request, "confirmacion_servicio.html")