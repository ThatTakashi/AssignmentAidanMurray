from django.urls import path
from . import views

urlpatterns = [
    # --- Home ---
    path('', views.home, name='home'),

    # --- Authentication ---
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # --- Admin Views ---
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-slot/', views.admin_add_slot, name='admin_add_slot'),
    path('admin/edit-appointment/<int:appointment_id>/', views.admin_edit_appointment, name='admin_edit_appointment'),
    path('admin/cancel-appointment/<int:appointment_id>/', views.admin_cancel_appointment, name='admin_cancel_appointment'),
    path('admin/manage-users/', views.admin_manage_users, name='admin_manage_users'),
    # Admin Doctor Views
    path('admin/add-doctor/', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin/edit-doctor/<int:doctor_id>/', views.admin_edit_doctor, name='admin_edit_doctor'),
    path('admin/delete-doctor/<int:doctor_id>/', views.admin_delete_doctor, name='admin_delete_doctor'),

    # --- Patient Views ---
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/doctors/', views.view_doctors, name='view_doctors'),
]