from rest_framework import viewsets, generics, mixins
from rest_framework.filters import SearchFilter
from .permissions import IsAdminUserOrReadOnly, NoUpdateAndDestroyOnlyForAdmin
from .models import *
from .serializers import *
from .paginations import ProductPagination
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response





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





class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user





class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=200)
        return Response(serializer.errors, status=400)





class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (NoUpdateAndDestroyOnlyForAdmin,)

    def get_queryset(self):
        queryset = Order.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset
            return queryset.filter(user=self.request.user)
        return []

    def perform_create(self, serializer):
        cart_data = serializer.validated_data.pop('cart')
        total = 0.00
        order = serializer.save(user=self.request.user, total=total)
        for sample in cart_data['products']:
            quantity = sample['quantity']
            size_product_relation = SizeProductRelation.objects.get(pk=sample['product_size_relation'])
            size_product_relation.quantity -= quantity
            size_product_relation.save()
            total += quantity * float(size_product_relation.product.price)
            OrderSizeProductRelation.objects.create(
                order=order,
                size_product_relation=size_product_relation,
                quantity=quantity
            )
        total += float(order.payment_method.price)
        total += float(order.shipping_method.price)
        return order.save(total=total)







