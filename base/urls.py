from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('search/', views.search, name='search'),
    path('search_user/', views.search_user, name='search_user'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('meep_like/<int:pk>', views.meep_like, name='meep_like'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('meep_show/<int:pk>', views.meep_show, name='meep_show'),
    path('delete_meep/<int:pk>', views.delete_meep, name='delete_meep'),
    path('edit_meep/<int:pk>', views.edit_meep, name='edit_meep'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('dashboard_chat/', views.dashboard_chat, name='dashboard_chat'),
    path('meeting/', views.videocall, name='meeting'),
    path('join/', views.join, name='join'),
    path('appointment/', views.appointment, name='appointment'),
    path('success/', views.success_view, name='success'),
]
