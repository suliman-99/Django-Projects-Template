from django.utils import timezone
from rest_framework import serializers
from translation.fields import UpdateTranslationField, GetTranslationField
from test_app.models import TestTranslationModel, TestTimeModel, TestDeleteModel, TestDeleteModel2


class TestUpdateTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTranslationModel
        fields = (
            'id',
            'text',
            'translated_text',
        )

    translated_text = UpdateTranslationField(
        required_languages=['ar'],
        accepted_languages=['ar', 'en'],
    )


class TestGetTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTranslationModel
        fields = (
            'id',
            'text',
            'translated_text',
        )

    translated_text = GetTranslationField()


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
    

class TestDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestDeleteModel
        fields = '__all__'
    

class TestDeleteSerializer2(serializers.ModelSerializer):
    class Meta:
        model = TestDeleteModel2
        fields = '__all__'
