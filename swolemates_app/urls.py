from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('swolemates', views.home),
    path('swolemates/<str:username>', views.profile),
    path('swolemates/<str:username>/profile_post_create', views.profile_post_create)
]