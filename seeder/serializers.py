from rest_framework import serializers
from users.models import User


class SuperUserSeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        return User.objects.create_superuser(
            email=validated_data['email'], 
            password=validated_data['password'],
        )
