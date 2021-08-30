from rest_framework import serializers
from django.template.defaultfilters import slugify
from django.db import models
from datetime import date




#serializer that will create slug base on name before save
class ModelAutoSlugSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        return instance




#extend for models that include address data (User and Order)
class ModelWithAddress(models.Model):
    street = models.CharField(max_length=128)
    home_number = models.CharField(max_length=16)
    apartament_number = models.CharField(max_length=16, blank=True, null=True)
    zip_code = models.CharField(max_length=16)
    city = models.CharField(max_length=64)




#check if code exists and is active
class DiscountsValidator:
    def get_if_exists(code, queryset):
        res = queryset.filter(code=code)
        if res.exists():
            discount = res.first()
            if discount.start_date <= date.today() <= discount.end_date:
                return discount
        return None
