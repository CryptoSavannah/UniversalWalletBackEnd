from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for the User Model
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'phone_number', 'location')

    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_client=True
        user.save()
        return user

class UserSaveSerializer(serializers.ModelSerializer):
    """
    Save serializer for User details
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'location')

class UserShortDetailsSerializer(serializers.ModelSerializer):
    """
    Short Detail serializer for User
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'location', 'phone_number')

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)