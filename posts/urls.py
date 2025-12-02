from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('archived/', views.PostArchivedListView.as_view(), name='archived'),
    path('drafts/', views.PostDraftListView.as_view(), name='drafts'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostCreateView.as_view(), name='new'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
