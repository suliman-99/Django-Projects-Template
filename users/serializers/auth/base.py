from rest_framework import serializers
from ...models import User
from ..group.nested import SmallGroupSerializer


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            
            'is_active',
            'is_staff',
            'is_superuser',
            'is_admin',

            'date_joined',
            'first_login',
            'last_login',
            'last_refresh',

            'email',
            'email_verified',

            'phone_number',
            'phone_number_verified',

            'first_name',
            'last_name',
            'language_code',

            'groups',
            'all_permissions_full_names',
        )

    groups = serializers.SerializerMethodField()
    all_permissions_full_names = serializers.SerializerMethodField()
    
    def get_groups(self, user: User):
        return SmallGroupSerializer(user.groups.all(), many=True, context=self.context).data

    def get_all_permissions_full_names(self, user: User):
        return user.get_all_permissions()
