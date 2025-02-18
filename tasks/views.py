from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django import forms
from .models import Task, Project, User
from .serializers import UserSerializer, TaskSerializer, ProjectSerializer
from .forms import CustomUserCreationForm  # Import from forms.py
from django.views.decorators.csrf import csrf_exempt

# 📌 Home Page (TMS Dashboard)
def home(request):
    return render(request, 'tasks/home.html')

# 📌 Task List Page (HTML)
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# 📌 User Registration with Role-Based Redirection
def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = form.cleaned_data['role']  # Save role from form
                
                # Set admin privileges based on role
                if user.role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                
                user.save()
                login(request, user)
                messages.success(request, f"Welcome, {user.username}! Registration successful.")
                
                return redirect('admin_dashboard' if user.is_staff else 'user_dashboard')

            except IntegrityError:
                messages.error(request, "This username or email is already taken.")
        else:
            messages.error(request, "Sign up failed. Please check your details.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})

# 📌 Login Page with Role-Based Redirection
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('admin_dashboard' if user.is_staff else 'user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "tasks/login.html")

# 📌 Admin Dashboard (For Admins Only)
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    users = User.objects.all()
    tasks = Task.objects.all()
    projects = Project.objects.all()
    return render(request, 'tasks/admin_dashboard.html', {
        'users': users,
        'tasks': tasks,
        'projects': projects
    })

# 📌 User Dashboard (For Standard Users)
@login_required
def user_dashboard(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/user_dashboard.html', {'tasks': user_tasks})

# 📌 API Views
@csrf_exempt
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = form.cleaned_data['role']
                
                if user.role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                
                user.save()
                return Response({
                    "message": f"User {user.username} created successfully.",
                    "role": user.role
                }, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response({"error": "Username/email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 DRF Viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer