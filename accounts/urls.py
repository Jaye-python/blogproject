from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('user-profile/', views.ProfileView.as_view(), name='user-profile'),    
    path('profile-update/', views.profile_update, name='profile-update'),
     
    
    
]