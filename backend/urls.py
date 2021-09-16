from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/', include('app.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/auth/', include('user.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
