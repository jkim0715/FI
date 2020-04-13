# Fake Instagram

> Django를 활용한 인스타그램 클론 코딩



## 기능

- 회원가입 / 로그인 / 로그아웃
- 게시물 작성 / 수정 / 삭제 
- Alert 안내 메시지 (django message framework.fresh message)
  - "one-time notification message" : 새로고침하면 없어짐



## 프로젝트 구성

```bash
~/ $django-admin startproject instagram
~/instagram $python manage.py startapp articles
~/instagram $python manage.py startapp accounts
```

> `App` 이름은 복수형 



`Instagram`

- `articles`
- `accounts`







### Articles/

**models.py**

```python
class article (models.Model)
	title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now =True)
```

> `Model` 이름은 단수형



**admin.py**

```python
class ArticleAdmin(Article):
    list_display =  ['id','title','created_at'] # 추가정보 표시
    list_dispaly_links = ['title']
    list_filter = ['created_at'] 
    
admin.site.register(Article, ArticleAdmin)
```



**forms.py**

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        
```



**views.py**

```python
from .models import Article 
def index(request):
    articles = Article.object.order_by('pk')
    context = {
        'articles':articles
    }
    return render('.html', context)
```



**urls.py**

```python
import path
app_name = 'articles'

urls_patters=[
    path('', views.index, name ='index'),
]
```

> Restful API 



**Instagram/urls.py**

```python
from aricles import views
URL_patterns =[
    path('', views.index), #루트설정
]
```





### Accounts/

**views.py**

```python 
from django.contrib.auth import get_user_model

User = get_user_model()
def index(request):
    accounts = User.objects.all()
    context={
        'accounts' : accounts
    }
    return render(request,'accounts/index.html',context)
```

> 바로 auth.User 객체에 접근해서 import 하지말기





## modules



#### django message framework

> Fallback Storage

- Cookie 먼저 확인 -> session 확인

