# myapp/urls.py
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('all_emp/', views.all_emp, name='all_emp'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('remove_emp/', views.remove_emp, name='remove_emp'),
    path('remove_emp/<int:emp_id>/', views.remove_emp, name='remove_emp'),
    path('filter_emp/', views.filter_emp, name='filter_emp'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]