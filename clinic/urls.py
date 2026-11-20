# URL routes for the REST API (replaces the old server-rendered pages).
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

# Router auto-generates CRUD endpoints for each viewset
router = DefaultRouter()
router.register(r'doctors', api_views.DoctorViewSet, basename='doctor')
router.register(r'slots', api_views.AppointmentSlotViewSet, basename='slot')
router.register(r'appointments', api_views.AppointmentViewSet, basename='appointment')

urlpatterns = [
    # JWT login (returns access + refresh tokens) and token refresh
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Custom auth endpoints
    path('api/register/', api_views.register, name='register'),
    path('api/health/', api_views.health, name='health'),
    path('api/me/', api_views.me, name='me'),
    # Viewset endpoints: /api/doctors/, /api/slots/, /api/appointments/
    path('api/', include(router.urls)),
]