from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator  # ✅ ADD THIS
from . import views


app_name = 'account'  # ← এটি থাকা বাধ্যতামূলক

# Custom LogoutView that allows GET requests
@method_decorator(csrf_exempt, name='dispatch')
class LogoutViewGET(LogoutView):
    def get(self, request, *args, **kwargs):
        # Call the original post() method on GET
        return self.post(request, *args, **kwargs)


urlpatterns = [    
    path('', views.homepage, name='homepage'),
    path('acc/', views.account, name='account'),
    path('book', views.book, name='book'),
    path('tn', views.teacher_name, name='teacher_name'),
    path('block_info', views.block_info, name='block_info'),
    path('EmpInfoEntry', views.EmployeeInfoEntryView, name='EmpInfoEntry'),  
    path('success', views.success_page, name='success_page'),  # ✅ Success Page    
    
    
    path('blockname-list/', views.blockname_list, name='blockname_list'),
    

    path('success_emp',views.success_page_emp, name='success_emp'),  
    # path('account/', views.account_view, name='account'),  # /account/ ইউআরএল
    path('login/', views.login_view, name='login'),       # লগইন পেজ ইউআরএল
    path('logout/', views.custom_logout_view, name='logout'),

    path('employee_list', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('update/<str:pk>/', views.employee_update, name='employee_update'),
    path('delete/<str:pk>/', views.employee_delete, name='employee_delete'),

    path('insert_common_exp/', views.insert_common_exp, name='insert_common_exp'),
    path('common_exp_report/', views.common_exp_report, name='common_exp_report'),

    path('head-exp/', views.view_head_exp, name='view_head_exp'),
    path('head-exp/insert/', views.insert_head_exp, name='insert_head_exp'),
    path('head-exp/update/<str:pk>/', views.update_head_exp, name='update_head_exp'),

    path('subhead/', views.subhead_entry, name='subhead'),

    
    path('register/', views.register, name='register'),   

    # path('home', views.HomeView.as_view(), name='home'),
    path('home/', views.login_view, name='home'),

    path('advance_insert/', views.advance_insert,name='advance_insert'),
    path('advance_info/', views.advance_info,name='advance_info'),
    path('advance/<int:pk>/edit/', views.advance_edit, name='advance_edit'),

    path('profile/', views.userprofile_view, name='profile'),

]