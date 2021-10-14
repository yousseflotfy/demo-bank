from rest_framework import serializers 
from .models import LoanFund, LoanTerm , FundApplication , TermApplication



class FundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            '__all__'
        )
        model = FundApplication


class TermApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            '__all__'
        )
        model = TermApplication


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