from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model #회원가입 유저/
from django.contrib.auth.forms import AuthenticationForm #로그인 form
from django.contrib.auth import login as auth_login #로그인 정보 세션에 저장
User = get_user_model() # 유저 Import

# Create your views here.
def index(request):

    return render(request, 'accounts/index.html')


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
    return ''

def logout(request):
    pass