from django.contrib import admin
from app import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Brand)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Product)
admin.site.register(models.Picture)
admin.site.register(models.SizeProductRelation)
admin.site.register(models.PaymentMethod)
admin.site.register(models.ShippingMethod)



