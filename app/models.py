from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from address.models import AddressField
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
import uuid





class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name





class SubCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name





class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name')
    logo = models.FileField(upload_to='brands', null=True, blank=True)

    def __str__(self):
        return self.name





class Color(models.Model):
    name = models.CharField(max_length=32)
    value = ColorField(format='hexa')

    def __str__(self):
        return self.name





class Size(models.Model):
    value = models.CharField(max_length=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)





class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=.0)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class Picture(models.Model):
    file = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')

    def __str__(self):
        return self.file.name





class SizeProductRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()





class PaymentMethod(models.Model):
    name = models.CharField(max_length=64, unique=True)
    link = models.TextField(unique=True)
    picture = models.ImageField(upload_to='payments')
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.name





class ShippingMethod(models.Model):
    name = models.CharField(max_length=64, unique=True)
    picture = models.ImageField(upload_to='payments')
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.name





class Order(models.Model):
    number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(SizeProductRelation, through='OrderSizeProductRelation')
    with_discount = models.BooleanField(default=False)
    address = AddressField(on_delete=models.CASCADE)

    def __str__(self):
        return 'Order #' + str(self.pk)





class OrderSizeProductRelation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    size_product_relation = models.ForeignKey(SizeProductRelation, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(unique=True)
    score = models.PositiveIntegerField(default=0)
    joined = models.DateTimeField(auto_now_add=True)
    address = AddressField(on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + ' profile'





class DiscountCode(models.Model):
    code = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(0.99)])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.value
