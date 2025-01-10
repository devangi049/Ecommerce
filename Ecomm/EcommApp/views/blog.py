from django.shortcuts import render
from EcommApp.models.blog import BlogPost

def blog_view(request):
    posts = BlogPost.objects.all()
    print("Blog posts :",posts)
    return render(request, 'blog.html', {'posts': posts})