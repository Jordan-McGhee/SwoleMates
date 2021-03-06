from django.urls import path
from . import views

urlpatterns = [
    # LOGIN FUNCTIONS
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),


    # HOME PAGES & FUNCTIONS
    path('swolemates', views.home),

    # HOME POST FUNCTIONS
    path('swolemates/home_post_create', views.home_post_create),
    path('swolemates/home/post/<int:post_id>/add_like', views.home_post_add_like),
    path('swolemates/home/post/<int:post_id>/remove_like', views.home_post_remove_like),

    # HOME COMMENT FUNCTIONS
    path('swolemates/home/post/<int:post_id>/add_comment', views.home_post_add_comment),
    path('swolemates/home/post/<int:post_id>/comment/<int:comment_id>/delete', views.home_post_delete_comment),
    path('swolemates/home/comment/<int:comment_id>/add_like', views.home_comment_add_like),
    path('swolemates/home/comment/<int:comment_id>/remove_like', views.home_comment_remove_like),

    # HOME FRIEND FUNCTIONS
    path('swolemates/request/<str:username>/send_request', views.home_send_friend_request),
    path('swolemates/request/<str:username>/accept_request', views.home_accept_friend_request),
    path('swolemates/request/<str:username>/deny_request', views.home_deny_friend_request),
    path('swolemates/request/<str:username>/remove_friend', views.home_remove_friend),


    # POST PAGES & FUNCTIONS
    path('swolemates/post/<int:post_id>', views.view_post),
    path('swolemates/post/<int:post_id>/edit', views.edit_post),
    path('swolemates/post/<int:post_id>/update', views.update_post),
    path('swolemates/post/<int:post_id>/delete', views.delete_post),
    path('swolemates/post/<int:post_id>/add_like', views.post_add_like),
    path('swolemates/post/<int:post_id>/remove_like', views.post_remove_like),

    # POST COMMENT FUNCTIONS
    path('swolemates/post/<int:post_id>/add_comment', views.post_add_comment),
    path('swolemates/post/<int:post_id>/comment/<int:comment_id>/delete', views.post_delete_comment),
    path('swolemates/post/<int:post_id>/comment/<int:comment_id>/add_like', views.post_comment_add_like),
    path('swolemates/post/<int:post_id>/comment/<int:comment_id>/remove_like', views.post_comment_remove_like),
    

    # POST USER/PROFILE PAGES & FUNCTIONS
    path('swolemates/user/<str:username>', views.profile),
    path('swolemates/user/<str:username>/edit', views.profile_edit),
    path('swolemates/user/<str:username>/update', views.profile_update),

    # PROFILE FRIEND FUNCTIONS
    path('swolemates/user/request/<str:username>/send_request', views.profile_send_friend_request),
    path('swolemates/user/request/<str:username>/accept_request', views.profile_accept_friend_request),
    path('swolemates/user/request/<str:username>/deny_request', views.profile_deny_friend_request),
    path('swolemates/user/request/<str:username>/remove_friend', views.profile_remove_friend),
    
    # PROFILE POST FUNCTIONS
    path('swolemates/user/<str:username>/profile_post_create', views.profile_post_create),
    path('swolemates/user/<str:username>/post/<int:post_id>/add_like', views.profile_post_add_like),
    path('swolemates/user/<str:username>/post/<int:post_id>/remove_like', views.profile_post_remove_like),

    # POST COMMENT FUNCTIONS
    path('swolemates/user/<str:username>/post/<int:post_id>/add_comment', views.profile_add_comment),
    path('swolemates/user/<str:username>/post/<int:post_id>/comment/<int:comment_id>/delete', views.profile_delete_comment),
    path('swolemates/user/<str:username>/comment/<int:comment_id>/add_like', views.profile_comment_add_like),
    path('swolemates/user/<str:username>/comment/<int:comment_id>/remove_like', views.profile_comment_remove_like),


    # FRIEND LIST PAGES & FUNCTIONS
    path('swolemates/user/<str:username>/friends', views.friends_list),
    path('swolemates/friends/request/<str:username>/send_request', views.friends_send_friend_request),
    path('swolemates/friends/request/<str:username>/accept_request', views.friends_accept_friend_request),
    path('swolemates/friends/request/<str:username>/deny_request', views.friends_deny_friend_request),
    path('swolemates/friends/request/<str:username>/remove_friend', views.friends_remove_friend),


    # WORKOUT LIST PAGES & FUNCTIONS
    path('swolemates/user/<str:username>/workouts', views.workouts_list),
    path('swolemates/workout', views.workout_form),
    path('swolemates/workout/create', views.workout_create),
    path('swolemates/workout/<int:id>', views.workout_view),
    path('swolemates/workout/<int:id>/edit', views.workout_edit),
    path('swolemates/workout/<int:id>/update', views.workout_update),
    path('swolemates/workout/<int:id>/delete', views.workout_delete)
]