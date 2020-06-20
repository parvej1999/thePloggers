from django.urls import path
from . import views
from .views import blogListView, blogDetailView, blogCreateView, blogUpdateView, blogDeleteView

app_name = 'blogs'

urlpatterns = [
    # path('', views.index, name='blog-index'),
    path('', blogListView.as_view(), name='blog-index'),
    path('<int:pk>', views.blogDetailView, name='blog-detail'),
    path('<str:username>', views.userPost, name='user-blogs'),
    path('post/create', blogCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>', blogUpdateView.as_view(), name='blog-update'),
    path('delete/post/<int:pk>', blogDeleteView.as_view(), name='blog-delete'),

]
