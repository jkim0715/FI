# Fake Instagram

> Django를 활용한 인스타그램 클론 코딩



## 기능

- 회원가입 / 로그인 / 로그아웃 / 마이페이지 /비밀번호 변경 (hash)
  - 회원 팔로잉
- 게시물 작성 / 수정 / 삭제 / 이미지 업로드
  - 게시물 좋아요 
- Alert 안내 메시지 (django message framework.fresh message)
  - "one-time notification message" : 새로고침하면 없어짐



## 프로젝트 구성

`Instagram` (프로젝트 폴더)

- `accounts`
- `posts`

```bash
~/ $django-admin startproject instagram
~/instagram $python manage.py startapp accounts
~/instagram $python manage.py startapp posts
```

> `App` 이름은 복수형 



**추가 라이브러리 모음**

`requirements.txt`

```python
beautifulsoup4==4.9.0
Django==2.1.15
django-appconf==1.0.4
django-bootstrap4==1.1.1 # 부트스트랩
django-extensions==2.2.9 # Shell_plus 활용
django-imagekit==4.0.2 # 이미지 리사이즈
pilkit==2.0 # 이미지 리사이즈
Pillow==7.1.2 # ImageField() 사용
pytz==2019.3
six==1.14.0
soupsieve==2.0
```



### 커스텀 유저 

> 장고 권장 기본 커스텀 유저 설정.

**accounts**

```python
### models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): #Abstact 유저를 상속받는 Class로 재정의
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings') # N:M관계.
    
### forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

# Create/Update 로직을 구현하기 위한 커스텀 Form
class CustomUserChageForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields ='__all__'
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields= ['username']        
```

**Mainapp.settings.py**

```python
#커스텀 유저 모델 세팅
AUTH_USER_MODEL='accounts.User'
```



### 이미지 업로드

1. **ImageField**

```bash
$ pip install pillow
```

2. **resizing**

```bash
$ pip install pilkit django-imagekit 
```

**posts**

```python 
### .models.py
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail
# ResizeToFill : 300*300 자르는 것(crop)
# ResizeToFit : 가장 긴 곳(너비/높이)을 300으로 맞추고, 비율에 맞춰서


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image=models.ImageField()
    image_thumbnail = ImageSpecField(source='image',
                        processors=[Thumbnail(300, 300)],
                        format='JPEG',
                        options={'quality': 60})
    # 원본 잘라서 저장 : ProcessedImageField
    # image = ProcessedImageField(
    #                       processors=[ResizeToFill(100, 50)],
    #                       format='JPEG',
    #                       options={'quality': 60})
```

**Mainapp**

```python
##.settings.py
# 미디어 파일 저장경로 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

##urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path(),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

**.html**

```django 
<form action="" method="POST" enctype="multipart/form-data"> 
{% csrf_token %}
    {%form%}
    <button>제출</button>
</form>
```





### Posts/

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

