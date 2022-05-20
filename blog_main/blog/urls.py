from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.categories_posts),
    path('tag/<str:slug>/', views.tag_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),
]