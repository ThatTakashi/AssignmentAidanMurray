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