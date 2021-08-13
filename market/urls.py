from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='post-delete'),
    path('users/<int:user_id>/',
         views.ProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/reviews/',
         views.UserPostView.as_view(), name='user-posts-list'),
    path('users/set-profile/',
         views.ProfileSetView.as_view(), name='profile-set'),
]
