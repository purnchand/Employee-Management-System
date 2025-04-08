from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Q
from .models import Employee
from django.shortcuts import get_object_or_404

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Error during registration!')
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
            return redirect('index')  
        else:
            messages.error(request, 'Invalid credentials!')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('index')

# Index View
def index(request):
    return render(request, 'index.html')

# View for listing all employees
@login_required(login_url='login')
def all_emp(request):
    emps = Employee.objects.all()
    return render(request, 'all_emp.html', {'emps': emps})

# View for adding a new employee
@login_required(login_url='login')
def add_emp(request):
    if request.method == 'POST':
        try:
            full_name = request.POST['full_name']
            salary = float(request.POST['salary'])
            email = request.POST['email']
            phone = int(request.POST['phone'])
            location = request.POST['location']
            resume = request.FILES.get('resume')
            job_role = request.POST.get('job_role', '').strip()

            with transaction.atomic():
                new_emp = Employee(
                    full_name=full_name,
                    salary=salary,
                    email=email,
                    phone=phone,
                    job_role=job_role,
                    location=location,
                    resume=resume
                )
                new_emp.save()

            return redirect('all_emp')

        except IntegrityError as e:
            if 'email' in str(e).lower():
                messages.error(request, "This Email Id already exists.")
            elif 'phone' in str(e).lower():
                messages.error(request, "This Phone Number already exists.")
            else:
                messages.error(request, "Duplicate entry detected.")
        except KeyError as e:
            messages.error(request, f"Found missing data: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, 'add_emp.html')

# View for removing an employee
@login_required(login_url='login')
def remove_emp(request, emp_id=0):
    if emp_id > 0:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
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
        keyword = request.POST.get('keyword', '').strip().lower()
        emps = Employee.objects.all()
        if keyword:
            if keyword in ['yes', 'ye', 'y', 'es']:
                emps = emps.filter(~Q(resume='') & ~Q(resume=None))
            elif keyword in ['no']:
                emps = emps.filter(Q(resume='') | Q(resume=None))
            else:
                emps = emps.filter(
                    Q(full_name__icontains=keyword) |
                    Q(job_role__icontains=keyword) |
                    Q(location__icontains=keyword) |
                    Q(phone__icontains=keyword) |
                    Q(salary__icontains=keyword) |
                    Q(email__icontains=keyword)
                )

        context = {'emps': emps}
        return render(request, 'all_emp.html', context)

    return render(request, 'filter_emp.html')

# View for editing employees
@login_required(login_url='login')
def edit_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        try:
            emp.full_name = request.POST['full_name']
            emp.salary = float(request.POST['salary'])
            emp.email = request.POST['email']
            emp.phone = int(request.POST['phone'])
            emp.location = request.POST['location']
            emp.job_role = request.POST.get('job_role', '').strip()
            if request.FILES.get('resume'):
                emp.resume = request.FILES['resume']

            with transaction.atomic():
                emp.save()
            return redirect('all_emp')

        except Exception as e:
            messages.error(request, f"Update failed: {str(e)}")

    return render(request, 'add_emp.html', {'emp': emp})



