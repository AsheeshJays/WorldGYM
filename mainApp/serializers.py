from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.Serializer):
    pid = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    pro_code = serializers.CharField(max_length=10)
    price = serializers.IntegerField()
    mfcdate = serializers.DateField()
    expdate = serializers.DateField()
    pro_owner = serializers.CharField(max_length=50)
    


    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class MainCatSerializer(serializers.Serializer):
    mcid = serializers.IntegerField()
    name = serializers.CharField(max_length=30)


class SubCatSerializer(serializers.Serializer):
    mcid = serializers.IntegerField()
    name = serializers.CharField(max_length=30)

class BrandSerializer(serializers.Serializer):
    mcid = serializers.IntegerField()
    name = serializers.CharField(max_length=30)




