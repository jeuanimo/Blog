from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Status(models.Model):
    """Status choices for posts (Draft, Published, etc.)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')
    
    class Meta:
        verbose_name_plural = 'Status'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, default='')
    body = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('posts:detail', args={'pk': self.id})


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
