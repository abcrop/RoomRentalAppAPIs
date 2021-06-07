from os import write
from endpoints import services
from wsgiref.handlers import read_environ
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField, EmailField, HiddenField, ReadOnlyField
from endpoints import models
from apis import settings
from django.utils import timezone
import re
import logging


logger = logging.getLogger(__name__)
del logging

#utility class : timezone aware dataAndTime
class DateTimeFieldWithTimeZone(serializers.DateTimeField):
    
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super().to_representation(value)


class CategorySerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.Category
        fields = ("__all__")
        
class FavoriteSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.Favorite
        fields = ("__all__")
        
class HouseSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta: 
        model = models.House
        fields = ("__all__")
        
class FeatureSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.Feature
        fields = ("__all__")

class RoomSerializer(serializers.ModelSerializer):
    room_image = serializers.ImageField(max_length=None, use_url=True, required=False)
    # With related_name in Feature Model
    features = FeatureSerializer(read_only=True, many=True)
    room_expires_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT,)
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.Room
        # fields = ['room_image', 'features', ]
        fields =  [field.name for field in model._meta.fields]
        fields.append('features')

    
class RoomRequestSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.RoomRequest
        fields = ("__all__")

class RewardSerializer(serializers.ModelSerializer):
    
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta: 
        model = models.Reward
        fields = ("__all__")

class RewardTrackerSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.RewardTracker
        fields = ("__all__")
    
class RentalDataSerializer(serializers.ModelSerializer):
    # Without related_name in model, only ForeignKey
    room_id = RoomSerializer(read_only = True)
    rewards = RewardTrackerSerializer(read_only = True, many=True)
    last_paid_date = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT,)
    next_payable_date = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT,)
    advance_paid_date = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT,)
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.RentalData
        fields = ("__all__")

class FavoriteSerializer(serializers.ModelSerializer):
    created_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    
    class Meta:
        model = models.Favorite
        fields = ("__all__")
        
class SignupUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    is_staff = ReadOnlyField()
    is_active = ReadOnlyField()
    is_superuser = ReadOnlyField()
    date_joined = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    is_blocked = ReadOnlyField()
    password = CharField(write_only=True)
    groups = CharField(default=None, read_only=True)
    user_permissions = CharField(default=None, read_only=True)
    last_login = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only = True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    
    def validate_password(self, value):
      return services.validate_password(self,value)
    
    def validate(self, data):
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'education', 'occupation', 'user_type', ]
        keys = [key for key in data.keys()]
        
        print(keys)
        
        #checking if required_fields is a subset of keys
        # result = all( field in keys for field in keys)
        
        if not set(keys).issubset(set(required_fields)):        
            raise serializers.ValidationError(f'You have missed required fields.')
        
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',data['email']):
            services.validate_email_api(data['email'])
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('write_only_char_field', None)
        password = validated_data.pop('password')
        user = models.AppUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        return instance
        
    class Meta:
        model = models.AppUser
        fields = [field.name for field in model._meta.fields]
        fields.append('groups')
        fields.append('user_permissions')
    

class PasswordUpdateSerializer(serializers.ModelSerializer):
    current_password = CharField(write_only=True)
    new_password = CharField(write_only=True)
    refresh_token = CharField(write_only=True)
    password = HiddenField(default="Not Visible")
    first_name = HiddenField(default="Not Visible")
    last_name = HiddenField(default="Not Visible")
    email = HiddenField(default="Not Visible")
    username = HiddenField(default="Not Visible")
    date_of_birth = HiddenField(default="Not Visible")
    phone_number = HiddenField(default="Not Visible")
    is_blocked = HiddenField(default="Not Visible")
    user_type = HiddenField(default="Not Visible")
    occupation = HiddenField(default="Not Visible")
    education = HiddenField(default="Not Visible")
    image = HiddenField(default="Not Visible")
    address = HiddenField(default="Not Visible")
    last_login = HiddenField(default="Not Visible")
    is_superuser = HiddenField(default="Not Visible")
    is_staff = HiddenField(default="Not Visible")
    is_active = HiddenField(default="Not Visible")
    date_joined = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only=True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only=True)
    
    def validate_new_password(self, value):
       return services.validate_password(self,value)
    
    class Meta:
        model = models.AppUser
        fields = [field.name for field in model._meta.fields]
        fields.append("current_password")
        fields.append("new_password")
        fields.append("refresh_token")
        
        # extra_kwargs = {
        #     'id' : {
        #         'er'
        #     }
        # }


class UserUpdateSerializer(serializers.ModelSerializer):
    password = HiddenField(default="Not Visible")
    email = HiddenField(default="Not Visible")
    date_of_birth = HiddenField(default="Not Visible")
    phone_number = HiddenField(default="Not Visible")
    is_blocked = HiddenField(default="Not Visible")
    user_type = HiddenField(default="Not Visible")
    last_login = HiddenField(default="Not Visible")
    is_superuser = HiddenField(default="Not Visible")
    is_staff = HiddenField(default="Not Visible")
    is_active = HiddenField(default="Not Visible")
    date_joined = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only=True)
    updated_at = DateTimeFieldWithTimeZone(format=settings.DATETIME_FORMAT, read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    
        
    """
    Change all except: password, email, phone_number, is_blocked, user_type, date_of_birth
    """
    def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.username = validated_data.get('username', instance.username)
            if validated_data.get('image'):
                instance.image = validated_data.get('image')
            else: 
                instance.image = instance.image
            instance.education = validated_data.get('education', instance.education)
            instance.occupation = validated_data.get('occupation', instance.occupation)
            instance.address = validated_data.get('address', instance.address)
            instance.save()
            return instance
    
    class Meta:
        model = models.AppUser
        fields = [field.name for field in model._meta.fields]
        
class UserDeleteSerializer(serializers.ModelField):
    class Meta:
        model = models.AppUser
        fields = [field.name for field in model._meta.fields]

class UserListSerializer(serializers.ModelSerializer):
    password = HiddenField(default="Not Visible")
    
    class Meta:
        model = models.AppUser
        fields = ("__all__")

class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
     
    class Meta:
        model = models.Favorite
        fields = ('username', 'password', )
    
class RefreshTokenSerializer(serializers.ModelSerializer):
    refresh_token = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        pass
    
    class Meta:
        model = models.Favorite
        fields = ('refresh_token', )

class RevokeTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = ( )
    
"""
Dummy RoomRequestSerializer
-to demonstrate serializer with custom fields
"""
# class RoomRequestSerializer(serializers.ModelSerializer):
#     tenant_id = serializers.CharField(max_length=2)
#     room_id = serializers.CharField(max_length=2)
#     request_msg = serializers.CharField(max_length=100)
    
#     class Meta:
#         #You can write any model here
#         model = models.Room 
#         fields = ('tenant_id', 'room_id', 'request_msg')
    

