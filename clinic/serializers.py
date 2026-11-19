# Serializers convert Django models to/from JSON for the REST API.
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, AppointmentSlot, Appointment


# ---- User serializers ----

class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer used to show user info (e.g. /api/me/)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Handles patient registration. Password is write-only."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # create_user() hashes the password automatically
        return User.objects.create_user(**validated_data)


# ---- Clinic serializers ----

class DoctorSerializer(serializers.ModelSerializer):
    """Full read/write serializer for doctors."""
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'speciality', 'email', 'phone']


class AppointmentSlotSerializer(serializers.ModelSerializer):
    """Slot serializer. Includes the doctor's name for display."""
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time',
                  'end_time', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment serializer with nested display info."""
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    doctor_name = serializers.CharField(source='slot.doctor.name', read_only=True)
    slot_date = serializers.DateField(source='slot.date', read_only=True)
    slot_start = serializers.TimeField(source='slot.start_time', read_only=True)
    slot_end = serializers.TimeField(source='slot.end_time', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_username', 'slot', 'doctor_name',
                  'slot_date', 'slot_start', 'slot_end', 'status', 'notes',
                  'created_at']
        read_only_fields = ['patient', 'created_at']

    def validate(self, data):
        """Prevent booking a slot that is already taken."""
        slot = data.get('slot')
        if slot and Appointment.objects.filter(
            slot=slot, status='scheduled'
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("The selected slot is already booked.")
        return data
