from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only= True)

    class Meta:
        model = User
        fields = (
            'id', 
            'username',
            'email', 
            'image',
            'password',
            'confirm_password'
        )
        read_only_fields = ['is_teacher']

    def create(self, validated_data):
        if not validated_data['confirm_password']:
            raise serializers.ValidationError('Confirm your password')
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError('passwords are not same!')
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user