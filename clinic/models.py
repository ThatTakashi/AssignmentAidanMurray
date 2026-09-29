from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Doctor(models.Model):
    # Define doctor attributes
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # String representation of the doctor
    def __str__(self):
        return f"Dr. {self.name} - {self.speciality}"

class AppointmentSlot(models.Model):
    # Define doctor and slot relationships
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    # String representation of the slot
    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time} - {self.end_time}"

class Appointment(models.Model):
    # Create appointment status choices
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
    ]

    # Define patient and slot relationships
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    # Timestamp added automatically when the appointment is created
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    # Validate appointment slot
    def clean(self):
        # If the slot is not available
        if self.slot and not self.slot.is_available:
            raise ValidationError("The selected slot is not available.")

        # If the slot is already booked
        if Appointment.objects.filter(slot=self.slot, status='scheduled').exclude(id=self.id).exists():
            raise ValidationError("The selected slot is already booked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Mark slot as unavailable when appointment slot is already booked
        if self.status == 'scheduled':
            self.slot.is_available = False
            self.slot.save()
        elif self.status == 'cancelled':
            self.slot.is_available = True
            self.slot.save()

    # String representation of the appointment
    def __str__(self):
        return f"{self.patient.username} - {self.slot}"