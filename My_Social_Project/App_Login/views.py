from django.shortcuts import render,HttpResponseRedirect
from .forms import CreateNewUser,EditProfile
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from .models import UserProfile,User,Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from App_Posts.forms import PostForm


def signup(request):
    form = CreateNewUser()
    registered = False
    if request.method == "POST":
        form = CreateNewUser(data = request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user = user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))

    return render(request,'App_Login/signup.html',context={'title':'Sign up ','form':form})


def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password=password)
            if user is not None:
                login(request,user)
                print("[+] User Logged in")
                return HttpResponseRedirect(reverse('App_Posts:home'))
                #test

    return render(request,'App_Login/login.html',{'title':'Login','form':form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/profile.html', context={'c_user':current_user,'form':form, 'title':'Edit Profile . Social'})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


@login_required
def profile(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request,'App_Login/user.html',context={'title':'User Profile','form':form})

@login_required
def user(request,username):
    you = request.user
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=you,following=user_other)
    ## if he click his own profile
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/user_other.html',context={'user_other':user_other,'already_followed':already_followed})

@login_required
def follow(request,username):
    you = request.user
    other_people = User.objects.get(username=username)
    ##check if already foloed
    already_followed = Follow.objects.filter(follower=you,following=other_people)
    if not already_followed:
        followed_user = Follow(follower=you,following=other_people)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user',kwargs={'username':username}))

@login_required
def unfollow(request,username):
    you = request.user
    other_people = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=you,following=other_people)
    already_followed.delete()
    return HttpResponseRedirect(reverse("App_Login:user",kwargs={'username':username}))
