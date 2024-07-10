from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blogposts"),
    path('blogpost/create/', views.BlogPostCreateView.as_view(), name='create-blogpost'),
    path("update-blogpost/<pk>/", views.BlogPostUpdateView.as_view(), name="update-blogpost"),
    path("delete-blogpost/<pk>/", views.BlogPostDeleteView.as_view(), name="delete-blogpost"),
    path("blogpost-detail/<pk>/", views.blogpost_detail, name="blogpost-detail"),
    
    ###############Category#############
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("category/create/", views.CategoryCreateView.as_view(), name='create-category'),
    path("update-category/<pk>/", views.CategoryUpdateView.as_view(), name="update-category"),
    path('loadcategories/', views.load_categories, name='loadcategories'),
    
    

]