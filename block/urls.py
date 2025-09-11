from django.contrib import admin
from django.urls import path
from . import views

app_name = 'block'  # ← এটি থাকা বাধ্যতামূলক

urlpatterns = [ 
    path('', views.home, name='block'),
    path('userlist', views.userlist, name='userlist'),
    path('advance_insert', views.advance_insert, name='advance_insert'),
    path('success', views.success_advance, name='success'),    

    path('advance_info/', views.advance_info,name='advance_info'),
    
    path('budget/add/', views.budget_insert, name='budget_insert'),    
    path('budget/list/', views.budget_list, name='budget_list'),
    path('budget/<int:pk>/edit/', views.update_record, name='budget_edit'),

    path('person/list', views.person_list, name='person_list'),
    path('person/create', views.create_person, name='person_create'),
    path('person/<str:pk>/edit', views.person_edit, name='person_edit'),

    path('landmeasure_list', views.landmeasure_list, name='landmeasure_list'),
    path('create/', views.landmeasure_create, name='landmeasure_create'),
    path('edit/<int:pk>/', views.landmeasure_edit, name='landmeasure_edit'),
  
    
    
]

