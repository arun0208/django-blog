from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost,Comment
from .forms import BlogPostForm,CommentForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('post_list')



def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def base(request):
    posts = BlogPost.objects.all()
    return render(request, 'base.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('post_list')


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user  # Assign the current logged-in user to the comment
            new_comment.save()
            # Redirect to the post detail page after adding a comment
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})