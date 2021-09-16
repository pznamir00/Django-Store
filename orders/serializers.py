from rest_framework import serializers
from .models import Cart, CartProduct, Order, DiscountCode





class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'





class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ('number', 'expire_time', 'products',)





class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ('number', 'user', 'created_at', 'total', 'payment_method', 'shipping_method', 'address', 'cart')
        read_only_fields = ('number', 'created_at', 'total')

    def validate(self, data):
        """
        Payment_method and shipping_method are not required because there is capability to delete payment and app won't be deleting
        orders, thats why it's necessery to look up this data here
        """
        if 'payment_method' not in data or 'shipping_method' not in data:
            raise serializers.ValidationError({'message': [
                "No field payment_method or shipping_method in request"
            ]})
        return data





class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ('pk', 'value', 'start_at', 'end_at',)