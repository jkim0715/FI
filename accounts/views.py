from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model #회원가입 유저/
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm #로그인 form
from django.contrib.auth import login as auth_login #로그인 정보 세션에 저장

User = get_user_model() # 유저 Import

# Create your views here.
def index(request):
    accounts = User.objects.all()
    context ={
       'accounts': accounts 
    }
    return render(request, 'accounts/index.html',context)

def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')

    form = UserCreationForm()
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

def logout(request):
    pass