from django.contrib import admin

# Register your models here.
from .models import LoanFund, LoanTerm

admin.site.register(LoanFund)
admin.site.register(LoanTerm)
#admin.site.register(Status)

