from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(request):
    return render(request, 'cg/homepage.html')

def cg_info(request):
    return render(request, 'cg/contract_grower.html')

def cg_bill(request):
    return render(request, 'cg/cg_bill.html')