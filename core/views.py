from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.views import View
# Create your views here.
class home(View):
    def get(self,request):
        return HttpRequest('how are you')

def no_permission(request):
    return render(request,'no_permission.html')


def nonlogged_dashboard(request):
    return render(request,'home.html')