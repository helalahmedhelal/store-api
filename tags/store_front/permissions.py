from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow anonymous users to perform GET requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow administrators to perform POST requests
        return bool(request.user and request.user.is_staff)