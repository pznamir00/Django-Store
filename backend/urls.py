from django.urls import path, include
from django.contrib import admin
from .router import router
from app.views import ProductAPIView, ProductDetailAPIView, UserDetailAPIView, CartAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/auth/', include('rest_auth.urls')),
    path('api/user/', UserDetailAPIView.as_view()),
    path('api/cart/', CartAPIView.as_view()),
    path('api/products/', ProductAPIView.as_view()),
    path('api/products/<slug:slug>/', ProductDetailAPIView.as_view()),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
