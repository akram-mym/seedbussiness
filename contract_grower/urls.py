from django.contrib import admin
from django.urls import path
from . import views

app_name = 'contract_grower' 

urlpatterns = [ 
    path('', views.homepage, name='homepage'),  
    path('cg_info', views.cg_info, name='cg_info'),
    path('cg_bill',views.cg_bill,name='cg_bill')
]