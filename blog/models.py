from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    recently_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:blog-detail', kwargs={'pk': self.pk})


class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_on = models.DateTimeField(auto_now=True)
    body = models.TextField()

    def __str__(self):
        return self.body

class feedback(models.Model):
    fullName = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    email = models.EmailField(max_length = 254, null=True)
    msg = models.CharField(max_length=300)
    def __str__(self):
        return self.fullName