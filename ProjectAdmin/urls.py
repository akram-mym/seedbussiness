from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ProjectAdmin'  # ← এটি থাকা বাধ্যতামূলক

urlpatterns = [ 
    path('', views.home, name='padmin'),
    path('com_info_entry', views.company_entry_view, name='company_entry'),    
    path('success_page', views.success_view, name='success_page'),

    path('com_info', views.com_info, name='com_info'),
    path('search-company/', views.search_company, name='search_company'),
    path('blockname_entry', views.blockname_entry, name='blockname_entry'),
    path('blockname-list/', views.blockname_list, name='blockname_list'),

    path('blist', views.block_delete, name='block_info_d'),    
    path('block/update/<str:pk>/', views.block_update_view, name='block_update'),

    path('subheadlist/', views.subheadlist, name='subheadlist'),
    path('subheadadd/', views.subhead_entry, name='subheadadd'),
    path('subhead/<int:pk>/edit/', views.subhead_edit, name='subheadedit'),
    path('subhead/<int:pk>/delete/', views.subhead_delete, name='subheaddelete'),


    path('pa', views.home1, name='home1'),    
    path('dealing-year/add/', views.add_dealing_year, name='add_dealing_year'),    
    path('dealing-year/', views.dealing_year_list, name='dealing_year_list'),
    path('dealing-year/edit/<slug:dy_session>/', views.edit_dealing_year, name='edit_dealing_year'),
    path('dealing-year/delete/<slug:dy_session>/', views.delete_dealing_year, name='delete_dealing_year'),

    path('CreateUser/', views.CreateUser, name='CreateUser'),
    path('userlist', views.userlist, name='userlist'),

    path('profiles/', views.userprofile_list, name='userprofile_list'),
    path('profiles/<int:pk>/', views.userprofile_view, name='userprofile_view'),
    path('profiles/<int:pk>/edit/', views.userprofile_edit, name='userprofile_edit'),
    path('profiles/<int:pk>/delete/', views.userprofile_delete, name='userprofile_delete'),

    path('catagory/add/', views.Catagory_add, name='catagory_add'),
    path('catagory/list/', views.Catagory_list, name='catagory_list'),
    path('catagory/edit/<int:pk>/', views.Catagory_edit, name='catagory_edit'),
    path('catagory/delete/<int:pk>/', views.Catagory_delete, name='catagory_delete'),

    path("hvarieties/", views.create_hvariety, name="create_hvariety"),
    path("hvarieties/list/", views.hvariety_list, name="hvariety_list"),
    path("hvarieties/<str:pk>/edit/", views.edit_hvariety, name="edit_hvariety"),
    path("hvarieties/<str:pk>/delete/", views.delete_hvariety, name="delete_hvariety"),
]

