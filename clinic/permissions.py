# Custom DRF permission classes for patient vs administrator access.
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Only staff users (administrators) may access this endpoint."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_staff)
