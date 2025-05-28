from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name', 'role', 'password', 'phone', 'department']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {
                'required': True,
                'error_messages': {
                    'required': 'Email is required',
                    'invalid': 'Enter a valid email address'
                }
            },
            'name': {
                'required': True,
                'error_messages': {
                    'required': 'Name is required'
                }
            },
            'role': {
                'required': True,
                'error_messages': {
                    'required': 'Role is required'
                }
            },
            'password': {
                'required': True,
                'write_only': True,
                'error_messages': {
                    'required': 'Password is required'
                }
            },
            'phone': {
                'required': True,
                'error_messages': {
                    'required': 'Phone number is required',
                    'invalid': 'Enter a valid phone number'
                }
            },
            'department': {
                'required': True,
                'error_messages': {
                    'required': 'Department is required',
                    'invalid': 'Enter a valid department'
                }
            }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate_role(self, value):
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Invalid role. Must be 1 (Admin), 2 (Teacher), or 3 (Student)")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data['role'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            department=validated_data['department']
        )

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address'
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            'required': 'Password is required'
        }
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        data['user'] = user
        return data