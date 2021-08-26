from rest_framework import serializers
from .models import *
from .helpers import ModelAutoSlugSerializer
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist




class SubCategorySerializer(ModelAutoSlugSerializer):
    class Meta:
        model = SubCategory
        fields = ('pk', 'name', 'slug', 'category')
        read_only_fields = ('slug',)





class CategorySerializer(ModelAutoSlugSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('pk', 'name', 'slug', 'subcategories',)
        read_only_fields = ('slug', 'subcategories',)





class BrandSerializer(ModelAutoSlugSerializer):
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'description', 'logo')
        read_only_fields = ('slug',)





class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('pk', 'name', 'value')





class PictureSerializer(serializers.ModelSerializer):
    base64file = Base64ImageField(write_only=True)
    class Meta:
        model = Picture
        fields = ('base64file', 'file',)
        read_only_fields = ('file',)




class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('pk', 'value', 'category')





class SizeProductRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeProductRelation
        fields = ('pk', 'size', 'quantity',)





class ProductSerializer(ModelAutoSlugSerializer):
    sizes = SizeProductRelationSerializer(many=True)
    base64files = PictureSerializer(many=True, write_only=True)
    pictures = PictureSerializer(many=True, read_only=True)

    def _set_sizes_and_files(self, instance, sizes, files):
        for size in sizes:
            SizeProductRelation.objects.create(**size, product=instance)
        for file in files:
            Picture.objects.create(file=file['base64file'], product=instance)





class ProductSimpleSerializer(ProductSerializer):
    sizes = SizeProductRelationSerializer(many=True, write_only=True)
    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'color', 'brand', 'subcategory', 'sizes', 'pictures', 'base64files', 'price')
        read_only_fields = ('slug',)
        extra_kwargs = {
            'description': { 'write_only': True }, 
            'color': { 'write_only': True }, 
            'brand': { 'write_only': True }, 
            'subcategory': { 'write_only': True }
        }

    def create(self, validated_data):
        sizes, base64files = validated_data.pop('sizes'), validated_data.pop('base64files')
        instance = super(ProductSimpleSerializer, self).create(validated_data)
        self._set_sizes_and_files(instance, sizes, base64files)
        return instance





class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at')

    def __clear_sizes_and_files(self, instance):
        for size in instance.sizes.all():
            size.delete()
        for picture in instance.pictures.all():
            picture.delete()

    def update(self, instance, validated_data):
        sizes, base64files = validated_data.pop('sizes'), validated_data.pop('base64files')
        instance = super(ProductDetailSerializer, self).update(instance, validated_data)
        self.__clear_sizes_and_files(instance)
        self._set_sizes_and_files(instance, sizes, base64files)
        return instance





class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'





class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'





class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'joined', 'score', 'street', 'home_number', 'apartament_number', 'zip_code', 'city')
        read_only_fields = ('joined', 'score')





class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('pk', 'email', 'is_superuser', 'profile')





class CartSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            required=True
        ),
        required=True
    )

    def to_representation(self, value):
        data = super(CartSerializer, self).to_representation(value)
        for index, sample in enumerate(data['products']):
            try:
                relation = SizeProductRelation.objects.get(pk=sample['product_size_relation'])
                product_data = ProductSimpleSerializer(instance=relation.product).data
                if relation.quantity < sample['quantity']:
                    raise serializers.ValidationError({
                        'message': ["Quantity of your product in cart cannot be greater than available"]
                    })
                data['products'][index] = {
                    'product': product_data,
                    'size': relation.size.value,
                    'quantity': sample['quantity']
                }
            except KeyError:
                raise serializers.ValidationError({
                    'message': ["Wrong field inside products variable. Excepted only product_size_relation and quantity parameters in each sample."]
                })
            except ObjectDoesNotExist:
                raise serializers.ValidationError({
                    'message': ["This size or product does not exist"]
                })
        return data




class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required=True, write_only=True)
    class Meta:
        model = Order
        fields = ('pk', 'user', 'created_at', 'total', 'payment_method', 'shipping_method', 'products')
        read_only_fields = ('pk', 'created_at', 'total', 'products')