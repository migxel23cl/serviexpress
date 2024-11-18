from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Servicio
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission

def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

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

@user_passes_test(is_in_group('empleado'))
@login_required
def employee_index(request):
    return render(request, "employee_index.html")

@user_passes_test(lambda u: u.is_superuser)
@login_required
def superuser_index(request):
    return render(request, "superuser_index.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def service_view(request):
    if request.method == "POST":
        context = {}
        
        # Service fields
        tipo_servicio = request.POST.get("tipo_servicio")
        modelo_vehiculo = request.POST.get("modelo_vehiculo")
        descripcion_problema = request.POST.get("descripcion_problema")
        patente = request.POST.get("patente")

        # Create service request
        user = request.user

        Servicio.objects.create(
            tipo_servicio=tipo_servicio,
            modelo_vehiculo=modelo_vehiculo,
            descripcion_problema=descripcion_problema,
            patente=patente,
            user=user
        )

        return redirect('service_request')

    return render(request, "service.html")

@login_required
def service_request(request):
    return render(request, "confirmacion_servicio.html")

@login_required
def invoice_request(request):
    return render(request, "invoice.html")

@login_required
def view_request(request):
    user = request.user
    services = Servicio.objects.filter(user=user)
    context = {'services': services}
    
    return render(request, "view_request.html", context)

@login_required
def delete_service(request, id):
    service = get_object_or_404(Servicio, id=id, user=request.user)
    if request.method == "POST":
        service.delete()
        return redirect('view_request')

    return render(request, "delete_service.html", {"service": service})