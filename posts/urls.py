from django.urls import path
from . import views

app_name="posts"
urlpatterns = [
    path('create/', views.create, name="create"),
    path('update/<int:post_id>/', views.update, name="update"),
    path('delete/<int:post_id>/', views.delete, name="delete"),
    path('like/<int:post_id>/', views.like, name="like"),
    path('createcomment/<int:post_id>/', views.createcomment, name="createcomment"),
]