from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, "dashboard/dashboard.html")

def account(request):
    return render(request, "dashboard/account.html")

def admin_section(request):
    return render(request, "dashboard/admin.html")

def marketing(request):
    return render(request, "dashboard/marketing.html")

def production(request):
    return render(request, "dashboard/production.html")
