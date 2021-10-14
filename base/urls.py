from django.urls import path , include
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter





router = DefaultRouter()
router.register('loanfund-viewset', views.LoanFundViewSet)
router.register('loanTerm-viewset', views.LoanTermViewSet)
# router.register('loanfund-get', views.getLoanFund)

urlpatterns = [
    path('',include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    url(r'^investorAPI',views.investorAPI.as_view()),
    url(r'^viewloansAPI',views.viewloansAPI.as_view()),
    url(r'^customerAPI',views.customerAPI.as_view()),
    url(r'^editFundStatusAPI',views.editFundApplicationsAPI.as_view()),
    url(r'^editTermStatusAPI',views.editTermApplicationsAPI.as_view()),
    url(r'^amortizationAPI',views.amotizationAPI.as_view()),
   
    # path('',views.home, name = "home"),
    # path('loanfund-viewset',views.LoanFundViewSet, name = "loanfund-viewset"),
    
]
