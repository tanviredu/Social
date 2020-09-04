from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request,"App_Posts/home.html",{'title':'Homepage'})