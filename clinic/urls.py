from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),

    # Admin Views
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-doctor/', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin/edit-doctor/<int:doctor_id>/', views.admin_edit_doctor, name='admin_edit_doctor'),
    path('admin/delete-doctor/<int:doctor_id>/', views.admin_delete_doctor, name='admin_delete_doctor'),
]