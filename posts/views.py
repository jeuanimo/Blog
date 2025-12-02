from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm  


class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Post.objects.filter(status__name='Published')


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status__name='Published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('-created_on')
        if "form" not in context:
            context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'subtitle', 'body', 'status', 'image']
    success_url = reverse_lazy('posts:list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'subtitle', 'body', 'status', 'image']
    success_url = reverse_lazy('posts:list')
    context_object_name = 'post'
    login_url = 'login'
    permission_denied_message = 'You do not have permission to edit this post.'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts:list')
    login_url = 'login'
    permission_denied_message = 'You do not have permission to delete this post.'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'posts/detail.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'posts/comment_edit.html'
    context_object_name = 'comment'
    login_url = 'login'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'
    context_object_name = 'comment'
    login_url = 'login'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.post.pk})


class PostArchivedListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/archived.html'
    context_object_name = 'archived_posts'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter posts with Archived status that belong to the logged-in user
        context['archived_posts'] = Post.objects.filter(
            status__name='Archive',
            author=self.request.user
        ).order_by('-created_on')
        return context


class PostDraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/drafts.html'
    context_object_name = 'draft_posts'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter posts with Draft status that belong to the logged-in user (author only)
        context['draft_posts'] = Post.objects.filter(
            status__name='Draft',
            author=self.request.user
        ).order_by('-created_on')
        return context


