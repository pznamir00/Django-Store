from .models import Cart, CartProduct, Order, OrderSizeProductRelation, DiscountCode
from .serializers import CartProductSerializer, CartSerializer, OrderSerializer, DiscountCodeSerializer
from .permissions import NoUpdateAndDestroyOnlyForAdmin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import IsAdminUser
from datetime import date




class CartView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'number'

    @action(methods=['post'], detail=True, url_name='add_product')
    def add_product(self, request, number):
        cart = self.get_object()
        data = request.data.copy()
        data['cart'] = cart.pk
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(methods=['delete'], detail=True, url_name='remove_product')
    def remove_product(self, request, number):
        cart_product_pk = request.data['cart_product_pk']
        CartProduct.objects.filter(pk=cart_product_pk, cart__number=number).delete()
        return Response({
            'message': 'Deleted from cart'
        }, status=200)





class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (NoUpdateAndDestroyOnlyForAdmin,)
    lookup_field = 'number'

    """
    returns empty list if user not logged,
    returns list of user's orders if is logged,
    returns all data is user is admin
    """
    def get_queryset(self):
        queryset = Order.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset
            return queryset.filter(user=self.request.user)
        return []

    def perform_create(self, serializer):
        #cart object
        cart = serializer.validated_data.pop('cart')
        #discount code (if exists, else None)
        discount_code = serializer.validated_data.pop('discount_code') if 'discount_code' in serializer.validated_data else ''
        #start of calculating total price
        total = 0.00
        order = serializer.save(user=self.request.user, total=total)
        for cart_product in cart['products']:
            quantity = cart_product['quantity']
            size_product_relation = cart_product['product_size_relation']
            #update of quantity of those size_product_relations
            size_product_relation.quantity -= quantity
            size_product_relation.save()
            #increase total
            total += quantity * float(size_product_relation.product.price) 
            OrderSizeProductRelation.objects.create(
                order=order,
                size_product_relation=size_product_relation,
                quantity=quantity
            )
        order.total += float(order.payment_method.price)
        order.total += float(order.shipping_method.price)
        today = date.today()
        discount = DiscountCode.objects.filter(
            code=discount_code, 
            start_date__gte=today, 
            start_date__lte=today
        ).first()
        if discount:
            #consider discount code if is existing and is correct
            diff = 1.0 - discount.value
            order.total *= diff
            order.with_discount = True
        return order.save()





class DicountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
    permission_classes = (IsAdminUser,)