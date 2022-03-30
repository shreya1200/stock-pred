from rest_framework import serializers
from . models import *
  
class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ['name', 'detail']