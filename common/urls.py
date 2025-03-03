from django.urls import path, include

from .views import LoginAPIView, LogoutAPIView, ProfileInfoAPIView, RegisterAPIView, UserAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    
]