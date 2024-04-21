from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_seeding.models import AppliedSeeder
from django_seeding.seeder_registry import SeederRegistry
from common.permissions import IsSuperuser


class AppliedSeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedSeeder
        fields = ('id', )

    def update(self, instance, validated_data):
        instance.delete()
        return AppliedSeeder.objects.create(**validated_data)
    

class SeedAllSerializer(serializers.Serializer):
    debug = serializers.BooleanField(required=False, allow_null=True)
    ids = serializers.ListField(required=False, allow_null=True, child=serializers.CharField())

    def create(self, validated_data):
        SeederRegistry.import_all_then_seed_all(**validated_data)
        return True


class AppliedSeederViewSet(ModelViewSet):
    permission_classes = (IsSuperuser, )
    queryset = AppliedSeeder.objects.all()
    serializer_class = AppliedSeederSerializer
    
    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request, *args, **kwargs):
        AppliedSeeder.objects.all().delete()
        return Response({})
    
    @action(detail=False, methods=['post'], url_path='seed-all')
    def seed_all(self, request, *args, **kwargs):
        serializer = SeedAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})
