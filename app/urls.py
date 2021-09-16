from rest_framework import routers
from . import views
from django.urls import include, path


router = routers.SimpleRouter()
router.register('categories', views.CategoryViewSet)
router.register('subcategories', views.SubCategoryViewSet)
router.register('brands', views.BrandViewSet)
router.register('colors', views.ColorViewSet)
router.register('sizes', views.SizeViewSet)
router.register('payment-methods', views.PaymentMethodViewSet)
router.register('shipping-methods', views.ShippingMethodViewSet)

urlpatterns = [
    path('products/', views.ProductAPIView.as_view()),
    path('products/<slug:slug>/', views.ProductDetailAPIView.as_view()),
    path('', include(router.urls))
]