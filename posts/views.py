from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'object_list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('posts:list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts:list')
