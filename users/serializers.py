from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=127, write_only=True)
    
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    
    birthdate = serializers.DateField(allow_null=True, default=None)
    email = serializers.EmailField()
    
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False, read_only=True)

   
    def validate_email(self, validate_email):
        if User.objects.filter(email=validate_email).exists():
            raise ValidationError("email already registered.")
        return validate_email


    def validate_username(self, validate_username):
        if User.objects.filter(username=validate_username).exists():
            raise ValidationError("username already taken.")
        return validate_username
    
    
    def create(self, validated_data):
        if validated_data["is_employee"] is False:
            user_type = User.objects.create_user(**validated_data)
        else:
            user_type = User.objects.create_superuser(**validated_data)
    
        return user_type
    
    
    def update(self, instance: User, validated_data: dict):
        for k, v in validated_data.items():
            if k == "password":
                instance.set_password(v)
            else:
                setattr(instance, k, v)
        instance.save()
        return instance
    
