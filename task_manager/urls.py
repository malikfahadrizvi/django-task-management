"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import (
    UserViewSet, TaskViewSet, ProjectViewSet, register_user, home, task_list, register_page, 
    login_view, admin_dashboard, user_dashboard
)
from django.contrib.auth import views as auth_views

# ✅ API Router for REST API
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    # ✅ Home & Authentication Routes
    path('', home, name='home'),
    path('register/', register_page, name='register_page'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # ✅ Role-Based Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),

    # ✅ Task Management Pages
    path('tasks/', task_list, name='task_list'),

    # ✅ API Endpoints
    path('api/', include(router.urls)),  
    path('api/register/', register_user, name='register_user'),
]