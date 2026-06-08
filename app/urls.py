from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.indexpage ,name='index'),
    path('signup/',views.SignupPage,name='signup'),
    path('register/',views.RegisterUser,name='register'),
    path('otppage/',views.OTPPage,name='otppage'),
    path('otp/',views.otpverify,name='otp'),
    path('loginpage/',views.LoginPage,name='loginpage'),
    path('loginuser/',views.LoginUser,name='login'),
    path('profile/<int:pk>/', views.ProfilePage, name='profile'),
    path('updateprofile/<int:pk>/', views.UpdateProfile, name='updateprofile'),
    path('logout/', views.logout_user, name='logout'),
    
    ]

