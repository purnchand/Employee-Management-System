from datetime import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Employee, Role, Department
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error during registration. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')  # Redirect to home page after login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('index')

# Index View
def index(request):
    return render(request, 'index.html')

# View for listing all employees
@login_required(login_url='login')
def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'all_emp.html', context)

# View for adding a new employee
@login_required(login_url='login')
def add_emp(request):
    if request.method == 'POST':
        try:
            # Gather POST data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = float(request.POST['salary'])
            bonus = float(request.POST['bonus'])
            phone = int(request.POST['phone'])
            location = request.POST['location']
            hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d').date()

            # Handle Role
            new_role_name = request.POST.get('new_role', '').strip()
            role = None
            if new_role_name:
                role, _ = Role.objects.get_or_create(role=new_role_name)
            else:
                role_id = request.POST.get('role')
                if role_id:
                    role = get_object_or_404(Role, id=role_id)

            # Handle Department
            new_dept_name = request.POST.get('new_dept', '').strip()
            department = None
            if new_dept_name:
                department, _ = Department.objects.get_or_create(dept_no=new_dept_name)
            else:
                dept_id = request.POST.get('dept_no')
                if dept_id:
                    department = get_object_or_404(Department, id=dept_id)

            # Ensure atomic save
            with transaction.atomic():
                new_emp = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    salary=salary,
                    bonus=bonus,
                    phone=phone,
                    role=role,
                    dept_no=department,
                    location=location,
                    hire_date=hire_date
                )
                new_emp.save()

            messages.success(request, "Employee added successfully!")
            return redirect('all_emp')

        except KeyError as e:
            messages.error(request, f"Missing data: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    elif request.method == 'GET':
        roles = Role.objects.all()
        departments = Department.objects.all()
        return render(request, 'add_emp.html', {'roles': roles, 'departments': departments})

    return HttpResponse('An unexpected error occurred.')

# View for removing an employee
@login_required(login_url='login')
def remove_emp(request, emp_id=0):
    if emp_id > 0:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            messages.success(request, f"Employee removed successfully!")
            return redirect('all_emp')
        except Employee.DoesNotExist:
            messages.error(request, f"Employee does not exist.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        emps = Employee.objects.all()
        context = {'emps': emps}
        return render(request, 'remove_emp.html', context)

# View for filtering employees
@login_required(login_url='login')
def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        role = request.POST.get('role', '').strip()
        location = request.POST.get('location', '').strip()

        # Start with all employees
        emps = Employee.objects.all()

        # Apply filters if values are provided
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if role:
            emps = emps.filter(role__role__icontains=role)
        if location:
            emps = emps.filter(location__icontains=location)

        context = {'emps': emps}
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')

    return HttpResponse('An unexpected error occurred.')
