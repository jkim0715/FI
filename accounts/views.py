from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model #회원가입 유저/
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm #로그인 form
from django.contrib.auth import login as auth_login #로그인 정보 세션에 저장
from django.contrib.auth import logout as auth_logout

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch

from .forms import CustomUserChangeForm, CustomUserCreationForm


from posts.models import Post, Comment
from posts.forms import CommentForm

User = get_user_model() # 유저 Import

# Create your views here.
def index(request):
    accounts = User.objects.all()
    # posts = Post.objects.all()
    # posts = Post.objects.prefetch_related('comment_set').order_by('-pk')
    # 2) 사용자 이름
    # posts = Post.objects.select_related('user').order_by('-pk')
    # 3) 댓글 목록
    # posts = Post.objects.prefetch_related('comment_set').order_by('-pk')

    posts = Post.objects.prefetch_related(
        	Prefetch(
        	    'comment_set',
    		    queryset=Comment.objects.select_related('user')
		    )
    	).order_by('-pk')

    commentform = CommentForm()
    context ={
       'accounts': accounts,
       'posts': posts,
       'commentform':commentform
    }
    return render(request, 'accounts/index.html',context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')

    form = CustomUserCreationForm()
    context={
        'form':form
    }
    return render(request, 'accounts/form.html',context)


def login(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user()) # Session을 생성하면서 Session Id를 부여
                return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context ={
        'form' : form
    }
    return render(request,'accounts/form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
@require_POST
def delete(request):
    request.user.delete()
    return redirect ('accounts:index')

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user = request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! 로그인 상태 유지.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(user = request.user)
    context ={
        'form':form
    }
    return render(request,'accounts/update.html',context)

@login_required
def follow(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user == user:
        return redirect('accounts:index')
    else:
        if user.followers.filter(pk = request.user.id).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)

        
        return redirect('accounts:index')