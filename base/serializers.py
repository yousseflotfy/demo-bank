from rest_framework import serializers 
from .models import LoanFund, LoanTerm , FundApplication , TermApplication



class FundApplicationSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField('get_type_name')
    def get_type_name(self, obj):
        return obj.fund_type.name
    class Meta:
        fields = (
            'fund_type',
            'amount',
            'status',
            'type_name',
            

        )
        model = FundApplication


class TermApplicationSerializer(serializers.ModelSerializer):

    type_name = serializers.SerializerMethodField('get_type_name')
    def get_type_name(self, obj):
        return obj.term_type.name
    class Meta:
        fields = (
            'term_type',
            'amount',
            'status',
            'type_name',
            

        )
        model = TermApplication


    # def save(self):
    #     term_type = self.validated_data['term_type']    


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


