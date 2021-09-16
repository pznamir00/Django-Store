from rest_framework.permissions import IsAdminUser, SAFE_METHODS



class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return True if request.method in SAFE_METHODS else super(IsAdminUserOrReadOnly, self).has_permission(request, view)
