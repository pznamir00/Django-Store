from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField





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





class BrandSerializer(serializers.ModelSerializer):
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
    def create_sizes_and_files(self, instance, sizes, files):
        for size in sizes:
            SizeProductRelation.objects.create(**size, product=instance)
        for file in files:
            Picture.objects.create(file=file['base64file'], product=instance)





class ProductSimpleSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'color', 'brand', 'subcategory', 'sizes', 'pictures', 'base64files', 'price')
        read_only_fields = ('slug',)
        extra_kwargs = {
            'description': { 'write_only': True },
            'color': { 'write_only': True },
            'brand': { 'write_only': True },
            'subcategory': { 'write_only': True },
            'sizes': { 'write_only': True }
        }

    def create(self, validated_data):
        sizes, base64files = validated_data.pop('sizes'), validated_data.pop('base64files')
        instance = super(ProductSimpleSerializer, self).create(validated_data)
        self.create_sizes_and_files(instance, sizes, base64files)
        return instance





class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at')

    #delete sizes and pictures of instance that could update object's assets
    def delete_sizes_and_files(self, instance):
        Picture.objects.filter(product=instance).delete()
        SizeProductRelation.objects.filter(Product=instance).delete()

    def update(self, instance, validated_data):
        base64files = validated_data.pop('base64files')
        instance = super(ProductDetailSerializer, self).update(instance, validated_data)
        #update sizes and pictures
        self.delete_files(instance)
        self.create_files(instance, base64files)
        return instance





class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'





class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'


