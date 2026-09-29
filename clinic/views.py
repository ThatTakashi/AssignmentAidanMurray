from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Doctor, AppointmentSlot, Appointment

# Create your views here.
def home(request):
    return render(request, 'clinic/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('patient_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'clinic/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'clinic/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')

# ---- Admin Views ----
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    patients = request.user.__class__.objects.all()

    return render(request, 'clinic/admin_dashboard.html', {
        'doctors': doctors,
        'appointments': appointments,
        'patients': patients
    })

@login_required
def admin_add_doctor(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        speciality = request.POST.get('speciality')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        Doctor.objects.create(
            name=name,
            speciality=speciality,
            email=email,
            phone=phone
        )
        messages.success(request, 'Doctor added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_add_doctor.html')

@login_required
def admin_delete_doctor(request, doctor_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_delete_doctor.html', {'doctor': doctor})

@login_required
def admin_edit_doctor(request, doctor_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.speciality = request.POST.get('speciality')
        doctor.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.save()
        messages.success(request, 'Doctor updated successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_edit_doctor.html', {'doctor': doctor})

@login_required
def admin_add_slot(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        doctor = get_object_or_404(Doctor, id=doctor_id)

        AppointmentSlot.objects.create(
            doctor = doctor,
            date = date,
            start_time = start_time,
            end_time = end_time
        )
        messages.success(request, 'Slot added successfully!')
        return redirect('admin_dashboard')

    doctors = Doctor.objects.all()
    return render(request, 'clinic/admin_add_slot.html', {'doctors': doctors})

@login_required
def admin_edit_appointment(request, appointment_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.status = request.POST.get('status')
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_edit_appointment.html', {'appointment': appointment})

@login_required
def admin_cancel_appointment(request, appointment_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_cancel_appointment.html', {'appointment': appointment})

@login_required
def admin_manage_users(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    users = request.user.__class__.objects.all()
    return render(request, 'clinic/admin_manage_users.html', {'users': users})

