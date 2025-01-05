from rest_framework import serializers
from .models import *

class DiabetesDataSerializers(serializers.ModelSerializer):

    gender = serializers.SlugRelatedField(
        queryset = Gender.objects.all(),
        slug_field = 'name'
    )

    region = serializers.SlugRelatedField(
        queryset = Region.objects.all(),
        slug_field = 'name'
    )

    results = serializers.SlugRelatedField(
        queryset = Results.objects.all(),
        slug_field = 'name'
    )

    class Meta:
        model = DiabetesData
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'