from django.contrib import admin
from django.urls import path,include
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('ac/', include('account.urls')),  # Note: 'account.urls' should be a string   
    path('bl/', include('block.urls')),  # Note: 'block.urls' should be a string   
    path('mk/', include(('marketing.urls', 'marketing'), namespace='marketing')),
                      # Note: 'marketing.urls' should be a string
    path('cg/', include(('contract_grower.urls', 'contract_grower'), namespace='contract_grower')),      # Note: 'contract_grower.urls' should be a string    
    path('pa/', include('ProjectAdmin.urls')), # Note: 'ProjectAdmin.urls' should be a string

    
]
