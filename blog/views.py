from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, comment
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import commentForm


class blogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-posted_on']
    paginate_by = 5


def userPost(request, username):
    try:
        author = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404()

    posts = Post.objects.filter(author=author)
    context = {
        'posts': posts
    }
    return render(request, 'blog/userPost.html', context)


def blogDetailView(request, pk):
    current_post = Post.objects.get(pk=pk)
    form = commentForm()
    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            Comment = comment(
                user=request.user,
                Comment=current_post,
                body=form.cleaned_data["body"],

            )
            Comment.save()

    comments = list(current_post.comment_set.all())
    if len(comments) == 0:
        comments = False
    print(comments)

    context = {
        'object': current_post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)


class blogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

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
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False
