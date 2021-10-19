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
from datetime import date
from rest_framework import status
from django.shortcuts import get_object_or_404

import numpy_financial as np
import pandas as pd

from collections import OrderedDict
from dateutil.relativedelta import *





# def home(request):
#     return HttpResponse('Home Page')


#investor API


        # fundType = request.data.get('type')
        # loanFund = LoanFund.objects.get_object_or_404(name = fundType)
        # fundamount = request.data.get('amount')
        # if(fundamount > int(loanFund.max_amount) or fundamount < int (loanFund.min_amount)):
        #     return Response({"please enter a valid amount"})
        # else :
        #     fund = FundApplication.objects.create(
        #         amount = fundamount,
        #         provider = request.user,
        #         fund_type = loanFund
        #     )
        #     serializer = FundApplicationSerializer(fund)
        #     return Response({"added Fund application":serializer.data})
def amortization_table(interest_rate, years, payments_year, principal, addl_principal=0, start_date=date.today()):
    """ Calculate the amortization schedule given the loan details

    Args:
        interest_rate: The annual interest rate for this loan
        years: Number of years for the loan
        payments_year: Number of payments in a year
        principal: Amount borrowed
        addl_principal (optional): Additional payments to be made each period. Assume 0 if nothing provided.
                                must be a value less then 0, the function will convert a positive value to
                                negative
        start_date (optional): Start date. Will start on first of next month if none provided

    Returns:
        schedule: Amortization schedule as a pandas dataframe
        summary: Pandas dataframe that summarizes the payoff information
    """
    # Ensure the additional payments are negative
    if addl_principal > 0:
        addl_principal = -addl_principal

    # Create an index of the payment dates
    rng = pd.date_range(start_date, periods=years * payments_year, freq='MS')
    rng.name = "Payment_Date"

    # Build up the Amortization schedule as a DataFrame
    df = pd.DataFrame(index=rng,columns=['Payment', 'Principal', 'Interest', 
                                        'Addl_Principal', 'Curr_Balance'], dtype='float')

    # Add index by period (start at 1 not 0)
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "Period"

    # Calculate the payment, principal and interests amounts using built in Numpy functions
    per_payment = np.pmt(interest_rate/payments_year, years*payments_year, principal)
    df["Payment"] = per_payment
    df["Principal"] = np.ppmt(interest_rate/payments_year, df.index, years*payments_year, principal)
    df["Interest"] = np.ipmt(interest_rate/payments_year, df.index, years*payments_year, principal)

    # Round the values
    df = df.round(2) 

    # Add in the additional principal payments
    df["Addl_Principal"] = addl_principal

    # Store the Cumulative Principal Payments and ensure it never gets larger than the original principal
    df["Cumulative_Principal"] = (df["Principal"] + df["Addl_Principal"]).cumsum()
    df["Cumulative_Principal"] = df["Cumulative_Principal"].clip(lower=-principal)

    # Calculate the current balance for each period
    df["Curr_Balance"] = principal + df["Cumulative_Principal"]

    # Determine the last payment date
    try:
        last_payment = df.query("Curr_Balance <= 0")["Curr_Balance"].idxmax(axis=1, skipna=True)
    except ValueError:
        last_payment = df.last_valid_index()

    last_payment_date = "{:%m-%d-%Y}".format(df.loc[last_payment, "Payment_Date"])

    # Truncate the data frame if we have additional principal payments:
    if addl_principal != 0:

        # Remove the extra payment periods
        df = df.ix[0:last_payment].copy()

        # Calculate the principal for the last row
        df.ix[last_payment, "Principal"] = -(df.ix[last_payment-1, "Curr_Balance"])

        # Calculate the total payment for the last row
        df.ix[last_payment, "Payment"] = df.ix[last_payment, ["Principal", "Interest"]].sum()

        # Zero out the additional principal
        df.ix[last_payment, "Addl_Principal"] = 0

    # Get the payment info into a DataFrame in column order
    payment_info = (df[["Payment", "Principal", "Addl_Principal", "Interest"]]
                    .sum().to_frame().T)

    # Format the Date DataFrame
    payment_details = pd.DataFrame.from_items([('payoff_date', [last_payment_date]),
                                            ('Interest Rate', [interest_rate]),
                                            ('Number of years', [years])
                                            ])
    # Add a column showing how much we pay each period.
    # Combine addl principal with principal for total payment
    payment_details["Period_Payment"] = round(per_payment, 2) + addl_principal

    payment_summary = pd.concat([payment_details, payment_info], axis=1)
    return df, payment_summary


def amortize(principal, interest_rate, years, addl_principal=0, annual_payments=12, start_date=date.today()):

    pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principal
    end_balance = principal

    while end_balance > 0:

        # Recalculate the interest based on the current balance
        interest = round(((interest_rate/annual_payments) * beg_balance), 2)

        # Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principal = pmt - interest

        # Ensure additional payment gets adjusted if the loan is being paid off
        addl_principal = min(addl_principal, beg_balance - principal)
        end_balance = beg_balance - (principal + addl_principal)

        yield OrderedDict([('Month',start_date),
                        ('Period', p),
                        ('Begin Balance', beg_balance),
                        ('Payment', pmt),
                        ('Principal', principal),
                        ('Interest', interest),
                        ('Additional_Payment', addl_principal),
                        ('End Balance', end_balance)])

        # Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance


    # schedule = pd.DataFrame(amortize(700000, .04, 30, addl_principal=200, start_date=date(2016, 1,1)))
    # schedule.head()


    # schedule.tail()


    # schedule1, stats1 = amortization_table(100000, .04, 30, addl_principal=50, start_date=date(2016,1,1))
    # schedule2, stats2 = amortization_table(100000, .05, 30, addl_principal=200, start_date=date(2016,1,1))
    # schedule3, stats3 = amortization_table(100000, .04, 15, addl_principal=0, start_date=date(2016,1,1))

    # pd.DataFrame([stats1, stats2, stats3])


    # additional_payments = [0, 50, 200, 500]
    # fig, ax = plt.subplots(1, 1)

    # for pmt in additional_payments:
    #     result, _ = amortization_table(100000, .04, 30, addl_principal=pmt, start_date=date(2016,1,1))
    #     ax.plot(result['Month'], result['End Balance'], label='Addl Payment = ${}'.format(str(pmt)))
    # plt.title("Pay Off Timelines")
    # plt.ylabel("Balance")
    # ax.legend();
class investorAPI(APIView):
    permission_classes = [isInvestor]

    def get(self,request):
        queryset = FundApplication.objects.filter(provider = request.user)
        serializer = FundApplicationSerializer(queryset, many=True)
        return Response({"Your Fund applications":serializer.data})


    def post(self,request):
        serializer = FundApplicationSerializer(data = request.data)
        if serializer.is_valid():
            fundType = request.data.get('fund_type')
            
            fundAmount = request.data.get('amount')
        
            loanfund = get_object_or_404(LoanFund,id = fundType)
            if(int(fundAmount) > int(loanfund.max_amount) or int( fundAmount )< int (loanfund.min_amount)):
                return Response({"please enter a valid amount"})
            # serializer.data.customer = request.user    
            serializer.save(provider = request.user , fund_type = loanfund , status = "IP" )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       



class amotizationAPI(APIView):
    # permission_classes = [isCustomer]






    def get(self,request,pk):
        # termId =  request.data.get('termNumber')
        if request.user.groups.filter(name = "customer"):
            termId = pk
            app = get_object_or_404(TermApplication,id = termId)
            loan = get_object_or_404(LoanTerm,id = app.term_type.id) 
            interestRate = loan.intrest_rate
            years = loan.duration_years 
            principalBorrowed = app.amount
            #monthlyPayment   = np.pmt(interestRate, numberOfMonths, principalBorrowed)
            return Response(amortize(principalBorrowed,interestRate,years))
        elif request.user.groups.filter(name = "investor"):
            termId = pk
            app = get_object_or_404(FundApplication,id = termId)
            loan = get_object_or_404(LoanFund,id = app.fund_type.id) 
            interestRate = loan.intrest_rate
            years = loan.duration_years 
            principalBorrowed = app.amount
            #monthlyPayment   = np.pmt(interestRate, numberOfMonths, principalBorrowed)
            return Response(amortize(principalBorrowed,interestRate,years))  
        return Response("Not Accessible")      

class customerAPI(APIView):
    permission_classes = [isCustomer]
    def get(self,request):
        queryset = TermApplication.objects.filter(customer = request.user)
        serializer = TermApplicationSerializer(queryset, many=True)
        return Response({"Your Fund applications":serializer.data})



    def post(self,request):

        serializer = TermApplicationSerializer(data = request.data)
        if serializer.is_valid():
            termType = request.data.get('term_type')
            
            termAmount = request.data.get('amount')
        
            loanterm = get_object_or_404(LoanTerm,id = termType)
            if(int(termAmount) > int(loanterm.max_amount) or int( termAmount )< int (loanterm.min_amount)):
                return Response({"please enter a valid amount"})
            # serializer.data.customer = request.user    
            serializer.save(customer = request.user , term_type = loanterm , status = "IP" )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

        # termType = request.data.get('type')
        # loanTerm = get_object_or_404(LoanTerm, name = termType)
        # termAmount = request.data.get('amount')
        # if(termAmount > int(loanTerm.max_amount) or termAmount < int (loanTerm.min_amount)):
        #     return Response({"please enter a valid amount"})
        # else :
        #     term = TermApplication.objects.create(
        #         amount = termAmount,
        #         customer = request.user,
        #         term_type = loanTerm
        #     )
        #     serializer = TermApplicationSerializer(term)
        #     return Response({"added loan application":serializer.data})    


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
            # self.check_object_permissions(request,LoanFund.objects.get(id=1))
            return Response({"Loan Funds":serializer.data})
        elif (request.user.groups.filter(name = "cutomer")):
            queryset = LoanFund.objects.all()
            amount = request.data.get('amount')
            queryset = LoanTerm.objects.all().filter(max_amount__gte = amount)
            queryset = queryset.filter(min_amount__lte = amount)
            serializer = LoanTermSerializer(queryset, many=True)
            # self.check_object_permissions(request,LoanTerm.objects.get(id=1))
            return Response({"Loan Terms":serializer.data})
        else :
            return Response({"Not Accessible"})    


        


class editFundApplicationsAPI(APIView):
    permission_classes = [isBank]
    def get(self,request):
        queryset = FundApplication.objects.all()
        serializer = FundApplicationSerializer(queryset, many = True)
        return Response({"Fund Applications": serializer.data})


    def put(self,request,pk,format = None):
        fund = get_object_or_404(FundApplication.objects.all(),id = pk)
        #loanfund = self.get_object(pk)
        # serializer = TermApplicationSerializer(fund , data = request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

        # loanFundId = request.data.get('fundNumber')
        # loanFund = LoanFund.objects.get(id=loanFundId)
        if request.data.get('status') == 'DN' or request.data.get('status')== 'AP' :
            status = request.data.get('status')
            fund.status = status
            fund.save()
            return Response('Status updated')   
        return Response('Please enter valid status')


class makePaymentAPI(APIView):
    permission_classes = [isCustomer]

    def put(self,request,pk):
        payment  = request.data.get('amount')
        queryset = TermApplication.objects.filter(customer = request.user)
        loan = queryset.get(id = pk)
        if loan == None :
            return Response({"loan not avialable "})
        if payment > loan.amount :
            return Response({"payment is greater then the total amount of your loan"})
        loan.amount = loan.amount - payment
        loan.save()
        serializer = TermApplicationSerializer(loan)
        return Response({"Thank you for your payment": serializer.data})    







class editTermApplicationsAPI(APIView):
    permission_classes = [isBank]

    def get(self,request):
        queryset = TermApplication.objects.all()
        serializer = TermApplicationSerializer(queryset, many = True)
        return Response({"Term Applications":serializer.data})
    
    def put(self,request,pk):
        term = get_object_or_404(TermApplication.objects.all(),id = pk)

        if request.data.get('status')== 'DN' :
            status = request.data.get('status')
            term.status = status
            term.save()
            return Response('Status updated')

        if request.data.get('status') == 'AP':
            totalfunds = 0 
            totalloans = term.amount
            funds = FundApplication.objects.all()
            loans = TermApplication.objects.all()
            for f in funds :
                if f.status == 'AP':
                    totalfunds+= f.amount
            for l in loans :
                if l.status == 'AP':
                    totalloans += l.amount         
            if totalloans > totalfunds :
                return Response('Can not perform action as loans would exceed funds')
            status = request.data.get('status')
            term.status = status
            term.save()
            return Response('Status updated')    
        return Response('Please enter valid status')

class bankReportsAPI(APIView):
    permission_classes = [isBank]
    def get(self,request):
   
        bank_count = User.objects.filter(groups = 1).count()
        customer_count = User.objects.filter(groups = 3).count()
        investor_count = User.objects.filter(groups = 2).count()
        totalapfunds = 0 
        totalaploans = 0
        totaldenfunds = 0 
        totaldenloans = 0
        funds = FundApplication.objects.all()
        loans = TermApplication.objects.all()
        for f in funds :
            if f.status == 'AP':
                totalapfunds+= f.amount
            if f.status == 'DN':
                totaldenfunds+= f.amount    
        for l in loans :
            if l.status == 'AP':
                totalaploans += l.amount 
            if l.status == 'DN':
                totaldenloans += l.amount 
        return Response({"number of employees":bank_count ,
                        "number of investors":investor_count ,
                        "number of customers":customer_count ,
                        "total amount of approved funds" : totalapfunds,
                        "total amount of approved loans" : totalaploans,
                        "total amount of denied funds" : totaldenfunds,
                        "total amount of denied loans" : totaldenloans
                        })            


     

class loantermAPI(APIView):
    permission_classes = [isBank]
    def get(self,request):
        queryset = LoanTerm.objects.all()
        serializer = LoanTermSerializer(queryset, many=True)
        return Response({"Loan terms":serializer.data})



    def post(self,request):

        serializer = LoanTermSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.data.customer = request.user    
            serializer.save(creator = request.user )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class loanfundAPI(APIView):
    permission_classes = [isBank]
    def get(self,request):
        queryset = LoanFund.objects.all()
        serializer = LoanFundSerializer(queryset, many=True)
        return Response({"Loan funds":serializer.data})



    def post(self,request):

        serializer = LoanFundSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.data.customer = request.user    
            serializer.save(creator = request.user )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        




# class LoanFundViewSet(viewsets.ModelViewSet):
#     queryset = LoanFund.objects.all()
#     permission_classes = (IsAuthenticated,isBank)
#     serializer_class = LoanFundSerializer


# class LoanTermViewSet(viewsets.ModelViewSet):
#     queryset = LoanTerm.objects.all()
#     permission_classes = (IsAuthenticated,isBank)
#     serializer_class = LoanFundSerializer    




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
