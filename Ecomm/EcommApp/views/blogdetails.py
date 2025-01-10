from django.shortcuts import render, get_object_or_404
from EcommApp.models.blog import BlogPost, Comment

def blog_details_view(request, id):
    # Fetch the blog post by its ID
    post = get_object_or_404(BlogPost, id=id)
    
    # Fetch related comments
    comments = Comment.objects.filter(blog_post=post)
    
    return render(request, 'blogdetails.html', {
        'post': post,
        'comments': comments,
    })
