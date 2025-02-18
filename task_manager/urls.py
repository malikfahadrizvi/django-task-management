from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import (
    UserViewSet, TaskViewSet, ProjectViewSet,
    register_user, home, task_list, register_page,
    login_view, admin_dashboard, user_dashboard
)
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    # 🏠 Core Pages
    path('', home, name='home'),
    path('tasks/', task_list, name='task_list'),
    # 🔐 Authentication
    path('register/', register_page, name='register_page'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # 👩💻 Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    
    # 📡 API Endpoints
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register_user'),
]