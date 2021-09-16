from rest_framework import permissions

#denied for put and patch and delete only for admin
class NoUpdateAndDestroyOnlyForAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return self.request.is_superuser if request.method == 'DELETE' else True