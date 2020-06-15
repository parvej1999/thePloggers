from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

# posts = [
#     {
#         "author": "parvej khan",
#         "pub_date": "05 jun 2020",
#         "content": "Hi first post to check frontend website",
#         'title': "First Post"
#     },
#     {
#         "author": "parvej khan",
#         "pub_date": "05 jun 2020",
#         "content": "Hi first post to check frontend website",
#         'title': "First Post"
#     },
# ]


def index(request):
    posts = Post.objects.all().order_by('-recently_updated_on')
    return render(request, 'blog/index.html', {'posts': posts})


class blogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-posted_on']
    paginate_by = 5


def userPost(request, username):
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    context = {
        'posts':posts
    }
    return render(request, 'blog/userPost.html', context)


class blogDetailView(DetailView):
    model = Post


class blogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # success_url = 'blogs:blog-index'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class blogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class blogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blogs"

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False
