from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('swolemates', views.home),
    path('swolemates/home_post_create', views.home_post_create),
    path('swolemates/request/<str:username>/send_request', views.home_send_friend_request),
    path('swolemates/request/<str:username>/accept_request', views.home_accept_friend_request),
    path('swolemates/request/<str:username>/deny_request', views.home_deny_friend_request),
    path('swolemates/request/<str:username>/remove_friend', views.home_remove_friend),
    path('swolemates/user/<str:username>', views.profile),
    path('swolemates/user/<str:username>/profile_post_create', views.profile_post_create),
    path('swolemates/user/request/<str:username>/send_request', views.profile_send_friend_request),
    path('swolemates/user/request/<str:username>/accept_request', views.profile_accept_friend_request),
    path('swolemates/user/request/<str:username>/deny_request', views.profile_deny_friend_request),
    path('swolemates/user/request/<str:username>/remove_friend', views.profile_remove_friend),
    path('swolemates/user/<str:username>/friends', views.friends_list),
    path('swolemates/friends/request/<str:username>/send_request', views.friends_send_friend_request),
    path('swolemates/friends/request/<str:username>/accept_request', views.friends_accept_friend_request),
    path('swolemates/friends/request/<str:username>/deny_request', views.friends_deny_friend_request),
    path('swolemates/friends/request/<str:username>/remove_friend', views.friends_remove_friend),
    path('swolemates/user/<str:username>/workouts', views.workouts_list),
    path('swolemates/workout', views.workout_form),
    path('swolemates/workout/create', views.workout_create),
    path('swolemates/workout/<int:id>', views.workout_view),
    path('swolemates/workout/<int:id>/edit', views.workout_edit),
    path('swolemates/workout/<int:id>/update', views.workout_update),
    path('swolemates/workout/<int:id>/delete', views.workout_delete)
]