from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def home(request):
    all_posts = Post.objects.all()

    return render(request, "posts/home.html",  context={"all_posts": all_posts})


# Class to create a post
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("home_page")


    # Set the author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)


# def post_page(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     comments = Comment.objects.filter(post=post)

#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.author = request.user
#             new_comment.save()
#             return redirect("post_page", post_id=post_id)
#     else:
#         comment_form = CommentForm()

#     return render(
#         request,
#         "posts/post.html",
#         {
#             "post": post,
#             "comments": comments,
#             "comment_form": comment_form,
#         },
#     )