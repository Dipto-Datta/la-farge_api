from rest_framework.permissions import BasePermission

from rest_framework.permissions import IsAuthenticated
class default_user(BasePermission):

    permission_classes = [IsAuthenticated]
    def has_permission(self, request, view):
        print(request.user)
        if request.user.groups.filter(name='default'):# and request.method in YOUR_ALLOWED_METHODS:
            
            return True
        return False

class admin_user(BasePermission):

    permission_classes = [IsAuthenticated]
    def has_permission(self, request, view):
        print(request.user)
        if request.user.groups.filter(name='admin'): # and request.method in YOUR_ALLOWED_METHODS:
           return True
        return False


class default_permission(BasePermission):

    permission_classes = [IsAuthenticated]
    def has_permission(self, request, view):
        print(request.user)
        if request.user.groups.filter(name='admin'): # and request.method in YOUR_ALLOWED_METHODS:
           return True
        return False
