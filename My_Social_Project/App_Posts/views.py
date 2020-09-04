from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile
from django.contrib.auth.models import User
@login_required
def home(request):
    if request.method=="GET":
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains=search)
        print(result)
    return render(request,"App_Posts/home.html",{'title':'Homepage','search':search,'result':result})