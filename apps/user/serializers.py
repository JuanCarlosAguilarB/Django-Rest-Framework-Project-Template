# Python
import json

# Django
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

# Django rest
from rest_framework import serializers

# Apps
from apps.user.models import UserAuth


class ListUserSerializer(serializers.ModelSerializer):
    """ 
    serializers for list all users
    """
    
    class Meta:
        model = UserAuth
        exclude = ('password', 'user_permissions', 'is_superuser', 'last_login', 'is_staff', 'is_active', 'groups')
 
        
class CreateUserSerializer(serializers.ModelSerializer):
    """ 
    serializers for create an user with corfimn password 
    """
    
    # field by verify password    
    password2 = serializers.CharField(write_only=True)
    
    
    def validate_password2(self, value):
        """ 
        Funtion for validate password 
        """
        
        if value != self.context["password"]:
            raise serializers.ValidationError(_("password don't match"))
        
    def create(self, validated_data):
        """ 
        Funtion for to create a user 
        """
        validated_data.pop("password2")
        
        #is needly to encripted  the password
        validated_data['password'] = make_password(validated_data['password'])
        return UserAuth.objects.create(**validated_data)
    
    class Meta:
        model = UserAuth
        exclude = ('user_permissions', 'is_superuser', 'last_login', 'is_staff', 'is_active', 'groups')
        
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAuth
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    

class DeleteAccount(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAuth
        fields = ('password',)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value


    