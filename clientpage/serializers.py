from rest_framework import serializers

from clientpage.models import * 


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

