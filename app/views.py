from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from .permissions import IsAdminUserOrReadOnly
from .models import *
from .serializers import *
from .paginations import ProductPagination
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend






class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'





class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'





class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAdminUserOrReadOnly,)





class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = (IsAdminUserOrReadOnly,)





class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = (IsAdminUserOrReadOnly,)





class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_class = ProductFilter
    search_fields = ('name', 'description',)





class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)





class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = (IsAdminUserOrReadOnly,)





class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
