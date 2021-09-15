from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS



class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return True if request.method in SAFE_METHODS else super(IsAdminUserOrReadOnly, self).has_permission(request, view)


#denied for put and patch and delete only for admin
class NoUpdateAndDestroyOnlyForAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return self.request.is_superuser if request.method == 'DELETE' else True
