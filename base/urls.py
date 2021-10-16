from django.urls import path , include
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter





router = DefaultRouter()
# router.register('loanfund-viewset', views.LoanFundViewSet)
# router.register('loanTerm-viewset', views.LoanTermViewSet)
# router.register('loanfund-get', views.getLoanFund)

urlpatterns = [
    # path('',include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('investorAPI',views.investorAPI.as_view()),
    path('viewloansAPI',views.viewloansAPI.as_view()),
    path('customerAPI',views.customerAPI.as_view()),
    path('editFundStatusAPI/<int:pk>/',views.editFundApplicationsAPI.as_view()),
    path('editFundStatusAPI/',views.editFundApplicationsAPI.as_view()),
    path('editTermStatusAPI/<int:pk>/',views.editTermApplicationsAPI.as_view()),
    path('editTermStatusAPI/',views.editTermApplicationsAPI.as_view()),
    path('amortizationAPI/<int:pk>/',views.amotizationAPI.as_view()),
    path('loantermAPI',views.loantermAPI.as_view()),
    path('loanfundAPI',views.loanfundAPI.as_view()),
   
    # path('',views.home, name = "home"),
    # path('loanfund-viewset',views.LoanFundViewSet, name = "loanfund-viewset"),
    
]
