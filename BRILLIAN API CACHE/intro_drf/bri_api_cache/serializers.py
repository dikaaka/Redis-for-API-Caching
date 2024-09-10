from rest_framework import serializers
from .models import *

class InstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institutions
        fields = '__all__'

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ['sector', 'sub_sector','sub_sector_id']

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'