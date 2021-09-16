from django.contrib.auth.models import User
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from address.forms import AddressField
from .models import UserProfile




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