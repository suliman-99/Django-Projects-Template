from django.utils import timezone
from rest_framework import serializers
from translation.methods import translate, translation_field_required_kwargs
from translation.fields import UpdateTranslationField
from translation.plugs import JsonTranslationPlug
from test_app.models import TestTimeModel, Test, SubTest


class UpdateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            *translate('text'),
            'un',
        )
        extra_kwargs = {
            **translation_field_required_kwargs('text'),
        }


class ByFieldUpdateTestSerializer(JsonTranslationPlug, serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            'text',
            'un',
        )

    text = UpdateTranslationField(base_is_enough=True)


class GetTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            'text',
            'un',
        )


class SubTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTest
        fields = (
            'id',
            'text',
            'test',
        )


class TestTimeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTimeModel
        fields = (
            'created_at', 
            'timezone_now', 
            'timezone_localtime_timezone_now',
        )
        extra_kwargs = {
            'timezone_now': { 'read_only': True },
            'timezone_localtime_timezone_now': { 'read_only': True },
        }

    def create(self, validated_data):
        validated_data['timezone_now'] = timezone.now()
        validated_data['timezone_localtime_timezone_now'] = timezone.localtime(timezone.now())
        return super().create(validated_data)
