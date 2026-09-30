from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Doctor, AppointmentSlot, Appointment

# Create your views here.

# Home View
def home(request):
    return render(request, 'clinic/home.html')

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # Validate form
        if form.is_valid():
            # Save user and login
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('patient_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'clinic/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        # Get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'clinic/login.html')

# Logout View
@login_required
def user_logout(request):
    # Logout user
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')

# ---- Admin Views ----
# Admin Dashboard View
@login_required
def admin_dashboard(request):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get all doctors, appointments, and patients
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    patients = request.user.__class__.objects.all()

    # Render admin dashboard with all doctors, appointments, and patients
    return render(request, 'clinic/admin_dashboard.html', {
        'doctors': doctors,
        'appointments': appointments,
        'patients': patients
    })

# Add Doctor View
@login_required
def admin_add_doctor(request):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        speciality = request.POST.get('speciality')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Create new Doctor object
        Doctor.objects.create(
            name=name,
            speciality=speciality,
            email=email,
            phone=phone
        )
        messages.success(request, 'Doctor added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_add_doctor.html')

# Delete Doctor View
@login_required
def admin_delete_doctor(request, doctor_id):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get Doctor object
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Delete Doctor object
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_delete_doctor.html', {'doctor': doctor})

# Edit Doctor View
@login_required
def admin_edit_doctor(request, doctor_id):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get Doctor object
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Edit Doctor object based on form data
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.speciality = request.POST.get('speciality')
        doctor.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.save()
        messages.success(request, 'Doctor updated successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_edit_doctor.html', {'doctor': doctor})

# Add Appointment Slot View
@login_required
def admin_add_slot(request):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Add Appointment Slot based on form data
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
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

# Edit Appointment Slot View
@login_required
def admin_edit_appointment(request, appointment_id):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get Appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Edit Appointment object based on form data
    if request.method == 'POST':
        appointment.status = request.POST.get('status')
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_edit_appointment.html', {'appointment': appointment})

# Cancel Appointment View
@login_required
def admin_cancel_appointment(request, appointment_id):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get Appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Cancel Appointment object based on form data
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('admin_dashboard')

    return render(request, 'clinic/admin_cancel_appointment.html', {'appointment': appointment})

# Manage Users View
@login_required
def admin_manage_users(request):
    # Check if user is a staff member
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('patient_dashboard')

    # Get all users
    users = request.user.__class__.objects.all()
    return render(request, 'clinic/admin_manage_users.html', {'users': users})

# ---- Patient Views ----
# Patient Dashboard View
@login_required
def patient_dashboard(request):
    # Get all scheduled appointments for the patient
    appointments = Appointment.objects.filter(patient=request.user, status='scheduled')
    return render(request, 'clinic/patient_dashboard.html', {'appointments': appointments})

# View Doctors View
@login_required
def view_doctors(request):
    # Get all doctors
    doctors = Doctor.objects.all()
    return render(request, 'clinic/view_doctors.html', {'doctors': doctors})

# View Slots View
@login_required
def view_slots(request, doctor_id):
    # Get Doctor object and time slots
    doctor = get_object_or_404(Doctor, id=doctor_id)
    slots = AppointmentSlot.objects.filter(doctor=doctor, is_available=True)
    return render(request, 'clinic/view_slots.html', {'doctor': doctor, 'slots': slots})

# Book Appointment View
@login_required
def book_appointment(request, slot_id):
    # Get AppointmentSlot object
    slot = get_object_or_404(AppointmentSlot, id=slot_id)

    if request.method == 'POST':
        try:
            # Create new Appointment object
            appointment = Appointment.objects.create(
                patient = request.user,
                slot = slot
            )
            # Save Appointment object
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')
        # Handle validation errors
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'clinic/book_appointment.html', {'slot': slot})

# Edit Appointment View
@login_required
def edit_appointment(request, appointment_id):
    # Get Appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    # Edit Appointment object based on form data
    if request.method == 'POST':
        new_notes = request.POST.get('notes')
        appointment.notes = new_notes
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('patient_dashboard')

    return render(request, 'clinic/edit_appointment.html', {'appointment': appointment})

# Cancel Appointment View
@login_required
def cancel_appointment(request, appointment_id):
    # Get Appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    # Cancel Appointment object based on form data
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('patient_dashboard')

    return render(request, 'clinic/cancel_appointment.html', {'appointment': appointment})


