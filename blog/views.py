from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from .models import Post, comment
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import commentForm
from .models import feedback

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

def feedbacks(request):
    if request.method == "POST":
        fname = request.POST.get('fName')
        phone = request.POST.get('cntct')
        _msg = request.POST.get('message')
        _mail = request.POST.get('mail')
        print(phone, fname, _msg)
        instance = feedback.objects.create(fullName=fname, contact=phone, msg=_msg, email=_mail)
        instance.save()
        return JsonResponse({
            'data':'saved',
        })
    return render(request, 'blog/feedbackform.html')


def indexFeedbacks(request):
    if User.is_superuser:
        feedbacks = feedback.objects.all().order_by('-timeStamp')
        context = {
            "feedbacks":feedbacks,
        }
        if request.method == 'POST':
            pk = request.POST.get('id')
            print(pk)
            instance = feedback.objects.get(id = pk)
            if (instance.visited == False):
                instance.visited = True
            print(instance.visited)
            instance.save()
        return render(request, 'blog/allFeedback.html', context)
    else:
        return render(request, 'blog/index.html', context)
