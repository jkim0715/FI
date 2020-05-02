from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Post
from .forms import PostForm,CommentForm

# Create your views here.
def create(request):
    if request.method =="POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("accounts:index")
    else:
        form = PostForm()
    
    context ={
        'form':form
    }
    return render(request, 'posts/form.html',context)
    


def update(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method=="POST":
        form =PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            print('hello')
            form.save()
            return redirect('posts:update',post_id)
    else:
        form=PostForm(instance=post)
    context={
        'form':form
    }
    
    return render(request, 'posts/detail.html',context)


def delete(request,post_id):

    return

def createcomment(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
        
        return redirect('accounts:index')

    else:
        messages.warning(request, '댓글작성을 위해서는 로그인 필요합니다')
        return redirect('accounts:login')
        # return HttpResponse(status=401)