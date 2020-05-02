from django.shortcuts import render,redirect
from .forms import PostForm

# Create your views here.
def create(request):
    if request.method =="POST":
        form = PostForm(request.POST, request.FILES)
        print('1')
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
    
    return ''


def delete(request,post_id):

    return