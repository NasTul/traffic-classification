from rest_framework import serializers
from api.models import uploadfile, graphfile, graphdata



class uploadfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadfile
        fields = '__all__'


class graphfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = graphfile
        fields = '__all__'


class graphdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = graphdata
        fields = '__all__'