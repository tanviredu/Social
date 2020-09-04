from django.shortcuts import render,HttpResponseRedirect
from .forms import CreateNewUser
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy

def signup(request):
    form = CreateNewUser()
    registered = False
    if request.method == "POST":
        form = CreateNewUser(data = request.POST)
        if form.is_valid():
            form.save()
            registered = True
            pass

    return render(request,'App_Login/signup.html',context={'title':'Sign up ','form':form})


