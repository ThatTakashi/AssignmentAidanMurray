# REST API views built with Django REST Framework viewsets
# These replace the old server-rendered Django views/pages
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Doctor, AppointmentSlot, Appointment
from .serializers import (DoctorSerializer, AppointmentSlotSerializer,
                          AppointmentSerializer, RegisterSerializer,
                          UserSerializer)
from .permissions import IsAdminUser


# ---- Auth endpoints ----

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Create a new patient account."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Registration successful.'},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Public health check used by Render's healthCheckPath."""
    return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Return the currently logged-in user's info."""
    return Response(UserSerializer(request.user).data)


# ---- Doctor endpoints ----

class DoctorViewSet(viewsets.ModelViewSet):
    """CRUD for doctors. Anyone logged in can list; only admins can modify."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        # Safe methods (GET) need only login; writes need admin
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


# ---- Appointment slot endpoints ----

class AppointmentSlotViewSet(viewsets.ModelViewSet):
    """CRUD for appointment slots. Patients can view; admins manage."""
    queryset = AppointmentSlot.objects.select_related('doctor').all()
    serializer_class = AppointmentSlotSerializer
    # Allow filtering by ?doctor=<id> and ?is_available=true
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['doctor__name', 'doctor__speciality']
    ordering_fields = ['date', 'start_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Optional query params: ?doctor=1&is_available=true
        doctor_id = self.request.query_params.get('doctor')
        is_available = self.request.query_params.get('is_available')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


# ---- Appointment endpoints ----

class AppointmentViewSet(viewsets.ModelViewSet):
    """Appointments: patients see/book/cancel their own; admins see all."""
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        # Admins see every appointment; patients only their own
        if self.request.user.is_staff:
            return Appointment.objects.select_related(
                'patient', 'slot__doctor').all()
        return Appointment.objects.filter(
            patient=self.request.user).select_related('patient', 'slot__doctor')

    def perform_create(self, serializer):
        # The logged-in user is always the patient
        serializer.save(patient=self.request.user)

    def get_permissions(self):
        # Patients may create/update/cancel their own appointments,
        # but only admins may delete appointments outright.
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        # Patients may only edit notes/status on their own appointments
        appointment = self.get_object()
        if not self.request.user.is_staff and appointment.patient != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only modify your own appointments.")
        serializer.save()
