from django.urls import path, include, re_path
from django.contrib import admin
from .router import router
from django.conf.urls import url
from app.views import ProductAPIView, ProductDetailAPIView, UserDetailAPIView, CartAPIView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/auth/user/', UserDetailAPIView.as_view()),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/password/', include('django.contrib.auth.urls')), #here you should define your own frontend url and get this fields from email
    path('api/cart/', CartAPIView.as_view()),
    path('api/products/', ProductAPIView.as_view()),
    path('api/products/<slug:slug>/', ProductDetailAPIView.as_view()),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
