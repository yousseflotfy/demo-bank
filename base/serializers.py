from rest_framework import serializers 
from .models import LoanFund, LoanTerm






class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            '__all__'
        )
        model = LoanFund

class LoanTermSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            '__all__'
        )
        model = LoanTerm        