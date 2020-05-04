from django.db import models
from django.conf import settings
# from django.contrib.auth.model import User  // 이거 사용하지 않는 이유 ?

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now =True)

    

class Comment(models.Model):
    content = models.CharField( max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now =True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)