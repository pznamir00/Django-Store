from django.urls import path, include
from .router import router
from app.views import ProductAPIView, ProductDetailAPIView, UserDetailAPIView, CartAPIView

urlpatterns = [
    path('api/auth/', include('rest_auth.urls')),
    path('api/user/', UserDetailAPIView.as_view()),
    path('api/cart/', CartAPIView.as_view()),
    path('api/products/', ProductAPIView.as_view()),
    path('api/products/<slug:slug>/', ProductDetailAPIView.as_view()),
    path('api/', include(router.urls)),
]
