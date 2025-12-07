from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Blog Post CRUD URLs
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # Search and Tag URLs
    path('search/', views.PostSearchView.as_view(), name='post-search'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
    
    # Comment CRUD URLs (Template-based)
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:pk>/comment/<int:comment_pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:pk>/comment/<int:comment_pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    
    # Comment API URLs
    path('api/post/<int:post_id>/comment/', views.CommentAPIListView.as_view(), name='comment-api-list'),
    path('api/post/<int:post_id>/comment/create/', views.CommentAPICreateView.as_view(), name='comment-api-create'),
    path('api/comment/<int:pk>/update/', views.CommentAPIUpdateView.as_view(), name='comment-api-update'),
    path('api/comment/<int:pk>/delete/', views.CommentAPIDeleteView.as_view(), name='comment-api-delete'),
    
    # Home URL
    path('', views.home, name='home'),
]