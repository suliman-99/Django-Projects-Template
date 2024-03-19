from common.audit.serializers import AuditSerializer
from users.models import User
# from product.models import Category, SubCategoryfrom rest_framework import serializers


class SuperUserSeederSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        return User.objects.create_superuser(
            email=validated_data['email'], 
            password=validated_data['password'],
        )


# class CategorySerializer(AuditSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', )


# class SubCategorySerializer(AuditSerializer):
#     class Meta:
#         model = SubCategory
#         fields = ('name', 'category_name')

#     category_name = serializers.CharField()

#     def create(self, validated_data):
#         validated_data['category'] = Category.objects.get(name=validated_data.pop('category_name'))
#         return super().create(validated_data)
