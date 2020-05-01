from django.db import models
from django.conf import settings
# from django.contrib.auth.model import User  // 이거 사용하지 않는 이유 ?


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image=models.ImageField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now =True)
    

class Comment(models.Model):
    content = models.CharField( max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now =True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)