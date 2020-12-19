
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login_reg', views.login_reg),
    path('create_user', views.register),
    path('login', views.login),
    path('recent', views.recent),
    path('trending', views.trending),
    path('a-z', views.a_z),
    path('create', views.create)
]
