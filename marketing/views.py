from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage_mk(request):
    return render(request, 'marketing/mk1.html')

def mk_area(request):
    return HttpResponse ('<h1>This is Marketing Area.</h1>')

def mk_sd(request):
    return HttpResponse('<h1><font color=red> This List of Seed Dealer</font></h1>')

def marketing_page(request):
    return render(request, 'marketing/marketing.html')

