from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .models import Post
from .forms import PostForm, RegisterForm


# READ
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {
        "posts": posts
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, "blog/post_detail.html", {
        "post": post
    })



@login_required
def post_create(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("post_list")

    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {
        "form": form,
        "title": "Post yaratish"
    })



@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {
        "form": form,
        "title": "Postni tahrirlash"
    })



@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return render(request, "blog/post_delete.html", {
        "post": post
    })

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("post_list")

    else:
        form = RegisterForm()

    return render(request, "blog/register.html", {
        "form": form
    })



def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("post_list")

    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {
        "form": form
    })



@login_required
def logout_view(request):
    logout(request)
    return redirect("post_list")