from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('swolemates', views.home),
    path('swolemates/home_post_create', views.home_post_create),
    path('swolemates/user/<str:username>', views.profile),
    path('swolemates/user/<str:username>/profile_post_create', views.profile_post_create),
    path('swolemates/user/<str:username>/friends', views.friends_list),
    path('swolemates/user/<str:username>/workouts', views.workouts_list),
    path('swolemates/workout', views.workout_form),
    path('swolemates/workout/create', views.workout_create),
    path('swolemates/workout/<int:id>', views.workout_view),
    path('swolemates/workout/<int:id>/edit', views.workout_edit),
    path('swolemates/workout/<int:id>/update', views.workout_update),
    path('swolemates/workout/<int:id>/delete', views.workout_delete)
]