from django.shortcuts import render,redirect
from django.http import HttpRequest
# Create your views here.
def home(request):
    return HttpRequest('how are you')

def no_permission(request):
    return render(request,'no_permission.html')


def nonlogged_dashboard(request):
    return render(request,'home.html')