
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login_reg', views.login_reg),
    path('create_user', views.register),
    path('login', views.login),
    path('cards/recent', views.recent),
    path('cards/trending', views.trending),
    path('cards/a-z', views.a_z),
    path('create', views.create),
    path('logout', views.logout),
    path('create/<int:img_id>', views.image_details),
    path('search', views.search),
    path('test', views.send_email),
    path('upload', views.upload_media),
    path('review/<int:img_id>', views.review),
    path('view_card/<int:card_id>', views.view_card),
    path('send_email/<int:card_id>', views.send_email),
]
