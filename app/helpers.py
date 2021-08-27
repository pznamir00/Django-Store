from rest_framework import serializers
from django.template.defaultfilters import slugify
from django.db import models





class ModelAutoSlugSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return self.Meta.model.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        return instance




    
class ModelWithAddress(models.Model):
    street = models.CharField(max_length=128)
    home_number = models.CharField(max_length=16)
    apartament_number = models.CharField(max_length=16, blank=True, null=True)
    zip_code = models.CharField(max_length=16)
    city = models.CharField(max_length=64)