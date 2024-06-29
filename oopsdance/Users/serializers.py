from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'password', 'full_name', 'contact_number', 'role', 'date_of_birth', 'username', 'avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.setdefault('role', 'guest')
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data.get('full_name', ''),
            contact_number=validated_data.get('contact_number', ''),
            role=validated_data.get('role', 'guest'),
            date_of_birth=validated_data.get('date_of_birth', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Thông tin đăng nhập không chính xác.")
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is not correct')
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError('New password cannot be the same as the old password')
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user