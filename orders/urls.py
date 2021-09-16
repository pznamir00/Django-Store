from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('orders', views.OrderViewSet)
router.register('cart', views.CartView)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<str:number>/add-product/', views.CartView.as_view({ 'post': 'add_product' })),
    path('cart/<str:number>/remove-product/', views.CartView.as_view({ 'delete': 'remove_product' }))
]