from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [  
    path('', views.homepage_mk, name='homepage_mk'),       
    path('mk_area', views.mk_area, name='mk_area'),
    path('mk_sd',views.mk_sd,name='mk_sd'),
    path('marketing_page', views.marketing_page, name='marketing_page'),   
]