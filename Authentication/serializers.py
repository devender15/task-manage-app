from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'fname', 'phone')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def create(self, validated_data):

        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'], fname=validated_data['fname'], phone=validated_data['phone'])

        return user


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'