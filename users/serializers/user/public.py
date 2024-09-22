from rest_framework import serializers
from ...models import User

# this is for displaying the user profile for anyone
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
        )
