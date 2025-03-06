from django.urls import path, include
from  . import views
urlpatterns = [
    path('', views.RecipesHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    # path('user_posts/', views.user_posts, name='user_posts'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.RecipesCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete_page'),
]