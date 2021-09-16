from django.db import models
from datetime import datetime, timedelta
from app.serializers import SizeProductRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models import PaymentMethod, ShippingMethod
from address.models import AddressField
from django.contrib.auth.models import User
import uuid





class Cart(models.Model):
    number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expire_time = models.DateTimeField(default=datetime.now()+timedelta(days=3))

    def __str__(self):
        return self.number





class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    size_product_relation = models.ForeignKey(SizeProductRelation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()





class DiscountCode(models.Model):
    code = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(0.99)])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.value





class Order(models.Model):
    number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(SizeProductRelation, through='OrderSizeProductRelation')
    with_discount = models.BooleanField(default=False)
    address = AddressField(on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return 'Order #' + str(self.pk)





class OrderSizeProductRelation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    size_product_relation = models.ForeignKey(SizeProductRelation, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()