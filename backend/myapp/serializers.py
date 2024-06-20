from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
           
        )
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ['user', 'profile_image']


