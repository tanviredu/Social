from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile
from django.contrib.auth.models import User
from App_Login.models import Follow
from .models import Post,Like


@login_required
def home(request):
    # get the following list 
    following_list = Follow.objects.filter(follower=request.user)
    ## value_list('following ') means author will be searched with the following_list
    ## following list have three column we search the author in the 'following' column
    #3 find the following user and then search as a author  posts
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    ##all the liked object by the user
    liked_post = Like.objects.filter(user=request.user)
    ## get the array
    ## find the pk of the post primary key thet are liked
    liked_post_list = liked_post.values_list('post',flat=True)

    if request.method=="GET":
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains=search)
    return render(request,"App_Posts/home.html",{'title':'Homepage','search':search,'result':result,'following_list':following_list,'posts':posts,'liked_post_list':liked_post_list})

@login_required
def liked(request,pk):
    post = Post.objects.get(pk=pk)
    you = request.user
    already_liked = Like.objects.filter(post=post,user=you)
    if not already_liked:
        liked_post = Like(post=post,user=you)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unliked(request,pk):
    post = Post.objects.get(pk=pk)
    you = request.user
    already_liked = Like.objects.filter(post=post,user=you)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))



