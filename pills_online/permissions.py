from rest_framework import permissions


class RegistrationPermission(permissions.BasePermission):
    """
    Permission:
    For registration method for unauth users
    """
    message = 'Access denied'

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'POST':
            return False

        if request.method == 'POST':
            return True

        return False

class GetAuthPermission(permissions.BasePermission):
    """
    Permission:
    For registration method for unauth users
    """
    message = 'Access denied'

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'GET':
            return True

        return False
