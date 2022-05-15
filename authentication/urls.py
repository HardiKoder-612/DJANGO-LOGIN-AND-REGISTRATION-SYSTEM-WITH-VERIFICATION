from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views             #password reset email

#To-do list
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('login',views.signin,name="login"),
    path('signout',views.signout,name="signout"),
    path('linkactivate',views.linkactivate,name="linkactivate"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),               #uidb is userid encoded in base 64 and token is to check whether the password is valid
    path('signedin',views.signedin,name='signedin'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),


    #To-Do-List
    path('tasks',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-create',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),


    #Reset Password
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),             #notify user to enter its e-mail
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),         #notify user to check their e-mail
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),      #It will automatically create a token/link for us
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]