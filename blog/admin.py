from django.contrib import admin
from .models import Post, comment, feedback

# Register your models here.
admin.site.register(Post)
admin.site.register(comment)
admin.site.register(feedback)
