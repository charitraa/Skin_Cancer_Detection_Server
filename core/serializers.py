from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required fields.
    """
    full_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    class Meta:
        model = User
        fields ='__all__'

    def create(self, validated_data):
        """
         Create and return a new user with the validated data.
        """
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'message': 'A user with this email already exists.'})
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({'message': 'A user with this username already exists.'})
        user = User.objects.create_user(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password'],)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username', 'full_name','password']

    def update(self, instance, validated_data):
        # Prevent duplicate emails
        if 'email' in validated_data and User.objects.filter(email=validated_data['email']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        # Prevent duplicate usernames
        if 'username' in validated_data and User.objects.filter(username=validated_data['username']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})

        # Update fields
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # ⚠️ IMPORTANT: Password handling
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Use set_password to hash

        instance.save()
        return instance
