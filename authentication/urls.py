from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views             #password reset email
urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('linkactivate',views.linkactivate,name="linkactivate"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('signedin',views.signedin,name='signedin'),

]