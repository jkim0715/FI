from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

# 그대로 활용하지 못하는 경우는 항상 상속받아서 custom!!!!
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=20,
        label = '이름',
        help_text = '이름을 입력하세요',
        widget= forms.TextInput(
            attrs={
                'placeholder': '이름 입력'
            }
        )
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields= ['username']