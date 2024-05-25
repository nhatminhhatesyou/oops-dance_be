from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return IsAuthenticated().has_permission(request, view)