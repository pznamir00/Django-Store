from rest_framework import routers
from app import views


router = routers.SimpleRouter()
router.register('categories', views.CategoryViewSet)
router.register('subcategories', views.SubCategoryViewSet)
router.register('brands', views.BrandViewSet)
router.register('colors', views.ColorViewSet)
router.register('sizes', views.SizeViewSet)
router.register('payment-methods', views.PaymentMethodViewSet)
router.register('shippin-gmethods', views.ShippingMethodViewSet)
router.register('orders', views.OrderViewSet, basename='orders')