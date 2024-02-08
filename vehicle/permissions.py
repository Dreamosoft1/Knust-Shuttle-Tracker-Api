from rest_framework import permissions
from .models import Driver  # Import your Driver model

class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user is associated with a Driver model
            try:
                driver = Driver.objects.get(user=request.user)
                return True  # The user is associated with a Driver model
            except Driver.DoesNotExist:
                return False  # The user is not associated with a Driver model
        return False  # User is not authenticated

