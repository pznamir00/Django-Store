from django.db import models
from django.contrib.auth.models import User
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(unique=True)
    score = models.PositiveIntegerField(default=0)
    joined = models.DateTimeField(auto_now_add=True)
    address = AddressField(on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.email + ' profile'