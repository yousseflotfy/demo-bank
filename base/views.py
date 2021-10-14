from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import LoanFund, LoanTerm  , User  , Group , FundApplication , TermApplication
from .serializers import LoanFundSerializer, LoanTermSerializer , FundApplicationSerializer , TermApplicationSerializer
from rest_framework.response import Response
from .permissions import isInvestor, isBank , isCustomer
from rest_framework.permissions import IsAdminUser
import numpy_financial as np



# def home(request):
#     return HttpResponse('Home Page')


#investor API

class investorAPI(APIView):
    permission_classes = [isInvestor]

    def get(self,request):
        queryset = FundApplication.objects.filter(provider = request.user)
        serializer = FundApplicationSerializer(queryset, many=True)
        return Response({"Your Fund applications":serializer.data})


    def post(self,request):
        fundType = request.data.get('type')
        loanFund = LoanFund.objects.get(name = fundType)
        fundamount = request.data.get('amount')
        if(fundamount > int(loanFund.max_amount) or fundamount < int (loanFund.min_amount)):
            return Response({"please enter a valid amount"})
        else :
            fund = FundApplication.objects.create(
                amount = fundamount,
                provider = request.user,
                fund_type = loanFund
            )
            serializer = FundApplicationSerializer(fund)
            return Response({"added Fund application":serializer.data})




class amotizationAPI(APIView):
    permission_classes = [isCustomer]
    def get(self,request):
        loanTermId =  request.data.get('termNumber')
        loanterm = LoanTerm.objects.get(id = loanTermId)
        interestRate = loanterm.intrest_rate/12
        numberOfMonths = loanterm.duration_years * 12
        principalBorrowed = loanterm.amount
        monthlyPayment   = np.pmt(interestRate, numberOfMonths, principalBorrowed)
        return Response(monthlyPayment)

class customerAPI(APIView):
    permission_classes = [isCustomer]
    def get(self,request):
        queryset = TermApplication.objects.filter(customer = request.user)
        serializer = TermApplicationSerializer(queryset, many=True)
        return Response({"Your Fund applications":serializer.data})



    def post(self,request):
        termType = request.data.get('type')
        loanterm = LoanTerm.objects.get(name = termType)
        termAmount = request.data.get('amount')
        if(termAmount > int(loanTerm.max_amount) or termAmount < int (loanTerm.min_amount)):
            return Response({"please enter a valid amount"})
        else :
            term = TermApplication.objects.create(
                amount = termAmount,
                customer = request.user,
                term_type = loanterm
            )
            serializer = TermApplicationSerializer(term)
            return Response({"added loan application":serializer.data})    


    # def put(self,request):
    #     LoanTermId = request.data.get('termNumber')
    #     loanTerm = LoanTerm.objects.get(id=LoanTermId)
    #     amount = request.data.get('amount')
    #     status = LoanTerm.status.IN_PROCESS
    #     # status = Status.objects.get(phase='in Process')
    #     self.check_object_permissions(request,loanTerm)
    #     if(loanTerm.provider is not None):
    #        return Response('fund already taken please chose another one')
    #     if(amount >= loanTerm.min_amount and amount <= loanTerm.max_amount):
    #         loanTerm.amount = amount
    #         loanTerm.status = status
    #         loanTerm.provider = request.user
    #         loanTerm.save()
    #         return Response('Loan Term application sent')
    #     else:
    #         return Response('Please enter a valid amount')  




class viewloansAPI(APIView):
    def get(self,request):
        if(request.user.groups.filter(name = "investor")):
            queryset = LoanFund.objects.all()
            amount = request.data.get('amount')
            queryset = LoanFund.objects.all().filter(max_amount__gte = amount)
            queryset = queryset.filter(min_amount__lte = amount)
            serializer = LoanFundSerializer(queryset, many=True)
            self.check_object_permissions(request,LoanFund.objects.get(id=1))
            return Response({"Loan Funds":serializer.data})
        else if (request.user.groups.filter(name = "cutomer")):
            queryset = LoanFund.objects.all()
            amount = request.data.get('amount')
            queryset = LoanTerm.objects.all().filter(max_amount__gte = amount)
            queryset = queryset.filter(min_amount__lte = amount)
            serializer = LoanTermSerializer(queryset, many=True)
            self.check_object_permissions(request,LoanTerm.objects.get(id=1))
            return Response({"Loan Terms":serializer.data})
        else :
            return Response({"Not Accessible"})    


        


class editFundApplicationsAPI(APIView):
    permission_classes = [isBank]
    
    def put(self,request):
        LoanFundId = request.data.get('fundName')
        loanFund = LoanFund.objects.get(name=loanFundId)
        status = request.data.get('status')
        loanFund.status = status
        loanFund.save()
        return Response('Status updated')



class editTermApplicationsAPI(APIView):
    permission_classes = [isBank]
    
    def put(self,request):
        LoanTermId = request.data.get('termNumber')
        loanTerm = LoanTerm.objects.get(id=LoanTermId)
        status = request.data.get('status')
        loanTerm.status = status
        loanTerm.save()
        return Response('Status updated')






class LoanFundViewSet(viewsets.ModelViewSet):
    queryset = LoanFund.objects.all()
    permission_classes = (IsAuthenticated,isBank)
    serializer_class = LoanFundSerializer


class LoanTermViewSet(viewsets.ModelViewSet):
    queryset = LoanTerm.objects.all()
    permission_classes = (IsAuthenticated,isBank)
    serializer_class = LoanFundSerializer    




# def createLoanFund(request):
#     if request.method == 'POST':
#         if(request.user.group == 'bankPersonnel'):
#             LoanFund.objects.Create(
#                 creator = request.user,
#                 fund_type = request.POST.get('fund_type'),
#                 duration_years = request.POST.get('duration_years'),
#                 interest_rate = request.POST.get('interest_rate'),
#                 max_amount  = request.POST.get('max_amount'),
#                 min_amount = request.POST.get('min_amount'),
#             )
#         else :
#             HttpResponse('not authorized')
                

# Create your views here.
