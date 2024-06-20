from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name="home"),
    path('register/', views.Register, name="register"),
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('verify/', views.verifyMessage, name='verify'),
    path('verify/<str:auth_token>/', views.verify_account, name="verify_account"),
]