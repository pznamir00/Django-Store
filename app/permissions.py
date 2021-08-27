from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return True if request.method in SAFE_METHODS else super(IsAdminUserOrReadOnly, self).has_permission(request, view)


class NoUpdateAndDestroyOnlyForAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'PATCH':
            return False
        if request.method == 'DELETE':
            return self.request.is_superuser
        return True

    def has_obj_permission(self, request, view, obj):
        return self.request.is_superuser or obj.user == self.request.user
