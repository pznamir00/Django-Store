from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from dj_rest_auth.registration.serializers import RegisterSerializer
from address.forms import AddressField





class ExtendedRegisterSerializer(RegisterSerializer):
    address = AddressField()

    def get_cleaned_data(self):
        #validate during registration
        super(ExtendedRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'address': self.validated_data.get('address', {})
        }

    def save(self, request):
        user = super(ExtendedRegisterSerializer, self).save(request)
        #immidenty create profile after user's save
        UserProfile.objects.create(
            user=user,
            phone_number=request._data['phone_number'],
            address=request._data['address']
        )
        return user





class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('pk', 'name', 'slug', 'category')
        read_only_fields = ('slug',)





class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('pk', 'name', 'slug', 'subcategories',)
        read_only_fields = ('slug', 'subcategories',)





class BrandSerializer(ModelAutoSlugSerializer):
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'description', 'logo',)
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




#base serializer for ProductSimpleSerializer and ProductDetailSerializer
class ProductSerializer(serializers.ModelSerializer):
    #objects of SizeProductRelation instance
    sizes = SizeProductRelationSerializer(many=True)
    #only for input (which requires only base64 encoded files)
    base64files = PictureSerializer(many=True, write_only=True)
    #objects of Picture instance
    pictures = PictureSerializer(many=True, read_only=True)

    #create sizes and pictures objects for instance
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

    #delete sizes and pictures of instance that could update object's assets
    def __clear_sizes_and_files(self, instance):
        sizes = instance.sizes.all()
        pictures = instance.pictures.all()
        for size in sizes:
            size.delete()
        for picture in pictures:
            picture.delete()

    def update(self, instance, validated_data):
        sizes, base64files = validated_data.pop('sizes'), validated_data.pop('base64files')
        instance = super(ProductDetailSerializer, self).update(instance, validated_data)
        #clean sizes and pictures
        self.__clear_sizes_and_files(instance)
        #save new
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
        fields = ('phone_number', 'joined', 'score', 'address')
        read_only_fields = ('joined', 'score')





class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('pk', 'email', 'is_superuser', 'profile')





class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'





class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)
    class Meta:
        model = Cart
        fields = ('number', 'products',)





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
